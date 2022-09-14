
from emora._coronavirus.covid19 import df as coronavirus, State as coronavirus_states
from emora._coronavirus.corona_virus import cv as coronavirus_op

coronavirus_str = '{coronavirus,corona virus,' \
                      'covid,' \
                      '[{china,chinese,wuhan,global,widespread,pandemic,epidemic},{virus,disease,illness}],' \
                      '[{virus,disease,illness},{china,chinese,wuhan,global,widespread,pandemic,epidemic}]}'


def add_components_to(cdf):
    # cdf.add_component(coronavirus, 'coronavirus')
    # # cdf.add_system_transition('get_to_know_intro', 'coronavirus_intro', '#GATE(coronavirusv:None)')
    # cdf.add_system_transition('coronavirus_intro', ('coronavirus', coronavirus_states.START),
    #                           '#SET($coronavirusv=True)')
    # cdf.controller().update_state_settings('coronavirus_intro', system_multi_hop=True)
    # cdf.controller().update_state_settings(('coronavirus', coronavirus_states.START), system_multi_hop=True)
    #
    # coronavirus.add_system_transition(coronavirus_states.ERROR, ('SYSTEM', 'from_coronavirus'), '')
    # coronavirus.update_state_settings(('SYSTEM', 'from_coronavirus'), system_multi_hop=True)
    # cdf.add_system_transition('from_coronavirus', 'activity_intro',
    #                           '[!#GATE(activityv:None) "Ok, well, I know that life might seem a little weird right now, '
    #                           'but we should just do the best that we can. So, "]', score=2.0)
    # cdf.add_system_transition('from_coronavirus', 'end_coronavirus', '')
    # cdf.controller().update_state_settings('end_coronavirus', system_multi_hop=True)

    ######

    # cdf.add_component(coronavirus_op, 'coronavirus_op')
    # # cdf.add_system_transition('get_to_know_intro', 'coronavirus_op_intro', '#GATE(coronavirusopv:None)')
    # cdf.add_system_transition('coronavirus_op_intro', ('coronavirus_op', 'sr'), '#SET($coronavirusopv=True)')
    # cdf.controller().update_state_settings('coronavirus_op_intro', system_multi_hop=True)
    # cdf.controller().update_state_settings(('coronavirus_op', 'sr'), system_multi_hop=True)
    #
    # coronavirus_op.add_system_transition('sr', ('SYSTEM', 'from_coronavirus_op'), '#SET($focus=None)', score=0.0)
    # coronavirus_op.update_state_settings(('SYSTEM', 'from_coronavirus_op'), system_multi_hop=True)
    # cdf.add_system_transition('from_coronavirus_op', 'activity_intro',
    #                           '[!#GATE(activityv:None) "I know that life might seem a little weird right now, '
    #                           'but we should just do the best that we can. So, "]', score=2.0)
    # cdf.add_system_transition('from_coronavirus_op', 'end_coronavirus_op', '')
    # cdf.controller().update_state_settings('end_coronavirus_op', system_multi_hop=True)

    # if all planned transitions are used
    # cdf.controller().add_system_transition('end_coronavirus_op', 'intermediate_topic_switch', '', score=0.0)

    # add_transitions(cdf)

