
def add_components_to(cdf):
    cdf.add_system_transition('root', 'teleportation_intro', '#GATE(teleportationv:None)', score=0.95)
    cdf.add_system_transition('teleportation_intro', 'teleportation:cold_start', '#SET($teleportationv=True)')
    cdf.controller().update_state_settings('teleportation_intro', system_multi_hop=True)

    # if all planned transitions are used
    cdf.controller().add_system_transition('teleportation_topic_switch', 'intermediate_topic_switch',
                                           '[!"I have really enjoyed talking about teleportation with you. "]',
                                           score=0.0)


    add_transitions(cdf)

def add_transitions(cdf):
    cdf.add_system_transition('teleportation_topic_switch', 'house:start', '')

    cdf.add_system_transition('teleportation_topic_switch', 'worklife:start', '`You know, you seem like a pretty interesting person. `')
    cdf.add_system_transition('teleportation_topic_switch', 'worklife:start->worklife:remember_is_employed_open', '', score=9.0)
    cdf.add_system_transition('teleportation_topic_switch', 'worklife:start->worklife:like_job_answer', '', score=10.0)

    cdf.add_system_transition('teleportation_topic_switch', 'school_new:start', '`Hey by the way, `', score=2.0)
    cdf.add_system_transition('teleportation_topic_switch', 'sibling:start', '`You know, I can\'t put my finger on why, but you kind of seem like you have a sister.`')

    cdf.add_system_transition('teleportation_topic_switch', 'relationships:dating', '')
    cdf.add_system_transition('teleportation_topic_switch', 'relationships:dating->relationships:relationship_length', '', score=10.0)
    cdf.add_system_transition('teleportation_topic_switch', 'relationships:marriage', '')
    cdf.add_system_transition('teleportation_topic_switch', 'relationships:marriage->relationships:how_long_married', '', score=10.0)

    cdf.add_system_transition('teleportation_topic_switch', 'baby:start', '')
    cdf.add_system_transition('teleportation_topic_switch', 'baby:start->baby:asked_kids_age', '', score=10.0)

    cdf.add_system_transition('teleportation_topic_switch', 'hobby:start', '')
    cdf.add_system_transition('teleportation_topic_switch', 'hobby:today_flow', '')

    cdf.add_system_transition('teleportation_topic_switch', 'cv_final:start', '')

    cdf.add_system_transition('teleportation_topic_switch', 'movies_return:start', '', score=15.0)
    cdf.add_system_transition('teleportation_topic_switch', 'pets_return:start', '', score=15.0)
    cdf.add_system_transition('teleportation_topic_switch', 'baby:returning', '', score=15.0)
    cdf.add_system_transition('teleportation_topic_switch', 'relationships:returning', '', score=15.0)
    cdf.add_system_transition('teleportation_topic_switch', 'school_new:returning', '', score=15.0)
    cdf.add_system_transition('teleportation_topic_switch', 'worklife:returning', '', score=15.0)

    # TELEPORTATION -> MOVIES

    cdf.add_system_transition('teleportation_topic_switch', 'teleportation_to_movies', '#GATE(moviesv:None)')
    cdf.controller().update_state_settings('teleportation_to_movies', system_multi_hop=True)
    cdf.add_system_transition('teleportation_to_movies', 'ask_teleportation_movies',
                              '"I cannot seem to remember any movies that involve teleportation, although I know it is popular in science fiction novels. Can you think of any movies that use teleportation?"')
    cdf.add_user_transition('ask_teleportation_movies', 'yes_teleportation_movies',
                            '[{#AGREE, probably, [#NOT(not,dont), likely]}]')
    cdf.add_user_transition('ask_teleportation_movies', 'no_teleportation_movies',
                            '[{#DISAGREE,[{dont,not},{really,likely}]}]')
    cdf.controller().set_error_successor('ask_teleportation_movies', 'unknown_teleportation_movies')
    cdf.add_system_transition('yes_teleportation_movies', 'movies_intro',
                              '"You do? I will have to look into these movies then. "')
    cdf.add_system_transition('no_teleportation_movies', 'movies_intro',
                              '"Yeah, it does seem to be a mystery. "')
    cdf.add_system_transition('unknown_teleportation_movies', 'movies_intro',
                              '"Good one. I will have to remember that. "')

    # TELEPORTATION -> SPORTS

    cdf.add_system_transition('teleportation_topic_switch', 'teleportation_to_sports', '#GATE(sportsv:None)')
    cdf.controller().update_state_settings('teleportation_to_sports', system_multi_hop=True)
    cdf.add_system_transition('teleportation_to_sports', 'ask_teleportation_sports',
                              '"You know, I have heard that high school sports sometimes require teams to travel like two hours away or even more, which is a lot of time to just play like a few games. Do you find travelling long distances tiring?"')
    cdf.add_user_transition('ask_teleportation_sports', 'yes_teleportation_sports',
                            '[{#AGREE, probably, [#NOT(not,dont), likely]}]')
    cdf.add_user_transition('ask_teleportation_sports', 'no_teleportation_sports',
                            '[{#DISAGREE,[{dont,not},{really,likely}]}]')
    cdf.controller().set_error_successor('ask_teleportation_sports', 'unknown_teleportation_sports')
    cdf.add_system_transition('yes_teleportation_sports', 'sports_intro',
                              '"Yeah, I hear that from a lot of people. This is definitely one of those cases where I think something like teleportation would come in handy. "')
    cdf.add_system_transition('no_teleportation_sports', 'sports_intro',
                              '"Really? Well, I am glad it does not bother you so much. "')
    cdf.add_system_transition('unknown_teleportation_sports', 'sports_intro',
                              '"Yeah, I see that. In my opinion, I think it would be helpful to a lot of people to get somewhere instantly in cases like this. "')

    # TELEPORTATION -> MUSIC

    cdf.add_system_transition('teleportation_topic_switch', 'teleportation_to_music', '#GATE(musicv:None)')
    cdf.controller().update_state_settings('teleportation_to_music', system_multi_hop=True)
    cdf.add_system_transition('teleportation_to_music', 'ask_teleportation_music',
                              '"I like teleportation because I just really find the idea of even modern travel so time-consuming. It is so hard sometimes to go to all of the places that you want to, like if some concert is in a different state or even country. Are you annoyed by this too?"')
    cdf.add_user_transition('ask_teleportation_music', 'yes_teleportation_music',
                            '[{#AGREE, probably, [#NOT(not,dont), likely]}]')
    cdf.add_user_transition('ask_teleportation_music', 'no_teleportation_music',
                            '[{#DISAGREE,[{dont,not},{really,likely}]}]')
    cdf.controller().set_error_successor('ask_teleportation_music', 'unknown_teleportation_music')
    cdf.add_system_transition('yes_teleportation_music', 'music_intro',
                              '"Yeah, I think a lot of people are. Speaking of music concerts, "')
    cdf.add_system_transition('no_teleportation_music', 'music_intro',
                              '"Really? Well, I am glad it does not bother you so much. Speaking of music concerts, "')
    cdf.add_system_transition('unknown_teleportation_music', 'music_intro',
                              '"Sure, but for a lot of people, I think it would be helpful to get somewhere instantly. Speaking of music concerts, "')
