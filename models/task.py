from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """任务数据模型"""
    id: Optional[int] = None
    title: str = ""
    description: str = ""
    is_important: bool = False
    is_completed: bool = False
    due_date: Optional[str] = None
    due_time: Optional[str] = None
    reminder: Optional[str] = None
    list_id: int = 0  # 所属列表 ID
    sort_order: int = 0  # 排序顺序
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.updated_at is None:
            self.updated_at = self.created_at

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'is_important': int(self.is_important),
            'is_completed': int(self.is_completed),
            'due_date': self.due_date,
            'due_time': self.due_time,
            'reminder': self.reminder,
            'list_id': self.list_id,
            'sort_order': self.sort_order,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        return cls(
            id=data.get('id'),
            title=data.get('title', ''),
            description=data.get('description', ''),
            is_important=bool(data.get('is_important', 0)),
            is_completed=bool(data.get('is_completed', 0)),
            due_date=data.get('due_date'),
            due_time=data.get('due_time'),
            reminder=data.get('reminder'),
            list_id=data.get('list_id', 0),
            sort_order=data.get('sort_order', 0),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
        )


@dataclass
class TaskList:
    """任务列表（分类）模型"""
    id: Optional[int] = None
    name: str = ""
    color: str = "#0078D4"  # 列表颜色
    is_system: bool = False  # 是否系统内置（不可删除）
    sort_order: int = 0
    icon: str = "📋"  # 列表图标
    created_at: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color,
            'is_system': int(self.is_system),
            'sort_order': self.sort_order,
            'icon': self.icon,
            'created_at': self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'TaskList':
        return cls(
            id=data.get('id'),
            name=data.get('name', ''),
            color=data.get('color', '#0078D4'),
            is_system=bool(data.get('is_system', 0)),
            sort_order=data.get('sort_order', 0),
            icon=data.get('icon', '📋'),
            created_at=data.get('created_at'),
        )