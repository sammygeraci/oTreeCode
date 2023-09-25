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
    selected_round = models.IntegerField()
    a = models.IntegerField()
    R = models.IntegerField()
    x = models.IntegerField()
    opponent_x = models.IntegerField()
    pi = models.IntegerField()
    round_dollars = models.CurrencyField()
    color = models.StringField()
    win = models.StringField()
    r_x = models.IntegerField()
    r_pi = models.IntegerField()
    r_flip = models.StringField()
    r_dollars = models.CurrencyField()
    total_dollars = models.CurrencyField()


def calculate_payoffs(group):
    for p in group.get_players():
        p.selected_round = p.participant.final_round_num
        p.pi = p.participant.round_pi
        p.round_dollars = p.pi / 50
        p.a = p.participant.round_a
        p.R = p.participant.round_r
        p.x = p.participant.round_x
        p.opponent_x = p.participant.round_opponent_x
        p.win = p.participant.round_win
        p.color = p.participant.round_color
        p.r_x = p.participant.risk_x
        p.r_pi = p.participant.risk_pi
        p.r_flip = p.participant.risk_flip
        p.r_dollars = p.r_pi / 50
        p.total_dollars = p.round_dollars + p.r_dollars + 5


# PAGES
class CalculatePayoff(WaitPage):
    after_all_players_arrive = 'calculate_payoffs'


class Results(Page):
    pass


page_sequence = [CalculatePayoff, Results]
