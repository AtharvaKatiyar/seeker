from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QScrollArea
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
import time
import os
import signal
import psutil

class EventCard(QWidget):
    def __init__(self, name, event_type):
        super().__init__()

        self.name = name
        self.event_type = event_type
        self.count = 1
        self.pids = set()
        self.state = event_type
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.key = name   # ✅ track exact key
        # Header
        self.header = QLabel(f"{name} • {event_type}")
        self.header.setStyleSheet(self.get_header_style(event_type))
        self.layout.addWidget(self.header)

        # Buttons
        btn_layout = QHBoxLayout()

        self.ignore_btn = QPushButton("Ignore")
        self.kill_btn = QPushButton("Kill")

        self.kill_btn.setStyleSheet("""
            background-color: #FF4C4C;
            color: white;
            border-radius: 5px;
            padding: 3px;
        """)

        self.ignore_btn.setStyleSheet("""
            background-color: #555;
            color: white;
            border-radius: 5px;
            padding: 3px;
        """)

        btn_layout.addWidget(self.ignore_btn)
        btn_layout.addWidget(self.kill_btn)

        self.layout.addLayout(btn_layout)

        self.kill_btn.clicked.connect(self.kill_process)
        self.ignore_btn.clicked.connect(self.ignore_process)
        # Expandable details
        self.logs = []

        self.details_widget = QWidget()
        self.details_layout = QVBoxLayout()
        self.details_widget.setLayout(self.details_layout)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.details_widget)
        self.scroll.setVisible(False)
        self.scroll.setMaximumHeight(150)
        self.layout.addWidget(self.scroll)

        self.header.mousePressEvent = self.start_drag
        self.header.mouseMoveEvent = self.drag_move
        self.header.mouseDoubleClickEvent = self.toggle_details

        self.cleanup_timer = QTimer()
        self.cleanup_timer.timeout.connect(self.check_process_alive)
        self.cleanup_timer.start(2000)   # check every 2 sec

        self.setStyleSheet("""
            background-color: rgba(30, 30, 30, 230);
            border-radius: 10px;
            padding: 8px;
        """)

    def refresh_logs(self):
        # clear old logs
        for i in reversed(range(self.details_layout.count())):
            self.details_layout.itemAt(i).widget().deleteLater()

        # add logs
        for log in self.logs:
            label = QLabel(log)
            label.setStyleSheet("""
                color: white;
                padding: 2px;
            """)
            self.details_layout.addWidget(label)

    def get_header_style(self, state):
        if state == "SPIKE":
            color = "#FFA500"   # orange
        elif state == "WARNING":
            color = "#FF4C4C"   # red
        elif state == "NEW":
            color = "#4FC3F7"   # blue
        elif state == "KILLED":
            color = "#9E9E9E"   # gray
        else:
            color = "#FFFFFF"

        return f"""
            color: {color};
            font-weight: bold;
            font-size: 13px;
        """

    def update_data(self, text):
        self.count += 1
        self.header.setText(f"{self.name} • {self.state} ({self.count})")

        self.logs.append(text)

        # keep last 20 logs
        if len(self.logs) > 20:
            self.logs.pop(0)

        self.refresh_logs()

    def toggle_details(self, event):
        self.scroll.setVisible(not self.scroll.isVisible())

    
    def kill_process(self):
        target_name = self.name

        for proc in psutil.process_iter(['pid', 'name']):
            try:
                cmd = ' '.join(proc.cmdline()) if proc.cmdline() else ""
                name = proc.info.get("name", "")

                if target_name in cmd or target_name in name:
                    try:
                        pgid = os.getpgid(proc.pid)
                        os.killpg(pgid, signal.SIGKILL)
                    except:
                        pass

                    proc.kill()

            except:
                continue

        self.cleanup_timer.stop()   # 🔥 ADD THIS

        self.update_state("KILLED")
        self.logs.append("All related processes terminated")
        self.refresh_logs()
    
    def force_kill_again(self):
        import psutil

        for pid in list(self.pids):
            try:
                proc = psutil.Process(pid)
                proc.kill()
            except:
                pass

    def ignore_process(self):
        ignored_processes[self.name] = time.time()
        self.setVisible(False)

    def update_state(self, new_state):
        self.state = new_state
        self.event_type = new_state

        self.header.setText(f"{self.name} • {new_state} ({self.count})")
        self.header.setStyleSheet(self.get_header_style(new_state))

        self.setStyleSheet("""
            background-color: rgba(30, 30, 30, 230);
            border-radius: 10px;
            padding: 8px;
        """)

        # 🔥 Button logic
        if new_state == "KILLED":
            self.kill_btn.setVisible(False)
            self.ignore_btn.setVisible(False)

            if not hasattr(self, "close_btn"):
                self.close_btn = QPushButton("✖")
                self.layout.addWidget(self.close_btn)
                self.close_btn.clicked.connect(self.close_card)

            # 🔥 auto-remove after 3 sec
            QTimer.singleShot(3000, self.close_card)

    def close_card(self):
        self.cleanup_timer.stop()

        parent = self.parent()
        if parent and hasattr(parent, "cards"):
            parent.cards.pop(self.key, None)

        self.deleteLater()

    def process_exists(self):
        for pid in self.pids:
            if psutil.pid_exists(pid):
                return True
        return False
    
    def check_process_alive(self):
        if not self.process_exists():
            self.handle_process_end()

    def handle_process_end(self):
        if self.state == "KILLED":
            return

        self.cleanup_timer.stop()

        self.update_state("KILLED")
        self.logs.append("Process ended automatically")
        self.refresh_logs()

        QTimer.singleShot(5000, self.close_card)

    def start_drag(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint()

    def drag_move(self, event):
        if hasattr(self, "drag_pos"):
            parent = self.window()
            delta = event.globalPosition().toPoint() - self.drag_pos
            parent.move(parent.pos() + delta)
            self.drag_pos = event.globalPosition().toPoint()


class LogWidget(QWidget):
    log_signal = pyqtSignal(object)
    def __init__(self):
        super().__init__()

        self.cards = {}   # ✅ KEEP THIS HERE
        self.offset = None
        self.setWindowTitle("MemWatch")
        self.setGeometry(1600, 800, 300, 200)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(8)

        self.log_signal.connect(self._handle_event_ui)

    def _handle_event_ui(self, payload):
        key = payload["key"]
        event_type = payload["type"]
        text = payload["text"]

        # 🔥 ignore logic
        if key in ignored_processes:
            if time.time() - ignored_processes[key] < IGNORE_TIME:
                return
            else:
                ignored_processes.pop(key)

        # 🔥 remove stale card
        if key in self.cards:
            card = self.cards[key]
            if not card.isVisible():
                self.cards.pop(key)
                card.deleteLater()

        priority = {"SPIKE": 1, "NEW": 1, "WARNING": 2, "KILLED": 3}

        if key in self.cards:
            card = self.cards[key]

            if priority[event_type] > priority.get(card.state, 0):
                card.update_state(event_type)

            incoming = payload.get("pids", [])
            card.pids.update(incoming)

            card.update_data(text)

        else:
            card = EventCard(key, event_type)

            incoming = payload.get("pids", [])
            card.pids.update(incoming)

            self.layout.addWidget(card)
            self.cards[key] = card
            card.update_data(text)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.offset = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self.offset is not None:
            self.move(event.globalPosition().toPoint() - self.offset)

    def mouseReleaseEvent(self, event):
        self.offset = None


_widget = None
ignored_processes = {}
IGNORE_TIME = 10

def set_widget(widget):
    global _widget
    _widget = widget

def handle_event_ui(event):
    if not _widget:
        return

    if event["type"] == "SPIKE":
        for p in event["data"]:
            _widget.log_signal.emit({
                "key": p["name"],
                "type": "SPIKE",
                "text": f"Memory spike: +{p['delta_mb']/1024:.1f} GB → Now {p['memory_mb']/1024:.1f} GB",
                "pids": p.get("pids", [p["pid"]])
            })

    elif event["type"] == "WARNING":
        for p in event["data"]:
            _widget.log_signal.emit({
                "key": p["name"],
                "type": "WARNING",
                "text": f"High usage: {p['memory_mb']/1024:.1f} GB RAM",
                "pids": p.get("pids", [p["pid"]])
            })

    elif event["type"] == "NEW_HEAVY":
        for p in event["data"]:
            _widget.log_signal.emit({
                "key": p["name"],
                "type": "NEW",
                "text": f"Started using {p['memory_mb']/1024:.1f} GB RAM",
                "pids": p.get("pids", [p["pid"]])
            })

    elif event["type"] == "AUTO_KILL":
        data = event["data"]
        _widget.log_signal.emit({
            "key": data["name"],
            "type": "KILLED",
            "text": f"Process terminated ({len(data['pids'])} instances)"
        })