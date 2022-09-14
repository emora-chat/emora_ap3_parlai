
sports_str = '{sport,sports,basketball,football,hockey,tennis,baseball,soccer,superbowl,kobe bryant}'

def add_components_to(cdf):
    cdf.controller().add_system_transition('root', 'sports_intro', '#GATE(sportsv:None) `So, `')

    #already talked about topic
    # cdf.add_system_transition('sports_intro', 'sports_topic_switch',
    #                           '#IF($sportsv=True) ``',
    #                           score=2.0)

    cdf.controller().add_system_transition('sports_intro', 'sports',
                                           '[!#SET($sportsv=True) #SetTopicSuggestion(nba) #GOAL(nba) #GSRET(sports_return)'
                                           '"<<nba>> I see. Well, I find sports so exciting, but I have encountered many people who don\'t."]')
    cdf.controller().add_user_transition('sports', 'sports', '#CheckExternalComp(nba)', score=0.5)
    cdf.controller().add_user_transition('sports', 'move_on_request',
                                         '[{[not,{#EXP(like),#LEM(watch,play,do,participate),[#EXP(want),#EXP(talk)]}],#ONT(hate)},%s] #GCOM(nba)' % "{sport,sports,athletics}")
    cdf.controller().add_user_transition('sports', 'sports_topic_switch', '/.*/ #GCOM(nba)', score=0.1)
    cdf.controller().add_system_transition('sports_return', 'sports_topic_switch', '#GCOM(nba)', score=0.1)
    cdf.controller().update_state_settings('sports_topic_switch', system_multi_hop=True)
    cdf.controller().add_system_transition('sports', 'sports',
                                           '[!#SET($sportsv=True) #SetTopicSuggestion(nba) #GSRET(sports_return)'
                                           '"<<nba>> I see. Well, I find sports so exciting, but I have encountered many people who don\'t."]',
                                           score=0.5)

    cdf.controller().update_state_settings('sports_intro', system_multi_hop=True)
    cdf.controller().update_state_settings('sports', system_multi_hop=False, user_multi_hop=False)

    # if all planned transitions are used
    cdf.controller().add_system_transition('sports_topic_switch', 'intermediate_topic_switch', '', score=0.0)

    add_transitions(cdf)


