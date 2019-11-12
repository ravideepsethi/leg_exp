from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants, Subsession, Group, Player
import numpy as np

class Auction(Page):
    def is_displayed(self):
        return self.participant.vars['alive'] == True and self.subsession.round_number > Constants.num_rounds/2

    form_model = 'player'
    form_fields = ['bid_role', 'bid']

    def vars_for_template(self):
        if self.round_number == 1: pass

        h_proposer = self.group.in_round(self.round_number - 1).proposer == self.player.in_round(self.round_number - 1).id_in_group
        h_proposal = self.group.in_round(self.round_number - 1).color1
        h_you_voted = self.player.in_round(self.round_number - 1).vote

        return dict(
            h_proposal=h_proposal,
            h_proposer=h_proposer,
            h_you_voted=h_you_voted
        )
        pass

class AuctionWaitPage(WaitPage):
    def is_displayed(self):
        return self.participant.vars['alive'] == True and self.subsession.round_number > Constants.num_rounds/2

    def after_all_players_arrive(self):
        group = self.group
        players = group.get_players()

        if group.selected1 == 1 and group.selected2 == 0 and group.selected3 == 0:
            group.get_player_by_id(1).bid_paid = group.get_player_by_id(1).bid
            group.get_player_by_id(2).bid_paid = 0
            group.get_player_by_id(3).bid_paid = 0
        elif group.selected1 == 0 and group.selected2 == 1 and group.selected3 == 0:
            group.get_player_by_id(1).bid_paid = 0
            group.get_player_by_id(2).bid_paid = group.get_player_by_id(2).bid
            group.get_player_by_id(3).bid_paid = 0
        else:
            group.get_player_by_id(1).bid_paid = 0
            group.get_player_by_id(2).bid_paid = 0
            group.get_player_by_id(3).bid_paid = group.get_player_by_id(3).bid

        for p in players:
            # determine the probability of role assignment
            if p.bid_role == 1:
                p.prob_role1 = 1 / 3 + (2 / 3) * p.bid / Constants.auc_endowment
                p.prob_role2 = (1 - p.prob_role1) / 2
                p.prob_role3 = (1 - p.prob_role1) / 2
            elif p.bid_role == 2:
                p.prob_role2 = 1 / 3 + (2 / 3) * p.bid / Constants.auc_endowment
                p.prob_role1 = (1 - p.prob_role2) / 2
                p.prob_role3 = (1 - p.prob_role2) / 2
            else:
                p.prob_role3 = 1 / 3 + (2 / 3) * p.bid / Constants.auc_endowment
                p.prob_role1 = (1 - p.prob_role3) / 2
                p.prob_role2 = (1 - p.prob_role3) / 2

        group.rand_role = np.random.random()
        # If member 1 is selected to pay and determine role assignment
        if group.selected1 == 1 and group.selected2 == 0 and group.selected3 == 0:
            # Apply the selected member's probability assignment as the groups' probability assignment
            group.selected_prob_role1 = group.get_player_by_id(1).prob_role1  # probability that the selected member is assigned role 1
            group.selected_prob_role2 = group.get_player_by_id(1).prob_role2  # probability that the selected member is assigned role 2
            group.selected_prob_role3 = group.get_player_by_id(1).prob_role3  # probability that the selected member is assigned role 3
            # Reassign roles
            if group.rand_role < group.selected_prob_role1 / 2:
                for p in players:
                    if p.id_in_group == 1:
                        p.id_in_group = 1
                    elif p.id_in_group == 2:
                        p.id_in_group = 2
                    else:
                        p.id_in_group = 3
            elif group.rand_role >= group.selected_prob_role1 / 2 and group.rand_role < group.selected_prob_role1:
                for p in players:
                    if p.id_in_group == 1 : p.id_in_group = 1
                    elif p.id_in_group == 2: p.id_in_group = 3
                    else: p.id_in_group = 2
            elif group.rand_role >= group.selected_prob_role1 and group.rand_role < group.selected_prob_role1 + group.selected_prob_role2 / 2:
                for p in players:
                    if p.id_in_group == 1 : p.id_in_group = 2
                    elif p.id_in_group == 2: p.id_in_group = 1
                    else: p.id_in_group = 3
            elif group.rand_role >= group.selected_prob_role1 + group.selected_prob_role2 / 2 and group.rand_role < group.selected_prob_role1 + group.selected_prob_role2:
                for p in players:
                    if p.id_in_group== 1 : p.id_in_group = 2
                    elif p.id_in_group == 2: p.id_in_group = 3
                    else: p.id_in_group = 1
            elif group.rand_role >= group.selected_prob_role1 + group.selected_prob_role2 and group.rand_role < group.selected_prob_role1 + group.selected_prob_role2 + group.selected_prob_role3 / 2:
                for p in players:
                    if p.id_in_group == 1 : p.id_in_group = 3
                    elif p.id_in_group == 2: p.id_in_group = 1
                    else: p.id_in_group = 2
            else:
                for p in players:
                    if p.id_in_group == 1 : p.id_in_group = 3
                    elif p.id_in_group == 2: p.id_in_group = 2
                    else: p.id_in_group = 1
        # If member 2 is selected to pay and determine role assignment
        elif group.selected1 == 0 and group.selected2 == 1 and group.selected3 == 0:
            # Apply the selected member's probabilty assignment as the groups' probability assignment
            group.selected_prob_role1 = group.get_player_by_id(2).prob_role1  # probability that the selected member is assigned role 1
            group.selected_prob_role2 = group.get_player_by_id(2).prob_role2  # probability that the selected member is assigned role 2
            group.selected_prob_role3 = group.get_player_by_id(2).prob_role3  # probability that the selected member is assigned role 3
            # Reassign roles
            if group.rand_role < group.selected_prob_role1 / 2:
                for p in players:
                    if p.id_in_group == 1 : p.id_in_group = 2
                    elif p.id_in_group == 2: p.id_in_group = 1
                    else: p.id_in_group = 3
            elif group.rand_role >= group.selected_prob_role1 / 2 and group.rand_role < group.selected_prob_role1:
                for p in players:
                    if p.id_in_group == 1 : p.id_in_group = 3
                    elif p.id_in_group == 2: p.id_in_group = 1
                    else: p.id_in_group = 2
            elif group.rand_role >= group.selected_prob_role1 and group.rand_role < group.selected_prob_role1 + group.selected_prob_role2 / 2:
                for p in players:
                    if p.id_in_group == 1 : p.id_in_group = 1
                    elif p.id_in_group == 2: p.id_in_group = 2
                    else: p.id_in_group = 3
            elif group.rand_role >= group.selected_prob_role1 + group.selected_prob_role2 / 2 and group.rand_role < group.selected_prob_role1 + group.selected_prob_role2:
                for p in players:
                    if p.id_in_group == 1 : p.id_in_group = 3
                    elif p.id_in_group == 2: p.id_in_group = 2
                    else: p.id_in_group = 1
            elif group.rand_role >= group.selected_prob_role1 + group.selected_prob_role2 and group.rand_role < group.selected_prob_role1 + group.selected_prob_role2 + group.selected_prob_role3 / 2:
                for p in players:
                    if p.id_in_group == 1 : p.id_in_group = 1
                    elif p.id_in_group == 2: p.id_in_group = 3
                    else: p.id_in_group = 2
            else:
                for p in players:
                    if p.id_in_group == 1 : p.id_in_group = 2
                    elif p.id_in_group == 2: p.id_in_group = 3
                    else: p.id_in_group = 1
        # If member 3 is selected to pay and determine role assignment
        else:
            # Apply the selected member's probabilty assignment as the groups' probability assignment
            group.selected_prob_role1 = group.get_player_by_id(3).prob_role1  # probability that the selected member is assigned role 1
            group.selected_prob_role2 = group.get_player_by_id(3).prob_role2  # probability that the selected member is assigned role 2
            group.selected_prob_role3 = group.get_player_by_id(3).prob_role3  # probability that the selected member is assigned role 3
            # Reassign roles
            if group.rand_role < group.selected_prob_role1 / 2:
                for p in players:
                    if p.id_in_group == 1 : p.id_in_group = 2
                    elif p.id_in_group == 2: p.id_in_group = 3
                    else: p.id_in_group = 1
            elif group.rand_role >= group.selected_prob_role1 / 2 and group.rand_role < group.selected_prob_role1:
                for p in players:
                    if p.id_in_group == 1 : p.id_in_group = 3
                    elif p.id_in_group == 2: p.id_in_group = 2
                    else: p.id_in_group = 1
            elif group.rand_role >= group.selected_prob_role1 and group.rand_role < group.selected_prob_role1 + group.selected_prob_role2 / 2:
                for p in players:
                    if p.id_in_group == 1 : p.id_in_group = 1
                    elif p.id_in_group == 2: p.id_in_group = 3
                    else: p.id_in_group = 2
            elif group.rand_role >= group.selected_prob_role1 + group.selected_prob_role2 / 2 and group.rand_role < group.selected_prob_role1 + group.selected_prob_role2:
                for p in players:
                    if p.id_in_group == 1 : p.id_in_group = 3
                    elif p.id_in_group == 2: p.id_in_group = 1
                    else: p.id_in_group = 2
            elif group.rand_role >= group.selected_prob_role1 + group.selected_prob_role2 and group.rand_role < group.selected_prob_role1 + group.selected_prob_role2 + group.selected_prob_role3 / 2:
                for p in players:
                    if p.id_in_group == 1 : p.id_in_group = 1
                    elif p.id_in_group == 2: p.id_in_group = 2
                    else: p.id_in_group = 3
            else:
                for p in players:
                    if p.id_in_group == 1 : p.id_in_group = 2
                    elif p.id_in_group == 2: p.id_in_group = 1
                    else: p.id_in_group = 3

        # Reassign colors
        group.get_player_by_id(1).color = group.color1
        group.get_player_by_id(2).color = group.color2
        group.get_player_by_id(3).color = group.color3

        # Reassign proposer status: stage 1
        group.rand_num_prop = np.random.random()
        if group.rand_num_prop <= Constants.rec_prob_1:
            group.proposer = 1
        elif group.rand_num_prop > Constants.rec_prob_1 and group.rand_num_prop <= Constants.rec_prob_1 + Constants.rec_prob_2:
            group.proposer = 2
        else:
            group.proposer = 3
        # Reassign proposer status: stage 2
        group.rand_num_prop_2 = np.random.random()
        if group.rand_num_prop_2 <= Constants.rec_prob_1_2nd:
            group.proposer_2 = 1
        elif group.rand_num_prop_2 > Constants.rec_prob_1_2nd and group.rand_num_prop_2 <= Constants.rec_prob_1_2nd + Constants.rec_prob_2_2nd:
            group.proposer_2 = 2
        else:
            group.proposer_2 = 3

        # Update color of the proposer: stage 1
        if group.proposer == 1:
            group.color_prop = group.get_player_by_id(1).color
        elif group.proposer == 2:
            group.color_prop = group.get_player_by_id(2).color
        else:
            group.color_prop = group.get_player_by_id(3).color
        # Update color of the proposer: stage 1
        if group.proposer_2 == 1:
            group.color_prop_2 = group.get_player_by_id(1).color
        elif group.proposer_2 == 2:
            group.color_prop_2 = group.get_player_by_id(2).color
        else:
            group.color_prop_2 = group.get_player_by_id(3).color

        #Take care of the dynamic display in Auction page (bid to probabilities)
        group.bid_1 = group.get_player_by_id(1).bid
        group.bid_2 = group.get_player_by_id(2).bid
        group.bid_3 = group.get_player_by_id(3).bid
        group.bid_paid_1 = group.get_player_by_id(1).bid_paid
        group.bid_paid_2 = group.get_player_by_id(2).bid_paid
        group.bid_paid_3 = group.get_player_by_id(3).bid_paid
        group.surplus_1 = group.auc_endowment- group.bid_paid_1
        group.surplus_2 = group.auc_endowment - group.bid_paid_2
        group.surplus_3 = group.auc_endowment - group.bid_paid_3


