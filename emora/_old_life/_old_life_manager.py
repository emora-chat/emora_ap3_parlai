from emora._old_life.school import df as school

def add_components_to(cdf):
    cdf.add_component(school, 'school')
    # cdf.add_system_transition('root', 'school_intro', '#GATE(schoolv:None)')
    cdf.add_system_transition('school_intro', ('school', 'root'), '#SET($schoolv=True)')
    cdf.controller().update_state_settings('school_intro', system_multi_hop=True)
    cdf.controller().update_state_settings(('school', 'root'), system_multi_hop=True)
    school.add_system_transition('end', ('SYSTEM', 'intermediate_topic_switch'), '"Anyway, "', score=0.0)
    school.update_state_settings(('SYSTEM', 'intermediate_topic_switch'), system_multi_hop=True)

    # cdf.add_component(worklife, 'worklife')
    # cdf.add_system_transition('root', 'worklife_intro', '#GATE(worklifev:None)')
    # cdf.add_system_transition('worklife_intro', ('worklife', 'root'), '#SET($worklifev=True)')
    # cdf.controller().update_state_settings('worklife_intro', system_multi_hop=True)
    # cdf.controller().update_state_settings(('worklife', 'root'), system_multi_hop=True)
    # worklife.add_system_transition('end', ('SYSTEM', 'intermediate_topic_switch'), '"Anyway, "', score=0.0)
    # worklife.update_state_settings(('SYSTEM', 'intermediate_topic_switch'), system_multi_hop=True)

    # add_transitions(cdf)

def add_transitions(cdf):
    cdf.add_system_transition("life_intro", "worklife_intro", '#GATE(worklifev:None)')
    cdf.add_system_transition("life_intro", "school_intro", "#GATE(schoolv:None)")
    cdf.controller().update_state_settings("life_intro", system_multi_hop=True)