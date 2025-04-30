import sys

from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QDialog

from CurlingLeague.gui.edit_league_dialog import EditLeagueDialog
from CurlingLeague import league_database
from CurlingLeague.league import League

Ui_MainWindow,QtBaseWindow = uic.loadUiType('league_main_window.ui')

class MainWindow(QtBaseWindow, Ui_MainWindow):

    def __init__(self, parent=None):
       super().__init__(parent)
       self.setupUi(self)
       self.db = league_database.LeagueDatabase().instance()
       self.add_league_button.clicked.connect(self.add_button_clicked)
       self.delete_league_button.clicked.connect(self.delete_league_button_clicked)
       self.edit_league_button.clicked.connect(self.edit_league_button_clicked)
       self.load_button.clicked.connect(self.load_button_clicked)
       self.save_button.clicked.connect(self.save_button_clicked)

    def update_ui(self):
        self.league_list_widget.clear()
        for league in self.db.leagues:
            self.league_list_widget.addItem(str(league))

    def get_selected(self):
        selection = self.league_list_widget.selectedItems()
        if len(selection) == 0:
            return -1
        assert len(selection) == 1
        selected_item = selection[0]
        for i, l in enumerate(self.db.leagues):
            if selected_item.text() == str(l):
                return i
        return -1

    def add_button_clicked(self):
        l = League(self.db.next_oid(), self.add_line_edit.text())
        self.db.add_league(l)
        self.update_ui()
        self.add_line_edit.clear()

    def delete_league_button_clicked(self):
        selected_item = self.get_selected()
        if selected_item == -1:
            pass
        else:
            dialog = QMessageBox()
            dialog.setIcon(QMessageBox.Icon.Question)
            dialog.setWindowTitle("Delete League")
            dialog.setText("Are you sure you want to delete this League?")
            dialog.setStandardButtons(QMessageBox.StandardButton.Yes |
                                      QMessageBox.StandardButton.No)
            result = dialog.exec()
            if result == QMessageBox.StandardButton.Yes:
                del self.db.leagues[selected_item]
                self.update_ui()
            else:
                pass

    def edit_league_button_clicked(self):
        selected = self.get_selected()
        if selected == -1:
            pass
        else:
            league = self.db.leagues[selected]
            dialog = EditLeagueDialog(league)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                pass
        self.update_ui()


    def load_button_clicked(self):
        dialog = QFileDialog()
        file_name = dialog.getOpenFileName(self,"Open File Name", None, "DAT Files (*.dat)")[0]
        if file_name:
            self.db = self.db.load(file_name)
        self.update_ui()


    def save_button_clicked(self):
        dialog = QFileDialog()
        file_name = dialog.getSaveFileName(self,"Save File Name", None, "DAT Files (*.dat)")[0]
        if file_name:
            self.db.save(file_name)
        self.update_ui()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())