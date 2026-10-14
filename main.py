import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontDatabase
from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow,
    QVBoxLayout, QLabel, QFrame,
    QPushButton, QScrollArea, QStackedWidget
)

from project_card import ProjectCard
from project_page import ProjectPage
from project_manager import ProjectManager


class PcBuilder(QMainWindow):
    def __init__(self):
        super().__init__()

        self.project_manager = ProjectManager("projects.json")

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Выбор проекта:")
        self.setFixedHeight(700)
        self.setFixedWidth(800)
        central_widget = QWidget()

        main_layout = QVBoxLayout(central_widget)

        # Создаем QStackedWidget() - контейнер для страниц
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        # Первая страница - показ всех проектов:
        self.list_page = self._build_list_page()
        self.stack.addWidget(self.list_page)

        # Вторая страница - детальная страница каждого проекта:
        self.project_page = ProjectPage(self.project_manager)
        # Обязательно нужно связать страницу, чтобы вернуться назад:
        self.project_page.go_back.connect(self.show_list_page)
        self.stack.addWidget(self.project_page)

        # По умолчанию ставим первую страницу:
        self.stack.setCurrentIndex(0)

        self.setCentralWidget(central_widget)

    def _build_list_page(self):
        """Эта функция "собирает" начальную страницу"""
        page = QWidget()
        layout = QVBoxLayout(page)

        blue_gradient_text = (
            "Добро пожаловать в "
            "<span style='color:#0041a8;'>P</span>"
            "<span style='color:#0055c4;'>C</span>"
            "<span style='color:#006ae0;'>B</span>"
            "<span style='color:#0080ff;'>u</span>"
            "<span style='color:#1aa3ff;'>i</span>"
            "<span style='color:#33b5ff;'>l</span>"
            "<span style='color:#4dc8ff;'>d</span>"
            "<span style='color:#66daff;'>e</span>"
            "<span style='color:#80ecff;'>r</span>!"
        )

        welcome_title_label = QLabel(blue_gradient_text)
        welcome_title_label.setObjectName("WelcomeTitle")
        welcome_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome_title_label)

        welcome_desc_label = QLabel(
            "Выберите проект из предпложенного списка:"
        )
        welcome_desc_label.setObjectName("WelcomeDesc")
        welcome_desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome_desc_label)

        # Скролл для просмотра всего списка проектов:
        scroll_area = QScrollArea()
        scroll_area.setObjectName("ProjectsScrollArea")
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )

        # Создаем контейнер для списка карточек:
        scroll_content = QWidget()
        scroll_content.setObjectName("ScrollContent")
        cards_layout = QVBoxLayout(scroll_content)
        cards_layout.setSpacing(15)
        cards_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # ЧИТАЕМ CSV и записываем их, чтобы потом не читать файл:
        all_projects = self.project_manager.get_all_projects()

        for pid, pd in all_projects.items():
            config = (
                f"{pd["cpu"]} | {pd["mat"]} | {pd["gpu"]} |"
                f"{pd["pb"]}"
            )

            # Создаем карточку проекта с краткой инфой:
            card = ProjectCard(
                project_id=pid,
                project_name=pd["name"],
                desc=pd["description"],
                price=pd["price"],
                config=config,
            )
            # Подключаемся к сигналу открытия страницы конкретного проекта:
            card.open_project.connect(self.open_project_page)

            cards_layout.addWidget(card)

        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)

        # Предложение создать новый проект
        alter_title = QLabel("Или создайте новый проект")
        alter_title.setObjectName("AlterTitle")
        alter_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(alter_title)

        alter_button = QPushButton("+ Создать проект")
        alter_button.setObjectName("AlterButton")
        alter_button.setFixedWidth(180)
        layout.addWidget(alter_button, alignment=Qt.AlignmentFlag.AlignCenter)

        return page

    def open_project_page(self, project_id):
        """
        Обработчик клика на ссылку "Подробнее"
        Загружает данные проекта и переключает на страницу деталей.
        """
        # Получаем данные из кеша:
        project_data = self.project_manager.get_project(project_id)
        # Проверка на наличие ключа в словаре:
        if project_data:
            self.project_page.load_project(project_data)
            self.stack.setCurrentIndex(1)
        else:
            print(f"Проект №{project_id} не найден!")

    def show_list_page(self):
        """Возврат к списку проектов (обработчик go_back)"""
        # Переключаемся обратно на страницу с индексом 0:
        self.stack.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    nunito_id = QFontDatabase.addApplicationFont("fonts/Nunito.ttf")
    jetbrains_id = QFontDatabase.addApplicationFont(
        "fonts/JetBrainsMono.ttf"
    )

    # Получаем имена шрифтов:
    nunito_family = ""
    jetbrains_family = ""

    if nunito_id != -1:
        nunito_family = QFontDatabase.applicationFontFamilies(nunito_id)[0]
    else:
        print("Ошибка: не удалось загрузить шрифт Nunito!")

    if jetbrains_id != -1:
        jetbrains_family = QFontDatabase.applicationFontFamilies(
            jetbrains_id)[0]
    else:
        print("Ошибка: не удалось загрузить шрифт JetBrainsMono")

    global_styles = """
        QMainWindow { background-color: #18191a; }

        #WelcomeTitle {
            font-size: 24px;
            color: white;
            font-weight: bold;
            margin-top: 10px;
            margin-bottom: 5px;
        }

        #WelcomeDesc {
            font-weight: 600;
            margin-bottom: 10px;
            font-size: 16px;
        }

        #ProjectsScrollArea, #ScrollContent {
            background-color: transparent;
        }

        QFrame#ProjectCard {
            background-color: white;
            border: 1px solid #ced4da;
            border-radius: 8px;
            padding: 10px;
        }

        QFrame#ProjectCard:hover {
            border: 1px solid #0078d7;
            background-color: #f4f9ff;
        }

        #ProjectTitle {
            font-weight: bold;
            font-size: 16px;
            color: #0078d7;
        }

        #ProjectDesc {
            color: black;
            background-color: #d9d9d9;
            border-radius: 5px;
            padding: 4px 10px;
        }

        #ProjectConfig {
            color: #555555;
            font-size: 12px;
            margin-top: 2px;
        }

        #ProjectPrice {
            font-weight: bold;
            color: #2e7d32;
            font-size: 14px;
        }

        #PriceIcon {
            padding-top: 2px;
        }

        #DetailsLink {
            font-weight: 600;
        }

        #AlterTitle {
            color: #e0e0e0;
            font-size: 18px;
            font-weight: 600;
            margin-top: 5px;
            margin-bottom: 5px;
        }

        /* Стили для кнопки "Создать проект" */
        QPushButton#AlterButton {
            background-color: #0078d7;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: bold;
            font-size: 14px;
            margin-bottom: 12px;
        }

        QPushButton#AlterButton:hover {
            background-color: #005a9e;
        }

        QPushButton#AlterButton:pressed {
            background-color: #004578;
        }

        /* Стили для страницы о проекте */
        #ProjectPage {
            background-color: #18191a;
        }

        #ProjectScroll, #ProjectContent {
            background-color: transparent;
        }

        QPushButton#BackButton {
            background-color: transparent;
            color: white;
            border: 1px solid white;
            border-radius: 6px;
            padding: 6px 14px;
            font-weight: bold;
            font-size: 13px;
        }

        QPushButton#BackButton:hover {
            background-color: rgba(128, 236, 255, 0.1);
        }

        #ProjectPageTitle {
            font-size: 20px;
            font-weight: 700;
            color: white;
        }

        QFrame#InfoBlock {
            background-color: white;
            border: 1px solid #3a3b3c;
            border-radius: 10px;
            padding: 15px;
        }

        QFrame#PriceBlock {
            background-color: white;
            border: 3px solid #2e7d32;
            border-radius: 10px;
            padding: 8px 15px;
        }

        #BlockHeader, #PriceBlockHeader {
            font-size: 16px;
            font-weight: bold;
        }

        #BlockHeader {
            color: #0078d7;
        }

        #PriceBlockHeader {
            color: green;
        }

        #BlockText {
            color: black;
            font-size: 14px;
            line-height: 1.5;
        }

        #BigPrice {
            color: green;
            font-size: 22px;
            font-weight: bold;
        }

        #ExportButton {
            background-color: transparent;
            color: white;
            border: 1px solid white;
            padding: 4px 10px;
            font-weight: bold;
            border-radius: 6px;
        }

        #ExportButton:hover {
            background-color: rgba(128, 236, 255, 0.15);
        }

        #ExportButton:pressed {
            background-color: rgba(128, 236, 255, 0.25);
        }

        /* Стили для кнопки редактирования */
        QPushButton#EditButton {
            background-color: transparent;
            border: none;
            border-radius: 15px;
            padding: 4px;
        }

        QPushButton#EditButton:hover {
            background-color: rgba(0, 120, 215, 0.2);
        }

        QPushButton#EditButton:pressed {
            background-color: rgba(0, 120, 215, 0.3);
        }

        /* Стили для диалога редактирования */
        QDialog#EditDialog {
            background-color: #18191a;
        }

        QLabel#EditDialogLabel {
            color: white;
            font-size: 16px;
            font-weight: bold;
        }

        QTextEdit#EditDialogTextEdit {
            background-color: #242526;
            color: white;
            border: 1px solid #3a3b3c;
            border-radius: 8px;
            padding: 10px;
            font-size: 14px;
        }

        QTextEdit#EditDialogTextEdit:focus {
            border: 1px solid #0078d7;
        }

        QPushButton#EditDialogButton {
            background-color: #0078d7;
            color: white;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            font-size: 13px;
        }

        QPushButton#EditDialogButton:hover {
            background-color: #005a9e;
        }

        QPushButton#EditDialogButton:pressed {
            background-color: #004578;
        }
    """

    # Применяем шрифт Nunito глобально:
    if nunito_family:
        global_styles += f"""
            * {{
                font-family: '{nunito_family}';
                font-size: 13px;
            }}
        """

    if jetbrains_family:
        global_styles += f"""
            #BlockText, #BigPrice, #ProjectConfig, #ProjectTitle,
            #DetailsLink, #AlterButton, #ProjectPageTitle, #BlockHeader,
            #PriceBlockHeader {{
                font-family: '{jetbrains_family}';
            }}
        """

    app.setStyleSheet(global_styles)

    window = PcBuilder()
    window.show()
    sys.exit(app.exec())
