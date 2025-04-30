
from .identified_object import IdentifiedObject

class Competition(IdentifiedObject):
    """
    Creates an object representing a competition.
    Inherits from IdentifiedObject.

    Attributes:
        oid(int): The id of the competition.
        location(str): The location of the competition.
        date_time(datetime): The date and time of the competition.

    """
    def __init__(self, oid, teams, location, datetime = None):
        """
        Creates a competition object representing a competition.
        Args:
            oid(int): The id of the competition.
            teams(list): List of teams associated with the competition.
            location(str): Location of the competition.
            date_time(datetime): The date and time of the competition.
        """
        super().__init__(oid)
        self._teams_competing = teams
        self.location = location
        self.date_time = datetime

    @property
    def teams_competing(self):
        """
        List of teams associated with the competition.
        Returns:
            list: List of teams associated with the competition.

        """
        return self._teams_competing

    def send_email(self, emailer, subject, message):
        """
        Sends an email to the team members competing in competition\
        via emailer object.
        Args:
            emailer(emailer): Emailer object to send the email.
            subject(str): Subject of the email.
            message(str): Message to send.

        """
        emails = [member.email for member in self.teams_competing[0].members]
        for member in self.teams_competing[1].members:
            emails.append(member.email)
        temp = []
        [temp.append(email) for email in emails if email not in temp]
        emailer.send_plain_email(temp, subject, message)

    def __str__(self):
        """
        Returns a string representation of the competition.

        Returns:
            str: String representation of the competition.

        """
        if self.date_time is None:
            return f"Competition at {self.location} with {len(self.teams_competing)} teams."
        else:
            return f"Competition at {self.location} on {self.date_time} with {len(self.teams_competing)} teams."