import time, random
from datetime import datetime
from collections import defaultdict
from emora.dialogue_manager_globals import *
from emora_stdm import DialogueFlow, CompositeDialogueFlow, Macro
import emora_stdm
from _globals import *

from emora._openings import _opening_manager
# from emora._activity import _activity_manager
# from emora._coronavirus import _coronavirus_manager
from emora._hobby import _hobby_manager
from emora._pets import _pets_manager
from emora._travel import _travel_manager
from emora._vr import _vr_manager
# from emora._stop import _stop_manager
from emora._flows import _system
from emora._news import _news_manager
from emora._movies import _movies_manager
from emora._music import _music_manager
from emora._sports import _sports_manager
from emora._students import _students_manager

from emora._flows._global_nlu import personal_nlu, global_update_rules, contraction_rule
from emora._openings.new_opening import IsNotLaunchRequest
from emora._hobby.hobby import ResetLoop
# from emora._stop.stop_conversation import stop_nlu, State as stop_states

class Evi(Macro):

    def run(self, ngrams, vars, args):
        if 'evi_response' in vars and len(vars['evi_response'].strip()) > 0:
            return vars['evi_response']
        return False

class ClearUponNewUser(Macro):

    def __init__(self, cdf):
        self.cdf = cdf

    def run(self, ngrams, vars, args):
        for name,component in self.cdf._components.items():
            component.set_gates(defaultdict(list))
        var_keys = list(vars.keys())
        for var in var_keys:
            if not var.startswith("_"):
                vars[var] = 'None'

QS = {'What else do you want to know?', 'What other questions do you have for me?', 'What else is on your mind?',
      'What further questions do you have?', 'What other things have you been wondering about?',
      'What else would you like to know?'}

class EndingQuestions(Macro):

    def run(self, ngrams, vars, args):
        if 'ending_question' not in vars:
            vars['ending_question'] = ''
        vars['ending_question'] = random.choice(list(QS - {vars['ending_question']}))
        return vars['ending_question']

RS = {'I\'m not sure of the right response to that.', 'That\'s a good one. I\'m not too familiar with it though.',
      'You got me with that one.', 'You have the most interesting questions. I don\'t know much about that one.'}

class EndingResponses(Macro):

    def run(self, ngrams, vars, args):
        if 'ending_response' not in vars:
            vars['ending_response'] = ''
        vars['ending_response'] = random.choice(list(RS - {vars['ending_response']}))
        return vars['ending_response']

