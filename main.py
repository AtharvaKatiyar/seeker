from PyQt6.QtWidgets import QApplication
import sys
import threading

from ui import LogWidget, handle_event_ui
from ui import set_widget  # add this import
from core import main as core_main


def start_core():
    core_main()


if __name__ == "__main__":
    core_thread = threading.Thread(target=start_core, daemon=True)
    core_thread.start()

    # Run UI in main thread
    app = QApplication(sys.argv)
    widget = LogWidget()

    set_widget(widget)

    widget.show()

    sys.exit(app.exec())