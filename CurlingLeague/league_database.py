import csv
import os
import pickle
import shutil

from CurlingLeague.league import League
from CurlingLeague.league_exceptions import DuplicateOid
from CurlingLeague.team import Team
from CurlingLeague.team_member import TeamMember

class LeagueDatabase:
    """A singleton creating a database for leagues."""

    _sole_instance= None
    """The only instance of this class."""

    @classmethod
    def instance(cls):
        """
        Returns the sole instance of the league database, creating one if it doesn't exist.'
        Returns:
           _sole_instance: The sole instance of the league database.
        """
        if cls._sole_instance is None:
            cls._sole_instance = cls()
        return cls._sole_instance

    @classmethod
    def load(cls, file_name):
        """
        Loads a LeagueDatabase from the specified file and stores it in _sole_instance.
        If backup file available will load if original file not found.

        Returns:
            cls: The league database instance.
        """
        try:
            with open(file_name, mode='rb') as f:
               cls._sole_instance = pickle.load(f)
        except FileNotFoundError:
            try:
                with open(f"{file_name}.backup", mode='rb') as f:
                   cls._sole_instance = pickle.load(f)
            except FileNotFoundError:
                print(f"File {file_name} not found.")
        return cls._sole_instance

    def __init__(self):
        """
        Initializes the league database.

        Attributes:
            leagues: a list of League objects
            _last_oid: the last id number that was supplied

        """
        self.leagues = []
        self._last_oid = 0

    def add_league(self, league):
        """
        Add the specified league to the leagues list
        Args:
            league(League): A league instance.

        """
        self.leagues.append(league)

    def remove_league(self, league):
        """
        Remove the specified league from the leagues list.
        Does nothing if league is not in the list.
        Args:
            league(League): A league instance.

        Returns:

        """
        if league in self.leagues:
            self.leagues.remove(league)
        else:
            pass

    def league_named(self, name):
        """
        Returns the league with the given name or None of no such league exists.
        Args:
            name(str): The name of the league.
        Returns:
            league: The league with the given name.
        """

        for league in self.leagues:
           if league.name == name:
               return league
           else:
               pass

    def next_oid(self):
        """
        Increments _last_oid and returns it's new value.
        Returns:
            int: new _last_oid value
        """
        self._last_oid += 1
        return self._last_oid


    def save(self, file_name):
        """
        Saves the league to the specified file.
        Args:
            file_name(str): The name of the file.
        """
        with open(file_name, mode='wb') as f:
            if os.path.isfile(file_name):
                backup_file = file_name +".backup"
                with open(backup_file, mode='wb') as b:
                    shutil.copy2(file_name, backup_file)
            pickle.dump(self, f)

    def import_league_teams(self, league, file_name):
        """
        Load the teams and team members in a league from a CSV formatted file.
        Args:
            league(League): A league instance.
            file_name(str): The name of the file.
        """
        l = league
        try:
            with open(file_name, mode='rt', encoding='utf-8') as f:
                csv_reader = csv.reader(f, delimiter=',')
                next(csv_reader)
                for row in csv_reader:
                    team_name = row[0]
                    member_name = row[1]
                    member_email = row[2]
                    team_member = TeamMember(self.next_oid(), member_name, member_email)
                    if l.team_named(team_name):
                        t = l.team_named(team_name)
                        try:
                            t.add_member(team_member)
                        except DuplicateOid:
                            pass
                    else:
                        t = Team(self.next_oid(), team_name)
                        l.add_team(t)
                        try:
                            t.add_member(team_member)
                        except DuplicateOid:
                            pass
                if l not in self.leagues:
                    self.add_league(l)
        except FileNotFoundError:
            print(f"File {file_name} not found.")

    def export_league_teams(self, league, file_name):
        """
        Write the specified league to a CSV formatted file.
        Args:
            league(League): A league instance.
            file_name(str): The name of the file.
            """

        l = league
        try:
            with open(file_name, mode='wt', newline='', encoding='utf-8') as f:
                csv_writer = csv.writer(f, delimiter=',')
                csv_writer.writerow(['Team name', 'Member name', 'Member email'])
                for teams in l.teams:
                    team_name = teams.name
                    for members in teams.members:
                        member_name = members.name
                        member_email = members.email
                        csv_writer.writerow([team_name, member_name, member_email])
        except FileNotFoundError:
            print(f"File {file_name} not found.")



