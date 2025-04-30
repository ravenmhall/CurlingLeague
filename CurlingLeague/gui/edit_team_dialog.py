from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox

from CurlingLeague import league_database
from CurlingLeague.league_exceptions import DuplicateEmail
from CurlingLeague.team_member import TeamMember

Ui_MainWindow, QtBaseWindow = uic.loadUiType('edit_team_dialog.ui')


class EditTeamDialog(QtBaseWindow, Ui_MainWindow):

    def __init__(self, team, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Edit Team')
        self.db = league_database.LeagueDatabase().instance()
        self.team = team
        self.update_ui()
        self.add_update_button.clicked.connect(self.add_update_member)
        self.delete_member_button.clicked.connect(self.delete_member)
        self.members_list_widget.itemSelectionChanged.connect(self.update_line_edits)

    def update_ui(self):
        self.name_line_edit.clear()
        self.email_line_edit.clear()
        self.members_list_widget.clear()
        self.error_label.setText("")
        for member in self.team.members:
            self.members_list_widget.addItem(str(member))

    def get_selected(self):
        selection = self.members_list_widget.selectedItems()
        if len(selection) == 0:
            return -1
        assert len(selection) == 1
        selected_item = selection[0]
        for i, m in enumerate(self.team.members):
            if selected_item.text() == str(m):
                return i
        return -1

    def update_line_edits(self):
        selected = self.get_selected()
        if selected == -1:
            pass
        else:
            member = self.team.members[selected]
            self.name_line_edit.setText(member.name)
            self.email_line_edit.setText(member.email)

    def add_update_member(self):
        selected = self.get_selected()

        if self.name_line_edit.text() == "":
            self.error_label.setText("Please enter a name.")
        elif self.email_line_edit.text() == "":
            self.error_label.setText("Please enter an email.")
        elif selected == -1:
            member = TeamMember(self.db.next_oid(), self.name_line_edit.text(),
                                self.email_line_edit.text())
            try:
                self.team.add_member(member)
            except DuplicateEmail:
                self.error_label.setText("Email address already exists.")
                return
            self.update_ui()
        else:
            member = self.team.members[selected]
            for m in self.team.members:
                if m is not member and self.email_line_edit.text() == m.email:
                    self.error_label.setText("Email address already exists.")
                    return
            member.name = self.name_line_edit.text()
            member.email = self.email_line_edit.text()
            self.update_ui()

    def delete_member(self):
        selected = self.get_selected()
        if selected == -1:
            pass
        else:
            dialog = QMessageBox()
            dialog.setIcon(QMessageBox.Icon.Question)
            dialog.setWindowTitle("Delete Member")
            dialog.setText("Are you sure you want to delete this Member?")
            dialog.setStandardButtons(QMessageBox.StandardButton.Yes |
                                      QMessageBox.StandardButton.No)
            result = dialog.exec()
            if result == QMessageBox.StandardButton.Yes:
                member = self.team.members[selected]
                self.team.remove_member(member)
                self.update_ui()
            else:
                pass

