#!/usr/bin/env python3
"""
JinSongToDo - Windows Todo Application
入口文件
"""

import sys
from PySide6.QtWidgets import QApplication
from views import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("JinSongToDo")
    app.setOrganizationName("JinSongToDo")

    # 设置应用样式
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()