from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'DictatorGame'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    w = 50


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pi = models.IntegerField(min=0, max=2 * C.w)
    x = models.IntegerField(min=0, max=C.w, label="Enter the amount to transfer to your counterpart:")
    opponent_x = models.IntegerField(min=0, max=C.w)


def calculate_dictator(group):
    player1 = group.get_player_by_id(1)
    player2 = group.get_player_by_id(2)
    player1.opponent_x = player2.x
    player2.opponent_x = player1.x
    player1.pi = C.w - player1.x + player1.opponent_x
    player2.pi = C.w - player2.x + player2.opponent_x


def creating_session(subsession):
    subsession.group_randomly()


# PAGES
class Dictator(Page):
    form_model = "player"
    form_fields = ['x']


class CalculateDictator(WaitPage):
    after_all_players_arrive = 'calculate_dictator'


class Results(Page):
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.dictator_x = player.x
        player.participant.dictator_pi = player.pi
        player.participant.dictator_opponent_x = player.opponent_x


page_sequence = [Dictator, CalculateDictator, Results]