class AuctionResult(Page):
    def is_displayed(self):
        return self.participant.vars['alive'] == True and self.subsession.round_number > Constants.num_rounds/2

class Proposal(Page):
    def is_displayed(self):
        return self.participant.vars['alive'] == True

    form_model = 'player'
    form_fields = ['offer_to_1','offer_to_2','offer_to_3']

    def error_message(self, values):
      if values['offer_to_1'] + values['offer_to_2'] + values['offer_to_3'] != self.group.budget:
                    return 'Your provisional allocation proposal must add up to {}'.format(self.group.budget)

    #Return the mute variable back to False
    def before_next_page(self):
        group = self.group
        players = group.get_players()
        for p in players:
          p.participant.vars['mute'] = False

class ProposalWaitPage(WaitPage):
    def is_displayed(self):
        return self.participant.vars['alive'] == True

    def after_all_players_arrive(self):
        group = self.group
        players = group.get_players()
        if group.proposer == 1:
            group.chosen_offer_to_1 = group.get_player_by_id(1).offer_to_1
            group.chosen_offer_to_2 = group.get_player_by_id(1).offer_to_2
            group.chosen_offer_to_3 = group.get_player_by_id(1).offer_to_3
        elif group.proposer == 2:
            group.chosen_offer_to_1 = group.get_player_by_id(2).offer_to_1
            group.chosen_offer_to_2 = group.get_player_by_id(2).offer_to_2
            group.chosen_offer_to_3 = group.get_player_by_id(2).offer_to_3
        else:
            group.chosen_offer_to_1 = group.get_player_by_id(3).offer_to_1
            group.chosen_offer_to_2 = group.get_player_by_id(3).offer_to_2
            group.chosen_offer_to_3 = group.get_player_by_id(3).offer_to_3

        for p in players:
            if self.subsession.round_number <= Constants.num_rounds / 2:
                p.bid_paid = 0


