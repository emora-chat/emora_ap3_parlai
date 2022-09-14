from emora._openings.new_opening import component as opening

def add_components_to(cdf):

    cdf.add_component(opening, 'opening')

    cdf.add_user_transition('root', ('opening', 'prestart'), '/.*?/', score=999)
    #cdf.controller().set_error_successor('start', ('opening', 'prestart'))
    cdf.controller().update_state_settings(('opening', 'prestart'), user_multi_hop=True)

    cdf.add_state('recovery_from_failure', 'recovery_from_failure')
    cdf.add_system_transition('recovery_from_failure', 'root', '"Hmm. I have not thought of that recently."')

    cdf.add_state('get_to_know_intro')
    cdf.controller().update_state_settings('get_to_know_intro', system_multi_hop=True)
    cdf.controller().update_state_settings('root', system_multi_hop=True, memory=0)
    opening.add_system_transition('opening_chat_choices', ('SYSTEM', 'get_to_know_intro'), '')
    opening.update_state_settings(('SYSTEM', 'get_to_know_intro'), system_multi_hop=True)

    cdf.add_system_transition('get_to_know_intro', 'root',
                              '`I am really excited to get to know you better. `', score=0.0)

    cdf.add_system_transition('get_to_know_intro', 'SYSTEM:root', '')
