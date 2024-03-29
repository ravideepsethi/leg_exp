# Generated by Django 2.2.4 on 2019-11-11 15:21

from django.db import migrations, models
import django.db.models.deletion
import otree.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('otree', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_in_subsession', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('budget', otree.db.models.FloatField(null=True)),
                ('rand_selected', otree.db.models.FloatField(null=True)),
                ('rand_role', otree.db.models.FloatField(null=True)),
                ('rand_num_prop', otree.db.models.FloatField(null=True)),
                ('rand_num_prop_2', otree.db.models.FloatField(null=True)),
                ('proposer', otree.db.models.IntegerField(null=True)),
                ('proposer_2', otree.db.models.IntegerField(null=True)),
                ('selected1', otree.db.models.IntegerField(null=True)),
                ('selected2', otree.db.models.IntegerField(null=True)),
                ('selected3', otree.db.models.IntegerField(null=True)),
                ('selected_prob_role1', otree.db.models.FloatField(null=True)),
                ('selected_prob_role2', otree.db.models.FloatField(null=True)),
                ('selected_prob_role3', otree.db.models.FloatField(null=True)),
                ('color1', otree.db.models.StringField(max_length=10000, null=True)),
                ('color2', otree.db.models.StringField(max_length=10000, null=True)),
                ('color3', otree.db.models.StringField(max_length=10000, null=True)),
                ('color_prop', otree.db.models.StringField(max_length=10000, null=True)),
                ('chosen_offer_to_1', otree.db.models.FloatField(null=True)),
                ('chosen_offer_to_2', otree.db.models.FloatField(null=True)),
                ('chosen_offer_to_3', otree.db.models.FloatField(null=True)),
                ('allocation_to_1', otree.db.models.FloatField(null=True)),
                ('allocation_to_2', otree.db.models.FloatField(null=True)),
                ('allocation_to_3', otree.db.models.FloatField(null=True)),
                ('color_prop_2', otree.db.models.StringField(max_length=10000, null=True)),
                ('chosen_offer_to_1_2', otree.db.models.FloatField(null=True)),
                ('chosen_offer_to_2_2', otree.db.models.FloatField(null=True)),
                ('chosen_offer_to_3_2', otree.db.models.FloatField(null=True)),
                ('allocation_to_1_2', otree.db.models.FloatField(null=True)),
                ('allocation_to_2_2', otree.db.models.FloatField(null=True)),
                ('allocation_to_3_2', otree.db.models.FloatField(null=True)),
                ('auc_round', otree.db.models.FloatField(null=True)),
                ('auc_endowment', otree.db.models.FloatField(null=True)),
                ('bid_1', otree.db.models.FloatField(null=True)),
                ('bid_2', otree.db.models.FloatField(null=True)),
                ('bid_3', otree.db.models.FloatField(null=True)),
                ('bid_paid_1', otree.db.models.FloatField(null=True)),
                ('bid_paid_2', otree.db.models.FloatField(null=True)),
                ('bid_paid_3', otree.db.models.FloatField(null=True)),
                ('surplus_1', otree.db.models.FloatField(null=True)),
                ('surplus_2', otree.db.models.FloatField(null=True)),
                ('surplus_3', otree.db.models.FloatField(null=True)),
                ('paying_round_indicator', otree.db.models.FloatField(null=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='barg_three_group', to='otree.Session')),
            ],
            options={
                'db_table': 'barg_three_group',
            },
        ),
        migrations.CreateModel(
            name='Subsession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('session', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='barg_three_subsession', to='otree.Session')),
            ],
            options={
                'db_table': 'barg_three_subsession',
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_in_group', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('_payoff', otree.db.models.CurrencyField(default=0, null=True)),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('_gbat_arrived', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
                ('_gbat_grouped', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
                ('bid_role', otree.db.models.IntegerField(choices=[(1, 1), (2, 2), (3, 3)], null=True)),
                ('bid', otree.db.models.FloatField(default=0.5, null=True)),
                ('bid_paid', otree.db.models.FloatField(null=True)),
                ('prob_role1', otree.db.models.FloatField(null=True)),
                ('prob_role2', otree.db.models.FloatField(null=True)),
                ('prob_role3', otree.db.models.FloatField(null=True)),
                ('offer_to_1', otree.db.models.FloatField(null=True)),
                ('offer_to_2', otree.db.models.FloatField(null=True)),
                ('offer_to_3', otree.db.models.FloatField(null=True)),
                ('offer_to_1_2', otree.db.models.FloatField(null=True)),
                ('offer_to_2_2', otree.db.models.FloatField(null=True)),
                ('offer_to_3_2', otree.db.models.FloatField(null=True)),
                ('vote', otree.db.models.StringField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10000, null=True, verbose_name='What is your vote?')),
                ('vote_no', otree.db.models.IntegerField(null=True)),
                ('vote_2', otree.db.models.StringField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10000, null=True, verbose_name='What is your vote?')),
                ('vote_no_2', otree.db.models.IntegerField(null=True)),
                ('paying_round', otree.db.models.IntegerField(null=True)),
                ('paying_round_indicator', otree.db.models.IntegerField(null=True)),
                ('participation_fee', otree.db.models.FloatField(null=True)),
                ('total_payoff', otree.db.models.FloatField(null=True)),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='barg_three.Group')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='barg_three_player', to='otree.Participant')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='barg_three_player', to='otree.Session')),
                ('subsession', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='barg_three.Subsession')),
            ],
            options={
                'db_table': 'barg_three_player',
            },
        ),
        migrations.AddField(
            model_name='group',
            name='subsession',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='barg_three.Subsession'),
        ),
    ]
