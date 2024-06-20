from PyQt5 import QtWidgets
from PyQt5.QtGui import QPainter, QColor, QPen
import sys

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.setWindowTitle('oxxo.studio')
        self.resize(300, 200)

    # 定義 paintEvent 屬性，注意需要包含 self 和 event 參數
    def paintEvent(self, event):
        qpainter = QPainter()
        qpainter.begin(self)

        qpainter.setPen(QPen(QColor('#ff0000'),5))
        qpainter.drawRect(50, 50, 100, 100)

        qpainter.end()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())