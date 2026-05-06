import sqlite3
import os
from datetime import datetime
from typing import Optional, List
from .task import Task, TaskList


class Database:
    """SQLite 数据库操作类"""

    def __init__(self, db_path: str = None):
        if db_path is None:
            # 默认在用户数据目录创建
            user_dir = os.path.expanduser("~")
            self.db_path = os.path.join(user_dir, ".wintodo", "wintodo.db")
        else:
            self.db_path = db_path

        # 确保目录存在
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        self.conn = None
        self.connect()

    def connect(self):
        """连接数据库"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        """创建数据表"""
        cursor = self.conn.cursor()

        # 任务列表表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS task_lists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                color TEXT DEFAULT '#0078D4',
                is_system INTEGER DEFAULT 0,
                sort_order INTEGER DEFAULT 0,
                icon TEXT DEFAULT '📋',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 任务表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT DEFAULT '',
                is_important INTEGER DEFAULT 0,
                is_completed INTEGER DEFAULT 0,
                due_date TEXT,
                due_time TEXT,
                reminder TEXT,
                list_id INTEGER DEFAULT 0,
                sort_order INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (list_id) REFERENCES task_lists(id)
            )
        """)

        # 设置表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)

        # 迁移：检查 icon 列是否存在，不存在则添加
        cursor.execute("PRAGMA table_info(task_lists)")
        columns = [row['name'] for row in cursor.fetchall()]
        if 'icon' not in columns:
            cursor.execute("ALTER TABLE task_lists ADD COLUMN icon TEXT DEFAULT '📋'")
        if 'is_system' not in columns:
            cursor.execute("ALTER TABLE task_lists ADD COLUMN is_system INTEGER DEFAULT 0")

        # 初始化默认列表 (id, name, color, is_system, sort_order, icon)
        cursor.execute("SELECT COUNT(*) FROM task_lists")
        if cursor.fetchone()[0] == 0:
            default_lists = [
                (1, "我的日程", "#0078D4", 1, 0, "📅"),
                (2, "重要", "#C42B1C", 1, 1, "⭐"),
                (3, "计划", "#107C10", 1, 2, "📆"),
                (4, "工作", "#8764B8", 0, 3, "💼"),
                (5, "生活", "#D83B01", 0, 4, "🏠"),
                (6, "学习", "#008386", 0, 5, "📚"),
            ]
            cursor.executemany(
                "INSERT INTO task_lists (id, name, color, is_system, sort_order, icon) VALUES (?, ?, ?, ?, ?, ?)",
                default_lists
            )

        self.conn.commit()

    # ==================== 任务列表操作 ====================

    def get_all_lists(self) -> List[TaskList]:
        """获取所有任务列表"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM task_lists ORDER BY sort_order")
        return [TaskList.from_dict(dict(row)) for row in cursor.fetchall()]

    def get_list(self, list_id: int) -> Optional[TaskList]:
        """获取指定列表"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM task_lists WHERE id = ?", (list_id,))
        row = cursor.fetchone()
        return TaskList.from_dict(dict(row)) if row else None

    def create_list(self, name: str, color: str = "#0078D4", icon: str = "📋") -> int:
        """创建新列表"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO task_lists (name, color, icon) VALUES (?, ?, ?)",
            (name, color, icon)
        )
        self.conn.commit()
        return cursor.lastrowid

    def update_list(self, list_id: int, name: str = None, color: str = None, icon: str = None):
        """更新列表"""
        cursor = self.conn.cursor()
        if name is not None:
            cursor.execute("UPDATE task_lists SET name = ? WHERE id = ?", (name, list_id))
        if color is not None:
            cursor.execute("UPDATE task_lists SET color = ? WHERE id = ?", (color, list_id))
        if icon is not None:
            cursor.execute("UPDATE task_lists SET icon = ? WHERE id = ?", (icon, list_id))
        self.conn.commit()

    def delete_list(self, list_id: int) -> bool:
        """删除列表（同时删除关联任务），返回是否成功"""
        cursor = self.conn.cursor()
        # 检查是否是系统列表
        cursor.execute("SELECT is_system FROM task_lists WHERE id = ?", (list_id,))
        row = cursor.fetchone()
        if row and row['is_system'] == 1:
            return False  # 不能删除系统列表
        cursor.execute("DELETE FROM tasks WHERE list_id = ?", (list_id,))
        cursor.execute("DELETE FROM task_lists WHERE id = ?", (list_id,))
        self.conn.commit()
        return True

    # ==================== 任务操作 ====================

    def get_tasks(self, list_id: int = 0, search: str = None) -> List[Task]:
        """获取任务列表"""
        cursor = self.conn.cursor()

        if list_id == -1:  # 重要任务
            query = "SELECT * FROM tasks WHERE is_important = 1"
            params = ()
        elif list_id == -2:  # 计划（已设置截止日期）
            query = "SELECT * FROM tasks WHERE due_date IS NOT NULL"
            params = ()
        elif list_id > 0:
            query = "SELECT * FROM tasks WHERE list_id = ?"
            params = (list_id,)
        else:  # 默认（所有任务）
            query = "SELECT * FROM tasks"
            params = ()

        if search:
            query += " AND title LIKE ?"
            params = params + (f"%{search}%",)

        if list_id == 0:  # 默认查看所有
            query += " ORDER BY is_important DESC, sort_order"
        else:
            query += " ORDER BY is_important DESC, sort_order, created_at DESC"

        cursor.execute(query, params)
        return [Task.from_dict(dict(row)) for row in cursor.fetchall()]

    def get_today_tasks(self) -> List[Task]:
        """获取今天的任务"""
        cursor = self.conn.cursor()
        today = datetime.now().strftime("%Y-%m-%d")
        cursor.execute(
            "SELECT * FROM tasks WHERE due_date = ? ORDER BY sort_order, created_at DESC",
            (today,)
        )
        return [Task.from_dict(dict(row)) for row in cursor.fetchall()]

    def get_task(self, task_id: int) -> Optional[Task]:
        """获取指定任务"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        return Task.from_dict(dict(row)) if row else None

    def create_task(self, task: Task) -> int:
        """创建新任务"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO tasks (title, description, is_important, due_date, due_time, reminder, list_id, sort_order)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            task.title,
            task.description,
            int(task.is_important),
            task.due_date,
            task.due_time,
            task.reminder,
            task.list_id,
            task.sort_order,
        ))
        self.conn.commit()
        return cursor.lastrowid

    def update_task(self, task: Task):
        """更新任务"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE tasks SET
                title = ?,
                description = ?,
                is_important = ?,
                is_completed = ?,
                due_date = ?,
                due_time = ?,
                reminder = ?,
                list_id = ?,
                sort_order = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            task.title,
            task.description,
            int(task.is_important),
            int(task.is_completed),
            task.due_date,
            task.due_time,
            task.reminder,
            task.list_id,
            task.sort_order,
            task.id,
        ))
        self.conn.commit()

    def delete_task(self, task_id: int):
        """删除任务"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()

    def toggle_task_completed(self, task_id: int):
        """切换任务完成状态"""
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE tasks SET is_completed = NOT is_completed, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (task_id,)
        )
        self.conn.commit()

    def update_task_order(self, task_ids: List[int]):
        """更新任务排序"""
        cursor = self.conn.cursor()
        for order, task_id in enumerate(task_ids):
            cursor.execute("UPDATE tasks SET sort_order = ? WHERE id = ?", (order, task_id))
        self.conn.commit()

    # ==================== 设置操作 ====================

    def get_setting(self, key: str) -> Optional[str]:
        """获取设置"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = cursor.fetchone()
        return row['value'] if row else None

    def set_setting(self, key: str, value: str):
        """设置"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
            (key, value)
        )
        self.conn.commit()

    # ==================== 统计 ====================

    def get_today_stats(self) -> tuple:
        """获取今日统计 (完成数, 总数)"""
        cursor = self.conn.cursor()
        today = datetime.now().strftime("%Y-%m-%d")
        cursor.execute(
            "SELECT COUNT(*) FROM tasks WHERE due_date = ? AND is_completed = 1",
            (today,)
        )
        completed = cursor.fetchone()[0]
        cursor.execute(
            "SELECT COUNT(*) FROM tasks WHERE due_date = ?",
            (today,)
        )
        total = cursor.fetchone()[0]
        return completed, total

    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()