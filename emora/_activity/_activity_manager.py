
from emora._activity.general_activity import df as activity

def add_components_to(cdf):
    cdf.add_component(activity, 'activity')
    cdf.add_system_transition('activity_intro', ('activity', 'ask_about_day'), '#SET($activityv=True)')
    cdf.controller().update_state_settings('activity_intro', system_multi_hop=True)
    cdf.controller().update_state_settings(('activity', 'ask_about_day'), system_multi_hop=True)

    add_transitions(cdf)

def add_transitions(cdf):
    cdf.add_system_transition('root', 'activity_intro', '#GATE(activityv:None)')

    activity.add_system_transition('transition_from_chore', ('SYSTEM', 'movies_intro'),
                                   '#GATE(moviesv:None) "A lot of people seem to like to put on a good movie or t v show when they do chores. "')
    activity.add_system_transition('transition_from_chore', ('SYSTEM', 'music_intro'),
                                   '#GATE(musicv:None) "You know, I have heard that putting on an upbeat song can make doing chores a lot more enjoyable. "')

    activity.add_system_transition('transition_from_homework', ('SYSTEM', 'movies_intro'),
                                   '#GATE(moviesv:None) "It seems like one of the most popular ways to take a break is to put on a good movie or t v show. "')
    activity.add_system_transition('transition_from_homework', ('SYSTEM', 'virtual_reality_intro'),
                                   '#GATE(virtual_realityv:None)')

    activity.add_system_transition('transition_from_finish_homework', ('SYSTEM', 'movies_intro'),
                                   '#GATE(moviesv:None) "It seems like one of the most popular ways to relax after putting in some good work is to watch a movie or t v show. "')
    activity.add_system_transition('transition_from_finish_homework', ('SYSTEM', 'virtual_reality_intro'),
                                   '#GATE(virtual_realityv:None)')
    activity.add_system_transition('transition_from_finish_homework', ('SYSTEM', 'music_intro'),
                                   '#GATE(musicv:None) "Now that you have finished some work, you could put on some music and do something more fun and relaxing. "')

    activity.add_system_transition('transition_from_homework_topic', ('SYSTEM', 'movies_intro'),
                                   '#GATE(moviesv:None) "Like, can you imagine if your homework involved watching a movie and maybe writing a paper on it. That would be pretty sweet. "')
    activity.add_system_transition('transition_from_homework_topic', ('SYSTEM', 'virtual_reality_intro'),
                                   '#GATE(virtual_realityv:None)')
    activity.add_system_transition('transition_from_homework_topic', ('SYSTEM', 'music_intro'),
                                   '#GATE(musicv:None) "Like, it would be so much fun to make your own song as a homework assignment. I guess, well, that could be pretty challenging though. "')

    activity.add_system_transition('transition_from_class', ('SYSTEM', 'movies_intro'),
                                   '#GATE(moviesv:None) "Since you are a student and that probably consumes most of your time, I am sure you always enjoy having a break, maybe like watching '
                                   'movies or t v or something. "')
    activity.add_system_transition('transition_from_class', ('SYSTEM', 'music_intro'),
                                   '#GATE(musicv:None) "I\'ve heard that some teachers put on soft music in the background when they teach to make it a little less boring. I think that is a '
                                   'cool idea to make class more enjoyable. Speaking of music, "')
    activity.add_system_transition('transition_from_class', ('SYSTEM', 'virtual_reality_intro'),
                                   '#GATE(virtual_realityv:None)')

    activity.add_system_transition('transition_from_work', ('SYSTEM', 'movies_intro'),
                                   '#GATE(moviesv:None) "Now more than ever, we need to figure out how to relax and have fun to keep ourselves as sane as possible. I hope you are able to '
                                   'find relaxation in things like watching movies or t v. "')
    activity.add_system_transition('transition_from_work', ('SYSTEM', 'music_intro'),
                                   '#GATE(musicv:None) "Now more than ever, we need to figure out how to relax and have fun to keep ourselves as sane as possible. I hope you are able to '
                                   'find relaxation by listening to some soothing music or upbeat music. "')
    activity.add_system_transition('transition_from_work', ('SYSTEM', 'virtual_reality_intro'),
                                   '#GATE(virtual_realityv:None)')

    activity.add_system_transition('transition_from_indoor_dest', ('SYSTEM', 'movies_intro'),
                                   '#GATE(moviesv:None) "There are some fun things you can do to keep busy at home, too, like watching movies with others in your home. "')
    activity.add_system_transition('transition_from_indoor_dest', ('SYSTEM', 'music_intro'),
                                   '#GATE(musicv:None) "There are some fun things you can do to keep busy at home, too, like finding some good new music. "')
    activity.add_system_transition('transition_from_indoor_dest', ('SYSTEM', 'virtual_reality_intro'),
                                   '#GATE(virtual_realityv:None)')

    activity.add_system_transition('transition_from_outdoor_dest', ('SYSTEM', 'movies_intro'),
                                   '#GATE(moviesv:None) "There are some fun things you can do to keep busy at home, too, like watching movies with others in your home. "')
    activity.add_system_transition('transition_from_outdoor_dest', ('SYSTEM', 'music_intro'),
                                   '#GATE(musicv:None) "There are some fun things you can do to keep busy at home, too, like finding some good new music. "')
    activity.add_system_transition('transition_from_outdoor_dest', ('SYSTEM', 'virtual_reality_intro'),
                                   '#GATE(virtual_realityv:None)')
    activity.add_system_transition('transition_from_outdoor_dest', ('SYSTEM', 'sports_intro'),
                                   '#GATE(sportsv:None) "You could always shoot some hoops or kick around a soccer ball with yourself for some fun outdoor activity, too. "')

    activity.add_system_transition('transition_from_exercise', ('SYSTEM', 'sports_intro'),
                                   '#GATE(sportsv:None) "Once we can get together with others in groups again, you could always try playing some team sports for a fun workout, too. "')

    # activity.add_system_transition('transition_from_family', ('SYSTEM','pet_intro'),
    #                                '"You know, I have heard that some people treat their pets just like family and friends. "')

    activity.add_system_transition('transition_from_hobby', ('SYSTEM', 'movies_intro'),
                                   '#GATE(moviesv:None) "Some other fun activities I have heard of are watching movies with others in your home. "')
    activity.add_system_transition('transition_from_hobby', ('SYSTEM', 'music_intro'),
                                   '#GATE(musicv:None) "It is really quite amazing the number of things you can do to have fun at home, like finding some good new music. "')
    activity.add_system_transition('transition_from_hobby', ('SYSTEM', 'virtual_reality_intro'),
                                   '#GATE(virtual_realityv:None)')
    activity.add_system_transition('transition_from_hobby', ('SYSTEM', 'pet_intro'),
                                   '#GATE(petv:None) "My friend has even started teaching their dog some tricks for fun. "')

    activity.add_system_transition('give_fun_activity', ('SYSTEM', 'movies_intro'),
                                   '#GATE(moviesv:None) "One thing that could be enjoyable to do right now is to watch a movie with others in your home. "')
    activity.add_system_transition('give_fun_activity', ('SYSTEM', 'music_intro'),
                                   '#GATE(musicv:None) "One thing that could be enjoyable to do right now is find some good new music. "')
    activity.add_system_transition('give_fun_activity', ('SYSTEM', 'virtual_reality_intro'),
                                   '#GATE(virtual_realityv:None)')
    activity.add_system_transition('give_fun_activity', ('SYSTEM', 'pet_intro'),
                                   '#GATE(petv:None) "One thing that could be enjoyable to do right now is to play with a pet, maybe even try to teach it some new tricks. "')

    # activity.add_system_transition('transition_to_coronavirus', ('SYSTEM', 'coronavirus_op_intro'), '')


    activity.add_system_transition('transition_to_vr', ('SYSTEM', 'virtual_reality_intro'),
                                   '#GATE(virtual_realityv:None)')
    activity.add_system_transition('transition_to_movies', ('SYSTEM', 'movies_intro'), '#GATE(moviesv:None)')
    activity.update_state_settings(('SYSTEM', 'virtual_reality_intro'), system_multi_hop=True)
    activity.update_state_settings(('SYSTEM', 'movies_intro'), system_multi_hop=True)
    activity.update_state_settings(('SYSTEM', 'music_intro'), system_multi_hop=True)
    activity.update_state_settings(('SYSTEM', 'sports_intro'), system_multi_hop=True)
    activity.update_state_settings(('SYSTEM', 'pet_intro'), system_multi_hop=True)
    # activity.update_state_settings(('SYSTEM', 'coronavirus_op_intro'), system_multi_hop=True)
    # activity.update_state_settings(('SYSTEM', 'teleportation_intro'), system_multi_hop=True)

    activity.update_state_settings('transition_to_vr', system_multi_hop=True)
    activity.update_state_settings('transition_to_movies', system_multi_hop=True)
    activity.update_state_settings('transition_from_chore', system_multi_hop=True)
    activity.update_state_settings('transition_from_homework', system_multi_hop=True)
    activity.update_state_settings('transition_from_finish_homework', system_multi_hop=True)
    activity.update_state_settings('transition_from_homework_topic', system_multi_hop=True)
    activity.update_state_settings('transition_from_class', system_multi_hop=True)
    activity.update_state_settings('transition_from_work', system_multi_hop=True)
    activity.update_state_settings('transition_from_indoor_dest', system_multi_hop=True)
    activity.update_state_settings('transition_from_outdoor_dest', system_multi_hop=True)
    activity.update_state_settings('transition_from_exercise', system_multi_hop=True)
    # activity.update_state_settings('transition_from_family', system_multi_hop=True)
    activity.update_state_settings('transition_from_hobby', system_multi_hop=True)
    activity.update_state_settings('give_fun_activity', system_multi_hop=True)
    # activity.update_state_settings('transition_to_coronavirus', system_multi_hop=True)

    activity.add_system_transition('transition_to_vr', ('SYSTEM', 'root'), '', score=0.0)
    activity.add_system_transition('transition_to_movies', ('SYSTEM', 'root'), '', score=0.0)
    activity.add_system_transition('transition_from_chore', ('SYSTEM', 'root'), '', score=0.0)
    activity.add_system_transition('transition_from_homework', ('SYSTEM', 'root'), '', score=0.0)
    activity.add_system_transition('transition_from_finish_homework', ('SYSTEM', 'root'), '', score=0.0)
    activity.add_system_transition('transition_from_homework_topic', ('SYSTEM', 'root'), '', score=0.0)
    activity.add_system_transition('transition_from_class', ('SYSTEM', 'root'), '', score=0.0)
    activity.add_system_transition('transition_from_work', ('SYSTEM', 'root'), '', score=0.0)
    activity.add_system_transition('transition_from_indoor_dest', ('SYSTEM', 'root'), '', score=0.0)
    activity.add_system_transition('transition_from_outdoor_dest', ('SYSTEM', 'root'), '', score=0.0)
    activity.add_system_transition('transition_from_exercise', ('SYSTEM', 'root'), '', score=0.0)
    activity.add_system_transition('transition_from_hobby', ('SYSTEM', 'root'), '', score=0.0)
    activity.add_system_transition('give_fun_activity', ('SYSTEM', 'root'), '', score=0.0)

    # USED FOR NEW EMORA / OPENING!!!!!
    activity.add_system_transition('transition_out', ('SYSTEM', 'root'), '')
    activity.update_state_settings('transition_out', system_multi_hop=True)
    activity.update_state_settings(('SYSTEM', 'root'), system_multi_hop=True)