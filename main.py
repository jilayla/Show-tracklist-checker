import sys
from PySide6.QtWidgets import QApplication
from rockwidget import RockWidget

app = QApplication(sys.argv)

window = RockWidget()
window.show()

app.exec() 