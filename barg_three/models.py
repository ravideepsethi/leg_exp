from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import numpy as np
#import random
#from otree_tools.models.fields import ListField

author = 'Salvatore Nunnari, Bocconi University'

doc = """
Multilateral alternating-offer legislative bargaining with three-players as in the model by Baron, David and John Ferejon 1989 
and in the experiments by Frechette, Guillaume, John Kagel and Steve Lehrer 2003 (closed rule without veto players) 
or by Kagel, John, Hankyoung Sung and Eyal Winter 2010 (closed rule with a veto player).
This app implements a single instance of a (potentially infinitely repeated) bargaining game (i.e., a single "match").
"""

class Constants(BaseConstants):
    ###IMPORTANT: CHANGE THE VARIABLES HERE IN EACH SESSION###
    treatment = 1
    # 1; baseline treatment 2; stage 2 probability modification 3; stage 2 automation
    ##########################################################
    if treatment == 1: # Baseline treatment
        power_modification = 0  # 1 if the stage 2 agenda setting power distribution is modified; 0 if not modified
        automation = 0  # 1 if stage 2 is automated; 0 if not automated
    elif treatment == 2: # stage 2 agenda setting power modified
        power_modification = 1  # 1 if the stage 2 agenda setting power distribution is modified; 0 if not modified
        automation = 0  # 1 if stage 2 is automated; 0 if not automated
    elif treatment == 3: # stage 2 automated
        power_modification = 0  # 1 if the stage 2 agenda setting power distribution is modified; 0 if not modified
        automation = 1  # 1 if stage 2 is automated; 0 if not automated

    name_in_url = 'barg_three'
    players_per_group = 3
    num_rounds = 2
    num_stages = 2
    budget = 42 # number of tokens to divide among committee members
    auc_endowment = 60 # endowment for the auction
    veto = False  # set to "True" for game with one veto player, set to "False" for game without veto players
    q = 2  # number of positive votes required for passage (if veto = True, this includes the veto player)
    rec_prob_1 = 0.36 # recognition probability of group member 1; if veto = True, this is the veto player
    rec_prob_2 = 0.33 # recognition probability of group member 2
    rec_prob_3 = 0.31 # recognition probability of group member 3
    if power_modification == 0 :
        rec_prob_1_2nd = 0.36  # recognition probability of group member 1; if veto = True, this is the veto player
        rec_prob_2_2nd = 0.33  # recognition probability of group member 2
        rec_prob_3_2nd = 0.31  # recognition probability of group member 3
    elif power_modification == 1 :
        rec_prob_1_2nd = 0.70  # recognition probability of group member 1; if veto = True, this is the veto player
        rec_prob_2_2nd = 0.26  # recognition probability of group member 2
        rec_prob_3_2nd = 0.04  # recognition probability of group member 3
    rec_perc_1 = round(rec_prob_1 *100)
    rec_perc_2 = round(rec_prob_2 *100)
    rec_perc_3 = round(rec_prob_3 *100)
    rec_perc_1_2nd = round(rec_prob_1_2nd *100)
    rec_perc_2_2nd = round(rec_prob_2_2nd * 100)
    rec_perc_3_2nd = round(rec_prob_3_2nd * 100)
    discount = 1 # only used in end-of-round template

class Subsession(BaseSubsession):
    def creating_session(self):
        import random
        print('in creating_session')
        if self.round_number == 1:
            paying_round = random.randint(1, Constants.num_rounds)
            self.session.vars['paying_round'] = paying_round
            print('set the paying round to', paying_round)

        self.group_randomly()
        groups = self.get_groups()

        for p in self.get_players():
            p.participant.vars['alive'] = True
            p.participant.vars['agreement'] = 'No'
            p.participant.vars['mute'] = False
            p.participant.vars['active'] = True

        for g in groups:
            # determine the person selected to pay in role assignment
            rand_selected = np.random.random()
            if rand_selected <= 1 / 3:
                g.selected1 = 1
                g.selected2 = 0
                g.selected3 = 0
            elif rand_selected > 1 / 3 and rand_selected <= 2 / 3:
                g.selected1 = 0
                g.selected2 = 1
                g.selected3 = 0
            else :
                g.selected1 = 0
                g.selected2 = 0
                g.selected3 = 1

            # determine the color assignment
            rand_color = np.random.random()
            if rand_color <= 1 / 6:
                g.color1 = "Orange"
                g.color2 = "Green"
                g.color3 = "Purple"
            elif rand_color > 1 / 6 and rand_color <= 2 / 6:
                g.color1 = "Orange"
                g.color2 = "Purple"
                g.color3 = "Green"
            elif rand_color > 2 / 6 and rand_color <= 3 / 6:
                g.color1 = "Green"
                g.color2 = "Orange"
                g.color3 = "Purple"
            elif rand_color > 3 / 6 and rand_color <= 4 / 6:
                g.color1 = "Green"
                g.color2 = "Purple"
                g.color3 = "Orange"
            elif rand_color > 4 / 6 and rand_color <= 5 / 6:
                g.color1 = "Purple"
                g.color2 = "Orange"
                g.color3 = "Green"
            else:
                g.color1 = "Purple"
                g.color2 = "Green"
                g.color3 = "Orange"

            g.get_player_by_id(1).color = g.color1
            g.get_player_by_id(2).color = g.color2
            g.get_player_by_id(3).color = g.color3

            g.budget = Constants.budget

            # determine identity of proposer in this round (stage 1 and then stage 2)
            rand_num_prop = np.random.random()
            if rand_num_prop <= Constants.rec_prob_1:
                g.proposer = 1
            elif rand_num_prop > Constants.rec_prob_1 and rand_num_prop <= Constants.rec_prob_1 + Constants.rec_prob_2:
                g.proposer = 2
            else:
                g.proposer = 3
            # g.proposer = np.random.randint(1, 4) # alternative way to randomly determine proposer with even probabilities

            rand_num_prop_2 = np.random.random()
            if rand_num_prop_2 <= Constants.rec_prob_1_2nd :
                g.proposer_2 = 1
            elif rand_num_prop_2 > Constants.rec_prob_1_2nd and rand_num_prop_2 <= Constants.rec_prob_1_2nd  + Constants.rec_prob_2_2nd :
                g.proposer_2 = 2
            else:
                g.proposer_2 = 3
            # g.proposer = np.random.randint(1, 4) # alternative way to randomly determine proposer with even probabilities

            # color of the proposer
            if g.proposer == 1:
                g.color_prop = g.color1
            elif g.proposer == 2:
                g.color_prop = g.color2
            else:
                g.color_prop = g.color3

            if g.proposer_2 == 1:
                g.color_prop_2 = g.color1
            elif g.proposer_2 == 2:
                g.color_prop_2 = g.color2
            else:
                g.color_prop_2 = g.color3

            if self.round_number > Constants.num_rounds/2:
                g.auc_round = 1
            else:
                g.auc_round = 0

            g.auc_endowment = Constants.auc_endowment

        for p in self.get_players():
            if self.round_number == self.session.vars['paying_round']:
                p.paying_round_indicator = 1
            else:
                p.paying_round_indicator = 0

