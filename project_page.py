import csv
import qtawesome as qta
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea,
    QFrame, QPushButton, QLabel,
    QHBoxLayout, QFileDialog, QMessageBox,
    QDialog
)
from PyQt6.QtCore import pyqtSignal, Qt, QSize

from edit_dialog import EditDialog


class ProjectPage(QWidget):
    """
    Данный класс используется для создания страницы о проекте.
    Включает в себя данные: описание, конфигурацию, стоимость
    Имеет кнопку "Назад" для возврата к главной странице
    """

    # Создаем сигнал для PyQt для возврата на главную страницу:
    go_back = pyqtSignal()

    def __init__(self, project_manager, parent=None):
        super().__init__(parent)
        self.project_manager = project_manager
        self.setObjectName("ProjectPage")
        self.current_project = None
        self._build_ui()

    def _build_ui(self):
        # Основной контейнер с прокруткой вниз на случай длинного описания:
        outer_layout = QVBoxLayout(self)

        btn_and_title_layout = QHBoxLayout()

        # Кнопка "Назад" для возвращения к предыдущей странице:
        back_button = QPushButton("<- Назад")
        back_button.setObjectName("BackButton")
        back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        back_button.setFixedSize(100, 30)
        back_button.clicked.connect(self.go_back.emit)
        btn_and_title_layout.addWidget(
            back_button, alignment=Qt.AlignmentFlag.AlignLeft
        )

        # Заголовок проекта:
        title_and_editbtn = QHBoxLayout()

        self.title_label = QLabel()
        self.title_label.setObjectName("ProjectPageTitle")
        self.title_label.setWordWrap(True)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # == Кнопка для изменения описания ==
        title_edit_btn = QPushButton()
        title_edit_btn.setIcon(qta.icon("fa6s.pen", color="white"))
        title_edit_btn.setIconSize(QSize(14, 14))
        title_edit_btn.setFixedSize(30, 30)
        title_edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        title_edit_btn.clicked.connect(self.edit_the_project_title)
        title_edit_btn.setObjectName("EditButton")

        # == Кнопка для изменения описания ==
        delete_project_btn = QPushButton()
        delete_project_btn.setIcon(qta.icon("fa6s.trash", color="red"))
        delete_project_btn.setIconSize(QSize(16, 16))
        delete_project_btn.setFixedSize(30, 30)
        delete_project_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_project_btn.clicked.connect(self.delete_the_project_title)
        delete_project_btn.setObjectName("DeleteButton")

        title_and_editbtn.addWidget(self.title_label)
        title_and_editbtn.addWidget(title_edit_btn)
        title_and_editbtn.addWidget(delete_project_btn)

        btn_and_title_layout.addLayout(title_and_editbtn)

        # Кнопки экспорта в CSV, TXT (справа):
        export_container = QFrame()
        export_container.setFixedSize(200, 50)
        export_layout = QHBoxLayout(export_container)
        export_layout.setSpacing(6)
        export_layout.addStretch()

        # Кнопка для экспорта в csv:
        csv_button = QPushButton("CSV")
        csv_button.setObjectName("ExportButton")
        csv_button.setCursor(Qt.CursorShape.PointingHandCursor)
        csv_button.setFixedSize(60, 30)
        csv_button.clicked.connect(self.export_to_csv)

        # Кнопка для экспорта в txt:
        txt_button = QPushButton("TXT")
        txt_button.setObjectName("ExportButton")
        txt_button.setCursor(Qt.CursorShape.PointingHandCursor)
        txt_button.setFixedSize(60, 30)
        txt_button.clicked.connect(self.export_to_txt)

        export_layout.addWidget(csv_button)
        export_layout.addWidget(txt_button)

        btn_and_title_layout.addWidget(export_container)

        outer_layout.addLayout(btn_and_title_layout)

        # Скролл - только контент
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setObjectName("ProjectScroll")

        content = QWidget()
        content.setObjectName("ProjectContent")
        layout = QVBoxLayout(content)
        layout.setSpacing(20)

        # Блок с описанием проекта:
        desc_frame = QFrame()
        desc_frame.setObjectName("InfoBlock")
        desc_layout = QVBoxLayout(desc_frame)
        desc_layout.setSpacing(8)

        desc_and_editbtn = QHBoxLayout()

        # === Лейбл с описанием ===
        desc_header = QLabel("Описание")
        desc_header.setObjectName("BlockHeader")

        # == Кнопка для изменения описания ==
        desc_edit_btn = QPushButton()
        desc_edit_btn.setIcon(qta.icon("fa6s.pen", color="black"))
        desc_edit_btn.setIconSize(QSize(14, 14))
        desc_edit_btn.setFixedSize(30, 30)
        desc_edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        desc_edit_btn.clicked.connect(self.edit_the_project_desc)
        desc_edit_btn.setObjectName("EditButton")

        desc_and_editbtn.addWidget(desc_header)
        desc_and_editbtn.addWidget(desc_edit_btn)

        desc_layout.addLayout(desc_and_editbtn)

        self.desc_label = QLabel()
        self.desc_label.setObjectName("BlockText")
        self.desc_label.setWordWrap(True)
        desc_layout.addWidget(self.desc_label)

        layout.addWidget(desc_frame)

        # Блок с конфигурацией:
        config_frame = QFrame()
        config_frame.setObjectName("InfoBlock")
        config_layout = QVBoxLayout(config_frame)
        config_layout.setSpacing(8)

        config_and_editbtn = QHBoxLayout()

        config_header = QLabel("Конфигурация:")
        config_header.setObjectName("BlockHeader")

        # == Кнопка для изменения конфигурации ==
        desc_edit_btn = QPushButton()
        desc_edit_btn.setIcon(qta.icon("fa6s.pen", color="black"))
        desc_edit_btn.setIconSize(QSize(14, 14))
        desc_edit_btn.setFixedSize(30, 30)
        desc_edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        desc_edit_btn.clicked.connect(self.edit_the_project_config)
        desc_edit_btn.setObjectName("EditButton")

        config_and_editbtn.addWidget(config_header)
        config_and_editbtn.addWidget(desc_edit_btn)

        config_layout.addLayout(config_and_editbtn)

        self.config_label = QLabel()
        self.config_label.setObjectName("BlockText")
        self.config_label.setWordWrap(True)
        config_layout.addWidget(self.config_label)

        layout.addWidget(config_frame)

        # Блок цена:
        price_frame = QFrame()
        price_frame.setObjectName("PriceBlock")
        price_layout = QVBoxLayout(price_frame)
        price_layout.setSpacing(8)

        price_header = QLabel("Стоимость:")
        price_header.setObjectName("PriceBlockHeader")
        price_layout.addWidget(price_header)

        self.price_label = QLabel()
        self.price_label.setObjectName("BigPrice")
        price_layout.addWidget(self.price_label)
        price_layout.addStretch()

        layout.addWidget(price_frame)

        scroll.setWidget(content)
        outer_layout.addWidget(scroll)

    def load_project(self, project_data):
        """
        Загружает данные проекта на страницу с хранилища project_data
        """

        self.current_project = project_data

        self.title_label.setText(f"Проект: {project_data["name"]}")
        self.desc_label.setText(project_data["description"])
        self.config_label.setText(
            f"<b>Процессор:</b> {project_data["config"]["cpu"]}<br>"
            f"<b>Материнская плата:</b> {project_data["config"]["mat"]}<br>"
            f"<b>Блок питания:</b> {project_data["config"]["pb"]}<br>"
            f"<b>Видеокарта:</b> {project_data["config"]["gpu"]}<br>"
            f"<b>Оперативная память:</b> {project_data["config"]["ram"]}<br>"
            f"<b>Накопитель (SSD):</b> {project_data["config"]["ssd"]}<br>"
            f"<b>Корпус:</b> {project_data["config"]["case"]}<br>"
            f"<b>Охлаждение:</b> {project_data["config"]["cooling"]}<br>"
        )
        self.price_label.setText(project_data["price"])

    # Функция для экспорта в CSV:
    def export_to_csv(self):
        if not self.current_project:
            return

        # Диалог выбора файла. Возвращает (путь, выбранный фильтр)
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить проект в CSV",
            f"{self.current_project["name"]}.csv",
            "CSV файлы (*.csv)"
        )

        if not file_path:
            return

        try:
            # Заголовки столбцов:
            headers = [
                "id", "name", "description", "price",
                "cpu", "mat", "pb", "gpu", "ram",
                "ssd", "case", "cooling"
            ]

            # Значения в таком же порядке, что и заголовки:
            values = [
                self.current_project["id"],
                self.current_project["name"],
                self.current_project["description"],
                self.current_project["config"]["price"],
                self.current_project["config"]["cpu"],
                self.current_project["config"]["mat"],
                self.current_project["config"]["pb"],
                self.current_project["config"]["gpu"],
                self.current_project["config"]["ram"],
                self.current_project["config"]["ssd"],
                self.current_project["config"]["case"],
                self.current_project["config"]["cooling"],
            ]

            with open(file_path, "w", encoding="utf8", newline="") as file:
                writer = csv.writer(file, delimiter=";")
                writer.writerow(headers)
                writer.writerow(values)

            QMessageBox.information(
                self, "Успех", f"Проект сохранён в:\n{file_path}"
            )

        except Exception:
            QMessageBox.critical(
                self, "Ошибка", f"Не удалось сохранить:\n{file_path}"
            )

    # Функция для эскпорта в txt:
    def export_to_txt(self):
        if not self.current_project:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить проект в TXT",
            f"{self.current_project["name"]}.txt",
            "TXT файлы (*.txt)"
        )

        if not file_path:
            return

        try:
            p = self.current_project

            content = (
                f"=== Проект: {p["name"]} ===\n\n"
                f"Описание:\n{p["description"]}\n\n"
                f"Конфигурация:\n"
                f"  - Процессор: {p["config"]["cpu"]}\n"
                f"  - Видеокарта: {p["config"]["gpu"]}\n"
                f"  - Материнская плата: {p["config"]["mat"]}\n"
                f"  - Блок питания: {p["config"]["pb"]}\n"
                f"  - Оперативная память: {p["config"]["ram"]}\n"
                f"  - SSD: {p["config"]["ssd"]}\n"
                f"  - Корпус: {p["config"]["case"]}\n"
                f"  - Охлаждение: {p["config"]["cooling"]}\n"
            )

            with open(file_path, "w", encoding="utf8") as file:
                file.write(content)

            QMessageBox.information(
                self, "Успех", f"Проект успешно сохранён в:\n{file_path}"
            )
        except Exception as e:
            QMessageBox.critical(
                self, "Ошибка", f"Не удалось сохранить:\n{e}"
            )

    def edit_the_project_title(self):
        if not self.current_project:
            return

        old_name = self.current_project["name"]

        dialog = EditDialog(
            title="Редактировать название",
            label_text="Введите новое название проекта:",
            initial_text=old_name,
            parent=self
        )

        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_name = dialog.get_text()

            if new_name.strip():
                project_id = self.current_project["id"]

                # Обновляем через ProjectManager:
                self.project_manager.update_project(
                    project_id,
                    {"name": new_name}
                )

                # Обновляем локально:
                self.current_project["name"] = new_name
                self.title_label.setText(new_name)

                if old_name != new_name:
                    # Отправляем сообщение об успехе операции:
                    QMessageBox.information(
                        self, "Успех", "Название обновлено!"
                    )

    def edit_the_project_desc(self):
        if not self.current_project:
            return

        old_desc = self.current_project["description"]

        dialog = EditDialog(
            title="Редактировать описание",
            label_text="Введите новое описание проекта:",
            initial_text=old_desc,
            parent=self
        )

        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_desc = dialog.get_text()

            if new_desc.strip():
                project_id = self.current_project["id"]

                # Обновляем через ProjectManager:
                self.project_manager.update_project(
                    project_id,
                    {"description": new_desc}
                )

                # Обновляем локальные данные:
                self.current_project["description"] = new_desc
                self.desc_label.setText(new_desc)

                if new_desc != old_desc:
                    QMessageBox.information(
                        self, "Успех", "Описание обновлено!"
                    )

    def edit_the_project_config(self):
        pass

    def delete_the_project_title(self):
        reply = QMessageBox.question(
            self,
            "Подтверждение", f"Удалить проект {self.current_project["name"]}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            project_id = self.current_project["id"]
            self.project_manager.delete_project(project_id)

            # Обязательно возвращаемся к списку проектов
            self.go_back.emit()