def add_transitions(cdf):

    # CORONAVIRUS --> VIRTUAL REALITY

    cdf.add_system_transition('end_coronavirus', 'vr_effect',
                              [
                                  '"Yeah, I really cannot believe so many people are working from home these days because of the coronavirus. Is this something happening a lot in the area around you?"',
                                  '"It is unprecedented how many universities have cancelled in-class sessions. Do you know a lot of other people affected like this?"'
                              ])
    cdf.add_user_transition('vr_effect', 'yes_vr_effect',
                            '[{#ONT(often_qualifier,sometimes_qualifier), #AGREE}]')
    cdf.add_user_transition('vr_effect', 'no_vr_effect',
                            '[{#DISAGREE, [not,{really,all,much}]}]')
    cdf.controller().set_error_successor('vr_effect', 'unknown_vr_effect')

    cdf.add_system_transition('unknown_vr_effect', 'ask_virtual_env',
                              [
                                  '"I see. '
                                  'Wouldn\'t it be great if we could recreate work and school environments in a virtual setting for situations like this?"',
                              ])
    cdf.add_system_transition('yes_vr_effect', 'ask_virtual_env',
                              [
                                  '"Wouldn\'t it be great if we could recreate work and school environments in a virtual setting for situations like this?"',
                                  '"Do you think it would be useful to make virtual environments for educational and professional settings in cases like this?"'
                              ])
    cdf.add_system_transition('no_vr_effect', 'ask_virtual_env',
                              [
                                  '"I\'m glad it does not seem to be affecting you as much as others. '
                                  'Wouldn\'t it be great if we could recreate work and school environments in a virtual setting for situations like this?"',
                                  '"You are lucky that it has not been so bad for you at the moment. '
                                  'Do you think it would be useful to make virtual environments for educational and professional settings in cases like this?"'
                              ])

    cdf.add_user_transition('ask_virtual_env', 'yes_virtual_env',
                            '[{#ONT(often_qualifier,sometimes_qualifier), #AGREE, [#NOT(not), {good,helpful,useful}]}]')
    cdf.add_user_transition('ask_virtual_env', 'no_virtual_env',
                            '[{#DISAGREE, [not,{really,all,much}]}]')
    cdf.controller().set_error_successor('ask_virtual_env', 'no_virtual_env')

    cdf.add_system_transition('yes_virtual_env', 'virtual_reality_intro', '"Me too! Actually, "')
    cdf.add_system_transition('no_virtual_env', 'virtual_reality_intro',
                              '"I think it could be helpful if done correctly. Actually, "')

    cdf.add_system_transition('end_coronavirus', 'ask_activity',
                              [
                                  '"So, now that a lot of people are spending so much time at home, what do you like to do to enjoy yourself?"',
                                  '"So, since everyone is constrained to being home most of the time, what are you doing to keep yourself busy?"'
                              ])

    cdf.add_user_transition('ask_activity', 'dont_know_activity', '#IDK')
    cdf.controller().set_error_successor('ask_activity', 'unknown_activity')

    cdf.add_system_transition('dont_know_activity', 'pet_intro',
                              '"Yeah, it can be hard to figure out what to do. I think people should take the time to find new hobbies.'
                              ' But I know a lot of people are spending it playing with their pets, though, too. "')
    cdf.add_system_transition('unknown_activity', 'pet_intro',
                              '"Yeah, I think people should take the time to catch up on work and hobbies they have forgotten.'
                              ' A lot of people are spending it playing with their pets, though, too. "')

    # CORONAVIRUS --> SPORTS

    cdf.add_system_transition('end_coronavirus', 'sports_effect',
                              [
                                  '"I still cannot believe how many sports games are being affected by the virus. '
                                  'Would you still be willing to go watch sports games in a time like this?"',
                                  '"I cannot wrap my head around the fact that even professional sports are being impacted by this virus. '
                                  'Do you think they should still have the games happen, instead of shutting them down?"'
                              ])
    cdf.add_user_transition('sports_effect', 'yes_sports_effect',
                            '[{#ONT(often_qualifier,sometimes_qualifier), #AGREE}]')
    cdf.add_user_transition('sports_effect', 'no_sports_effect',
                            '[{#DISAGREE, [not,{really,all,much}]}]')
    cdf.controller().set_error_successor('sports_effect', 'unknown_sports_effects')

    cdf.add_system_transition('yes_sports_effect', 'sports_intro',
                              [
                                  '"Well, you must really like sports, then. Actually, I really like sports too! "'
                              ])
    cdf.add_system_transition('no_sports_effect', 'sports_intro',
                              [
                                  '"Yeah, I think it is pretty risky to have such large and crowded events at a time like this. But, "'
                              ])
    cdf.add_system_transition('unknown_sports_effects', 'sports_intro',
                              [
                                  '"Yeah, maybe. You would have to really like sports to want the games to keep happening, I think! "'
                              ])

    #####

    cdf.add_system_transition('end_coronavirus_op', 'yes_vr_effect', '#GATE(virtual_realityv:None)')
    cdf.controller().update_state_settings('yes_vr_effect', system_multi_hop=True)

    cdf.add_system_transition('end_coronavirus_op', 'ask_activity', '[!#GATE(petv:None) '
                                                                    '{"So, if you were to stay home, what would you do to stay busy?",'
                                                                    '"So, what do you recommend for people to do to keep busy when they are stuck at home?"}'
                                                                    ']')

    cdf.add_system_transition('end_coronavirus_op', 'sports_effect',
                              '[! #GATE(sportsv:None) '
                              '"I still cannot believe how many sports games are being affected by the virus. '
                              'Would you still be willing to go watch sports games in a time like this?"]'
                              )