class Vote(Page):
    def is_displayed(self):
        return self.participant.vars['alive'] == True

    form_model = 'player'
    form_fields = ['vote']

class VoteWaitPage(WaitPage):
    def is_displayed(self):
        return self.participant.vars['alive'] == True

    def after_all_players_arrive(self):
        group = self.group
        players = group.get_players()
        for p in players:
            if p.vote == "No":
                p.vote_no = 1
            else:
                p.vote_no = 0

        votes_no = [p.vote_no for p in players]

        if sum(votes_no) < Constants.q:
            group.allocation_to_1 = group.chosen_offer_to_1
            group.allocation_to_2 = group.chosen_offer_to_2
            group.allocation_to_3 = group.chosen_offer_to_3

            for p in players:
                p.participant.vars['agreement'] = 'Yes'
                if p.id_in_group==1:
                    p.payoff = group.allocation_to_1 + group.auc_round*(group.auc_endowment - p.bid_paid)
                elif p.id_in_group==2:
                    p.payoff = group.allocation_to_2 + group.auc_round*(group.auc_endowment - p.bid_paid)
                else:
                    p.payoff = group.allocation_to_3 + group.auc_round*(group.auc_endowment - p.bid_paid)

        else:
            group.allocation_to_1 = 0
            group.allocation_to_2 = 0
            group.allocation_to_3 = 0

            for p in players:
                p.participant.vars['agreement'] = 'No'
                if p.id_in_group == 1:
                    p.payoff = group.allocation_to_1
                elif p.id_in_group == 2:
                    p.payoff = group.allocation_to_2
                else:
                    p.payoff = group.allocation_to_3

