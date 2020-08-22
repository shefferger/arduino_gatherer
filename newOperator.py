import glob
import serial
import time
from threading import Timer

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


class cnnt():
    def __init__(self):
        self.refreshClicked()

    def connect(self, ports):                                       # вызов от searchForPort
        for i in ports:                                             # для попытки подключения
            try:                                                    # пробуем каждый порт
                print("Trying ", i, "...")                          # реализуем экземпляр порта
                self.realport = serial.Serial(port=i, baudrate=self.speed, timeout=3)
                time.sleep(2)                                       # даем 2 секунды на соединение
                if self.realport:                                   # если порт готов, то отправляем послание
                    self.realport.write(b'search')                  # b - означает байтовый код
                raw_msg = self.realport.readline()                  # считываем ответ из порта
                if (raw_msg == b'imArduino'):                       # если ответ - imArduino - значит мы попали
                    print("Arduino found")
                    if self.realport:
                        self.realport.write(self.passw)
                    print('1')
                    raw_msg = self.realport.readline()
                    print('2')
                    print(raw_msg)
                    if (raw_msg == b'okok'):                          # Если ардуино сказала ОК - значит
                        self.connectedState = True                                          # подключились
                        print("connected at ", i)
                        self.realport.timeout = 0
                        return True                                 # возвращаем хорошие новости
                else:
                    print("Not responding")
                    self.realport.close()
            except Exception as e:
                print(e)
                pass
        return False

    def searchForPort(self):                                        # ищем порт, вызов из функции
        if sys.platform.startswith('win'):                          # refreshClicked
            ports = ['COM%s' % (i + 1) for i in range(256)]         # для каждой платформы свой способ
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
        result = []
        for port in ports:                                          # пробуем порты на exception
            try:                                                    # если нет эксепшена - запоминаем
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        if result:                                                 # если порты имеются - продолжаем
            print(result)                                          # запускаем метод подключения по handshake
            if self.connect(result):                               # если успех - запуск чтения буфера serial
                self.rt = RepeatedTimer(0.175, self.changeVals, self)                      # каждые 0.175 сек

    def refreshClicked(self):                           # триггер нажатия кнопки connec
        self.speed = 115200                         # скорость соединения
        self.connectedState = False
        self.passw = b'E209229'                     # наша секретная фраза
        self.searchForPort()                        # запускаем функцию поиска порта


if __name__ == "__main__":
    import sys
    app = cnnt()


