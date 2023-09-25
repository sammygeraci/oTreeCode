import random

from otree.api import *


doc = """
Uses the dictator game to gage how altruistic a player is. This allows us to control for altruism in the results.
"""


class C(BaseConstants):
    NAME_IN_URL = 'DictatorGame'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 2
    TOTAL_ROUNDS = 15
    w = 200
    max_a = 100


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    a = models.IntegerField(min=0, max=C.max_a, label="Enter the amount to transfer to your counterpart:")


class Player(BasePlayer):
    pi = models.IntegerField(min=C.w, max=C.w + C.max_a)
    dictator = models.BooleanField()


def calculate_dictator(group):
    player1 = group.get_player_by_id(group.round_number)
    player2 = group.get_player_by_id(3 - group.round_number)
    for player in group.get_players():
        if player == player1:
            player.dictator = True
        else:
            player.dictator = False
    player1.pi = C.w + C.max_a - group.a
    player2.pi = C.w + group.a

    for p in group.get_players():
        if p.participant.final_round_num == p.round_number:
            p.participant.round_pi = p.pi
            p.participant.round_a = p.group.a
            p.participant.round_r = 0
            p.participant.round_x = 0
            p.participant.round_opponent_x = 0
            p.participant.round_win = "DICTATOR_GAME"
            p.participant.round_color = "BLUE" if (p.id_in_group + p.round_number) % 2 == 0 else "GREEN"


def creating_session(subsession):
    if subsession.round_number == 1:
        for p in subsession.get_players():
            p.participant.final_round_num = random.randint(1, C.TOTAL_ROUNDS)
            p.participant.persistent_id = p.id_in_group
    subsession.group_randomly(fixed_id_in_group=True)


# PAGES
class Dictator(Page):
    form_model = "group"
    form_fields = ['a']

    @staticmethod
    def is_displayed(player):
        return player.id_in_group + player.round_number != 3


class Wait(Page):
    pass

    @staticmethod
    def is_displayed(player):
        return player.id_in_group + player.round_number == 3


class CalculateDictator(WaitPage):
    after_all_players_arrive = 'calculate_dictator'


class Results(Page):
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.dictator_x = player.x
        player.participant.dictator_pi = player.pi
        player.participant.dictator_opponent_x = player.opponent_x


page_sequence = [Dictator, Wait, CalculateDictator]
