from emora._news.breaking_news import df as news, State as news_states

news_str = '{news,politics,technology,business,events}'

def add_components_to(cdf):

    # breaking news

    # cdf.add_component(news, 'news')
    # cdf.add_system_transition('root', 'news_intro', '#IntLessThan(told_news,max_news) #GATE()')
    # cdf.add_system_transition('news_intro', ('news', news_states.START), '#SET($newsv=True) $breaking_news_intro=#ChooseBreakingIntro()')
    # cdf.controller().update_state_settings('news_intro', system_multi_hop=True)
    # cdf.controller().update_state_settings(('news', news_states.START), system_multi_hop=True)
    # news.add_system_transition(news_states.END, ('SYSTEM', 'intermediate_topic_switch'), '"Anyway, "', score=0.0)
    # news.update_state_settings(('SYSTEM', 'intermediate_topic_switch'), system_multi_hop=True)
    # news.update_state_settings(news_states.END, system_multi_hop=True)

    # external news

    # cdf.controller().add_system_transition('root', 'external_news_intro', '#GATE(external_newsv:None) #IF($news_in=True)')
    cdf.controller().add_system_transition('external_news_intro', 'external_news',
                                           '[!#SET($external_newsv=True) #SetTopicSuggestion(news) #GOAL(news) #GSRET(news_return)'
                                           '"<<news>> There is always so much news going on, it can be overwhelming to keep up with it all, you know?"]')
    cdf.controller().add_user_transition('external_news', 'external_news', '#CheckExternalComp(news)', score=0.5)
    cdf.controller().add_user_transition('external_news', 'move_on_request',
                                         '[{[not,{#EXP(like),#LEM(listen),[#EXP(want),#EXP(talk)]}],#ONT(hate)},%s] #GCOM(news)' % news_str)
    cdf.controller().add_user_transition('external_news', 'external_news_topic_switch', '/.*/ #GCOM(news)', score=0.1)
    cdf.controller().add_system_transition('news_return', 'external_news_topic_switch', '#GCOM(news)', score=0.1)
    cdf.controller().update_state_settings('external_news_topic_switch', system_multi_hop=True)
    cdf.controller().add_system_transition('external_news', 'external_news',
                                           '[!#SET($external_newsv=True) #SetTopicSuggestion(news) #GSRET(news_return)'
                                           '"<<news>> There is always so much news going on, it can be overwhelming to keep up with it all, you know?"]',
                                           score=0.5)

    cdf.controller().update_state_settings('external_news_intro', system_multi_hop=True)
    cdf.controller().update_state_settings('external_news', system_multi_hop=False, user_multi_hop=False)

    # if all planned transitions are used
    cdf.controller().add_system_transition('external_news_topic_switch', 'intermediate_topic_switch', '', score=0.0)

    add_transitions(cdf)

def add_transitions(cdf):
    
    cdf.add_system_transition('external_news_topic_switch', 'house:start', '')

    cdf.add_system_transition('external_news_topic_switch', 'worklife:start', '`You know, you seem like a pretty interesting person. `')
    cdf.add_system_transition('external_news_topic_switch', 'worklife:start->worklife:remember_is_employed_open', '', score=9.0)
    cdf.add_system_transition('external_news_topic_switch', 'worklife:start->worklife:like_job_answer', '', score=10.0)

    cdf.add_system_transition('external_news_topic_switch', 'school_new:start', '`Hey by the way, `', score=2.0)
    cdf.add_system_transition('external_news_topic_switch', 'sibling:start', '`You know, I can\'t put my finger on why, but you kind of seem like you have a sister.`')

    cdf.add_system_transition('external_news_topic_switch', 'relationships:dating', '')
    cdf.add_system_transition('external_news_topic_switch', 'relationships:dating->relationships:relationship_length', '', score=10.0)
    cdf.add_system_transition('external_news_topic_switch', 'relationships:marriage', '')
    cdf.add_system_transition('external_news_topic_switch', 'relationships:marriage->relationships:how_long_married', '', score=10.0)

    cdf.add_system_transition('external_news_topic_switch', 'baby:start', '')
    cdf.add_system_transition('external_news_topic_switch', 'baby:start->baby:asked_kids_age', '', score=10.0)

    cdf.add_system_transition('external_news_topic_switch', 'hobby:start', '')
    cdf.add_system_transition('external_news_topic_switch', 'hobby:today_flow', '')

    cdf.add_system_transition('external_news_topic_switch', 'cv_final:start', '')

    cdf.add_system_transition('external_news_topic_switch', 'movies_return:start', '', score=15.0)
    cdf.add_system_transition('external_news_topic_switch', 'pets_return:start', '', score=15.0)
    cdf.add_system_transition('external_news_topic_switch', 'baby:returning', '', score=15.0)
    cdf.add_system_transition('external_news_topic_switch', 'relationships:returning', '', score=15.0)
    cdf.add_system_transition('external_news_topic_switch', 'school_new:returning', '', score=15.0)
    cdf.add_system_transition('external_news_topic_switch', 'worklife:returning', '', score=15.0)