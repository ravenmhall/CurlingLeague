import unittest

from CurlingLeague.league_exceptions import DuplicateOid, DuplicateEmail
from CurlingLeague.team import Team
from CurlingLeague.team_member import TeamMember


class TestTeam(unittest.TestCase):

    def test_str(self):
        t = Team(1, "Team 1")
        tm1 = TeamMember(1, "Betty", "betty@generic.org")
        tm2 = TeamMember(2, "Veronica", "veronica@generic.org")
        t.add_member(tm1)
        self.assertEqual("Team 1: 1 members", t.__str__())
        t.add_member(tm2)
        self.assertEqual("Team 1: 2 members", t.__str__())
        t.remove_member(tm1)
        self.assertEqual("Team 1: 1 members", t.__str__())
        t.remove_member(tm2)
        self.assertEqual("Team 1: 0 members", t.__str__())

    def test_add_member(self):
        t = Team(1, "Team 1")
        tm1 = TeamMember(1, "Betty", "betty@generic.org")
        tm2 = TeamMember(2, "Veronica", "veronica@generic.org")

        tm3 = TeamMember(3, "JugHead", "veronica@generic.org")
        tm4 = TeamMember(4, "Archie", "BETTY@generic.ORG")
        t.add_member(tm1)
        t.add_member(tm2)
        with self.assertRaises(DuplicateOid):
            t.add_member(tm1)
        with self.assertRaises(DuplicateOid):
            t.add_member(tm2)
        with self.assertRaises(DuplicateEmail):
            t.add_member(tm3)
        with self.assertRaises(DuplicateEmail):
            t.add_member(tm4)

    if __name__ == '__main__':
        unittest.main()