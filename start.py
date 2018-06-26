import sys, time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


# Создаем индикаторы для Splash Screen анимации
splash_i = 0  # Индикатор текущего кадра SplashScreen
splash_stop = 0  # Индикатор остановки SplashScreen
max_i = 90  # Макс. кадр SplashScreen


# Обновление анимации SplashScreen
def updateSplashScreen():
    global splash_i, splash_stop

    # если текущий кадр равен максимальному то тормозим таймер анимации
    if splash_i == 583:
        splash_i = 0
        splash_stop = 1
    else: # иначе обновляем кадр на следующий
        if splash_i < max_i:
            splash_i = splash_i + 1
    pixmap = QPixmap('data/splash/splash_' + str(splash_i) + '.png')
    splashScreen.setPixmap(pixmap)


# Поток для определения завершения SplashScreen
class SplashThread(QThread):
    mysignal = pyqtSignal(int) # создаем сигнал, который будет информировать об остановке таймера

    def __init__(self, parent=None):
        QThread.__init__(self, parent)

    def run(self):
        global splash_i, splash_stop, max_i # подключаем индикаторы

        # Имитируем процессы
        start_time = time.time()  # вычисляем начало процесса
        time.sleep(3)  # 1 процесс (длительность)
        t = round(time.time() - start_time)  # вычисляем конец процесса и время его выполнения
        if t < 3:  # если процесс занял меньше времени чем у нас заготовлено для него анимации
            max_i = 90  # стопаем кадр на максимально для него отведенном
        elif t >= 3:  # если процесс занял больше времени или столько же сколько длится его анимация
            max_i = max_i + 90  # расширяем кадры сплеш скрина

        print('splash intro done')

        start_time = time.time()
        time.sleep(6)  # 2 процесс
        t = round(time.time() - start_time)
        if t < 3:
            max_i = 180
        elif t >= 3:
            max_i = max_i + 90

        print('loading widgets done')

        start_time = time.time()
        time.sleep(2)  # 3 процесс
        t = round(time.time() - start_time)
        if t < 3:
            max_i = 270
        elif t >= 3:
            max_i = max_i + 90

        print('loading data done')

        start_time = time.time()
        time.sleep(4)  # 4 процесс
        t = round(time.time() - start_time)
        if t < 3:
            max_i = 360
        elif t >= 3:
            max_i = max_i + 90

        print('loading settings done')

        start_time = time.time()
        time.sleep(1)  # 5 процесс
        t = round(time.time() - start_time)
        if t < 3:
            max_i = 480
        elif t >= 3:
            max_i = max_i + 103

        print('loading ram done')

        time.sleep(3)  # 6 процесс
        max_i = 583

        print('loading by cyberta done')

        # Ожидаем завершения всей анимации
        while splash_stop == 0:
            app.processEvents()
        if splash_stop == 1:
            self.mysignal.emit(1)  # отправляем сигнал из потока о том, что надо остановить SplashScreen


# Функция остановки таймера и закрытия SplashScreen окна
def stopTimer(signal):
    if signal == 1:
        timer.stop()  # останавливаем таймер
        Form.show()  # показываем форму
        splashScreen.finish(Form)  # закрываем SplashScreen
    else:
        pass


# главная форма проекта
class Form(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(420, 420)
        self.setObjectName('Form')
        self.setWindowTitle('Splash Screen by Cyberta')

        self.bg = QLabel(self)
        self.bg.setAlignment(Qt.AlignCenter)
        self.bg.setFixedSize(420, 420)
        self.bg.move(0, 0)
        pixmap = QPixmap('data/cyberta.png')
        self.bg.setPixmap(pixmap)


if __name__ == '__main__':
    # Создаем приложение
    app = QApplication(sys.argv)

    # Поток для SplashScreen
    SplashThread = SplashThread()

    # Создаем splashScreen
    splashScreen = QSplashScreen()
    splashPixmap = QPixmap('data/splash/splash_0.png')
    splashScreen.setPixmap(splashPixmap)
    splashScreen.show()

    # Создаем форму приложения
    Form = Form()

    # Создаем таймер для splashScreen
    timer = QTimer()
    timer.setInterval(33.33)
    timer.setSingleShot(False)
    timer.timeout.connect(updateSplashScreen)
    timer.start()

    # Коннектимся к потоку
    SplashThread.mysignal.connect(stopTimer)
    # Запускаем поток
    SplashThread.start()

    sys.exit(app.exec_())