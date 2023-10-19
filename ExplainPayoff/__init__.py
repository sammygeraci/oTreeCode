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


# PAGES
class CalculatePayoff(Page):
    pass

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.selected_round = player.participant.final_round_num
        player.pi = player.participant.round_pi
        player.round_dollars = player.pi / 50
        player.a = player.participant.round_a
        player.R = player.participant.round_r
        player.x = player.participant.round_x
        player.opponent_x = player.participant.round_opponent_x
        player.win = player.participant.round_win
        player.color = player.participant.round_color
        player.r_x = player.participant.risk_x
        player.r_pi = player.participant.risk_pi
        player.r_flip = player.participant.risk_flip
        player.r_dollars = player.r_pi / 50
        player.total_dollars = player.round_dollars + player.r_dollars + 5


class Results(Page):
    pass


page_sequence = [CalculatePayoff, Results]
