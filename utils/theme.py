"""
主题颜色管理
支持预设主题色，自动保存和加载
"""

# UI 规范色（固定）
PRIMARY = "#5a8f6e"
PRIMARY_LIGHT = "#7ab896"
PRIMARY_EXTRA_LIGHT = "#a8d5b8"
PRIMARY_TRANSPARENT = "rgba(122,158,135,0.12)"
PRIMARY_SHADOW = "rgba(90,143,110,0.25)"

TITLE_COLOR = "#2c2418"
BODY_COLOR = "#3c3020"
SECONDARY_COLOR = "#a09080"
LIGHT_TEXT = "#b0a898"
WARM_GRAY = "#c8bfb0"
VERY_LIGHT_GRAY = "#c0b0a0"
WARM_WHITE = "#ddd6c8"
CREAM = "#e8e0d4"

PAGE_BG = "#f0ebe0"
CARD_BG = "#fffdf8"
CARD_BORDER = "#e4ddd0"
CARD_SHADOW = "rgba(100,80,50,0.10)"
INPUT_BG = "#f7f3ec"
PROGRESS_TRACK = "#ede7dc"
SEPARATOR = "#ede7dc"

FOCUS_BORDER = "#7a9e87"
FOCUS_GLOW = "rgba(122,158,135,0.15)"


THEMES = {
    "blue": {
        "name": "蓝",
        "primary": "#0078D4",
        "hover": "#106EBE",
        "pressed": "#005A9E",
        "light": "#E6F2FA",
    },
    "green": {
        "name": "绿",
        "primary": "#5a8f6e",
        "hover": "#7ab896",
        "pressed": "#4a7f5e",
        "light": "#e8f4ee",
    },
    "purple": {
        "name": "紫",
        "primary": "#8764B8",
        "hover": "#6B4BA8",
        "pressed": "#563D8A",
        "light": "#F3EFF7",
    },
    "red": {
        "name": "红",
        "primary": "#C42B1C",
        "hover": "#A32616",
        "pressed": "#8A2012",
        "light": "#FAE6E4",
    },
    "orange": {
        "name": "橙",
        "primary": "#D83B01",
        "hover": "#BF3700",
        "pressed": "#A63000",
        "light": "#FCF0E6",
    },
    "pink": {
        "name": "粉",
        "primary": "#E3008C",
        "hover": "#C20078",
        "pressed": "#A10066",
        "light": "#FAE6F3",
    },
    "teal": {
        "name": "青",
        "primary": "#008386",
        "hover": "#006B6B",
        "pressed": "#005555",
        "light": "#E6F4F4",
    },
    "gray": {
        "name": "黄",
        "primary": "#FFA500",
        "hover": "#E69500",
        "pressed": "#CC8000",
        "light": "#FFE5CC",
    },
}


