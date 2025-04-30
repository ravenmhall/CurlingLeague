from CurlingLeague.league_exceptions import DuplicateOid
from CurlingLeague.identified_object import IdentifiedObject


class League(IdentifiedObject):
    """
    An object that represents a League.
    Inherits from IdentifiedObject.

    Attributes:
        oid(int): The identifier of the League.
        name(str): The name of the League.
    """
    def __init__(self, oid, name):
        """
        Creates an object that represents a League.
        Args:
            oid(int): Identifier of the League.
            name(str): The name of the League.
        """
        super().__init__(oid)
        self.name = name
        self._teams = []
        self._competitions = []

    @property
    def teams(self):
        """
        Returns the list of teams that are in the League.
        Returns:
            list: The list of teams in the League.
        """
        return self._teams

    @property
    def competitions(self):
        """
        Returns the list of competitions that are in the League.
        Returns:
            list: The list of competitions in the League.
        """
        return self._competitions

    def add_team(self, team):
        """
        Adds a team to the League if the team is not already present in League.
        Args:
            team(Team): The team to add to the League.
        Raises:
            DuplicateOid: If the team is already present in the League.
        """
        if team not in self.teams:
            self.teams.append(team)
        else:
            raise DuplicateOid(team.oid)

    def remove_team(self, team):
        """
        Removes a team from the League if the team is present in the League.
        Args:
            team(Team): The team to remove from the League.
        Raises:
            ValueError: If the team is part of a competition.
        """
        for comp in self.competitions:
            if team in comp.teams_competing:
                raise ValueError
        if team in self.teams:
             self.teams.remove(team)
        else:
            return

    def team_named(self, team_name):
        """
        Returns the teams named if the team is present in the League.
        Args:
            team_name(str): The team name to look for.

        Returns:
            Team: The team that is named if the team is present in the League.
        """
        for team in self.teams:
            if team.name == team_name:
                return team

    def add_competition(self, competition):
        """
        Adds competition to the League.
        Args:
            competition(Competition): The competition to add to the League.
        Raises:
            ValueError: If the one of the competing teams is not present in the League.
        """
        for team in competition.teams_competing:
            if team not in self.teams:
                raise ValueError()
        self.competitions.append(competition)

    def teams_for_member(self, member):
        """
        Returns a list of teams if the team member is present on the team.
        Args:
            member(TeamMember): The team member to collect teams for.

        Returns:
            list: The list of teams the team member belongs to.

        """
        member_teams = []
        for team in self.teams:
            for memb in team.members:
                if memb == member:
                    member_teams.append(team)

        return member_teams

    def competitions_for_team(self, team):
        """
        Returns a list of competitions team is competing in.
        Args:
            team(Team): The team to determine competitions for.

        Returns:
            list: The list of competitions the team is competing in.
        """
        team_competitions = []
        for competition in self.competitions:
            for tm in competition.teams_competing:
                if tm == team:
                    team_competitions.append(competition)

        return team_competitions

    def competitions_for_member(self, member):
        """
        Returns a list of competitions team member is competing in.
        Args:
            member(TeamMember): The team to determine competitions for.

        Returns:
            list: The list of competitions the team member is competing in.
        """
        member_competitions = []
        for competition in self.competitions:
            for team in competition.teams_competing:
                for memb in team.members:
                    if memb == member and competition not in member_competitions:
                        member_competitions.append(competition)

        return member_competitions

    def __str__(self):
        """
        Returns a string representation of the League.
        Returns:
            str: The string representation of the League.
        """
        return f"{self.name}: {len(self.teams)} teams, {len(self.competitions)} competitions"
