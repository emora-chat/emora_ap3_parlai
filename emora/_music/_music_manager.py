

music_str = '{music,musics,tunes,song,songs,melody,melodies,album,albums,concert,concerts}'

def add_components_to(cdf):
    cdf.controller().add_system_transition('root', 'music_intro',
                                           '[! #GATE(musicv:None) #IsNotLaunchRequest'
                                           '"There is a lot of new music that has come out recently."]')

    #already talked about topic
    cdf.add_system_transition('music_intro', 'music_repeat_switch',
                              '#IF($musicv=True) `I\'m kind of tired of talking about music in depth, to be honest. I '
                              'hope that is okay. `',
                              score=2.0)
    cdf.add_system_transition('music_repeat_switch', 'music_to_pet', '#GATE(petv:None)')
    cdf.add_system_transition('music_repeat_switch', 'music_to_sports', '`You know, ` #GATE(sportsv:None)')
    cdf.add_system_transition('music_repeat_switch', 'music_to_movies', '`You know, ` #GATE(moviesv:None)')
    cdf.add_system_transition('music_repeat_switch', 'music_to_travel', '`You know, ` #GATE(travelv:None)')
    cdf.add_system_transition('music_repeat_switch', 'music_to_teleportation', '#GATE(teleportationv:None)')
    cdf.add_system_transition('music_repeat_switch', 'music_to_vr', '`You know, ` #GATE(virtual_realityv:None)')
    cdf.add_system_transition('music_repeat_switch', 'music_topic_switch', '`Anyway, `', score=0.0)
    cdf.controller().update_state_settings('music_repeat_switch', system_multi_hop=True)

    cdf.controller().add_system_transition('music_intro', 'music',
                                           '[!#SET($musicv=True) #SetTopicSuggestion(music) #GOAL(music) #GSRET(music_return)'
                                           '"<<music>> Ok, well. I find it inspiring that we have so many different types of music to listen to."]')
    cdf.controller().add_user_transition('music', 'music', '#CheckExternalComp(music)', score=0.5)
    cdf.controller().add_user_transition('music', 'move_on_request',
                                         '[{[not,{#EXP(like),#LEM(listen),[#EXP(want),#EXP(talk)]}],#ONT(hate)},%s] #GCOM(music)' % music_str)
    cdf.controller().add_user_transition('music', 'music_topic_switch', '/.*/ #GCOM(music)', score=0.1)
    cdf.controller().add_system_transition('music_return', 'music_topic_switch', '#GCOM(music)', score=0.1)
    cdf.controller().update_state_settings('music_topic_switch', system_multi_hop=True)
    cdf.controller().add_system_transition('music', 'music',
                                           '[!#SET($musicv=True) #SetTopicSuggestion(music) #GSRET(music_return)'
                                           '"<<music>> Ok, well. I find it inspiring that we have so many different types of music to listen to."]',
                                           score=0.5)

    cdf.controller().update_state_settings('music_intro', system_multi_hop=True)
    cdf.controller().update_state_settings('music', system_multi_hop=False, user_multi_hop=False)

    # if all planned transitions are used
    cdf.controller().add_system_transition('music_topic_switch', 'intermediate_topic_switch', '', score=0.0)

    add_transitions(cdf)


