import unittest
import fitness

class TestHeatFitness(unittest.TestCase):

    def test_people_who_dont_care_get_no_goodness(self):
        cold = fitness.heatFitness('walter',1)
        self.assertEqual(cold,0)
        hot = fitness.heatFitness('walter',2)
        self.assertEqual(hot,0)
        hot = fitness.heatFitness('walter',3)
        self.assertEqual(hot,0)

    def test_people_who_love_cold_are_unhappy_in_heat(self):
        fit = fitness.heatFitness('mario',3)
        self.assertEqual(fit,0)

    def test_people_who_love_cold_are_kinda_happy_in_warm(self):
        fit = fitness.heatFitness('mario',2)
        self.assertEqual(fit,1)

    def test_people_who_love_cold_are_happy_in_cold(self):
        fit = fitness.heatFitness('mario',1)
        self.assertEqual(fit,4)

    def test_people_who_want_medium_are_kind_unhappy_in_heat(self):
        fit = fitness.heatFitness('octavio',3)
        self.assertEqual(fit,1)

    def test_people_who_want_medium_are_kind_unhappy_in_cold(self):
        fit = fitness.heatFitness('octavio',1)
        self.assertEqual(fit,1)

class TestTeamFitness(unittest.TestCase):

    def test_next_to_non_team_member_means_nothing(self):
        fit = fitness.teamFitness({1: 'walter'}, 'mario', 2)
        self.assertEqual(fit,0)

    def test_next_to_team_member_is_good_at_tier(self):
        fit = fitness.teamFitness({1: 'dax'}, 'mario', 2)
        self.assertEqual(fit,3)

    def test_next_to_team_member_is_good_at_lower_tier(self):
        fit = fitness.teamFitness({1: 'pia'}, 'walter', 2)
        self.assertEqual(fit,1)

    def test_next_to_two_team_members_is_doubly_good_at_tier(self):
        fit = fitness.teamFitness({1: 'dax', 3: 'daniel'}, 'mario', 2)
        self.assertEqual(fit,6)
class TestGlobalFitness(unittest.TestCase):

    def test_a_known_instance(self):
        fit = fitness.fitness({1: 'walter',2: 'mario'})
        self.assertEqual(fit,1)

if __name__ == '__main__':
    unittest.main()
