import random

from otree.api import *


doc = """
Uses a risk assessment game to gage how risk averse a player is. This allows us to control for risk aversion in data.
"""


class C(BaseConstants):
    NAME_IN_URL = 'RiskTolerance'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    w = 100


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pi = models.IntegerField(min=0, max=2 * C.w)
    x = models.IntegerField(min=0, max=C.w, label="Enter the amount to wager:")
    coin_flip = models.StringField()


def calculate_coin_flip(group):
    for p in group.get_players():
        coin = ["HEADS", "TAILS"]
        p.coin_flip = random.choice(coin)
        if p.coin_flip == "HEADS":
            p.pi = int(1.5 * p.x) + C.w
            if int(1.5 * p.x) < 1.5 * p.x:
                p.pi += 1
        else:
            p.pi = C.w - p.x


# PAGES
class Stop(Page):
    pass

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class MyPage(Page):
    form_model = "player"
    form_fields = ['x']


class CalculateCoinFlip(WaitPage):
    after_all_players_arrive = 'calculate_coin_flip'


class Results(Page):
    pass

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.risk_x = player.x
        player.participant.risk_pi = player.pi
        player.participant.risk_flip = player.coin_flip


page_sequence = [Stop, MyPage, CalculateCoinFlip, Results]