def build_dialogue_manager(precache=True):

    cdf = _system.cdf

    macros = {"ResetLoop": ResetLoop(), "IsNotLaunchRequest": IsNotLaunchRequest(),
              "SetTopicSuggestion":SetTopicSuggestion(), "CheckExternalComp":CheckExternalComp(),
              "ChooseTransitionOut": ChooseTransitionOut(),
              "IntLessThan":IntLessThan(), 'ChooseBreakingIntro':ChooseBreakingNews(),
              "EVI":Evi(), "USERCL": ClearUponNewUser(cdf), 'EOC': EndingQuestions(), 'GIDK': EndingResponses()}

    _opening_manager.add_components_to(cdf)
    # _activity_manager.add_components_to(cdf)
    # _coronavirus_manager.add_components_to(cdf)
    _hobby_manager.add_components_to(cdf)
    _pets_manager.add_components_to(cdf)
    _travel_manager.add_components_to(cdf)
    _vr_manager.add_components_to(cdf)
    # _stop_manager.add_components_to(cdf)
    _news_manager.add_components_to(cdf)
    # _movies_manager.add_components_to(cdf)
    # _music_manager.add_components_to(cdf)
    # _sports_manager.add_components_to(cdf)
    _students_manager.add_components_to(cdf)

    # INTERMEDIATE TOPIC
    cdf.add_system_transition('intermediate_topic_switch', 'root', "")
    cdf.controller().update_state_settings('intermediate_topic_switch', system_multi_hop=True)

    # COVERED ALL TOPICS

    no_options = {
        'state': 'root',

        '`I have been having a really good time talking with you so far. So I was wondering, '
        'what questions have been on your mind the most recently?`'
        '#GATE #SET($reached_evi=True)':{
            'state': 'no_options',
            'score': 0.1,

            '{[do you, know],[have you, heard]}':{
                'score': 11,
                'state': 'check_evi'
            },

            '{#IDK,[nothing],[none],[no,#LEM(question)],[not,{got,have},{any,further,more,another,additional,#LEM(question)}]}':{
                'state': 'no_further_questions',

                '`Well, this might be a good place to end our conversation then. I am still learning a lot, '
                'and this has been one of my favorite conversations so far. I hope you had a good time too! '
                'Just say, Emora stop, to end.`':{
                    'state': 'altr_end',

                    '{#IDK,#DISAGREE}':{
                        'state': 'altr_end_n',

                        '`Okay. I mean, I am flattered that you don\'t want to stop talking. I\'m not really sure what more '
                        'to talk about though. But if you have any questions for me, I will do my best to answer them.`':
                            'no_options'
                    },

                    '<#AGREE,#TOKLIMIT(2)>': {
                        'state': 'altr_end_y',

                        '`Well, if you want to leave, just say, alexa stop.`':
                            'no_options'
                    },

                    'error': {
                        'state': 'altr_end_err',

                        '`Well, remember that if you want to stop, just say, alexa stop. I\'m not really sure what more '
                        'to talk about. But if you have any questions for me, I will do my best to answer them.`':
                            'no_options'
                    }
                }
            },

            'error':{
                'state': 'check_evi',

                '#EVI ` . ` #EOC':
                    'no_options',

                '#GIDK ` . ` #EOC': {
                    'state': 'no_options',
                    'score': 0.0
                }
            }
        },

        '`So, what other questions are you looking to answer these days?`'
        '#SET($reached_evi=True)':{
            'state': 'no_options',
            'score': 0.0
        }
    }

    cdf.controller().load_transitions(no_options,DialogueFlow.Speaker.SYSTEM)

    # no_options_choice = '[#NOT(dont like,dislike,detest,bored,uninterested,hate,dont want,not),%s]'
    # cdf.controller().add_user_transition('no_options', 'external_news', no_options_choice% _news_manager.news_str)




    # GLOBALS
    flows = list(_system.flow_components.keys())
    flows.extend('SYSTEM')
    for name,component in cdf._components.items():
        if name not in flows:
            component.load_global_nlu(personal_nlu, 5.0)
            component.load_update_rules(contraction_rule, score=999999999999)
            component.load_update_rules(global_update_rules, score=999999999)
            component._kb.load_json_file(PATHDIR.replace('__***__', '_common.json'))
            component.add_macros({'CNC': emora_stdm.CheckNotComponent(cdf)})
        component._macros.update(macros)
        component._kb.load_json_file(STOPDIR.replace('__***__', "stop_convo.json"))


    # NEED NEW VERSION OF EMORA STDM FOR THIS TO WORK
    # alexa_commands = '{#ANY($intent=User_InstructionIntent), [!/([^ ]+)?/ {alexa,computer,echo}? [!can you]?' \
    #                  '$command={' \
    #                  '[!{play,sing} [{music,song,soundtrack,record}]],' \
    #                  '[!sing [{to,for},me]],' \
    #                  'help,' \
    #                  '[!{set,turn}[{volume,sound}]],' \
    #                  '[!{volume,sound} [{up,down,#LEM(loud),#LEM(quiet)}]],' \
    #                  '[!{volume,sound} [{one,two,three,four,five,six,seven,eight,nine,max,maximum,min,minimum}]],' \
    #                  'pause,mute,unmute,louder,quieter,' \
    #                  '[!read [to,me]],' \
    #                  '[!read,me,a,{book,story,tale}],' \
    #                  'restart,' \
    #                  'can you [call],' \
    #                  'can you {update,open} [my contacts],' \
    #                  'what time is [it],' \
    #                  '[{give,want,take,send} {different,new,other} {socialbot,bot}],' \
    #                  '[!{go,open} to? {netflix,hulu,spotify,music}],' \
    #                  '[!set [{timer,alarm,an alarm,a alarm,my alarm}]]' \
    #                  '} please?]}'
    # update_rules = [
    #     (alexa_commands, '"Hmm, I am really sorry, but I actually cannot do that '
    #                      'while we are talking. If you would like, you can say Emora stop to end this conversation and '
    #                      'I will return to a point where I am able to complete your request. But I really would like to keep talking with you. " (0.1)')
    # ]
    # add_update_rules_to_components(cdf._components, update_rules)

    if precache:
        print("precaching...")
        cdf.precache_transitions()
    return cdf


def untextify_input(text):
    return ''.join((c.lower() for c in text if c.isalnum() or c == ' '))


if __name__ == '__main__':
    t = str(datetime.now()).replace(" ","_").replace(":","_")
    t = t[:t.index(".")]
    cdf = build_dialogue_manager(precache=False)

    DEBUGGING = False
    # arg_dict = {'request_type': 'LaunchRequest', "prev_conv_date": '2020-06-01 00:30:41.692568-0400',
    #         "sentiment_type": "pos", 'global_user_table_name': 'GlobalUserTableBeta',
    #             "username":"sarah", "children":"None"}
    arg_dict = {"sentiment_type": "pos", 'global_user_table_name': 'GlobalUserTableBeta'}

    turn = 0
    s = None
    while True:
        cdf.new_turn()
        if s:
            cdf.deserialize(s)

        if turn == 0:
            arg_dict['request_type'] = 'LaunchRequest'
            cdf.controller()._vars.update({key: val for key, val in arg_dict.items() if val is not None})
        else:
            arg_dict['request_type'] = 'IntentRequest'
            cdf.controller()._vars.update({key: val for key, val in arg_dict.items() if val is not None})

        input_text = input("U: ")

        start = time.time()
        print('ORIGINAL:', cdf.state())
        cdf.controller().set_speaker(DialogueFlow.Speaker.USER)
        cdf.user_turn(untextify_input(input_text), debugging=DEBUGGING)
        print('AFTER USER:', cdf.state())
        cdf.controller().set_speaker(DialogueFlow.Speaker.SYSTEM)
        response = cdf.system_turn(debugging=DEBUGGING)
        print('AFTER SYSTEM:', cdf.state())
        s = cdf.serialize()
        print('Serialization', '*'*80)
        print(s)
        print('*'*80)
        print("S: " + response)
        print("[{:.2f}]".format(time.time()-start))
        turn += 1