class Group(BaseGroup):
    budget = models.FloatField()
    rand_selected = models.FloatField()
    rand_role = models.FloatField()
    rand_num_prop = models.FloatField()
    rand_num_prop_2 = models.FloatField()
    proposer = models.IntegerField()
    proposer_2 = models.IntegerField()
    selected1 = models.IntegerField()
    selected2 = models.IntegerField()
    selected3 = models.IntegerField()
    selected_prob_role1 = models.FloatField()
    selected_prob_role2 = models.FloatField()
    selected_prob_role3 = models.FloatField()
    color1 = models.StringField()
    color2 = models.StringField()
    color3 = models.StringField()
    color_prop = models.StringField()
    chosen_offer_to_1 = models.FloatField()
    chosen_offer_to_2 = models.FloatField()
    chosen_offer_to_3 = models.FloatField()
    allocation_to_1 = models.FloatField()
    allocation_to_2 = models.FloatField()
    allocation_to_3 = models.FloatField()
    color_prop_2 = models.StringField()
    chosen_offer_to_1_2 = models.FloatField()
    chosen_offer_to_2_2 = models.FloatField()
    chosen_offer_to_3_2 = models.FloatField()
    allocation_to_1_2 = models.FloatField()
    allocation_to_2_2 = models.FloatField()
    allocation_to_3_2 = models.FloatField()
    auc_round = models.FloatField()
    auc_endowment = models.FloatField()
    bid_1 = models.FloatField()
    bid_2 = models.FloatField()
    bid_3 = models.FloatField()
    bid_paid_1 = models.FloatField()
    bid_paid_2 = models.FloatField()
    bid_paid_3 = models.FloatField()
    surplus_1 = models.FloatField()
    surplus_2 = models.FloatField()
    surplus_3 = models.FloatField()
    paying_round_indicator = models.FloatField()

class Player(BasePlayer):
    bid_role = models.IntegerField(
        widget=widgets.RadioSelectHorizontal
    )

    def bid_role_choices(self):
        choices = [[1, self.group.color1], [1,self.group.color2], [3, self.group.color3]]
        return choices

    bid = models.FloatField(
        max=Constants.auc_endowment,
        min=0,
        initial=None,
        widget=widgets.Slider(attrs={'step': '0.01'}, show_value=False)
    )

    def bid_error_message(self, value):
        print("bid value " + str(value))
        if value == None:
            return "Please select a bid amount on the slider."

    bid_paid = models.FloatField(
        max=Constants.auc_endowment,
        min=0
    )

    prob_role1 = models.FloatField(
        max=1,
        min=0
    )
    prob_role2 = models.FloatField(
        max=1,
        min=0
    )
    prob_role3 = models.FloatField(
        max=1,
        min=0
    )

    offer_to_1 = models.FloatField(
        max=Constants.budget,
        min=0
    )
    offer_to_2 = models.FloatField(
        max=Constants.budget,
        min=0
    )
    offer_to_3 = models.FloatField(
        max=Constants.budget,
        min=0
    )
    offer_to_1_2 = models.FloatField(
        max=Constants.budget,
        min=0
    )
    offer_to_2_2 = models.FloatField(
        max=Constants.budget,
        min=0
    )
    offer_to_3_2 = models.FloatField(
        max=Constants.budget,
        min=0
    )

    vote = models.CharField(
        choices=['Yes', 'No'],
        verbose_name='What is your vote?',
        widget=widgets.RadioSelect
    )

    vote_no = models.IntegerField()
    
    vote_2 = models.CharField(
        choices=['Yes', 'No'],
        verbose_name='What is your vote?',
        widget=widgets.RadioSelect
    )

    vote_no_2 = models.IntegerField()

    paying_round = models.IntegerField()
    paying_round_indicator = models.IntegerField()
    participation_fee = models.FloatField()
    total_payoff = models.FloatField()

    def role(self):
        if self.id_in_group == 1:
            return 'Veto'
        else:
            return 'Non-Veto'

    def color(self):
        if self.id_in_group == 1:
            return self.group.color1
        elif self.id_in_group == 2:
            return self.group.color2
        else:
            return self.group.color3

    def selected(self):
        if self.id_in_group == 1:
            return self.group.selected1
        elif self.id_in_group == 2:
            return self.group.selected2
        else:
            return self.group.selected3