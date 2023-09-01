import random

from otree.api import *

doc = """
Demonstration of game that will be used for TIDE Lab research in group contest theory
"""


class C(BaseConstants):
    NAME_IN_URL = 'OneOnThreeGame'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 1
    INITIAL_ENDOWMENT_TOTAL = 120


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    p1_proposed_income = models.IntegerField(initial=0)
    p2_proposed_income = models.IntegerField(initial=0)
    p3_proposed_income = models.IntegerField(initial=0)
    p4_proposed_income = models.IntegerField(initial=0)
    p5_proposed_income = models.IntegerField(initial=0)
    total_effort = models.IntegerField()
    proposer_wins = models.BooleanField()


class Player(BasePlayer):
    initial_endowment = models.IntegerField()
    proposed_income = models.IntegerField(initial=0)
    accept_proposal = models.BooleanField()
    contest_prize = models.IntegerField(initial=0)
    potential_income_win = models.IntegerField(initial=0)
    potential_income_lose = models.IntegerField(initial=0)
    effort = models.IntegerField(initial=0)
    wins_contest = models.BooleanField()
    income = models.IntegerField()
    net_earnings = models.IntegerField(initial=0)


# returns sum of effort for all players in group including proposer and responders
def aggregate_effort(group):
    group.total_effort = 0
    for player in group.get_players():
        group.total_effort += player.effort


# returns True if proposer wins and False if responders win
def select_winner(group):
    return random.randint(0, group.total_effort) < group.get_player_by_id(1).effort


# updates wins contest variables for players after winner is selected
def update_winner_variables(group):
    group.get_player_by_id(1).wins_contest = group.proposer_wins
    for player in group.get_players()[1:]:
        player.wins_contest = not group.proposer_wins


# updates net earnings variables for all players
def update_net_earnings(group):
    for player in group.get_players():
        player.net_earnings = player.initial_endowment - player.effort + player.income


# initializes initial endowment variables for all players in group based on group size and initial endowment
def set_initial_endowments(group):
    group.get_player_by_id(1).initial_endowment = int(C.INITIAL_ENDOWMENT_TOTAL / 2)
    responder_endowment = int((C.INITIAL_ENDOWMENT_TOTAL / 2) / (C.PLAYERS_PER_GROUP - 1))
    for player in group.get_players()[1:]:
        player.initial_endowment = responder_endowment


# gets proposed income data from group to set players' proposed income variables
def update_proposal_vars(group):
    group.get_player_by_id(1).accept_proposal = True
    proposed_incomes = [group.p1_proposed_income, group.p2_proposed_income, group.p3_proposed_income,
                        group.p4_proposed_income, group.p5_proposed_income]
    group.get_player_by_id(1).proposed_income = C.INITIAL_ENDOWMENT_TOTAL
    for player in group.get_players()[1:]:
        player.proposed_income = proposed_incomes[player.id_in_group - 2]
        group.get_player_by_id(1).proposed_income -= player.proposed_income


# calculates potential income variables for all players if they win and lose the contest
def calculate_potential_incomes(group):
    group.get_player_by_id(1).potential_income_win = C.INITIAL_ENDOWMENT_TOTAL
    group.get_player_by_id(1).potential_income_lose = C.INITIAL_ENDOWMENT_TOTAL
    for player in group.get_players()[1:]:
        if player.accept_proposal:
            player.potential_income_win = player.proposed_income
            player.potential_income_lose = player.proposed_income
        else:
            player.potential_income_win = player.contest_prize
            player.potential_income_lose = 0  # This could also be the proposed_income
        group.get_player_by_id(1).potential_income_win -= player.potential_income_lose
        group.get_player_by_id(1).potential_income_lose -= player.potential_income_win
    group.get_player_by_id(1).contest_prize = group.get_player_by_id(1).potential_income_win - \
                                              group.get_player_by_id(1).potential_income_lose


# runs functions to aggregate effort and find winner, then uses that compute players' net earnings variables
def run_contest(group):
    aggregate_effort(group)
    group.proposer_wins = select_winner(group)
    update_winner_variables(group)
    for player in group.get_players():
        if player.wins_contest:
            player.income = player.potential_income_win
        else:
            player.income = player.potential_income_lose
    update_net_earnings(group)


# PAGES
class Introduction(WaitPage):
    after_all_players_arrive = 'set_initial_endowments'


class ProposalPage(Page):
    form_model = "group"

    @staticmethod
    def get_form_fields(group):
        if C.PLAYERS_PER_GROUP == 2:
            return ['p1_proposed_income']
        elif C.PLAYERS_PER_GROUP == 4:
            return ['p1_proposed_income', 'p2_proposed_income', 'p3_proposed_income']
        elif C.PLAYERS_PER_GROUP == 6:
            return ['p1_proposed_income', 'p2_proposed_income', 'p3_proposed_income', 'p4_proposed_income',
                    'p5_proposed_income']
        else:
            return ['']

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 1


class UpdateProposalVariables(WaitPage):
    after_all_players_arrive = 'update_proposal_vars'


class ProposalResponse(Page):
    form_model = 'player'
    form_fields = ['accept_proposal']

    @staticmethod
    def is_displayed(player):
        return player.id_in_group != 1


class SetContestPrize(Page):
    form_model = 'player'
    form_fields = ['contest_prize']

    @staticmethod
    def is_displayed(player):
        return player.id_in_group != 1 and player.accept_proposal == False


class CalculatePotentialIncomes(WaitPage):
    after_all_players_arrive = 'calculate_potential_incomes'


class ExpendEffort(Page):
    form_model = 'player'
    form_fields = ['effort']


class RunContest(WaitPage):
    after_all_players_arrive = 'run_contest'


class Results(Page):
    pass


page_sequence = [Introduction, ProposalPage, UpdateProposalVariables, ProposalResponse, SetContestPrize,
                 CalculatePotentialIncomes, ExpendEffort, RunContest, Results]
