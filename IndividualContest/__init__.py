import random

from otree.api import *

doc = """
Demonstration of game that will be used for TIDE Lab research in group contest theory
"""


class C(BaseConstants):
    NAME_IN_URL = 'IndividualContest'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    w = 200


class Subsession(BaseSubsession):
    Treatment = models.IntegerField(initial=1, min=1, max=2, )


class Group(BaseGroup):
    a = models.IntegerField(min=0, max=C.w)
    R = models.IntegerField(min=0, max=C.w / 2)
    winner = models.IntegerField(min=1, max=2)


class Player(BasePlayer):
    x = models.IntegerField(min=0, max=C.w / 2)
    opponent_x = models.IntegerField(min=0, max=C.w / 2)
    pi = models.IntegerField(min=0, max=2 * C.w)


# initializes additional income a given to player 2
def set_random_additional_income(group):
    if group.subsession.Treatment == 1:
        group.a = random.randint(0, C.w + 1)


def set_opponent_effort(player):
    player.opponent_x = player.group.get_player_by_id(3 - player.id_in_group).x


# runs functions to aggregate effort and find winner
def determine_winner(group):
    x1 = group.get_player_by_id(1).x
    x2 = group.get_player_by_id(2).x
    if x1 == 0 and x2 == 0:
        group.winner = random.randint(1, 3)
    elif random.randint(0, x1 + x2) < x1:
        group.winner = 1
    else:
        group.winner = 2


def calculate_profit(group):
    x1 = group.get_player_by_id(1).x
    x2 = group.get_player_by_id(2).x
    if group.winner == 1:
        group.get_player_by_id(1).pi = C.w + (C.w - group.a) - x1
        group.get_player_by_id(2).pi = C.w + group.a - x1
    elif group.winner == 2:
        group.get_player_by_id(1).pi = C.w + (C.w - group.a) - x1 - group.R
        group.get_player_by_id(2).pi = C.w + group.a - x2 + group.R


# PAGES
class Introduction(WaitPage):
    pass


class TransferAdditionalIncome(Page):
    form_model = "group"
    form_fields = ['a']

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 1 and player.subsession.Treatment == 2


class RandomRent(WaitPage):
    after_all_players_arrive = 'set_random_additional_income'


class SetRent(Page):
    form_model = 'group'
    form_fields = ['R']

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 2


class Invest(Page):
    form_model = 'player'
    form_fields = ['x']


class OpponentEffort(WaitPage):
    after_all_players_arrive = 'set_opponent_effort'


class DetermineWinner(WaitPage):
    after_all_players_arrive = 'determine_winner'


class CalculateProfits(WaitPage):
    after_all_players_arrive = 'calculate_profit'


class Results(Page):
    pass


page_sequence = [Introduction, TransferAdditionalIncome, SetRent, Invest, DetermineWinner, CalculateProfits, Results]
