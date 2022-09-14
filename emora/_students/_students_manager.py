
from emora._students.videogames import df as videogames, State as videogame_states
# from emora._students.calypso import df as calypso, State as calypso_states

videogames_str = '{[!video #LEM(game)],xbox,playstation,p s,ps,nintendo,switch,minecraft,fortnite,overwatch}'

def add_components_to(cdf):
    cdf.add_component(videogames, 'videogames')
    cdf.add_system_transition('root', 'videogames:start', '',score=0.9)
    videogames.update_state_settings('start', system_multi_hop=True)
    videogames.add_system_transition(videogame_states.END, 'SYSTEM:videogames_topic_switch', '')
    videogames.update_state_settings('SYSTEM:videogames_topic_switch', system_multi_hop=True)
    # if all planned transitions are used
    cdf.controller().add_system_transition('videogames_topic_switch', 'intermediate_topic_switch', '', score=0.0)

    # cdf.add_component(calypso, 'calypso')
    # cdf.add_system_transition('music_intro', 'calypso:start', '')
    # cdf.add_system_transition('music_intro', 'calypso:request', '#IF($calypso_in=True) #SET($musicv=True)', score=0.0)
    # calypso.update_state_settings('start', system_multi_hop=True)
    # calypso.add_system_transition(calypso_states.END, 'SYSTEM:music_topic_switch', '')
    # calypso.update_state_settings('SYSTEM:music_topic_switch', system_multi_hop=True)
    # if all planned transitions are used
    # cdf.controller().add_system_transition('videogame_topic_switch', 'intermediate_topic_switch', '', score=0.0)

    add_transitions(cdf)


def add_transitions(cdf):
    cdf.add_system_transition('videogames_topic_switch', 'house:start', '')

    cdf.add_system_transition('videogames_topic_switch', 'worklife:start', '`You know, you seem like a pretty interesting person. `')
    cdf.add_system_transition('videogames_topic_switch', 'worklife:start->worklife:remember_is_employed_open', '', score=9.0)
    cdf.add_system_transition('videogames_topic_switch', 'worklife:start->worklife:like_job_answer', '', score=10.0)

    cdf.add_system_transition('videogames_topic_switch', 'school_new:start', '`Hey by the way, `', score=2.0)
    cdf.add_system_transition('videogames_topic_switch', 'sibling:start', '`You know, I can\'t put my finger on why, but you kind of seem like you have a sister.`')

    cdf.add_system_transition('videogames_topic_switch', 'relationships:dating', '')
    cdf.add_system_transition('videogames_topic_switch', 'relationships:dating->relationships:relationship_length', '',
                              score=10.0)
    cdf.add_system_transition('videogames_topic_switch', 'relationships:marriage', '')
    cdf.add_system_transition('videogames_topic_switch', 'relationships:marriage->relationships:how_long_married', '',
                              score=10.0)

    cdf.add_system_transition('videogames_topic_switch', 'baby:start', '')
    cdf.add_system_transition('videogames_topic_switch', 'baby:start->baby:asked_kids_age', '', score=10.0)

    cdf.add_system_transition('videogames_topic_switch', 'hobby:start', '')
    cdf.add_system_transition('videogames_topic_switch', 'hobby:today_flow', '')

    cdf.add_system_transition('videogames_topic_switch', 'cv_final:start', '')

    cdf.add_system_transition('videogames_topic_switch', 'movies_return:start', '', score=15.0)
    cdf.add_system_transition('videogames_topic_switch', 'pets_return:start', '', score=15.0)
    cdf.add_system_transition('videogames_topic_switch', 'baby:returning', '', score=15.0)
    cdf.add_system_transition('videogames_topic_switch', 'relationships:returning', '', score=15.0)
    cdf.add_system_transition('videogames_topic_switch', 'school_new:returning', '', score=15.0)
    cdf.add_system_transition('videogames_topic_switch', 'worklife:returning', '', score=15.0)