def add_transitions(cdf):

    cdf.add_system_transition('sports_topic_switch', 'house:start', '')

    cdf.add_system_transition('sports_topic_switch', 'worklife:start', '`You know, you seem like a pretty interesting person. `')
    cdf.add_system_transition('sports_topic_switch', 'worklife:start->worklife:remember_is_employed_open', '', score=9.0)
    cdf.add_system_transition('sports_topic_switch', 'worklife:start->worklife:like_job_answer', '', score=10.0)

    cdf.add_system_transition('sports_topic_switch', 'school_new:start', '`Hey by the way, `', score=2.0)
    cdf.add_system_transition('sports_topic_switch', 'sibling:start', '`You know, I can\'t put my finger on why, but you kind of seem like you have a sister.`')

    cdf.add_system_transition('sports_topic_switch', 'relationships:dating', '')
    cdf.add_system_transition('sports_topic_switch', 'relationships:dating->relationships:relationship_length', '', score=10.0)
    cdf.add_system_transition('sports_topic_switch', 'relationships:marriage', '')
    cdf.add_system_transition('sports_topic_switch', 'relationships:marriage->relationships:how_long_married', '', score=10.0)

    cdf.add_system_transition('sports_topic_switch', 'baby:start', '')
    cdf.add_system_transition('sports_topic_switch', 'baby:start->baby:asked_kids_age', '', score=10.0)

    cdf.add_system_transition('sports_topic_switch', 'hobby:start', '')
    cdf.add_system_transition('sports_topic_switch', 'hobby:today_flow', '')

    cdf.add_system_transition('sports_topic_switch', 'cv_final:start', '')

    cdf.add_system_transition('sports_topic_switch', 'movies_return:start', '', score=15.0)
    cdf.add_system_transition('sports_topic_switch', 'pets_return:start', '', score=15.0)
    cdf.add_system_transition('sports_topic_switch', 'baby:returning', '', score=15.0)
    cdf.add_system_transition('sports_topic_switch', 'relationships:returning', '', score=15.0)
    cdf.add_system_transition('sports_topic_switch', 'school_new:returning', '', score=15.0)
    cdf.add_system_transition('sports_topic_switch', 'worklife:returning', '', score=15.0)

    # SPORTS -> TELEPORTATION

    cdf.add_system_transition('sports_topic_switch', 'sports_to_teleportation', '#GATE(teleportationv:None)')
    cdf.controller().update_state_settings('sports_to_teleportation', system_multi_hop=True)
    cdf.add_system_transition('sports_to_teleportation', 'ask_sports_teleportation',
                              '"You know, I have heard that high school sports sometimes require teams to travel like two hours away or even more, which is a lot of time to just play like a few games. Do you find travelling long distances tiring?"')
    cdf.add_user_transition('ask_sports_teleportation', 'yes_sports_teleportation',
                            '[{#AGREE, probably, [#NOT(not,dont), likely]}]')
    cdf.add_user_transition('ask_sports_teleportation', 'no_sports_teleportation',
                            '[{#DISAGREE,[{dont,not},{really,likely}]}]')
    cdf.controller().set_error_successor('ask_sports_teleportation', 'unknown_sports_teleportation')
    cdf.add_system_transition('yes_sports_teleportation', 'teleportation:start',
                              '[!#SET($teleportationv=True) "Yeah, this may seem kind of silly and crazy but I cannot help but think something like teleportation would come in handy for cases like this. "]')
    cdf.add_system_transition('no_sports_teleportation', 'teleportation:start',
                              '[!#SET($teleportationv=True) "Really? Well, I am glad it does not bother you so much. For me, I think it would be helpful and it reminds of the idea of teleportation for sure. "]')
    cdf.add_system_transition('unknown_sports_teleportation', 'teleportation:start',
                              '[!#SET($teleportationv=True) "Yeah, I see that. For me, I think it would be helpful to get somewhere instantly and it makes me think of the crazy idea of teleportation. "]')
    cdf.controller().update_state_settings('teleportation:start', system_multi_hop=True)

    # SPORTS -> PET

    cdf.add_system_transition('sports_topic_switch', 'sports_to_pet', '#GATE(petv:None)')
    cdf.controller().update_state_settings('sports_to_pet', system_multi_hop=True)
    cdf.add_system_transition('sports_to_pet', 'ask_sports_pet',
                              '"I heard that some sporting events let pets attend. Many professional baseball games welcome dog owners and their dogs at Bark in the Park events during the regular season. Do you think this is a good idea?"')
    cdf.add_user_transition('ask_sports_pet', 'yes_sports_pet',
                            '[{#AGREE, probably, [#NOT(not,dont), likely]}]')
    cdf.add_user_transition('ask_sports_pet', 'no_sports_pet',
                            '[{#DISAGREE,[{dont,not},{really,likely,want,like}], distracting,distraction,messy,disruptive,disruption,annoying,loud,annoy,noisy}]')
    cdf.controller().set_error_successor('ask_sports_pet', 'unknown_sports_pet')
    cdf.add_system_transition('yes_sports_pet', 'pet_intro',
                              '"Me too. Some people may find it annoying, but I think it is good to socialize your dogs while doing something fun yourself. "')
    cdf.add_system_transition('no_sports_pet', 'pet_intro',
                              '"Yeah, I think a lot of people would agree with you on that. It is probably too disruptive and noisy for others who want to watch the games. "')
    cdf.add_system_transition('unknown_sports_pet', 'pet_intro',
                              '"Yeah, maybe. I think it is hard to say. Some people may find it annoying, but others would enjoy taking their dogs out. "')

    # SPORTS -> VIRTUAL REALITY

    cdf.add_system_transition('sports_topic_switch', 'sports_to_vr', '#GATE(virtual_realityv:None)')
    cdf.controller().update_state_settings('sports_to_vr', system_multi_hop=True)
    cdf.add_system_transition('sports_to_vr', 'ask_sports_vr',
                              '"Most people focus on video games when talking about virtual reality right now, but I think it would be cool to be able to watch a live sports game using it. Do you think we will be able to watch sports games in realtime using V R soon?"')
    cdf.add_user_transition('ask_sports_vr', 'yes_sports_vr',
                            '[{#AGREE, probably, [#NOT(not,dont), likely]}]')
    cdf.add_user_transition('ask_sports_vr', 'no_sports_vr',
                            '[{#DISAGREE,[{dont,not},{really,likely}]}]')
    cdf.controller().set_error_successor('ask_sports_vr', 'unknown_sports_vr')
    cdf.add_user_transition('ask_sports_vr', 'dislike_sports',
                            '[{hate,dislike,[{dont,not},{like,want,wish,love,need,care}]}, {sport,sports,athletics,athletic,athlete,games}]')
    cdf.add_system_transition('yes_sports_vr', 'virtual_reality_intro',
                              '"I really hope so too. "')
    cdf.add_system_transition('no_sports_vr', 'virtual_reality_intro',
                              '"Yeah, There are still many technical challenges to it. "')
    cdf.add_system_transition('unknown_sports_vr', 'virtual_reality_intro',
                              '"I see. So, "')

    # SPORTS -> MOVIES

    cdf.add_system_transition('sports_topic_switch', 'sports_to_movies', '#GATE(moviesv:None)')
    cdf.controller().update_state_settings('sports_to_movies', system_multi_hop=True)
    cdf.add_system_transition('sports_to_movies', 'ask_sports_movies',
                              '"It seems like movies about sports teams and players that beat the odds have been pretty popular in the past. Do you remember seeing any movies like this?"')
    cdf.add_user_transition('ask_sports_movies', 'yes_sports_movies',
                            '[{#AGREE, probably, [#NOT(not,dont), likely]}]')
    cdf.add_user_transition('ask_sports_movies', 'no_sports_movies',
                            '[{#DISAGREE,[{dont,not},{really,likely}]}]')
    cdf.controller().set_error_successor('ask_sports_movies', 'unknown_sports_movies')
    cdf.add_system_transition('yes_sports_movies', 'movies_intro',
                              '"Yeah, I thought as much. It seems like almost everyone has seen at least one sports movie."')
    cdf.add_system_transition('no_sports_movies', 'movies_intro', '"I see. Sports movies aren\'t for everyone. "')
    cdf.add_system_transition('unknown_sports_movies', 'movies_intro', '"Gotcha. Well, anyways, "')

    # SPORTS -> MUSIC

    cdf.add_system_transition('sports_topic_switch', 'sports_to_music', '#GATE(musicv:None)')
    cdf.controller().update_state_settings('sports_to_music', system_multi_hop=True)
    cdf.add_system_transition('sports_to_music', 'ask_sports_music',
                              '"Every time my friends hear the song we will rock you by queen, they are reminded of high school basketball games. Do you have any songs that remind you of any sporting events?"')
    cdf.add_user_transition('ask_sports_music', 'yes_sports_music',
                            '[{#AGREE, probably, [#NOT(not,dont), likely]}]')
    cdf.add_user_transition('ask_sports_music', 'no_sports_music',
                            '[{#DISAGREE,[{dont,not},{really,likely}]}]')
    cdf.controller().set_error_successor('ask_sports_music', 'unknown_sports_music')
    cdf.add_system_transition('yes_sports_music', 'music_intro', '"Yeah, I feel like everyone has one. "')
    cdf.add_system_transition('no_sports_music', 'music_intro',
                              '"Lucky, it is kind of annoying to have those overplayed songs. "')
    cdf.add_system_transition('unknown_sports_music', 'music_intro', '"I see. Anyways, "')