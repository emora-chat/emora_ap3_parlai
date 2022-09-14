
movies_str = '{movie,movies,film,films,tv,shows,television}'

def add_components_to(cdf):
    cdf.controller().add_system_transition('root', 'movies_intro',
                                           '[! #GATE(moviesv:None) #IsNotLaunchRequest '
                                           '"You know, recently I have been really interested in movies and I know a lot about them."]')

    #already talked about topic
    cdf.add_system_transition('movies_intro', 'movies_repeat_switch',
                              '#IF($moviesv=True) `Well, I know a lot of people can talk about movies forever. '
                              'I personally think that gets kinda dull after a while. `',
                              score=2.0)
    cdf.add_system_transition('movies_repeat_switch', 'movies_to_music', '`You know, ` #GATE(musicv:None)')
    cdf.add_system_transition('movies_repeat_switch', 'movies_to_sports', '`You know, ` #GATE(sportsv:None)')
    cdf.add_system_transition('movies_repeat_switch', 'movies_to_vr', '`You know, ` #GATE(virtual_realityv:None)')
    cdf.add_system_transition('movies_repeat_switch', 'movies_to_travel', '`You know, ` #GATE(travelv:None)')
    cdf.add_system_transition('movies_repeat_switch', 'movies_to_teleportation', '`You know, ` #GATE(teleportationv:None)')
    cdf.add_system_transition('movies_repeat_switch', 'movies_topic_switch', '`Anyway, `', score=0.0)
    cdf.controller().update_state_settings('movies_repeat_switch', system_multi_hop=True)

    cdf.controller().add_system_transition('movies_intro', 'movies',
                                           '[!#SET($moviesv=True) #SetTopicSuggestion(movies) #GOAL(movies) #GSRET(movies_return)'
                                           '"<<movies>> Well, ok. I think watching movies is a great way to relax and have fun."]')
    cdf.controller().add_user_transition('movies', 'movies', '#CheckExternalComp(movies)', score=0.5)
    cdf.controller().add_user_transition('movies', 'move_on_request',
                                         '[{[not,{#EXP(like),#LEM(watch),[#EXP(want),#EXP(talk)]}],#ONT(hate)},%s] #GCOM(movies)' % movies_str)
    cdf.controller().add_user_transition('movies', 'movies_topic_switch', '/.*/ #GCOM(movies)', score=0.1)
    cdf.controller().add_system_transition('movies_return', 'movies_topic_switch', '#GCOM(movies)', score=0.1)
    cdf.controller().update_state_settings('movies_topic_switch', system_multi_hop=True)
    cdf.controller().add_system_transition('movies', 'movies',
                                           '[!#SET($moviesv=True) #SetTopicSuggestion(movies) #GSRET(movies_return)'
                                           '"<<movies>> Well, ok. I think watching movies is a great way to relax and have fun."]',
                                           score=0.5)

    cdf.controller().update_state_settings('movies_intro', system_multi_hop=True)
    cdf.controller().update_state_settings('movies', system_multi_hop=False, user_multi_hop=False)

    # if all planned transitions are used
    cdf.controller().add_system_transition('movies_topic_switch', 'intermediate_topic_switch', '', score=0.0)

    add_transitions(cdf)

