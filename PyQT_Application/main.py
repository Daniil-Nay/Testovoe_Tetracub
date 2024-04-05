import shutil
from typing import Set, List

from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QLineEdit, QMessageBox
import sys
import os
from datetime import datetime
import random


class App(QMainWindow):
    def __init__(self):
        """
        Инициализация главного окна
        """
        super().__init__()
        self.settings_window = None
        self.setFixedSize(600, 600)
        uic.loadUi('main_window.ui', self)
        self.actionchoose_path.triggered.connect(self.open_settings_window)
        self.StartButton.clicked.connect(self.StartProccess)

        self.path: str = r""
        self.processed_files: Set[str] = set()

    def StartProccess(self) -> None:
        """
        При нажатии кнопки start проверяется, был ли указан путь
        :return: None
        """
        if not self.path:
            QMessageBox.information(self, "Ошибка", "Не был введен путь!")
        else:
            self.PathReader()

    def open_settings_window(self) -> None:
        """
        Инициализация окна с настройками (указанием пути и сохранением)
        Кнопка сохранить и кнопка отмена
        :return: None
        """
        self.settings_window = QDialog()
        self.settings_window.setFixedSize(550,400)
        uic.loadUi('Settings.ui', self.settings_window)

        input_path_widget: QLineEdit = self.settings_window.findChild(QLineEdit, 'InputPath')
        if input_path_widget and self.path:
            input_path_widget.setText(self.path)

        self.settings_window.Save.clicked.connect(lambda: self.save_path(self.settings_window))
        self.settings_window.Cancel.clicked.connect(self.settings_window.reject)
        self.settings_window.exec_()

    def save_path(self, settings_window) -> None:
        """
        Функция для сохранения пути к папке с файлами(проверка на правильность ввода)
        :param settings_window:
        :return:
        """
        input_path_widget: QLineEdit = settings_window.findChild(QLineEdit, 'InputPath')

        path: str = input_path_widget.text()
        if not path:
            QMessageBox.warning(self, "Ошибка", "Не указан путь")
            return
        elif not os.path.exists(path):
            QMessageBox.warning(self, "Ошибка", "Указанный путь не существует")
            return
        elif not os.path.isdir(path):
            QMessageBox.warning(self, "Ошибка", "Указанный путь не является директорией к папке")
            return
        else:
            self.path = path
            QMessageBox.information(self, "Успех", "Операция была успешно выполнена!")
            settings_window.accept()

    def PathReader(self) -> None:
        """
        Чтение пути, по которому лежит папка с файлами
        selected_v - тип v (v1 или v2)
        total_files - подсчет количества файлов для отображения загрузочной шкалы.
        Далее происходит чтение файлов и создание новых, в которых записывается
        случайное число и метка исходя из названия.
        :return:
        """
        selected_v: str = self.comboBox.currentText()
        files: List[str] = [f for f in os.listdir(self.path) if f.endswith(selected_v) and f not in self.processed_files]

        total_files: int = len(files)
        self.progressBar.setMaximum(total_files)
        self.progressBar.setValue(0)

        if total_files > 0:
            i = 0
            for i, filename in enumerate(files, start=1):
                current_time = datetime.now()
                src_file: str = os.path.join(self.path, filename)
                # очень длинное название у нового файла...
                dst_file: str = os.path.join(self.path,
                                        f"{filename}_new_{current_time.date().strftime('%d-%m-%Y')}_{current_time.time().strftime('%H.%M')}.txt")
                shutil.copy(src_file, dst_file)
                with open(dst_file, 'a', encoding='utf-8') as nf:
                    nf.write(f"{random.randrange(100)} {selected_v}")
                self.processed_files.add(filename)
                self.progressBar.setValue(i)
                QCoreApplication.processEvents()
            if i == total_files:
                QMessageBox.information(self, "Завершено", "Все файлы были обработаны!")
        else:
            QMessageBox.information(self, "Завершено", "Нет файлов для обработки")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