class Results(Page):
    def is_displayed(self):
        return self.participant.vars['alive'] == True
    timeout_seconds = 30

    def vars_for_template(self):
        return {
            'vote1': self.group.get_player_by_id(1).vote,
            'vote2': self.group.get_player_by_id(2).vote,
            'vote3': self.group.get_player_by_id(3).vote,
            'agreement': self.participant.vars['agreement']
        }

    def before_next_page(self):
        if self.participant.vars['agreement'] == 'Yes':
            self.participant.vars['mute'] = True
        else:
            if Constants.automation == 1 :
                group = self.group
                players = group.get_players()
                if group.proposer_2 == 1:
                    group.allocation_to_1_2 = Constants.budget
                    group.allocation_to_2_2 = 0
                    group.allocation_to_3_2 = 0
                elif group.proposer_2 == 2:
                    group.allocation_to_1_2 = 0
                    group.allocation_to_2_2 = Constants.budget
                    group.allocation_to_3_2 = 0
                else:
                    group.allocation_to_1_2 = 0
                    group.allocation_to_2_2 = 0
                    group.allocation_to_3_2 = Constants.budget

                for p in players:
                    if p.id_in_group == 1:
                        p.payoff = group.allocation_to_1_2 + group.auc_round*(group.auc_endowment - p.bid_paid)
                    elif p.id_in_group == 2:
                        p.payoff = group.allocation_to_2_2 + group.auc_round*(group.auc_endowment - p.bid_paid)
                    else:
                        p.payoff = group.allocation_to_3_2 + group.auc_round*(group.auc_endowment - p.bid_paid)


class Automation(Page):
    def is_displayed(self):
        return self.participant.vars['alive'] == True and self.participant.vars['mute']  == False and Constants.automation==1

class ResultsWaitPage(WaitPage):
    wait_for_all_groups = True

class ResultsSummary(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        return dict(
            total_payoff= sum([p.payoff * p.paying_round_indicator for p in self.player.in_all_rounds()])+ self.session.config['participation_fee'],
            paying_round=self.session.vars['paying_round'],
            participation_fee=self.session.config['participation_fee'],
            player_in_all_rounds=self.player.in_all_rounds()
        )

page_sequence = [
    Auction,
    AuctionWaitPage,
    AuctionResult,
    Proposal,
    ProposalWaitPage,
    Vote,
    VoteWaitPage,
    Results,
    ResultsWaitPage,
    Automation,
    ResultsSummary
]