def add_transitions(cdf):

    cdf.add_system_transition('movies_topic_switch', 'house:start', '')

    cdf.add_system_transition('movies_topic_switch', 'worklife:start', '`You know, you seem like a pretty interesting person. `')
    cdf.add_system_transition('movies_topic_switch', 'worklife:start->worklife:remember_is_employed_open', '', score=9.0)
    cdf.add_system_transition('movies_topic_switch', 'worklife:start->worklife:like_job_answer', '', score=10.0)

    cdf.add_system_transition('movies_topic_switch', 'school_new:start', '`Hey by the way, `', score=2.0)
    cdf.add_system_transition('movies_topic_switch', 'sibling:start', '`You know, I can\'t put my finger on why, but you kind of seem like you have a sister.`')

    cdf.add_system_transition('movies_topic_switch', 'relationships:dating', '')
    cdf.add_system_transition('movies_topic_switch', 'relationships:dating->relationships:relationship_length', '', score=10.0)
    cdf.add_system_transition('movies_topic_switch', 'relationships:marriage', '')
    cdf.add_system_transition('movies_topic_switch', 'relationships:marriage->relationships:how_long_married', '', score=10.0)

    cdf.add_system_transition('movies_topic_switch', 'baby:start', '')
    cdf.add_system_transition('movies_topic_switch', 'baby:start->baby:asked_kids_age', '', score=10.0)

    cdf.add_system_transition('movies_topic_switch', 'hobby:start', '')
    cdf.add_system_transition('movies_topic_switch', 'hobby:today_flow', '')

    cdf.add_system_transition('movies_topic_switch', 'cv_final:start', '')

    cdf.add_system_transition('movies_topic_switch', 'movies_return:start', '', score=15.0)
    cdf.add_system_transition('movies_topic_switch', 'pets_return:start', '', score=15.0)
    cdf.add_system_transition('movies_topic_switch', 'baby:returning', '', score=15.0)
    cdf.add_system_transition('movies_topic_switch', 'relationships:returning', '', score=15.0)
    cdf.add_system_transition('movies_topic_switch', 'school_new:returning', '', score=15.0)
    cdf.add_system_transition('movies_topic_switch', 'worklife:returning', '', score=15.0)

    # MOVIES -> MUSIC

    cdf.add_system_transition('movies_topic_switch', 'movies_to_music', '#GATE(musicv:None)')
    cdf.controller().update_state_settings('movies_to_music', system_multi_hop=True)
    cdf.add_system_transition('movies_to_music', 'ask_movies_music',
                              '"It seems like every time a new movie comes out, so does some new music. Do you usually find new music that you like when you watch movies?"')
    cdf.add_user_transition('ask_movies_music', 'yes_movies_music',
                            '[{#AGREE, probably, [#NOT(not,dont), likely]}]')
    cdf.add_user_transition('ask_movies_music', 'no_movies_music',
                            '[{#DISAGREE,[{dont,not},{really,likely}]}]')
    cdf.controller().set_error_successor('ask_movies_music', 'unknown_movies_music')
    cdf.add_system_transition('yes_movies_music', 'music_intro', '"Yeah, I thought as much."')
    cdf.add_system_transition('no_movies_music', 'music_intro',
                              '"Yeah, you might like a movie and not be too fond of its music."')
    cdf.add_system_transition('unknown_movies_music', 'music_intro',
                              '"Yeah, even so, finding new music you enjoy can be difficult depending on your tastes."')

    # MOVIES -> SPORTS

    cdf.add_system_transition('movies_topic_switch', 'movies_to_sports', '#GATE(sportsv:None)')
    cdf.controller().update_state_settings('movies_to_sports', system_multi_hop=True)
    cdf.add_system_transition('movies_to_sports', 'ask_movies_sports',
                              '"It seems like movies about sports teams and players that beat the odds have been pretty popular in the past. Do you remember seeing any movies like this?"')
    cdf.add_user_transition('ask_movies_sports', 'yes_movies_sports',
                            '[{#AGREE, probably, [#NOT(not,dont), likely]}]')
    cdf.add_user_transition('ask_movies_sports', 'no_movies_sports',
                            '[{#DISAGREE,[{dont,not},{really,likely}]}]')
    cdf.controller().set_error_successor('ask_movies_sports', 'unknown_movies_sports')
    cdf.add_system_transition('yes_movies_sports', 'sports_intro',
                              '"Yeah, I thought as much. It seems like almost everyone has seen at least one sports movie."')
    cdf.add_system_transition('no_movies_sports', 'sports_intro', '"I see. Sports movies aren\'t for everyone. "')
    cdf.add_system_transition('unknown_movies_sports', 'sports_intro',
                              '"I will have to look into that. Well, anyways, "')

    # MOVIES -> TELEPORTATION

    cdf.add_system_transition('movies_topic_switch', 'movies_to_teleportation', '#GATE(teleportationv:None)')
    cdf.controller().update_state_settings('movies_to_teleportation', system_multi_hop=True)
    cdf.add_system_transition('movies_to_teleportation', 'ask_movies_teleportation',
                              '"I cannot seem to remember any movies that involve teleportation, although I know it is popular in science fictions novels. Can you think of any movies that use teleportation?"')
    cdf.add_user_transition('ask_movies_teleportation', 'yes_movies_teleportation',
                            '[{#AGREE, probably, [#NOT(not,dont), likely]}]')
    cdf.add_user_transition('ask_movies_teleportation', 'no_movies_teleportation',
                            '[{#DISAGREE,[{dont,not},{really,likely}]}]')
    cdf.controller().set_error_successor('ask_movies_teleportation', 'unknown_movies_teleportation')
    cdf.add_system_transition('yes_movies_teleportation', 'teleportation:start',
                              '[!#SET($teleportationv=True) "You do? I will have to catch up then with them. So, "]')
    cdf.add_system_transition('no_movies_teleportation', 'teleportation:start',
                              '[!#SET($teleportationv=True) "Yeah, it does seem to be a mystery. Anyways, "]')
    cdf.add_system_transition('unknown_movies_teleportation', 'teleportation:start',
                              '[!#SET($teleportationv=True) "Good one. I will have to remember that. In general, "]')

    # MOVIES -> VIRTUAL REALITY

    cdf.add_system_transition('movies_topic_switch', 'movies_to_vr', '#GATE(virtual_realityv:None)')
    cdf.controller().update_state_settings('movies_to_vr', system_multi_hop=True)
    cdf.add_system_transition('movies_to_vr', 'ask_movies_vr',
                              '"I have heard that they are now making movies in virtual reality so that it feels like you '
                              'are in the middle of the story watching it unfold! '
                              'Have you watched any movie in Virtual reality before?"')
    cdf.add_user_transition('ask_movies_vr', 'yes_movies_vr',
                            '[{#AGREE, probably, [#NOT(not,dont), likely]}]')
    cdf.add_user_transition('ask_movies_vr', 'no_movies_vr',
                            '[{#DISAGREE,[{isnt,not},{really,likely}]}]')
    cdf.controller().set_error_successor('ask_movies_vr', 'unknown_movies_vr')
    cdf.add_system_transition('yes_movies_vr', 'ask_better_movies_vr',
                              '"Awesome! It was a whole new experience, right? Did you like it more than a regular movie?"')
    cdf.add_user_transition('ask_better_movies_vr', 'yes_better_movies_vr',
                            '[{#AGREE, probably, [#NOT(not,dont), likely]}]')
    cdf.add_user_transition('ask_better_movies_vr', 'no_better_movies_vr',
                            '[{#DISAGREE,[{isnt,not},{really,likely}]}]')
    cdf.controller().set_error_successor('ask_better_movies_vr', 'unknown_movies_vr')
    cdf.add_system_transition('yes_better_movies_vr', 'virtual_reality_intro',
                              '"Yeah, it is definitely cool. "')
    cdf.add_system_transition('no_better_movies_vr', 'virtual_reality_intro',
                              '"I guess there are still some oddities that need to be worked out. Actually, "')
    cdf.add_system_transition('no_movies_vr', 'virtual_reality_intro',
                              '"You should definitely try it out, if you get a chance. Actually, "')
    cdf.add_system_transition('unknown_movies_vr', 'virtual_reality_intro',
                              '"Yeah, it is still a new thing, for sure. Actually, "')

    # MOVIES -> TRAVEL

    cdf.add_system_transition('movies_topic_switch', 'movies_to_travel', '#GATE(travelv:None)')
    cdf.controller().update_state_settings('movies_to_travel', system_multi_hop=True)
    cdf.add_system_transition('movies_to_travel', 'ask_movies_travel',
                              '"Sometimes, it seems like you can get a glimpse of a location if you watch a movie '
                              'that takes place there. Have you ever gotten an idea of a new place you want to travel to '
                              'based on a movie?"')
    cdf.add_user_transition('ask_movies_travel', 'yes_movies_travel',
                            '[{'
                            '#AGREE, [!i,#NOT(not,havent,dont),[have,think so]]'
                            '}]')
    cdf.add_user_transition('ask_movies_travel', 'no_movies_travel',
                            '[{'
                            '#DISAGREE, [!i,{dont,do not,havent,have not}]'
                            '}]')
    cdf.controller().set_error_successor('ask_movies_travel', 'unknown_movies_travel')
    cdf.add_system_transition('yes_movies_travel', 'travel_intro',
                              '"Yeah, movies can make different locations look so interesting, for sure. "')
    cdf.add_system_transition('no_movies_travel', 'travel_intro',
                              '"That makes sense. It could be hard to pay attention to the locations, '
                              'depending on what types of movie you are watching. "')
    cdf.add_system_transition('unknown_movies_travel', 'travel_intro',
                              '"Maybe so. "')