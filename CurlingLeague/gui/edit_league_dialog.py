from PyQt6 import uic
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QDialog

from CurlingLeague.gui.edit_team_dialog import EditTeamDialog
from CurlingLeague import league_database
from CurlingLeague.team import Team

Ui_MainWindow,QtBaseWindow = uic.loadUiType('edit_league_dialog.ui')

class EditLeagueDialog(QtBaseWindow, Ui_MainWindow):

    def __init__(self, league, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Edit League')
        self.db = league_database.LeagueDatabase().instance()
        self.league = league
        self.update_ui()
        self.add_team_button.clicked.connect(self.add_team)
        self.delete_team_button.clicked.connect(self.remove_team)
        self.edit_team_button.clicked.connect(self.edit_team)
        self.import_teams_button.clicked.connect(self.import_team)
        self.export_teams_button.clicked.connect(self.export_teams)

    def update_ui(self):
        self.team_list_widget.clear()
        for t in self.league.teams:
            self.team_list_widget.addItem(str(t))

    def get_selected(self):
        selection = self.team_list_widget.selectedItems()
        if len(selection) == 0:
            return -1
        assert len(selection) == 1
        selected_item = selection[0]
        for i, t in enumerate(self.league.teams):
            if selected_item.text() == str(t):
                return i
        return -1

    def add_team(self):
        t = Team(self.db.next_oid(), self.add_team_line_edit.text())
        self.league.add_team(t)
        self.update_ui()
        self.add_team_line_edit.clear()

    def remove_team(self):
        dialog = QMessageBox()
        dialog.setIcon(QMessageBox.Icon.Question)
        dialog.setWindowTitle("Delete Team")
        dialog.setText("Are you sure you want to delete this team?")
        dialog.setStandardButtons(QMessageBox.StandardButton.Yes |
                                  QMessageBox.StandardButton.No)
        result = dialog.exec()
        if result == QMessageBox.StandardButton.Yes:
            del self.league.teams[self.team_list_widget.currentRow()]
            self.update_ui()
        else:
            pass

    def edit_team(self):
        selected = self.get_selected()
        if selected != -1:
            team = self.league.teams[selected]
            dialog = EditTeamDialog(team)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                pass
        self.update_ui()

    def export_teams(self):
        dialog = QFileDialog()
        file_name = dialog.getSaveFileName(self,"Save File Name", "Teams", "CSV Files (*.csv)")[0]
        if file_name:
            self.db.export_league_teams(self.league, file_name)

    def import_team(self):
        dialog = QFileDialog()
        file_name = dialog.getOpenFileName(self,"Open File Name", None, "CSV Files (*.csv)")[0]
        if file_name:
            self.db.import_league_teams(self.league, file_name)
        self.update_ui()

