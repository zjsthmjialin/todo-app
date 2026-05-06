"""
控制器 - 任务业务逻辑
"""

from models import Task, Database


class TaskController:
    """任务控制器 - 处理任务相关业务逻辑"""

    def __init__(self):
        self.db = Database()

    # ==================== 列表操作 ====================

    def get_all_lists(self):
        return self.db.get_all_lists()

    def create_list(self, name: str, color: str = "#0078D4", icon: str = "📋"):
        return self.db.create_list(name, color, icon)

    def update_list(self, list_id: int, name: str = None, color: str = None, icon: str = None):
        self.db.update_list(list_id, name, color, icon)

    def delete_list(self, list_id: int):
        self.db.delete_list(list_id)

    # ==================== 任务操作 ====================

    def get_tasks(self, list_id: int = 0, search: str = None):
        return self.db.get_tasks(list_id, search)

    def get_today_tasks(self):
        return self.db.get_today_tasks()

    def get_important_tasks(self):
        return self.db.get_tasks(list_id=-1)

    def get_planned_tasks(self):
        return self.db.get_tasks(list_id=-2)

    def create_task(self, title: str, list_id: int = 0, is_important: bool = False,
                    due_date: str = None, due_time: str = None, description: str = ""):
        task = Task(
            title=title,
            description=description,
            is_important=is_important,
            due_date=due_date,
            due_time=due_time,
            list_id=list_id,
        )
        return self.db.create_task(task)

    def update_task(self, task: Task):
        self.db.update_task(task)

    def delete_task(self, task_id: int):
        self.db.delete_task(task_id)

    def toggle_completed(self, task_id: int):
        self.db.toggle_task_completed(task_id)

    def update_task_order(self, task_ids: list):
        self.db.update_task_order(task_ids)

    # ==================== 统计 ====================

    def get_today_stats(self):
        return self.db.get_today_stats()

    def get_completed_count(self, list_id: int = 0):
        """获取已完成任务数量"""
        tasks = self.db.get_tasks(list_id)
        return sum(1 for t in tasks if t.is_completed)

    def delete_completed_tasks(self, list_id: int = 0):
        """删除已完成的任务"""
        tasks = self.db.get_tasks(list_id)
        for task in tasks:
            if task.is_completed:
                self.db.delete_task(task.id)

    # ==================== 设置 ====================

    def get_setting(self, key: str):
        return self.db.get_setting(key)

    def set_setting(self, key: str, value: str):
        self.db.set_setting(key, value)