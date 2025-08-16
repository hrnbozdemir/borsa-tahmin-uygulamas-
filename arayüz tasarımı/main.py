from PyQt5.QtWidgets import QApplication, QMainWindow
from arayuz import Ui_MainWindow

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Butona tıklayınca label değişsin
        self.ui.pushButton.clicked.connect(self.labeli_guncelle)

    def labeli_guncelle(self):
        self.ui.label.setText("Veriler güncellendi!")

app = QApplication([])
pencere = MyApp()
pencere.show()
app.exec_()
