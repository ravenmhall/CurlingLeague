import os
import unittest

from CurlingLeague.league import League
from CurlingLeague.league_database import LeagueDatabase
from CurlingLeague.team import Team


class TestLeagueDatabase(unittest.TestCase):
    def setUp(self):
        LeagueDatabase._sole_instance = LeagueDatabase()
        self.file_name = "file.dat"
        self.backup_file_name = "file.dat.backup"
        self.teams_file_name = "Teams.csv"
        self.team_export_file_name = "MoreTeams.csv"
        if os.path.exists(self.file_name):
            os.remove(self.file_name)
        if os.path.exists(self.backup_file_name):
            os.remove(self.backup_file_name)

    def tearDown(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)
        if os.path.exists(self.backup_file_name):
            os.remove(self.backup_file_name)
        if os.path.exists(self.team_export_file_name):
            os.remove(self.team_export_file_name)

    def test_add_league(self):
        league = League(1, "A League")
        LeagueDatabase.instance().add_league(league)
        self.assertIn(league, LeagueDatabase.instance().leagues)
        league2 = League(2, "Another League")
        LeagueDatabase.instance().add_league(league2)
        self.assertIn(league2, LeagueDatabase.instance().leagues)

    def test_remove_league(self):
        league = League(1, "A League")
        LeagueDatabase.instance().add_league(league)
        league2 = League(2, "Another League")
        LeagueDatabase.instance().add_league(league2)
        self.assertIn(league, LeagueDatabase.instance().leagues)
        self.assertIn(league2, LeagueDatabase.instance().leagues)
        LeagueDatabase.instance().remove_league(league)
        self.assertNotIn(league, LeagueDatabase.instance().leagues)
        LeagueDatabase.instance().remove_league(league2)
        self.assertNotIn(league2, LeagueDatabase.instance().leagues)

    def test_save(self):
        league = League(1, "A League")
        LeagueDatabase.instance().add_league(league)
        LeagueDatabase.instance().save(self.file_name)
        self.assertTrue(os.path.exists(self.file_name))

    def test_league_named(self):
        league = League(1, "A League")
        LeagueDatabase.instance().add_league(league)
        self.assertEqual(league, LeagueDatabase.instance().league_named("A League"))
        league2 = League(2, "Another League")
        LeagueDatabase.instance().add_league(league2)
        self.assertEqual(league2, LeagueDatabase.instance().league_named("Another League"))
        self.assertIsNone(LeagueDatabase.instance().league_named("A League That Doesn't Exist"))

    def test_load(self):
        league = League(1, "A League")
        LeagueDatabase.instance().add_league(league)
        LeagueDatabase.instance().save(self.file_name)
        self.assertTrue(os.path.exists(self.file_name))
        LeagueDatabase.instance().load(self.file_name)
        self.assertEqual(league, LeagueDatabase.instance().league_named("A League"))

    def test_save_backup(self):
        league = League(1, "A League")
        LeagueDatabase.instance().add_league(league)
        LeagueDatabase.instance().save(self.file_name)
        LeagueDatabase.instance().save(self.file_name)
        self.assertTrue(os.path.exists(self.backup_file_name))

    def test_load_backup(self):
        league = League(1, "A League")
        LeagueDatabase.instance().add_league(league)
        LeagueDatabase.instance().save(self.file_name)
        LeagueDatabase.instance().save(self.file_name)
        self.assertTrue(os.path.exists(self.backup_file_name))
        LeagueDatabase.instance().load("NotARealFile.dat")
        self.assertEqual(league, LeagueDatabase.instance().league_named("A League"))

    def test_next_oid(self):
        oid = LeagueDatabase.instance().next_oid()
        self.assertEqual(oid + 1, LeagueDatabase.instance().next_oid())

    def test_import_league_teams(self):
        league = League(1, "A League")
        LeagueDatabase.instance().import_league_teams(league, self.teams_file_name)
        LeagueDatabase.instance().save(self.file_name)
        LeagueDatabase.instance().load(self.file_name)
        self.assertIn(league, LeagueDatabase.instance().leagues)
        self.assertEqual(league.teams[0], league.team_named("Flintstones"))
        self.assertEqual(league.teams[1], league.team_named("Curl Jam"))
        self.assertEqual(league.teams[0].members[0], league.team_named("Flintstones").member_named("Fred Flintstone"))

    def test_export_league_teams(self):
        league = League(1, "A League")
        team = Team(2, "A Team")
        league.add_team(team)
        LeagueDatabase.instance().export_league_teams(league, self.team_export_file_name)
        self.assertTrue(os.path.exists(self.team_export_file_name))
        LeagueDatabase.instance().import_league_teams(league, self.team_export_file_name)
        self.assertEqual(league, LeagueDatabase.instance().league_named("A League"))
        self.assertEqual(team, LeagueDatabase.instance().league_named("A League").team_named("A Team"))



if __name__ == '__main__':
    unittest.main()
