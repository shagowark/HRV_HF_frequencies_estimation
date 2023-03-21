import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 200, 650, 180)
        my_label = QLabel("Оценка HF частот")
        my_label.setFont(QFont('Serif', 24))
        my_label.setGeometry(200, -20, 650, 100)
        self.layout().addWidget(my_label)

        # Создаем кнопки
        self.button_load = QPushButton('Загрузить из файла', self)
        self.button_load.setGeometry(50, 100, 150, 30)
        self.button_load.clicked.connect(self.load_file)

        self.button_rr = QPushButton('Показать RR график', self)
        self.button_rr.setGeometry(250, 100, 150, 30)
        self.button_rr.clicked.connect(self.plot_rr)

        self.button_hf = QPushButton('Оценка HF частот', self)
        self.button_hf.setGeometry(450, 100, 150, 30)
        self.button_hf.clicked.connect(self.plot_hf)

        # Создаем переменные для хранения данных
        self.filename = None
        self.rr_intervals = None

    def load_file(self):
        # Открываем диалоговое окно для выбора файла
        self.filename, _ = QFileDialog.getOpenFileName(self, 'Выберите файл', '', '(*.rr)')

        if self.filename:
            # Считываем данные из файла
            with open(self.filename, 'r') as f:
                f.readline()
                data = f.read()

            # Преобразуем данные в массив RR интервалов
            self.rr_intervals = [int(x) for x in data.split()]

    def plot_rr(self):
        if self.rr_intervals:
            # Строим график
            plt.plot(self.rr_intervals)
            plt.xlabel('Отсчеты (шт)')
            plt.ylabel('RR интервалы (мс)')
            plt.title('График RR интервалов')
            plt.show()

    def plot_hf(self):
        if self.rr_intervals:
            # Вычисляем ДПФ
            fft_rr = np.fft.fft(self.rr_intervals)

            # Вычисляем амплитудный спектр
            amp_rr = np.abs(fft_rr)

            # Вычисляем мощность сигнала
            power_rr = np.square(amp_rr)


            # Вычисляем частотный диапазон
            freq_rr = np.fft.fftfreq(len(self.rr_intervals), d=1)

            # обрабатываем
            power_rr = np.delete(power_rr, 0)
            freq_rr = np.delete(freq_rr, 0)
            amp_rr = np.delete(amp_rr, 0)


            # Находим HF частоты и соответствующие амплитуды/мощности
            hf_freq_range = [0.15, 0.4]
            mask_hf = np.logical_and(freq_rr >= hf_freq_range[0], freq_rr <= hf_freq_range[1])
            freq_rr_hf = freq_rr[mask_hf]
            power_rr_hf = power_rr[mask_hf]
            hf_amp = amp_rr[mask_hf]

            # Строим график спектра
            plt.plot(freq_rr_hf, power_rr_hf)
            plt.xlabel(f'Частота (Гц) \n \n Коэф. HF = {np.sum(power_rr_hf)/np.sum(power_rr)}')
            plt.ylabel('Мощность (мс^2)')
            plt.title('HF частоты')
            plt.tight_layout()
            plt.show()


def run_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run_app()
