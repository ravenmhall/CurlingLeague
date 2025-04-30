import yagmail
class Emailer:
    """
    A class to send emails.
    """
    sender_address = ""
    """Address  of sender"""
    _sole_instance = None
    """The only instance of this class"""

    @classmethod
    def configure(cls, sender_address):
        """"
        Configures the sender address of the emailer.
        """
        cls.sender_address = sender_address

    @classmethod
    def instance(cls):
        """
        Returns the sole instance of the emailer.

        Returns:
            Emailer: The sole instance of the emailer.
        """
        if cls._sole_instance is None:
            cls._sole_instance = cls()
        return cls._sole_instance

    def __init__(self):
        self.recipients = []
        self.subject = ""
        self.message = ""

    def send_plain_email(self, recipients, subject, message):
        """

        Sends a plain email.

        Args:
            recipients(list): A list of emails to send email to.
            subject(str): The subject of the email.
            message(str): The message to send.
            """
        self.recipients = recipients
        self.subject = subject
        self.message = message
        for recipient in recipients:
            yagmail.SMTP(self.sender_address).send(recipient, subject, message)
