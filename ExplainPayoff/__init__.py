from otree.api import *


doc = """
Explains breakdown of payoff to player.
"""


class C(BaseConstants):
    NAME_IN_URL = 'ExplainPayoff'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


def calculate_payoffs(group):
    pass


# PAGES
class CalculatePayoff(WaitPage):
    after_all_players_arrive = 'calculate_payoffs'


class Results(Page):
    pass


page_sequence = [CalculatePayoff, Results]
