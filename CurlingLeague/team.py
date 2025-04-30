from CurlingLeague.league_exceptions import DuplicateOid, DuplicateEmail
from CurlingLeague.identified_object import IdentifiedObject

class Team(IdentifiedObject):
    """
    Creates an object representing a team.
    Inherits from IdentifiedObject.

    Attributes:
        oid(int): Identifies team.
        name(str): The name of the team.
    """
    def __init__(self, oid, name):
        """
        Creates a team object representing a team.
        Args:
            oid(int): Identifies team.
            name(str): The name of the team.
        """
        super().__init__(oid)
        self.name = name
        self._members = []

    @property
    def members(self):
        """
        Returns list containing members of the team.

        Returns:
            list[TeamMembers]: The members of the team.

        """
        return self._members

    def add_member(self, member):
        """
        Adds a member to the team if the member is not already present.

        Args:
            member(TeamMember): The member to add.
        Raises:
            DuplicateOid: If the member is already present.
            DuplicateEmail: If the email is already used by member.
        """
        if member in self.members:
            raise DuplicateOid(member.oid)
        else:
            for m in self.members:
              if m.email.casefold() == member.email.casefold():
               raise DuplicateEmail(member.email)
            self.members.append(member)

    def member_named(self, name):
        """
        Returns the name of the team member with the given name(case sensitive).

        Args:
            name(str): The name of the team member.

        Returns:
            TeamMember: The team member with the given name.
        """
        for member in self.members:
           if member.name == name:
               return member

    def remove_member(self, member):
        """
        Removes a specified member from the team.

        Args:
            member(TeamMember): The member to remove.
        """
        self.members.remove(member)

    def send_email(self, emailer, subject, message):
        """
        Sends an email to all team members if member has an\
        email address via the emailer argument.

        Args:
            emailer(emailer): The emailer to send the email through.
            subject(str): The subject of the email.
            message(str): The message to send.

        """
        recipients = [member.email for member in self.members if member.email is not None]
        emailer.send_plain_email(recipients, subject, message)

    def __str__(self):
        """
        Returns a string representation of the team.

        Returns:
            str: The string representation of the team.

        """
        return f"{self.name}: {len(self.members)} members"