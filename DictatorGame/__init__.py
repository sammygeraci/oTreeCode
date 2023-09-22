from otree.api import *


doc = """
Uses the dictator game to gage how altruistic a player is. This allows us to control for altruism in the results.
"""


class C(BaseConstants):
    NAME_IN_URL = 'DictatorGame'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 2
    w = 200
    max_x = 100


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pi = models.IntegerField(min=0, max=C.w + C.max_x)
    x = models.IntegerField(min=0, max=C.max_x, label="Enter the amount to transfer to your counterpart:")
    opponent_x = models.IntegerField(min=0, max=C.max_x, initial=0)
    dictator = models.BooleanField()


def calculate_dictator(group):
    player1 = group.get_player_by_id(group.round_number)
    player2 = group.get_player_by_id(3 - group.round_number)
    for player in group.get_players():
        if player == player1:
            player.dictator = True
        else:
            player.dictator = False
    player2.opponent_x = player1.x
    player2.x = 0
    player1.pi = C.w + C.max_x - player1.x
    player2.pi = C.w + player2.opponent_x


def creating_session(subsession):
    subsession.group_randomly(fixed_id_in_group=True)


# PAGES
class Dictator(Page):
    form_model = "player"
    form_fields = ['x']

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
