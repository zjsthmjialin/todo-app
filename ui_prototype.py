import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QListWidget, QStatusBar, QScrollArea
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPalette, QColor


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WinTodo")
        self.setMinimumSize(900, 600)
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 左侧导航栏
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar, 1)

        # 右侧任务区域
        task_area = self.create_task_area()
        main_layout.addWidget(task_area, 4)

        # 状态栏
        self.statusBar().showMessage("今日已完成 0/0")

    def create_sidebar(self):
        sidebar = QWidget()
        sidebar.setFixedWidth(220)
        sidebar.setObjectName("sidebar")

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(8, 16, 8, 8)
        layout.setSpacing(4)

        # 标题
        title = QLabel("WinTodo")
        title.setObjectName("sidebarTitle")
        layout.addWidget(title)

        layout.addSpacing(16)

        # 导航项
        nav_items = ["我的日程", "重要", "计划"]
        for item in nav_items:
            btn = QPushButton(item)
            btn.setObjectName("navButton")
            btn.setCheckable(True)
            layout.addWidget(btn)

        # 任务列表区域
        list_label = QLabel("任务列表")
        list_label.setObjectName("listLabel")
        layout.addWidget(list_label)

        lists = ["工作", "生活", "学习"]
        for lst in lists:
            btn = QPushButton(lst)
            btn.setObjectName("navButton")
            layout.addWidget(btn)

        layout.addStretch()

        # 颜色设置区域
        color_label = QLabel("主题颜色")
        color_label.setObjectName("colorLabel")
        layout.addWidget(color_label)

        color_layout = QHBoxLayout()
        colors = ["#0078D4", "#107C10", "#8764B8", "#C42B1C",
                  "#D83B01", "#E3008C", "#008386", "#5D5F61"]
        for c in colors:
            color_btn = QPushButton()
            color_btn.setFixedSize(24, 24)
            color_btn.setStyleSheet(f"background-color: {c}; border-radius: 4px; border: none;")
            color_btn.setObjectName("colorButton")
            color_layout.addWidget(color_btn)
        layout.addLayout(color_layout)

        return sidebar

    def create_task_area(self):
        container = QWidget()
        container.setObjectName("taskArea")

        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # 搜索栏
        search_layout = QHBoxLayout()
        search_input = QLineEdit()
        search_input.setPlaceholderText("搜索任务...")
        search_input.setObjectName("searchInput")
        search_layout.addWidget(search_input)

        add_btn = QPushButton("+ 添加任务")
        add_btn.setObjectName("addButton")
        search_layout.addWidget(add_btn)
        layout.addLayout(search_layout)

        # 当前列表标题
        self.list_title = QLabel("我的日程")
        self.list_title.setObjectName("listTitle")
        layout.addWidget(self.list_title)

        # 任务列表 (可滚动)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("taskScroll")

        task_widget = QWidget()
        task_layout = QVBoxLayout(task_widget)
        task_layout.setSpacing(8)
        task_layout.setContentsMargins(0, 0, 0, 0)

        # 示例任务卡片
        for i in range(5):
            card = self.create_task_card(f"示例任务 {i+1}", i % 2 == 0)
            task_layout.addWidget(card)

        task_layout.addStretch()

        scroll.setWidget(task_widget)
        layout.addWidget(scroll)

        return container

    def create_task_card(self, title, is_important=False):
        card = QWidget()
        card.setObjectName("taskCard")

        layout = QHBoxLayout(card)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        # 勾选框
        checkbox = QPushButton()
        checkbox.setFixedSize(20, 20)
        checkbox.setObjectName("checkbox")
        checkbox.setCheckable(True)
        layout.addWidget(checkbox)

        # 任务内容
        content_layout = QVBoxLayout()
        title_label = QLabel(title)
        title_label.setObjectName("taskTitle")
        if is_important:
            title_label.setText(f"⭐ {title}")
        content_layout.addWidget(title_label)

        date_label = QLabel("今天")
        date_label.setObjectName("taskDate")
        content_layout.addWidget(date_label)
        layout.addLayout(content_layout)

        # 删除按钮
        delete_btn = QPushButton("×")
        delete_btn.setFixedSize(24, 24)
        delete_btn.setObjectName("deleteButton")
        layout.addWidget(delete_btn)

        return card


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 设置浅色主题
    app.setStyle("Fusion")

    stylesheet = """
    QMainWindow {
        background-color: #F3F3F3;
    }
    #sidebar {
        background-color: #FFFFFF;
        border-right: 1px solid #E5E5E5;
    }
    #sidebarTitle {
        font-size: 18px;
        font-weight: bold;
        color: #0078D4;
        padding: 8px;
    }
    #navButton {
        background: transparent;
        border: none;
        text-align: left;
        padding: 10px 12px;
        font-size: 14px;
        border-radius: 4px;
        color: #323130;
    }
    #navButton:hover {
        background-color: #F3F3F3;
    }
    #navButton:checked {
        background-color: #0078D4;
        color: white;
    }
    #listLabel {
        font-size: 12px;
        color: #605E5C;
        padding: 8px 12px;
        font-weight: bold;
    }
    #colorLabel {
        font-size: 12px;
        color: #605E5C;
        padding: 8px 0;
    }
    #taskArea {
        background-color: #F3F3F3;
    }
    #searchInput {
        padding: 10px 16px;
        border: 1px solid #E5E5E5;
        border-radius: 6px;
        font-size: 14px;
        background-color: white;
    }
    #addButton {
        background-color: #0078D4;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 6px;
        font-size: 14px;
        font-weight: bold;
    }
    #listTitle {
        font-size: 24px;
        font-weight: bold;
        color: #323130;
    }
    #taskScroll {
        border: none;
        background: transparent;
    }
    #taskCard {
        background-color: white;
        border-radius: 8px;
        padding: 4px;
    }
    #taskTitle {
        font-size: 14px;
        color: #323130;
    }
    #taskDate {
        font-size: 12px;
        color: #A19F9D;
    }
    #checkbox {
        border: 2px solid #0078D4;
        border-radius: 10px;
        background: white;
    }
    #deleteButton {
        background: transparent;
        border: none;
        color: #A19F9D;
        font-size: 18px;
    }
    """
    app.setStyleSheet(stylesheet)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())