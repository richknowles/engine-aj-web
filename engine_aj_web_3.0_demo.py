# engine_aj_web_3.0_demo.py
# Copyright (c) 2025 Richard Knowles
# Elgin, Illinois USA
# ENGINE-AJ-WEB v2.0 DEMO
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the “Software”), to use
# the Software **for personal, non-commercial use only**, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED.
#
# Commercial redistribution or resale of this software is strictly prohibited
# without the express written permission of the copyright holder.
#
# All rights reserved.

from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return '''
    <html>
        <head>
            <title>ENGINE-AJ-WEB</title>
            <style>
                html, body { margin: 0; height: 100%; overflow: hidden; }
                iframe { width: 100%; height: 100%; border: none; }
            </style>
        </head>
        <body>
            <iframe src="http://localhost:6080/vnc.html?resize=remote&autoconnect=true&password="></iframe>
        </body>
    </html>
    '''

import csv
import re
import sys
from datetime import datetime, timedelta
from urllib.parse import quote

from PySide6.QtCore import QUrl, QTimer, Qt
from PySide6.QtGui import QFont, QPalette, QColor, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QFileDialog,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSplashScreen,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
# Guard import for Qt WebEngineWidgets
try:
    from PySide6.QtWebEngineWidgets import QWebEngineView
    web_engine_available = True
except ImportError:
    web_engine_available = False
    print("⚠️ QtWebEngineWidgets not available — Web views disabled")


# === DEMO LIMIT CONSTANTS ===
DEMO_MAX_MESSAGES = 10
BUILD_DATE = datetime.today()
EXPIRY_DATE = BUILD_DATE + timedelta(days=10)

# ---- Neon Console Theme ----
CONSOLE_BG = "#181b1a"
NEON_GREEN = "#19ff80"
CONTRAST_BG = "#232623"
TXT_BG = "#232d23"


def is_phone(val: str) -> bool:
    val = val.strip()
    if val.startswith("https://wa.me/") or val.startswith("https://api.whatsapp.com/send"):
        return True
    digits = re.sub(r"[^\d]", "", val)
    return 8 <= len(digits) <= 20

# Guard import for Qt WebEngineWidgets
try:
    from PySide6.QtWebEngineWidgets import QWebEngineView
    web_engine_available = True
except ImportError:
    web_engine_available = False
    print("⚠️ QtWebEngineWidgets not available — Web views disabled")

# Define CustomWebView only if WebEngine is available
if web_engine_available:
    class CustomWebView(QWebEngineView):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._user_agent = (
                "Mozilla/5.0 (Web NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.6367.208 Safari/537.36"
            )

        def createWindow(self, _type):  # noqa: U100
            return self

        def setUserAgent(self, agent: str = None):
            self._user_agent = agent or self._user_agent

        def userAgent(self) -> str:
            return self._user_agent

        def load(self, url: QUrl):
            profile = self.page().profile()
            profile.setHttpUserAgent(self._user_agent)
            super().load(url)
else:
    class CustomWebView:
        def __init__(self, *args, **kwargs):
            raise RuntimeError(
                "CustomWebView unavailable — QtWebEngine not installed."
            )

# after import guard
...
if web_engine_available:
    browser_frame = QFrame()
    br_layout = QVBoxLayout(browser_frame)
    self.webview = CustomWebView()
    br_layout.addWidget(self.webview)
    split.addWidget(browser_frame, stretch=5)

     # Load only if WebEngine is enabled
    self.webview.load(QUrl("https://web.whatsapp.com/"))
else:
    print("⚠️ Skipping browser frame and webview load — WebEngine disabled")


