import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QTabWidget, QMessageBox
from PyQt5.Qsci import QsciScintilla, QsciLexerPython, QsciScintillaBase

class Editor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Code Editor")

        self.centralTabs = QTabWidget()
        self.centralTabs.setTabsClosable(True)
        self.centralTabs.tabCloseRequested.connect(self.closeTab)
        self.centralTabs.tabBarDoubleClicked.connect(self.addNewTab)
        self.setCentralWidget(self.centralTabs)

        self.initMenuBar()
        self.initEditor()

        self.show()

    def initMenuBar(self):
        openFile = QAction('Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.triggered.connect(self.openFile)

        saveFile = QAction('Save', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.triggered.connect(self.saveFile)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)

    def initEditor(self):
        self.addNewTab()

    def addNewTab(self):
        newTab = QsciScintilla()
        lexer = QsciLexerPython()

        newTab.setLexer(lexer)
        newTab.setMarginWidth(1, "000")
        newTab.setMarginLineNumbers(1, True)
        newTab.setMarginType(1, QsciScintilla.NumberMargin)
        newTab.setMarginWidth(1, "50")

        newTab.SendScintilla(newTab.SCI_SETCARETSTYLE, QsciScintillaBase.CARETSTYLE_LINE)
        newTab.SendScintilla(newTab.SCI_SETCARETWIDTH, 2)
        newTab.SendScintilla(newTab.SCI_SETCARETFORE, 0x00FF00)

        self.centralTabs.addTab(newTab, "Untitled")
        self.centralTabs.setCurrentWidget(newTab)

    def openFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            with open(fileName, 'r') as file:
                content = file.read()
                self.addNewTab()
                currentTab = self.centralTabs.currentWidget()
                currentTab.setText(content)
                self.centralTabs.setTabText(self.centralTabs.currentIndex(), fileName)

    def saveFile(self):
        currentTab = self.centralTabs.currentWidget()
        if not currentTab:
            return

        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            if not fileName.endswith('.py'):
                fileName += '.py'
            content = currentTab.text()
            try:
                with open(fileName, 'w') as file:
                    file.write(content)
                    self.centralTabs.setTabText(self.centralTabs.currentIndex(), fileName)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file: {e}")

    def closeTab(self, index):
        currentTab = self.centralTabs.widget(index)
        if currentTab:
            if currentTab.isModified():
                res = QMessageBox.question(self, "Save Changes", "Save changes before closing?",
                                           QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
                if res == QMessageBox.Save:
                    self.saveFile()
                elif res == QMessageBox.Cancel:
                    return

            self.centralTabs.removeTab(index)
            currentTab.deleteLater()

def main():
    app = QApplication(sys.argv)
    editor = Editor()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