class ThemeManager:
    """主题管理器"""

    def __init__(self, db=None):
        self.db = db
        self.current_theme = "green"
        self._load_theme()

    def _load_theme(self):
        """从数据库加载保存的主题"""
        if self.db:
            saved = self.db.get_setting("theme")
            if saved and saved in THEMES:
                self.current_theme = saved

    def save_theme(self):
        """保存主题到数据库"""
        if self.db:
            self.db.set_setting("theme", self.current_theme)

    def set_theme(self, theme_key: str):
        """设置主题"""
        if theme_key in THEMES:
            self.current_theme = theme_key
            self.save_theme()

    def get_current_theme(self) -> dict:
        """获取当前主题的配色"""
        return THEMES.get(self.current_theme, THEMES["green"])

    def get_primary_color(self) -> str:
        """获取主色"""
        return THEMES[self.current_theme]["primary"]

    def get_all_themes(self) -> dict:
        """获取所有主题"""
        return THEMES

    def generate_stylesheet(self) -> str:
        """生成 QSS 样式表"""
        theme = self.get_current_theme()
        primary = theme["primary"]
        hover = theme["hover"]
        pressed = theme["pressed"]
        light = theme["light"]

        return f"""
        QMainWindow {{
            background-color: {PAGE_BG};
        }}
        #sidebar {{
            background-color: {PAGE_BG};
            border-right: 1px solid {CARD_BORDER};
        }}
        #sidebarTitle {{
            font-size: 18px;
            font-weight: 600;
            color: {primary};
            padding: 16px 20px;
            font-family: "Noto Serif SC", "SimSun", serif;
        }}
        #navButton {{
            background: transparent;
            border: none;
            text-align: left;
            padding: 12px 16px;
            font-size: 14px;
            color: {BODY_COLOR};
            border-radius: 10px;
        }}
        #navButton:hover {{
            background-color: {PRIMARY_TRANSPARENT};
        }}
        #navButton:checked {{
            background-color: {primary};
            color: white;
        }}
        #listLabel {{
            font-size: 11px;
            font-weight: 500;
            color: {SECONDARY_COLOR};
            padding: 16px 16px 8px;
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }}
        #colorLabel {{
            font-size: 11px;
            font-weight: 500;
            color: {SECONDARY_COLOR};
            padding: 16px 16px 8px;
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }}
        #taskArea {{
            background-color: {PAGE_BG};
        }}
        #searchInput {{
            padding: 12px 16px;
            border: 1px solid {WARM_WHITE};
            border-radius: 12px;
            font-size: 14px;
            background-color: {INPUT_BG};
            color: {BODY_COLOR};
        }}
        #searchInput:focus {{
            border-color: {FOCUS_BORDER};
            background-color: white;
        }}
        #searchInput::placeholder {{
            color: {LIGHT_TEXT};
        }}
        QPushButton#addButton {{
            background-color: {primary};
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 12px;
            font-size: 14px;
            font-weight: 500;
        }}
        QPushButton#addButton:hover {{
            background-color: {hover};
        }}
        QPushButton#addButton:pressed {{
            background-color: {pressed};
        }}
        #listTitle {{
            font-size: 30px;
            font-weight: 600;
            color: {TITLE_COLOR};
            font-family: "Noto Serif SC", "SimSun", serif;
        }}
        #taskScroll {{
            border: none;
            background: transparent;
        }}
        #quickAddInput {{
            padding: 12px 16px;
            border: 1px solid {WARM_WHITE};
            border-radius: 12px;
            font-size: 14px;
            background-color: {INPUT_BG};
            color: {BODY_COLOR};
        }}
        #quickAddInput:focus {{
            border-color: {FOCUS_BORDER};
            box-shadow: 0 0 0 3px {FOCUS_GLOW};
        }}
        #quickAddInput::placeholder {{
            color: {LIGHT_TEXT};
        }}
        #editButton {{
            background: transparent;
            border: none;
            color: {WARM_GRAY};
            font-size: 14px;
            padding: 4px;
        }}
        #editButton:hover {{
            color: {primary};
        }}
        QWidget#taskCard {{
            background-color: {INPUT_BG};
            border: 1px solid {CREAM};
            border-radius: 12px;
            padding: 13px 14px;
            margin-bottom: 8px;
        }}
        QWidget#taskCard:hover {{
            background-color: white;
            border-color: {CARD_BORDER};
        }}
        QWidget#taskCard QLabel#taskTitle {{
            font-size: 14px;
            font-weight: 300;
            color: {BODY_COLOR};
        }}
        QLabel#createdLabel {{
            font-size: 11px;
            color: {SECONDARY_COLOR};
            margin-left: 8px;
        }}
        QLabel#taskDate {{
            font-size: 12px;
            color: {SECONDARY_COLOR};
            background-color: {PRIMARY_TRANSPARENT};
            padding: 4px 12px;
            border-radius: 20px;
        }}
        QPushButton#taskCheckbox {{
            border: 1.5px solid {WARM_GRAY};
            border-radius: 6px;
            background: white;
            min-width: 22px;
            min-height: 22px;
        }}
        QPushButton#taskCheckbox:checked {{
            background-color: {primary};
            border-color: {primary};
        }}
        #deleteButton {{
            background: transparent;
            border: none;
            color: {WARM_GRAY};
            font-size: 14px;
        }}
        #deleteButton:hover {{
            color: #C42B1C;
        }}
        QPushButton#listButton {{
            background: transparent;
            border: none;
            text-align: left;
            padding: 10px 16px;
            font-size: 14px;
            color: {BODY_COLOR};
            border-radius: 10px;
        }}
        QPushButton#listButton:hover {{
            background-color: {PRIMARY_TRANSPARENT};
        }}
        QPushButton#listButton:checked {{
            background-color: {primary};
            color: white;
        }}
        QPushButton#addListButton {{
            background: transparent;
            border: none;
            text-align: left;
            padding: 10px 16px;
            font-size: 13px;
            color: {SECONDARY_COLOR};
        }}
        QPushButton#addListButton:hover {{
            color: {primary};
        }}
        #separator {{
            background-color: {SEPARATOR};
        }}
        #listScroll {{
            border: none;
            background: transparent;
        }}
        QScrollArea#listScroll {{
            background: transparent;
        }}
        QPushButton#colorButton {{
            border: 2px solid transparent;
            border-radius: 12px;
            min-width: 24px;
            min-height: 24px;
        }}
        QPushButton#colorButton:hover {{
            border-color: {SECONDARY_COLOR};
        }}
        #dropZone {{
            background-color: {PRIMARY_TRANSPARENT};
            border: 3px dashed {primary};
            border-radius: 12px;
        }}
        QLabel#dropIcon {{
            font-size: 48px;
        }}
        QLabel#dropText {{
            font-size: 16px;
            color: {SECONDARY_COLOR};
            font-weight: 500;
        }}
        QPushButton#emojiBtn {{
            font-size: 20px;
            border: 1px solid {WARM_WHITE};
            border-radius: 8px;
            background: white;
            padding: 6px;
        }}
        QPushButton#emojiBtn:hover {{
            background-color: {PRIMARY_TRANSPARENT};
            border-color: {primary};
        }}

        /* 菜单栏样式 */
        QMenuBar {{
            background-color: {CARD_BG};
            border-bottom: 1px solid {SEPARATOR};
            padding: 4px;
        }}
        QMenuBar::item {{
            padding: 8px 16px;
            color: {BODY_COLOR};
        }}
        QMenuBar::item:selected {{
            background-color: {PRIMARY_TRANSPARENT};
            color: {primary};
        }}
        QMenu {{
            background-color: {CARD_BG};
            border: 1px solid {CARD_BORDER};
            border-radius: 8px;
            padding: 4px;
        }}
        QMenu::item {{
            padding: 8px 24px;
            color: {BODY_COLOR};
        }}
        QMenu::item:selected {{
            background-color: {PRIMARY_TRANSPARENT};
            color: {primary};
        }}

        /* 状态栏样式 */
        QStatusBar {{
            background-color: {CARD_BG};
            border-top: 1px solid {SEPARATOR};
            color: {SECONDARY_COLOR};
            font-size: 12px;
        }}

        /* 复选框样式 */
        QCheckBox {{
            spacing: 8px;
            color: {BODY_COLOR};
        }}
        QCheckBox::indicator {{
            width: 22px;
            height: 22px;
            border: 1.5px solid {WARM_GRAY};
            border-radius: 6px;
            background: white;
        }}
        QCheckBox::indicator:checked {{
            background-color: {primary};
            border-color: {primary};
        }}

        /* 进度条样式 */
        QProgressBar {{
            background-color: {PROGRESS_TRACK};
            border: none;
            border-radius: 4px;
            height: 5px;
        }}
        QProgressBar::chunk {{
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                stop:0 {PRIMARY_LIGHT}, stop:1 {PRIMARY_EXTRA_LIGHT});
            border-radius: 4px;
        }}

        /* 下拉框样式 */
        QComboBox {{
            background-color: {INPUT_BG};
            border: 1px solid {WARM_WHITE};
            border-radius: 10px;
            padding: 8px 16px;
            color: {BODY_COLOR};
        }}
        QComboBox:hover {{
            border-color: {primary};
        }}
        QComboBox::drop-down {{
            border: none;
        }}
        QComboBox::down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid {SECONDARY_COLOR};
            margin-right: 8px;
        }}

        /* 对话框样式 */
        QDialog {{
            background-color: {CARD_BG};
            border-radius: 20px;
        }}
        QLabel#dialogTitle {{
            font-size: 18px;
            font-weight: 600;
            color: {TITLE_COLOR};
        }}

        /* 滚动条样式 */
        QScrollBar:vertical {{
            background: transparent;
            width: 8px;
            margin: 0;
        }}
        QScrollBar::handle:vertical {{
            background: {WARM_GRAY};
            border-radius: 4px;
            min-height: 40px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {SECONDARY_COLOR};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0;
        }}
        QScrollBar:horizontal {{
            background: transparent;
            height: 8px;
            margin: 0;
        }}
        QScrollBar::handle:horizontal {{
            background: {WARM_GRAY};
            border-radius: 4px;
            min-width: 40px;
        }}
        QScrollBar::handle:horizontal:hover {{
            background: {SECONDARY_COLOR};
        }}
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0;
        }}

        /* Header 区域 */
        #headerWidget {{
            background: transparent;
        }}
        #dateLabel {{
            font-size: 11px;
            font-weight: 500;
            color: {PRIMARY};
            background-color: {PRIMARY_TRANSPARENT};
            padding: 4px 12px;
            border-radius: 20px;
            letter-spacing: 0.05em;
        }}
        #listTitle {{
            font-size: 30px;
            font-weight: 600;
            color: {TITLE_COLOR};
            font-family: "Noto Serif SC", "SimSun", serif;
        }}
        #quoteLabel {{
            font-size: 13px;
            font-style: italic;
            color: {SECONDARY_COLOR};
        }}

        /* Progress 区域 */
        #progressWidget {{
            background: transparent;
        }}
        #progressText {{
            font-size: 18px;
            font-weight: 600;
            color: {PRIMARY};
            font-family: "Noto Serif SC", "SimSun", serif;
        }}
        #progressDetail {{
            font-size: 12px;
            color: {VERY_LIGHT_GRAY};
        }}

        /* Input 区域 */
        #inputWidget {{
            background: transparent;
        }}
        QPushButton#addButton {{
            background-color: {PRIMARY};
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 20px;
            font-weight: 400;
        }}
        QPushButton#addButton:hover {{
            background-color: {hover};
        }}
        QPushButton#addButton:pressed {{
            background-color: {pressed};
        }}

        /* Filter Tabs 区域 */
        #filterWidget {{
            background-color: {PAGE_BG};
            border-radius: 10px;
            padding: 4px;
        }}
        QPushButton#filterButton {{
            background: transparent;
            border: none;
            padding: 8px 16px;
            font-size: 12px;
            color: {SECONDARY_COLOR};
            border-radius: 8px;
        }}
        QPushButton#filterButton:hover {{
            background-color: {PRIMARY_TRANSPARENT};
        }}
        QPushButton#filterButton:checked {{
            background-color: {CARD_BG};
            color: {PRIMARY};
            font-weight: 500;
            box-shadow: 0 1px 4px rgba(100,80,50,0.08);
        }}

        /* Footer 区域 */
        #footerWidget {{
            background: transparent;
        }}
        QPushButton#clearButton {{
            background: {CARD_BG};
            border: 1px solid {WARM_WHITE};
            border-radius: 8px;
            padding: 6px 12px;
            font-size: 12px;
            color: {SECONDARY_COLOR};
        }}
        QPushButton#clearButton:hover {{
            border-color: {PRIMARY};
            color: {PRIMARY};
        }}
        #clearCountLabel {{
            font-size: 12px;
            color: {SECONDARY_COLOR};
        }}
        """