class RecipientItem(QWidget):
    def __init__(self, phone: str, name: str = ""):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 2, 4, 2)
        text = f"{phone} ({name})" if name else phone
        self.label = QLabel(text)
        self.progress = QProgressBar()
        self.progress.setFixedWidth(100)
        self.progress.setRange(0, 100)
        self.status_icon = QLabel("⏳")
        layout.addWidget(self.label)
        layout.addWidget(self.progress)
        layout.addWidget(self.status_icon)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ENGINE-AJ v2.0 DEMO – 10 MSG LIMIT / 10 DAY EXPIRY")
        self.resize(1280, 880)

        font = QFont("Consolas, Courier New, monospace", 13)
        QApplication.instance().setFont(font)
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(CONSOLE_BG))
        palette.setColor(QPalette.Base, QColor(TXT_BG))
        palette.setColor(QPalette.WindowText, QColor(NEON_GREEN))
        palette.setColor(QPalette.Text, QColor(NEON_GREEN))
        palette.setColor(QPalette.Button, QColor(CONSOLE_BG))
        palette.setColor(QPalette.ButtonText, QColor(NEON_GREEN))
        palette.setColor(QPalette.Highlight, QColor(NEON_GREEN))
        palette.setColor(QPalette.HighlightedText, QColor(CONSOLE_BG))
        self.setPalette(palette)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(8)

        banner = QLabel("┏━━━[ ENGINE-AJ v2.0 DEMO ]━━━┓")
        banner.setAlignment(Qt.AlignCenter)
        banner.setStyleSheet(
            f"color:{NEON_GREEN}; background:{CONSOLE_BG};"
            "font-size:17px; font-weight:bold;"
        )
        main_layout.addWidget(banner)

        split = QHBoxLayout()
        split.setSpacing(12)
        main_layout.addLayout(split)

        controls = QFrame()
        controls.setStyleSheet(
            f"background:{CONTRAST_BG};"
            f"border:2px solid {NEON_GREEN}; border-radius:8px; color:{NEON_GREEN};"
        )
        ctl_layout = QVBoxLayout(controls)
        ctl_layout.setContentsMargins(11, 11, 11, 11)
        ctl_layout.setSpacing(9)

        self.csv_btn = QPushButton("📂 Select Recipients CSV")
        self.csv_btn.clicked.connect(self.select_csv)
        ctl_layout.addWidget(self.csv_btn)
        self.csv_path = QLineEdit()
        self.csv_path.setReadOnly(True)
        self.csv_path.setPlaceholderText("No CSV selected...")
        ctl_layout.addWidget(self.csv_path)

        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet(f"background:{TXT_BG}; color:{NEON_GREEN};")
        ctl_layout.addWidget(self.list_widget, stretch=2)

        self.msg_edit = QTextEdit()
        self.msg_edit.setStyleSheet(f"background:{TXT_BG}; color:{NEON_GREEN};")
        self.msg_edit.setFixedHeight(120)
        self.msg_edit.setPlaceholderText("Type your message here…")
        ctl_layout.addWidget(self.msg_edit)

        self.send_btn = QPushButton("▶ Send to All")
        self.send_btn.clicked.connect(self.send_to_all)
        ctl_layout.addWidget(self.send_btn)

        self.progress = QProgressBar()
        self.progress.hide()
        ctl_layout.addWidget(self.progress)
        ctl_layout.addStretch()

        split.addWidget(controls, stretch=2)

        # Inside MainWindow.__init__, after building layouts like 'split'
        if web_engine_available:
            browser_frame = QFrame()
            br_layout = QVBoxLayout(browser_frame)
            self.webview = CustomWebView()
            br_layout.addWidget(self.webview)
            split.addWidget(browser_frame, stretch=5)

            self.webview.load(QUrl("https://web.whatsapp.com/"))
        else:
            print("⚠️ Skipping browser frame and webview load — WebEngine disabled")
            # Remove any other references to self.webview below
        
        self.recipients = []
        self.widgets = []

        # Expiry check
        if datetime.now() > EXPIRY_DATE:
            QMessageBox.critical(self, "Expired", "Demo expired.")
            sys.exit()

        #self.webview.load(QUrl("https://web.whatsapp.com/"))
        #self.webview.loadFinished.connect(self.inject_dark_mode_js)

    def select_csv(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select CSV", "", "CSV Files (*.csv)")
        if not path:
            return
        self.csv_path.setText(path)
        self.list_widget.clear()
        self.recipients.clear()
        self.widgets.clear()
        with open(path, newline='', encoding='utf-8-sig') as f:
            for row in csv.reader(f):
                phone, name = row[0].strip(), row[1].strip() if len(row) > 1 else ''
                if is_phone(phone):
                    item = QListWidgetItem()
                    widget = RecipientItem(phone, name)
                    self.list_widget.addItem(item)
                    self.list_widget.setItemWidget(item, widget)
                    self.recipients.append((phone, name))
                    self.widgets.append(widget)

    def inject_dark_mode_js(self):
        js = (
            "document.body.setAttribute('data-theme','dark');"
            "document.body.style.background='#181b1a';"
            "document.body.style.color='#19ff80';"
            "var s=document.createElement('style');"
            "s.innerHTML='* { font-family: Consolas !important; }';"
            "document.head.appendChild(s);"
        )
        self.webview.page().runJavaScript(js)

    def send_to_all(self):
        # Enforce demo limits
        if len(self.recipients) > DEMO_MAX_MESSAGES:
            QMessageBox.warning(
                self, "Demo Limit",
                f"Demo allows only {DEMO_MAX_MESSAGES} messages. Sending to first {DEMO_MAX_MESSAGES} recipients."
            )
            self.recipients = self.recipients[:DEMO_MAX_MESSAGES]
            self.widgets = self.widgets[:DEMO_MAX_MESSAGES]

        self._idx = 0
        self._msg = self.msg_edit.toPlainText().strip()
        if not self._msg:
            QMessageBox.warning(self, "No Message", "Please type a message before sending.")
            return
        total = len(self.recipients)
        self.progress.setRange(0, total)
        self.progress.setValue(0)
        self.progress.show()
        self._send_next()

    def _send_next(self):
        if self._idx >= len(self.recipients):
            QMessageBox.information(self, "Done", "All messages sent.")
            return
        phone, _ = self.recipients[self._idx]
        num = re.sub(r"[^\d]", "", phone)
        url = f"https://web.whatsapp.com/send?phone={num}&text={quote(self._msg)}&app_absent=0"
        widget = self.widgets[self._idx]
        widget.progress.setValue(50)
        self.webview.load(QUrl(url))
        QTimer.singleShot(6000, self._inject_and_continue)

    def _inject_and_continue(self):
        widget = self.widgets[self._idx]
        js = (
            "(function(){"
            "  var btn = document.querySelector(\"button[data-testid='compose-btn-send']\");"
            "  if(!btn) btn = document.querySelector(\"span[data-icon='send']\");"
            "  if(btn) btn.click();"
            "})();"
        )
        self.webview.page().runJavaScript(js)
        widget.progress.setValue(100)
        widget.status_icon.setText("✅")
        self._idx += 1
        self.progress.setValue(self._idx)
        if self._idx < len(self.recipients):
            QTimer.singleShot(2200, self._send_next)


if __name__ == "__main__":
    import multiprocessing
    from flask import Flask
    from threading import Thread

    # Flask app to show "we're alive" on port 5000
    flask_app = Flask(__name__)

    @flask_app.route("/")
    def index():
        return """
        <h1>ENGINE-AJ is running 💚</h1>
        <p>To use the GUI, <strong>connect via noVNC</strong>:<br>
        👉 <a href="https://engine-aj.ajricardo.com:6080" target="_blank">engine-aj.ajricardo.com:6080</a></p>
        """

    def run_flask():
        flask_app.run(host="0.0.0.0", port=5000)

    def run_qt():
        qt_app = QApplication(sys.argv)
        qt_app.processEvents()
        Web = MainWindow()
        Web.show()
        sys.exit(qt_app.exec())

    Thread(target=run_flask, daemon=True).start()
    run_qt()
