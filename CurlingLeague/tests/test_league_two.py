import unittest

from CurlingLeague.competition import Competition
from CurlingLeague.league import League
from CurlingLeague.league_exceptions import DuplicateOid
from CurlingLeague.team import Team
from CurlingLeague.team_member import TeamMember


class TestLeagueAgain(unittest.TestCase):
    def test_rm_team(self):
        league = League(1, "league 1")
        t1 = Team(1, "Team 1")
        t2 = Team(2, "Team 2")
        t3 = Team(3, "Team 3")
        league.add_team(t1)
        league.add_team(t2)
        league.add_team(t3)
        self.assertTrue(t1 in league.teams)
        self.assertTrue(t2 in league.teams)
        self.assertTrue(t3 in league.teams)
        league.remove_team(t1)
        self.assertFalse(t1 in league.teams)
        self.assertTrue(t2 in league.teams)
        self.assertTrue(t3 in league.teams)
        league.remove_team(t2)
        self.assertFalse(t2 in league.teams)
        self.assertTrue(t3 in league.teams)
        league.remove_team(t3)
        self.assertFalse(t3 in league.teams)
        league.add_team(t1)
        league.add_team(t2)
        c1 = Competition(1, [t1, t2], "Here", None)
        league.add_competition(c1)
        with self.assertRaises(ValueError):
            league.remove_team(t1)
        with self.assertRaises(ValueError):
            league.remove_team(t2)

    def test_competitions_for_teams(self):
        league = League(1, "league 1")
        t1 = Team(1, "Team 1")
        t2 = Team(2, "Team 2")
        t3 = Team(3, "Team 3")
        c1 = Competition(1, [t1, t2], "Here", None)
        c2 = Competition(2, [t1, t3], "Here", None)
        c3 = Competition(3, [t2, t3], "Here", None)
        league.add_team(t1)
        league.add_team(t2)
        league.add_team(t3)
        league.add_competition(c1)
        league.add_competition(c2)
        league.add_competition(c3)

        self.assertTrue(league.competitions_for_team(t1) == [c1, c2])
        self.assertTrue(league.competitions_for_team(t2) == [c1, c3])
        self.assertTrue(league.competitions_for_team(t3) == [c2, c3])
        self.assertFalse(league.competitions_for_team(t1) == [])
        self.assertFalse(league.competitions_for_team(t2) == [])
        self.assertFalse(league.competitions_for_team(t3) == [])
        self.assertFalse(league.competitions_for_team(t1) == [c1, c3])
        self.assertFalse(league.competitions_for_team(t2) == [c2, c3])
        self.assertFalse(league.competitions_for_team(t3) == [c1, c3])

    def test_competitions_for_members(self):
        c1, c2, c3, league, m1, m2, m3, m4, t1, t2, t3= self.build_league()

        self.assertTrue(league.competitions_for_member(m1) == [c1, c2])
        self.assertTrue(league.competitions_for_member(m2) == [c1, c2])
        self.assertTrue(league.competitions_for_member(m3) == [c1, c3])
        self.assertTrue(league.competitions_for_member(m4) == [c1, c2, c3])
        self.assertFalse(league.competitions_for_member(m1) == [])
        self.assertFalse(league.competitions_for_member(m2) == [])
        self.assertFalse(league.competitions_for_member(m3) == [])
        self.assertFalse(league.competitions_for_member(m4) == [])
        self.assertFalse(league.competitions_for_member(m1) == [c1, c3])
        self.assertFalse(league.competitions_for_member(m2) == [c2, c3])
        self.assertFalse(league.competitions_for_member(m3) == [c2, c3])

    def test_teams_for_members(self):
        c1, c2, c3, league, m1, m2, m3, m4, t1, t2, t3 = self.build_league()
        self.assertTrue(league.teams_for_member(m1) == [t1])
        self.assertTrue(league.teams_for_member(m2) == [t1])
        self.assertTrue(league.teams_for_member(m3) == [t2])
        self.assertTrue(league.teams_for_member(m4) == [t1, t3])
        self.assertFalse(league.teams_for_member(m1) == [])
        self.assertFalse(league.teams_for_member(m2) == [])
        self.assertFalse(league.teams_for_member(m3) == [])
        self.assertFalse(league.teams_for_member(m4) == [])
        self.assertFalse(league.teams_for_member(m1) == [t1, t2, t3])
        self.assertFalse(league.teams_for_member(m2) == [t2, t3])
        self.assertFalse(league.teams_for_member(m3) == [t3])
        self.assertFalse(league.teams_for_member(m4) == [t1, t2, t3])

    def test_str(self):
        c1, c2, c3, league, m1, m2, m3, m4, t1, t2, t3 = self.build_league()
        self.assertEqual(str(league), "League 1: 3 teams, 3 competitions")
        t4 = Team(4, "Team 4")
        league.add_team(t4)
        self.assertEqual(str(league), "League 1: 4 teams, 3 competitions")
        league_two = League(2, "Another League")
        self.assertEqual(str(league_two), "Another League: 0 teams, 0 competitions")

    def test_add_competition(self):
        c1, c2, c3, league, m1, m2, m3, m4, t1, t2, t3 = self.build_league()
        t4 = Team(4, "Team 4")
        c4 = Competition(4, [t3, t4], "Here", None)
        with self.assertRaises(ValueError):
            league.add_competition(c4)
        t5 = Team(5, "Team 5")
        c5 = Competition(5, [t5, t4], "Here", None)
        with self.assertRaises(ValueError):
            league.add_competition(c5)

    def test_add_team(self):
        l = League(1, "A League")
        t1 = Team(1, "Team 1")
        t2 = Team(2, "Team 2")
        t3 = Team(1, "Team 3")
        l.add_team(t1)
        l.add_team(t2)
        with self.assertRaises(DuplicateOid):
            l.add_team(t1)
        with self.assertRaises(DuplicateOid):
            l.add_team(t3)


    def build_league(self):
        league = League(1, "League 1")
        m1 = TeamMember(1, "Betty", "betty@generic.org")
        m2 = TeamMember(2, "Veronica", "veronica@generic.org")
        m3 = TeamMember(3, "Archi", "archie@generic.org")
        m4 = TeamMember(4, "Jughead", "jughead@generic.org")
        t1 = Team(1, "Team 1")
        t2 = Team(2, "Team 2")
        t3 = Team(3, "Team 3")
        t1.add_member(m1)
        t1.add_member(m2)
        t1.add_member(m4)
        t2.add_member(m3)
        t3.add_member(m4)
        c1 = Competition(1, [t1, t2], "Here", None)
        c2 = Competition(2, [t1, t3], "Here", None)
        c3 = Competition(3, [t2, t3], "Here", None)
        league.add_team(t1)
        league.add_team(t2)
        league.add_team(t3)
        league.add_competition(c1)
        league.add_competition(c2)
        league.add_competition(c3)
        return c1, c2, c3, league, m1, m2, m3, m4, t1, t2, t3