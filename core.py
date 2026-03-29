import psutil
import time
from ui import handle_event_ui

last_event_time = {
    "SPIKE": 0,
    "WARNING": 0,
    "DANGER": 0,
    "NEW_HEAVY": 0   # add this
}

COOLDOWN = 5  # seconds

SAFE_PROCESSES = [
    "systemd",
    "Xorg",
    "gnome-shell",
    "dbus-daemon"
]

def collect_memory_info():
    mem = psutil.virtual_memory()
    return {
        "total": mem.total,
        "available": mem.available,
        "used": mem.used,
        "percent": mem.percent
    }


def process_collector():
    processes = {}

    for p in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            mem_mb = p.info['memory_info'].rss / (1024 * 1024)

            processes[p.info['pid']] = {
                'pid': p.info['pid'],
                'name': p.info['name'],
                'memory_mb': mem_mb
            }

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return processes 


def get_top_processes(process_dict, n=5):
    return sorted(
        process_dict.values(),
        key=lambda x: x['memory_mb'],
        reverse=True
    )[:n]


def analysis_engine(memory_info, previous_memory=None):
    state = 'NORMAL'
    event = None

    available_gb = memory_info['available'] / (1024 ** 3)

    if available_gb < 2:
        state = 'DANGER'
    elif memory_info['percent'] > 80:
        state = 'WARNING'

    if previous_memory:
        delta = memory_info['used'] - previous_memory['used']
        if delta > (1 * 1024 ** 3):
            event = 'SPIKE'

    return state, event

def detect_new_heavy_processes(current, previous, threshold_mb=1000):
    new_heavy = []

    for pid, data in current.items():
        if pid not in previous and data['memory_mb'] > threshold_mb:
            new_heavy.append({
                'pid': pid,
                'name': data['name'],
                'memory_mb': data['memory_mb']
            })

    return new_heavy


def display(memory, processes, status):
    available_gb = memory['available'] / (1024 ** 3)

    print('\n' + '=' * 50)
    print(f'RAM Usage: {memory["percent"]}% ({available_gb:.2f} GB available)')
    print(f'System State: {status}')

    print('\nTop Memory-Consuming Processes:')
    for proc in processes:
        print(f"PID: {proc['pid']} | {proc['name']} | {proc['memory_mb']:.2f} MB")

    print('=' * 50 + '\n')

def group_processes_by_name(process_dict):
    grouped = {}

    for pid, data in process_dict.items():
        name = data['name']
        mem = data['memory_mb']

        if name not in grouped:
            grouped[name] = {
                "name": name,
                "total_memory_mb": 0,
                "pids": [],
                "count": 0
            }

        grouped[name]["total_memory_mb"] += mem
        grouped[name]["pids"].append(pid)
        grouped[name]["count"] += 1

    return grouped

def get_top_applications(grouped_dict, n=5):
    return sorted(
        grouped_dict.values(),
        key=lambda x: x['total_memory_mb'],
        reverse=True
    )[:n]

def display_grouped_apps(apps):
    print("\nTop Applications (Grouped):")

    for app in apps:
        print(
            f"{app['name']} | "
            f"{app['total_memory_mb']:.2f} MB | "
            f"{app['count']} processes"
        )

def detect_spike(current, previous):
    spikes = []

    for pid, curr_data in current.items():
        prev_data = previous.get(pid)

        if prev_data:
            delta = curr_data['memory_mb'] - prev_data['memory_mb']

            if delta > 1024:  # 1 GB in MB
                spikes.append({
                    'pid': pid,
                    'name': curr_data['name'],
                    'delta_mb': delta,
                    'memory_mb': curr_data['memory_mb']   # ✅ ADD THIS
                })

    return spikes


def create_event(event_type, data):
    return {
        "type": event_type,
        "data": data,
        "timestamp": time.time()
    }

def should_trigger(event_type):
    now = time.time()
    if now - last_event_time[event_type] > COOLDOWN:
        last_event_time[event_type] = now
        return True
    return False

def is_safe_process(name):
    return name in SAFE_PROCESSES

def detect_memory_pressure(memory):
    percent = memory['percent']

    if percent > 85:
        return "CRITICAL"
    elif percent > 75:
        return "HIGH"
    elif percent > 60:
        return "ELEVATED"
    return "NORMAL"

def main():
    previous_processes = None
    previous_memory = None
    previous_pressure = "NORMAL"
    killed_pids = set()
    
    while True:
        memory = collect_memory_info()
        process_dict = process_collector()
        current_pressure = detect_memory_pressure(memory)

        grouped = group_processes_by_name(process_dict)
        top_apps = get_top_applications(grouped)
        top_processes = get_top_processes(process_dict)
        top_process = top_processes[0] if top_processes else None
        state, event = analysis_engine(memory, previous_memory)

        display(memory, top_processes, state)
        display_grouped_apps(top_apps)

        events = []

        if event == "SPIKE" and should_trigger("SPIKE"):
            spikes = detect_spike(process_dict, previous_processes or {})
            if spikes:
                events.append(create_event("SPIKE", spikes))

        if state == "WARNING" and should_trigger("WARNING"):
            if top_process and not is_safe_process(top_process['name']):
                events.append(create_event("WARNING", [top_process]))

        if previous_processes:
            new_heavy = detect_new_heavy_processes(process_dict, previous_processes)
            if new_heavy and should_trigger("NEW_HEAVY"):
                events.append(create_event("NEW_HEAVY", new_heavy))

        if state == "DANGER" and should_trigger("DANGER"):
            if top_process:
                app = top_apps[0] if top_apps else None

                if app and app['pids']:
                    for pid in app['pids']:
                        proc_name = process_dict.get(pid, {}).get('name')

                        if proc_name and is_safe_process(proc_name):
                            continue

                        if pid not in killed_pids:
                            try:
                                psutil.Process(pid).kill()
                                killed_pids.add(pid)
                            except (psutil.NoSuchProcess, psutil.AccessDenied):
                                pass
                    events.append(create_event("AUTO_KILL", {
                        "name": app["name"],
                        "pids": app["pids"],
                        "memory_mb": app["total_memory_mb"]
                    }))
        # -------- MEMORY PRESSURE --------
        if current_pressure != previous_pressure:
            events.append(create_event("PRESSURE_CHANGE", {
                "level": current_pressure,
                "percent": memory['percent']
            }))
        for e in events:
            handle_event_ui(e)

        previous_processes = process_dict
        previous_pressure = current_pressure
        previous_memory = memory

        time.sleep(1)
