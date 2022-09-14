from emora._stop.stop_conversation import stop_nlu, df as stop, State as stop_states

def add_components_to(cdf):
    cdf.add_component(stop, 'stop')
    stop.add_system_transition(stop_states.END, ('SYSTEM', 'intermediate_topic_switch'), '')
    stop.update_state_settings(('SYSTEM', 'intermediate_topic_switch'), system_multi_hop=True)
