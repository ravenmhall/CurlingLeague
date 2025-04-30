from CurlingLeague.identified_object import IdentifiedObject

class TeamMember(IdentifiedObject):
    """
    Information about individual team members.
    Inherits from IdentifiedObject.

    Attributes:
        oid(int): Identifies the team member.
        name(str): The name of the team member.
        email(str): The email address of the team member.

    """

    def __init__(self, oid, name, email):
        """
        Initializes new instance of TeamMember.
        Calls parent class' __init__ method initializing oid.
        Sets name and email.

        Args:
            oid(int): Identifier of team member.
            name(str): Name of the team member.
            email(str): Email of the team member.
        """
        super().__init__(oid)
        self.name = name
        self.email = email

    def send_email(self, emailer, subject, message):
        """
        Sends email via emailer.

        Args:
            emailer(object): Email object.
            subject(str): Subject of the email.
            message(str): Message of the email.
        """
        emailer.send_plain_email([self.email], subject, message)

    def __str__(self):
        """
        Returns string representation of team member.

        Returns:
            str: String representation of team member.

        """
        return f"{self.name}<{self.email}>"