def add_transitions(cdf):

    cdf.add_system_transition('music_topic_switch', 'house:start', '')

    cdf.add_system_transition('music_topic_switch', 'worklife:start', '`You know, you seem like a pretty interesting person. `')
    cdf.add_system_transition('music_topic_switch', 'worklife:start->worklife:remember_is_employed_open', '', score=9.0)
    cdf.add_system_transition('music_topic_switch', 'worklife:start->worklife:like_job_answer', '', score=10.0)

    cdf.add_system_transition('music_topic_switch', 'school_new:start', '`Hey by the way, `', score=2.0)
    cdf.add_system_transition('music_topic_switch', 'sibling:start', '`You know, I can\'t put my finger on why, but you kind of seem like you have a sister.`')

    cdf.add_system_transition('music_topic_switch', 'relationships:dating', '')
    cdf.add_system_transition('music_topic_switch', 'relationships:dating->relationships:relationship_length', '', score=10.0)
    cdf.add_system_transition('music_topic_switch', 'relationships:marriage', '')
    cdf.add_system_transition('music_topic_switch', 'relationships:marriage->relationships:how_long_married', '', score=10.0)

    cdf.add_system_transition('music_topic_switch', 'baby:start', '')
    cdf.add_system_transition('music_topic_switch', 'baby:start->baby:asked_kids_age', '', score=10.0)

    cdf.add_system_transition('music_topic_switch', 'hobby:start', '')
    cdf.add_system_transition('music_topic_switch', 'hobby:today_flow', '')

    cdf.add_system_transition('music_topic_switch', 'cv_final:start', '')

    cdf.add_system_transition('music_topic_switch', 'movies_return:start', '', score=15.0)
    cdf.add_system_transition('music_topic_switch', 'pets_return:start', '', score=15.0)
    cdf.add_system_transition('music_topic_switch', 'baby:returning', '', score=15.0)
    cdf.add_system_transition('music_topic_switch', 'relationships:returning', '', score=15.0)
    cdf.add_system_transition('music_topic_switch', 'school_new:returning', '', score=15.0)
    cdf.add_system_transition('music_topic_switch', 'worklife:returning', '', score=15.0)

    # MUSIC -> PET

    cdf.add_system_transition('music_topic_switch', 'music_to_pet', '#GATE(petv:None)')
    cdf.controller().update_state_settings('music_to_pet', system_multi_hop=True)
    cdf.add_system_transition('music_to_pet', 'ask_music_pet',
                              '"You know, my friends always sing to their pets. Do you think animals like music in the same way people do?"')
    cdf.add_user_transition('ask_music_pet', 'yes_music_pet',
                            '[{#AGREE, probably, [#NOT(not,dont), likely]}]')
    cdf.add_user_transition('ask_music_pet', 'no_music_pet',
                            '[{#DISAGREE,[{dont,not},{really,likely}]}]')
    cdf.controller().set_error_successor('ask_music_pet', 'unknown_music_pet')
    cdf.add_system_transition('yes_music_pet', 'pet_intro',
                              '"Yeah, it may be likely that a pleasant melody is soothing to every creature. "')
    cdf.add_system_transition('no_music_pet', 'pet_intro',
                              '"Yeah, maybe music is something uniquely enjoyable to people. "')
    cdf.add_system_transition('unknown_music_pet', 'pet_intro',
                              '"Ok. Well, I think a pleasant sound is enjoyable to every creature, but what is considered to be pleasant may vary among species. "')

    # MUSIC -> SPORTS

    cdf.add_system_transition('music_topic_switch', 'music_to_sports', '#GATE(sportsv:None)')
    cdf.controller().update_state_settings('music_to_sports', system_multi_hop=True)
    cdf.add_system_transition('music_to_sports', 'ask_music_sports',
                              '"Every time my friends hear the song we will rock you by queen, they are reminded of high school basketball games. Do you have any songs that remind you of any sporting events?"')
    cdf.add_user_transition('ask_music_sports', 'yes_music_sports',
                            '[{#AGREE, probably, [#NOT(not,dont), likely]}]')
    cdf.add_user_transition('ask_music_sports', 'no_music_sports',
                            '[{#DISAGREE,[{dont,not},{really,likely}]}]')
    cdf.controller().set_error_successor('ask_music_sports', 'unknown_music_sports')
    cdf.add_system_transition('yes_music_sports', 'sports_intro', '"Yeah, I feel like everyone has one. "')
    cdf.add_system_transition('no_music_sports', 'sports_intro',
                              '"Lucky, it is kind of annoying to have those overplayed songs. "')
    cdf.add_system_transition('unknown_music_sports', 'sports_intro', '"I see. Anyways, "')

    # MUSIC -> TELEPORTATION

    cdf.add_system_transition('music_topic_switch', 'music_to_teleportation', '#GATE(teleportationv:None)')
    cdf.controller().update_state_settings('music_to_teleportation', system_multi_hop=True)
    cdf.add_system_transition('music_to_teleportation', 'ask_music_teleportation',
                              '"You know, it is so hard sometimes to go to all of the places that you want to, like if some concert is in a different state or even country. Life just gets in the way. Wouldn\'t it be nice if travel was not so time-consuming?"')
    cdf.add_user_transition('ask_music_teleportation', 'yes_music_teleportation',
                            '[{#AGREE, probably, [#NOT(not,dont), likely]}]')
    cdf.add_user_transition('ask_music_teleportation', 'no_music_teleportation',
                            '[{#DISAGREE,[{dont,not},{really,likely}]}]')
    cdf.controller().set_error_successor('ask_music_teleportation', 'unknown_music_teleportation')
    cdf.add_system_transition('yes_music_teleportation', 'teleportation:start',
                              '[!#SET($teleportationv=True) "Yeah, this may seem kind of silly and crazy but I cannot help but think something like teleportation would come in handy for cases like this. "]')
    cdf.add_system_transition('no_music_teleportation', 'teleportation:start',
                              '[!#SET($teleportationv=True) "Really? Well, I am glad it does not bother you so much. For me, I think it would be helpful and it reminds of the idea of teleportation for sure. "]')
    cdf.add_system_transition('unknown_music_teleportation', 'teleportation:start',
                              '[!#SET($teleportationv=True) "Yeah, I see that. For me, I think it would be helpful to get somewhere instantly and it reminds of the idea of teleportation. "]')

    # MUSIC -> VIRTUAL REALITY

    cdf.add_system_transition('music_topic_switch', 'music_to_vr', '#GATE(virtual_realityv:None)')
    cdf.controller().update_state_settings('music_to_vr', system_multi_hop=True)
    cdf.add_system_transition('music_to_vr', 'ask_music_vr',
                              '"I have heard that a lot of live music performances may become available to experience using '
                              'virtual reality. I think that is pretty cool, since music tickets can be expensive. '
                              'Do you think seeing a concert using virtual reality would be worth it?"')
    cdf.add_user_transition('ask_music_vr', 'yes_music_vr',
                            '[{#AGREE, probably, [#NOT(not,dont), likely]}]')
    cdf.add_user_transition('ask_music_vr', 'no_music_vr',
                            '[{#DISAGREE,[{dont,not},{really,likely,same}]}]')
    cdf.controller().set_error_successor('ask_music_vr', 'unknown_music_vr')
    cdf.add_system_transition('yes_music_vr', 'virtual_reality_intro', '"Yeah, me too! "')
    cdf.add_system_transition('no_music_vr', 'virtual_reality_intro',
                              '"You are probably right. It wouldn\'t be the same. Anyway, "')
    cdf.add_system_transition('unknown_music_vr', 'virtual_reality_intro',
                              '"Well, I think it could be worth it. Anyway, "')

    # MUSIC -> MOVIES

    cdf.add_system_transition('music_topic_switch', 'music_to_movies', '#GATE(moviesv:None)')
    cdf.controller().update_state_settings('music_to_movies', system_multi_hop=True)
    cdf.add_system_transition('music_to_movies', 'ask_music_movies',
                              '"It seems like every time a new movie comes out, so does some new music. Do you notice new music that you like when you watch movies?"')
    cdf.add_user_transition('ask_music_movies', 'yes_music_movies',
                            '[{#AGREE, probably, [#NOT(not,dont), likely]}]')
    cdf.add_user_transition('ask_music_movies', 'no_music_movies',
                            '[{#DISAGREE,[{dont,not},{really,likely}]}]')
    cdf.controller().set_error_successor('ask_music_movies', 'unknown_music_movies')
    cdf.add_system_transition('yes_music_movies', 'movies_intro', '"Yeah, I thought as much."')
    cdf.add_system_transition('no_music_movies', 'movies_intro',
                              '"Yeah, you might like a movie and not be too fond of its music."')
    cdf.add_system_transition('unknown_music_movies', 'movies_intro',
                              '"Yeah, even so, finding new music you enjoy can be difficult depending on your tastes."')

    # MUSIC -> TRAVEL

    cdf.add_system_transition('music_topic_switch', 'music_to_travel', '#GATE(travelv:None)')
    cdf.controller().update_state_settings('music_to_travel', system_multi_hop=True)
    cdf.add_system_transition('music_to_travel', 'ask_music_travel',
                              '"Musical tastes around the world are pretty varied and you may not notice that until '
                              'you travel around a bit. Do you notice different styles of music when you explore new '
                              'places?"')
    cdf.add_user_transition('ask_music_travel', 'yes_music_travel',
                            '[{'
                            '#AGREE, [!i,#NOT(not,havent,dont),[do,have,think so]]'
                            '}]')
    cdf.add_user_transition('ask_music_travel', 'no_music_travel',
                            '[{'
                            '#DISAGREE, [!i,{dont,do not,havent,have not}]'
                            '}]')
    cdf.controller().set_error_successor('ask_music_travel', 'unknown_music_travel')
    cdf.add_system_transition('yes_music_travel', 'travel_intro',
                              '"Makes sense. I think it is a great way to get to know the places you travel to. "')
    cdf.add_system_transition('no_music_travel', 'travel_intro',
                              '"No? You may want to try learning about the music and its significance when '
                              'you travel. You never know what you might find. "')
    cdf.add_system_transition('unknown_music_travel', 'travel_intro',
                              '"Well, I think it could be fun and interesting to learn about music that is specific to '
                              'certain locations. "')