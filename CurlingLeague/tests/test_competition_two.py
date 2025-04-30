import unittest
from datetime import datetime

from CurlingLeague.competition import Competition
from CurlingLeague.team import Team
from CurlingLeague.team_member import TeamMember
from CurlingLeague.tests.fake_emailer import FakeEmailer


class TestCompetition(unittest.TestCase):

    def test_str(self):
        dt = datetime.today()
        # create team
        t1 = Team(1, "Gals")
        t2 = Team(2, "Guys")
        # create competition
        c1 = Competition(1, [t1, t2], "Here", None)
        c2 = Competition(2, [t1, t2], "There", dt)
        # test str
        self.assertEqual("Competition at Here with 2 teams.", c1.__str__())
        self.assertEqual(f"Competition at There on {dt} with 2 teams.", c2.__str__())

    def test_send_email(self):
        #create members
        m1 = TeamMember(1, "Betty", "betty@generic.org")
        m2 = TeamMember(2, "Veronica", "veronica@generic.org")
        m3 = TeamMember(3, "Archi", "archie@generic.org")
        m4 = TeamMember(4, "Jughead", "jughead@generic.org")
        #create team
        t1 = Team(1, "Gals")
        t2 = Team(2, "Guys")
        #add memembers to team
        t1.add_member(m1)
        t2.add_member(m3)
        #create competition
        c1 = Competition(1, [t1, t2], "Here", None)
        fe = FakeEmailer()
        #test send_email
        c1.send_email(fe, "Meeting", "Meet here.")
        self.assertEqual([m1.email, m3.email], fe.recipients)
        self.assertEqual("Meeting", fe.subject)
        self.assertEqual("Meet here.", fe.message)
        #add additional team member and test send_email
        t1.add_member(m2)
        c1.send_email(fe, "Meeting", "Meet here.")
        self.assertEqual([m1.email, m2.email, m3.email], fe.recipients)
        self.assertEqual("Meeting", fe.subject)
        self.assertEqual("Meet here.", fe.message)
        #test send_email with duplicate team members
        t2.add_member(m4)
        t1.add_member(m4)
        c1.send_email(fe, "Meeting", "Meet here.")
        self.assertEqual([m1.email, m2.email, m4.email, m3.email], fe.recipients)
        self.assertEqual("Meeting", fe.subject)
        self.assertEqual("Meet here.", fe.message)





