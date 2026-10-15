import json
from pathlib import Path


class ProjectManager:
    """
    Данный класс хранит данные в памяти (в кеш) и синхронизируется с файлом
    """

    def __init__(self, filepath="projects.json"):
        self.filepath = Path(filepath)
        self.projects = {}
        self.load()

    def load(self):
        """Загружает все проекты из JSON в кеш"""
        if self.filepath.exists():
            with open(self.filepath, "r", encoding="utf8") as file:
                self.projects = json.load(file)

        else:
            self.projects = {}

    def save(self):
        """Сохраняет кеш в JSON"""
        with open(self.filepath, "w", encoding="utf8") as file:
            json.dump(self.projects, file, ensure_ascii=False, indent=2)

    def get_project(self, project_id):
        """Получить проект по ID (из кеша)"""
        project_id = str(project_id)
        project = self.projects.get(project_id)

        if project:
            # Возвращаем копию, чтобы случайные изменения не сломали кеш:
            return {"id": project_id, **project}
        return None

    def get_all_projects(self):
        """Получить все проекты (из кеша)"""
        return {
            pid: {"id": pid, **pdata}
            for pid, pdata in self.projects.items()
        }

    def create_project(self, project_id, data):
        """Создать проект"""
        project_id = str(project_id)
        self.projects[project_id] = data
        self.save()

    def update_project(self, project_id, data):
        """
        Обновляет проект
        Изменяет и кеш, и файл, чтобы не было десинхроза
        """

        project_id = str(project_id)
        if project_id in self.projects:
            self.projects[project_id].update(data)
            self.save()
            return True

        return False

    def delete_project(self, project_id):
        """Удалить проект"""
        project_id = str(project_id)
        if project_id in self.projects:
            del self.projects[project_id]
            self.save()
            return True
        return False

    def get_next_id(self):
        """Получить следующий доступный ID"""
        if not self.projects:
            return "1"

        max_id = max(int(pid) for pid in self.projects.keys())
        return str(max_id + 1)
