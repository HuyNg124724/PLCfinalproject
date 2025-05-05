import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem
from components.lexica import MyLexer
from components.parsers import MyParser
from components.memory import MEMORY

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("components/main.ui", self)
        self.runButton.clicked.connect(self.run_code)

    def run_code(self):
        code = self.codeTextEdit.toPlainText()
        MEMORY.clear()
        lexer = MyLexer()
        parser = MyParser()
        try:
            ast = parser.parse(lexer.tokenize(code))
            for stmt in ast:
                stmt.run()
        except Exception as e:
            self.outputTextEdit.setPlainText(f"Error: {e}")
            return
        self.outputTextEdit.setPlainText(MEMORY.get_output())
        self.astTree.clear()
        for stmt in ast:
            top = QTreeWidgetItem([str(stmt)])
            self.astTree.addTopLevelItem(top)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
