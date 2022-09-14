
from emora._travel.travel import df as travel, State as travel_states

travel_str = '{travel,traveling,city,cities,vacation,vacations}'

def add_components_to(cdf):
    # cdf.add_component(travel, 'travel')
    cdf.add_system_transition('root', 'travel_intro', '#GATE(travelv:None)', score=0.95)

    #already talked about topic
    cdf.add_system_transition('travel_intro', 'travel_repeat_switch',
                              '#IF($travelv=True) `I wish that I knew more about the locations of the world, but there '
                              'is a lot to get familiar with in such a short amount of time. `',
                              score=2.0)

    cdf.add_system_transition('travel_repeat_switch', 'travel_to_movies', '`You know, ` #GATE(moviesv:None)')
    cdf.add_system_transition('travel_repeat_switch', 'travel_to_music', '`You know, ` #GATE(musicv:None)')
    cdf.add_system_transition('travel_repeat_switch', 'travel_to_teleportation', '#GATE(teleportationv:None)')
    cdf.add_system_transition('travel_repeat_switch', 'travel_to_virtual_reality', '#GATE(virtual_realityv:None)')
    cdf.add_system_transition('travel_repeat_switch', 'travel_topic_switch', '`Anyway, `', score=0.0)
    cdf.controller().update_state_settings('travel_repeat_switch', system_multi_hop=True)

    # cdf.add_system_transition('travel_intro', ('travel', travel_states.START), '#SET($travelv=True,$original_travel=True) #IF($new_travel=None)')
    cdf.controller().update_state_settings('travel_intro', system_multi_hop=True)
    # cdf.controller().update_state_settings(('travel', travel_states.START), system_multi_hop=True)
    # travel.update_state_settings(travel_states.START, system_multi_hop=True)
    # travel.add_system_transition(travel_states.END, ('SYSTEM', 'travel_topic_switch'), '')
    # travel.update_state_settings(('SYSTEM', 'travel_topic_switch'), system_multi_hop=True)
    # if all planned transitions are used
    cdf.controller().add_system_transition('travel_topic_switch', 'intermediate_topic_switch',
                                           '"For what it is worth, I think travelling to new places is something everyone could benefit from in their lives."',
                                           score=0.0)

    cdf.add_system_transition('travel_intro', 'vacations:start', '#SET($travelv=True,$new_travel=True) #IF($original_travel=None)')

    add_transitions(cdf)

