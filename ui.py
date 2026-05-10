from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QScrollArea,
    QGraphicsDropShadowEffect,
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QColor
import time
import os
import signal
import psutil

STATE_STYLES = {
    "SPIKE": ("#F59E0B", "#2A1E0A"),
    "WARNING": ("#EF4444", "#2B1111"),
    "NEW": ("#38BDF8", "#0B1E2A"),
    "KILLED": ("#9CA3AF", "#1C1F24"),
    "DEFAULT": ("#E5E7EB", "#1C2026"),
}


class EventCard(QWidget):
    def __init__(self, name, event_type):
        super().__init__()

        self.name = name
        self.event_type = event_type
        self.count = 0
        self.pids = set()
        self.state = event_type
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.key = name

        self.layout.setContentsMargins(12, 10, 12, 12)
        self.layout.setSpacing(10)

        self.header_widget = QWidget()
        self.header_layout = QHBoxLayout()
        self.header_layout.setContentsMargins(0, 0, 0, 0)
        self.header_layout.setSpacing(8)
        self.header_widget.setLayout(self.header_layout)

        self.title_label = QLabel(name)
        self.title_label.setStyleSheet(
            """
            color: #F8FAFC;
            font-weight: 600;
            font-size: 13px;
            font-family: "IBM Plex Sans", "Noto Sans", "DejaVu Sans";
            """
        )

        self.state_badge = QLabel(event_type)
        self.state_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.count_badge = QLabel("0")
        self.count_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.close_btn = QPushButton("X")
        self.close_btn.setVisible(False)
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_btn.clicked.connect(self.close_card)

        self.header_layout.addWidget(self.title_label, 1)
        self.header_layout.addWidget(self.state_badge)
        self.header_layout.addWidget(self.count_badge)
        self.header_layout.addWidget(self.close_btn)
        self.layout.addWidget(self.header_widget)

        self.summary_label = QLabel("")
        self.summary_label.setWordWrap(True)
        self.summary_label.setStyleSheet(
            """
            color: rgba(226, 232, 240, 0.85);
            font-size: 11px;
            line-height: 18px;
            padding: 2px 0 6px 0;
            font-family: "IBM Plex Sans", "Noto Sans", "DejaVu Sans";
            """
        )
        self.layout.addWidget(self.summary_label)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(8)

        self.ignore_btn = QPushButton("Ignore")
        self.kill_btn = QPushButton("Kill")

        self.kill_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ignore_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        self.kill_btn.setStyleSheet(self.get_button_style("danger"))
        self.ignore_btn.setStyleSheet(self.get_button_style("ghost"))

        btn_layout.addWidget(self.ignore_btn)
        btn_layout.addWidget(self.kill_btn)

        self.layout.addLayout(btn_layout)

        self.kill_btn.clicked.connect(self.kill_process)
        self.ignore_btn.clicked.connect(self.ignore_process)
        # Expandable details
        self.logs = []

        self.details_widget = QWidget()
        self.details_layout = QVBoxLayout()
        self.details_layout.setContentsMargins(8, 8, 8, 8)
        self.details_layout.setSpacing(6)
        self.details_widget.setLayout(self.details_layout)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.details_widget)
        self.scroll.setVisible(False)
        self.scroll.setMaximumHeight(150)
        self.scroll.setStyleSheet(
            """
            QScrollArea {
                border: 1px solid rgba(148, 163, 184, 0.2);
                border-radius: 10px;
                background-color: rgba(15, 18, 22, 0.6);
            }
            QScrollBar:vertical {
                background: transparent;
                width: 6px;
                margin: 2px;
            }
            QScrollBar::handle:vertical {
                background: rgba(148, 163, 184, 0.4);
                border-radius: 3px;
            }
            """
        )
        self.layout.addWidget(self.scroll)

        self.header_widget.mousePressEvent = self.start_drag
        self.header_widget.mouseMoveEvent = self.drag_move
        self.header_widget.mouseDoubleClickEvent = self.toggle_details

        self.cleanup_timer = QTimer()
        self.cleanup_timer.timeout.connect(self.check_process_alive)
        self.cleanup_timer.start(2000)   # check every 2 sec

        self.setStyleSheet(
            """
            background-color: rgba(20, 22, 26, 0.92);
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 14px;
            """
        )

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(24)
        shadow.setColor(QColor(0, 0, 0, 160))
        shadow.setOffset(0, 6)
        self.setGraphicsEffect(shadow)

        self.apply_state_style(event_type)

    def refresh_logs(self):
        # clear old logs
        for i in reversed(range(self.details_layout.count())):
            self.details_layout.itemAt(i).widget().deleteLater()

        # add logs
        for log in self.logs:
            label = QLabel(log)
            label.setStyleSheet("""
                color: rgba(226, 232, 240, 0.9);
                padding: 6px 8px;
                font-size: 11px;
                line-height: 16px;
                font-family: "IBM Plex Sans", "Noto Sans", "DejaVu Sans";
            """)
            self.details_layout.addWidget(label)

    def get_button_style(self, kind):
        if kind == "danger":
            return (
                """
                QPushButton {
                    background-color: #EF4444;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 6px 10px;
                    font-weight: 600;
                    font-size: 11px;
                    font-family: "IBM Plex Sans", "Noto Sans", "DejaVu Sans";
                }
                QPushButton:hover {
                    background-color: #F87171;
                }
                """
            )

        return (
            """
            QPushButton {
                background-color: rgba(148, 163, 184, 0.15);
                color: #E2E8F0;
                border: 1px solid rgba(148, 163, 184, 0.2);
                border-radius: 8px;
                padding: 6px 10px;
                font-weight: 600;
                font-size: 11px;
                font-family: "IBM Plex Sans", "Noto Sans", "DejaVu Sans";
            }
            QPushButton:hover {
                background-color: rgba(148, 163, 184, 0.3);
            }
            """
        )

    def apply_state_style(self, state):
        fg, bg = STATE_STYLES.get(state, STATE_STYLES["DEFAULT"])

        self.state_badge.setText(state)
        self.state_badge.setStyleSheet(
            f"""
            color: {fg};
            background-color: {bg};
            border: 1px solid {fg};
            border-radius: 8px;
            padding: 2px 6px;
            font-size: 10px;
            font-weight: 700;
            font-family: "IBM Plex Sans", "Noto Sans", "DejaVu Sans";
            """
        )

        self.count_badge.setStyleSheet(
            """
            color: #CBD5F5;
            background-color: rgba(51, 65, 85, 0.6);
            border-radius: 8px;
            padding: 2px 6px;
            font-size: 10px;
            font-weight: 600;
            font-family: "IBM Plex Sans", "Noto Sans", "DejaVu Sans";
            """
        )

        self.close_btn.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                color: rgba(226, 232, 240, 0.6);
                border: none;
                padding: 2px 6px;
                font-size: 11px;
                font-weight: 700;
            }
            QPushButton:hover {
                color: #F8FAFC;
            }
            """
        )

    def update_data(self, text):
        self.count += 1
        self.count_badge.setText(str(self.count))

        self.summary_label.setText(text)
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

        self.cleanup_timer.stop()

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

        self.apply_state_style(new_state)

        # Button logic
        if new_state == "KILLED":
            self.kill_btn.setVisible(False)
            self.ignore_btn.setVisible(False)

            self.close_btn.setVisible(True)

            # Auto-remove after 3 sec
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

        self.cards = {}
        self.offset = None
        self.setObjectName("root")
        self.setWindowTitle("Seeker")
        self.setGeometry(1600, 800, 360, 260)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(12, 12, 12, 12)

        self.header_widget = QWidget()
        self.header_layout = QHBoxLayout()
        self.header_layout.setContentsMargins(0, 0, 0, 0)
        self.header_layout.setSpacing(8)
        self.header_widget.setLayout(self.header_layout)

        self.title_label = QLabel("seeker")
        self.title_label.setStyleSheet(
            """
            color: #F8FAFC;
            font-size: 16px;
            font-weight: 700;
            letter-spacing: 1px;
            font-family: "IBM Plex Sans", "Noto Sans", "DejaVu Sans";
            """
        )

        self.subtitle_label = QLabel("memory sentinel")
        self.subtitle_label.setStyleSheet(
            """
            color: rgba(148, 163, 184, 0.9);
            font-size: 11px;
            font-weight: 500;
            font-family: "IBM Plex Sans", "Noto Sans", "DejaVu Sans";
            """
        )

        self.header_layout.addWidget(self.title_label)
        self.header_layout.addWidget(self.subtitle_label)
        self.header_layout.addStretch(1)

        self.layout.addWidget(self.header_widget)

        self.log_signal.connect(self._handle_event_ui)

        self.setStyleSheet(
            """
            QWidget#root {
                background-color: rgba(15, 18, 22, 0.88);
                border: 1px solid rgba(148, 163, 184, 0.15);
                border-radius: 18px;
            }
            """
        )

    def _handle_event_ui(self, payload):
        key = payload["key"]
        event_type = payload["type"]
        text = payload["text"]

        # Ignore logic
        if key in ignored_processes:
            if time.time() - ignored_processes[key] < IGNORE_TIME:
                return
            else:
                ignored_processes.pop(key)

        # Remove stale card
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
                "text": f"Memory spike: +{p['delta_mb']/1024:.1f} GB -> Now {p['memory_mb']/1024:.1f} GB",
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