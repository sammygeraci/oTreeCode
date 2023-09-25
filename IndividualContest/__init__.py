import random

from otree.api import *

doc = """
Demonstration of game that will be used for TIDE Lab research in group contest theory
"""


class C(BaseConstants):
    NAME_IN_URL = 'IndividualContest'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 14
    w = 200


class Subsession(BaseSubsession):
    Treatment = models.IntegerField(initial=2, min=1, max=2)
    Adjusted_Round = models.IntegerField(initial=2)


class Group(BaseGroup):
    a = models.IntegerField(min=0, max=C.w / 2, label="Enter the amount to transfer to your counterpart:")
    R = models.IntegerField(min=0, max=C.w / 2, label="Enter the amount for the lottery prize:")
    winner = models.IntegerField(min=1, max=2)


class Player(BasePlayer):
    x = models.IntegerField(min=0, max=C.w / 2, label="Enter the number of lottery tickets you purchase:")
    opponent_x = models.IntegerField(min=0, max=C.w / 2)
    pi = models.IntegerField(min=0, max=2 * C.w)
    opponent_pi = models.IntegerField(initial=0, min=0, max=2 * C.w)


def creating_session(subsession):
    subsession.Adjusted_Round = subsession.round_number + 2
    matrix = subsession.get_group_matrix()
    blue = []
    green = []
    new_mat = []
    if subsession.round_number == 1:
        for p in subsession.get_players():
            if p.participant.persistent_id == 1:
                blue.append(p)
            else:
                green.append(p)
    else:
        for row in matrix:
            blue.append(row[0])
            green.append(row[1])
    random.shuffle(blue)
    random.shuffle(green)
    if subsession.round_number % 2 == 0:
        for i in range(len(blue)):
            new_mat.append([green.pop(), blue.pop()])
    else:
        for i in range(len(blue)):
            new_mat.append([blue.pop(), green.pop()])
    subsession.set_group_matrix(new_mat)


# initializes additional income a given to player 2
def set_random_additional_income(group):
    if group.subsession.Treatment == 1:
        group.a = random.randint(0, C.w + 1)


def set_opponent_effort(group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    if group.R == 0:
        p1.x = 0
        p2.x = 0
    p1.opponent_x = p2.x
    p2.opponent_x = p1.x


# runs functions to aggregate effort and find winner
def determine_winner(group):
    x1 = group.get_player_by_id(1).x
    x2 = group.get_player_by_id(2).x
    if x1 == 0 and x2 == 0:
        group.winner = random.randint(1, 2)
    elif random.randint(1, x1 + x2) <= x1:
        group.winner = 1
    else:
        group.winner = 2


def calculate_profit(group):
    x1 = group.get_player_by_id(1).x
    x2 = group.get_player_by_id(2).x
    if group.winner == 1:
        group.get_player_by_id(1).pi = C.w + (int(C.w / 2) - group.a) - x1
        group.get_player_by_id(2).opponent_pi = C.w + (int(C.w / 2) - group.a) - x1
        group.get_player_by_id(2).pi = C.w + group.a - x2
        group.get_player_by_id(1).opponent_pi = C.w + group.a - x2
    elif group.winner == 2:
        group.get_player_by_id(1).pi = C.w + (int(C.w / 2) - group.a) - x1 - group.R
        group.get_player_by_id(2).opponent_pi = C.w + (int(C.w / 2) - group.a) - x1 - group.R
        group.get_player_by_id(2).pi = C.w + group.a - x2 + group.R
        group.get_player_by_id(1).opponent_pi = C.w + group.a - x2 + group.R


def update_data(group):
    for p in group.get_players():
        if p.participant.final_round_num == p.subsession.Adjusted_Round:
            p.participant.round_pi = p.pi
            p.participant.round_a = p.group.a
            p.participant.round_r = p.group.R
            p.participant.round_x = p.x
            p.participant.round_opponent_x = p.opponent_x
            p.participant.round_win = "YES" if p.group.winner == p.id_in_group else "NO"
            p.participant.round_color = "BLUE" if p.id_in_group == 1 else "GREEN"


# PAGES
class TransferAdditionalIncome(Page):
    form_model = "group"
    form_fields = ['a']

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 1 and player.subsession.Treatment == 2


class DisplayAdditionalIncome(Page):
    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 2 and player.subsession.Treatment == 2


class RandomAdditionalIncome(WaitPage):
    after_all_players_arrive = 'set_random_additional_income'


class DisplayIncomeTransfer(Page):
    pass

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 1


class SetRent(Page):
    form_model = 'group'
    form_fields = ['R']

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 2


class WaitForRent(WaitPage):
    pass


class DisplayRent(Page):
    pass


class Invest(Page):
    form_model = 'player'
    form_fields = ['x']

    @staticmethod
    def is_displayed(player):
        return player.group.R > 0


class OpponentEffort(WaitPage):
    after_all_players_arrive = 'set_opponent_effort'


class DetermineWinner(WaitPage):
    after_all_players_arrive = 'determine_winner'


class CalculateProfits(WaitPage):
    after_all_players_arrive = 'calculate_profit'


class Results(Page):
    pass

    @staticmethod
    def is_displayed(player):
        return player.group.R > 0


class ResultsNoLottery(Page):
    pass

    @staticmethod
    def is_displayed(player):
        return player.group.R == 0


class UpdateParticipantData(WaitPage):
    after_all_players_arrive = 'update_data'


class ShuffleWaitPage(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession):
        pass


page_sequence = [TransferAdditionalIncome, DisplayAdditionalIncome,RandomAdditionalIncome, DisplayIncomeTransfer,
                 SetRent, WaitForRent, Invest,OpponentEffort, DetermineWinner, CalculateProfits, Results,
                 ResultsNoLottery, UpdateParticipantData, ShuffleWaitPage]