def add_transitions(cdf):


    cdf.add_system_transition('travel_topic_switch', 'house:start', '')

    cdf.add_system_transition('travel_topic_switch', 'worklife:start', '`You know, you seem like a pretty interesting person. `')
    cdf.add_system_transition('travel_topic_switch', 'worklife:start->worklife:remember_is_employed_open', '', score=9.0)
    cdf.add_system_transition('travel_topic_switch', 'worklife:start->worklife:like_job_answer', '', score=10.0)

    cdf.add_system_transition('travel_topic_switch', 'school_new:start', '`Hey by the way, `', score=2.0)
    cdf.add_system_transition('travel_topic_switch', 'sibling:start', '`You know, I can\'t put my finger on why, but you kind of seem like you have a sister.`')

    cdf.add_system_transition('travel_topic_switch', 'relationships:dating', '')
    cdf.add_system_transition('travel_topic_switch', 'relationships:dating->relationships:relationship_length', '', score=10.0)
    cdf.add_system_transition('travel_topic_switch', 'relationships:marriage', '')
    cdf.add_system_transition('travel_topic_switch', 'relationships:marriage->relationships:how_long_married', '', score=10.0)

    cdf.add_system_transition('travel_topic_switch', 'baby:start', '')
    cdf.add_system_transition('travel_topic_switch', 'baby:start->baby:asked_kids_age', '', score=10.0)

    cdf.add_system_transition('travel_topic_switch', 'hobby:start', '')
    cdf.add_system_transition('travel_topic_switch', 'hobby:today_flow', '')

    cdf.add_system_transition('travel_topic_switch', 'cv_final:start', '')

    cdf.add_system_transition('travel_topic_switch', 'movies_return:start', '', score=15.0)
    cdf.add_system_transition('travel_topic_switch', 'pets_return:start', '', score=15.0)
    cdf.add_system_transition('travel_topic_switch', 'baby:returning', '', score=15.0)
    cdf.add_system_transition('travel_topic_switch', 'relationships:returning', '', score=15.0)
    cdf.add_system_transition('travel_topic_switch', 'school_new:returning', '', score=15.0)
    cdf.add_system_transition('travel_topic_switch', 'worklife:returning', '', score=15.0)

    # TRAVEL -> VIRTUAL REALITY

    cdf.add_system_transition('travel_topic_switch', 'travel_to_virtual_reality', '#GATE(virtual_realityv:None)')
    cdf.controller().update_state_settings('travel_to_virtual_reality', system_multi_hop=True)
    cdf.add_system_transition('travel_to_virtual_reality', 'ask_travel_virtual_reality',
                              '"You know, one thing that could be awesome as technology advances is to experience '
                              'different locations through virtual reality. Then, you could at least see all of the '
                              'sights without having to actually go there. Wouldn\'t that be cool?"')
    cdf.add_user_transition('ask_travel_virtual_reality', 'yes_travel_virtual_reality',
                            '[{'
                            '#AGREE, '
                            '[#NOT(dont,not),think,{so,[!{would,could,might},be]}], '
                            '[#NOT(not,doesnt,never,dont,arent),{cool,amazing,awesome,great,good,nice,sweet}]'
                            '}]')
    cdf.add_user_transition('ask_travel_virtual_reality', 'no_travel_virtual_reality',
                            '[{'
                            '#DISAGREE,'
                            '[{dont,do not},think,{so,[!{would,could,might},be]}],'
                            '[{not,doesnt,never,dont,arent},{good,great,awesome,cool,impressive,amazing,nice,sweet,same,equivalent,equal}],'
                            '[#NOT(not,doesnt,never,dont,arent),{bad,stupid,boring,dumb,unimpressive}]'
                            '}]')
    cdf.controller().set_error_successor('ask_travel_virtual_reality', 'unknown_travel_virtual_reality')
    cdf.add_system_transition('yes_travel_virtual_reality', 'virtual_reality_intro',
                              '"Yeah, I think a lot of people would enjoy it, too. Anyway, "')
    cdf.add_system_transition('no_travel_virtual_reality', 'virtual_reality_intro',
                              '"Yeah, it\'s not the same. Anyway, "')
    cdf.add_system_transition('unknown_travel_virtual_reality', 'virtual_reality_intro',
                              '"It probably isn\'t as cool the actual location. Anyway, "')

    # TRAVEL -> MOVIES

    cdf.add_system_transition('travel_topic_switch', 'travel_to_movies', '#GATE(moviesv:None)')
    cdf.controller().update_state_settings('travel_to_movies', system_multi_hop=True)
    cdf.add_system_transition('travel_to_movies', 'ask_travel_movies',
                              '"Sometimes, it seems like you can get a glimpse of a location if you watch a movie '
                              'that takes place there. Have you ever found a new place you want to travel to '
                              'based on a movie?"')
    cdf.add_user_transition('ask_travel_movies', 'yes_travel_movies',
                            '[{'
                            '#AGREE, [!i,#NOT(not,havent,dont),[have,think so]]'
                            '}]')
    cdf.add_user_transition('ask_travel_movies', 'no_travel_movies',
                            '[{'
                            '#DISAGREE, [!i,{dont,do not,havent,have not}]'
                            '}]')
    cdf.controller().set_error_successor('ask_travel_movies', 'unknown_travel_movies')
    cdf.add_system_transition('yes_travel_movies', 'movies_intro',
                              '"Yeah, movies can make different locations look so interesting, for sure. "')
    cdf.add_system_transition('no_travel_movies', 'movies_intro',
                              '"That makes sense. It could be hard to pay attention to the locations, '
                              'depending on what types of movie you are watching. "')
    cdf.add_system_transition('unknown_travel_movies', 'movies_intro',
                              '"Maybe so. "')

    # TRAVEL -> MUSIC

    cdf.add_system_transition('travel_topic_switch', 'travel_to_music', '#GATE(musicv:None)')
    cdf.controller().update_state_settings('travel_to_music', system_multi_hop=True)
    cdf.add_system_transition('travel_to_music', 'ask_travel_music',
                              '"I love that different locations can often be identified by their specific style of '
                              'music. Do you notice these differences in music too?"')
    cdf.add_user_transition('ask_travel_music', 'yes_travel_music',
                            '[{'
                            '#AGREE, [!i,#NOT(not,havent,dont),[do,have,think so]]'
                            '}]')
    cdf.add_user_transition('ask_travel_music', 'no_travel_music',
                            '[{'
                            '#DISAGREE, [!i,{dont,do not,havent,have not}]'
                            '}]')
    cdf.controller().set_error_successor('ask_travel_music', 'unknown_travel_music')
    cdf.add_system_transition('yes_travel_music', 'music_intro',
                              '"It\'s hard not to. I think listening to the local music is a great way to get to know the'
                              'different places that you travel to. "')
    cdf.add_system_transition('no_travel_music', 'music_intro',
                              '"No? You may want to try learning about the music and its cultural significance when '
                              'you travel. You never know what you might find. "')
    cdf.add_system_transition('unknown_travel_music', 'music_intro',
                              '"Well, I think it could be fun and interesting to learn about music that is specific to '
                              'different regions. "')

    # TRAVEL -> TELEPORTATION

    cdf.add_system_transition('travel_topic_switch', 'travel_to_teleportation',
                              '#GATE(teleportationv:None) #SET($teleportationv=True)')
    cdf.controller().update_state_settings('travel_to_teleportation', system_multi_hop=True)
    cdf.add_system_transition('travel_to_teleportation', 'teleportation:start',
                              '"You know, it is pretty difficult to take the time to travel to many places. '
                              'I know this is a wild idea, but if we could '
                              'just teleport anywhere in the world, it would be so much easier! "')
