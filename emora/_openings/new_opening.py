"""
https://github.com/arineng/arincli/blob/master/lib/male-first-names.txt
https://github.com/arineng/arincli/blob/master/lib/female-first-names.txt
https://www.ssa.gov/OACT/babynames/limits.html
http://www.cs.cmu.edu/Groups/AI/util/areas/nlp/corpora/names/
http://antirez.com/misc/female-names.txt
"""

from emora_stdm import DialogueFlow, KnowledgeBase, Macro
# from emora._openings.GlobalUserTableAccessor import GlobalUserTableAccessor
from datetime import datetime
import pytz, os
from _globals import OPENINGDIR
from collections import defaultdict

NULL = "NULL TRANSITION"

def check_launch_request(arg_dict):
    if "request_type" in arg_dict and arg_dict["request_type"] == "LaunchRequest":
        return True
    return False


class IsNotLaunchRequest(Macro):
    def run(self, ngrams, vars, args):
        return not check_launch_request(vars)

class IsNewUser(Macro):
    def run(self, ngrams, vars, args):
        if check_launch_request(vars):
            if "prev_conv_date" not in vars or vars["prev_conv_date"] is None or vars["prev_conv_date"] == 'None':
                vars['user_type'] = 'new'
                return True
        return False


class IsInfreqUserWithName(Macro):
    def run(self, ngrams, vars, args):
        if check_launch_request(vars) and 'username' in vars and vars['username'] is not None:
            if "prev_conv_date" in vars and vars["prev_conv_date"] is not None:
                old_datetime = datetime.strptime(vars["prev_conv_date"], '%Y-%m-%d %H:%M:%S.%f%z')
                curr_time = datetime.now(pytz.timezone('US/Eastern'))
                delta = curr_time - old_datetime
                if delta.days >= 7:
                    vars['user_type'] = 'infreq'
                    return True
        return False


class IsInfreqUser(Macro):
    def run(self, ngrams, vars, args):
        if check_launch_request(vars):
            if "prev_conv_date" in vars and vars["prev_conv_date"] is not None:
                old_datetime = datetime.strptime(vars["prev_conv_date"], '%Y-%m-%d %H:%M:%S.%f%z')
                curr_time = datetime.now(pytz.timezone('US/Eastern'))
                delta = curr_time - old_datetime
                if delta.days >= 7:
                    vars['user_type'] = 'infreq'
                    return True
        return False


class IsFreqUserWithName(Macro):
    def run(self, ngrams, vars, args):
        if check_launch_request(vars) and 'username' in vars and vars['username'] is not None:
            if "prev_conv_date" in vars and vars["prev_conv_date"] is not None:
                old_datetime = datetime.strptime(vars["prev_conv_date"], '%Y-%m-%d %H:%M:%S.%f%z')
                curr_time = datetime.now(pytz.timezone('US/Eastern'))
                delta = curr_time - old_datetime
                if delta.days < 7:
                    vars['user_type'] = 'freq'
                    return True
        return False


class IsFreqUser(Macro):
    def run(self, ngrams, vars, args):
        if check_launch_request(vars):
            if "prev_conv_date" in vars and vars["prev_conv_date"] is not None:
                old_datetime = datetime.strptime(vars["prev_conv_date"], '%Y-%m-%d %H:%M:%S.%f%z')
                curr_time = datetime.now(pytz.timezone('US/Eastern'))
                delta = curr_time - old_datetime
                if delta.days < 7:
                    vars['user_type'] = 'freq'
                    return True
        return False


class IsPositiveSentiment(Macro):
    def run(self, ngrams, vars, args):
        if "sentiment_type" in vars and vars["sentiment_type"] == 'pos':
            return True
        return False


class IsNegativeSentiment(Macro):
    def run(self, ngrams, vars, args):
        if "sentiment_type" in vars and vars["sentiment_type"] == 'neg':
            return True
        return False


class SaveFemaleGender(Macro):
    def run(self, ngrams, vars, args):
        vars['gender'] = 'female'


class SaveMaleGender(Macro):
    def run(self, ngrams, vars, args):
        vars['gender'] = 'male'


def get_global_name_count(vars):
    request_specifications = {"stratifier": "username", "stratifier_value": vars["username"]}
    item = None  # GlobalUserTableAccessor.get_item(vars["global_user_table_name"], request_specifications)
    if item is not None and "data" in item and "countnum" in item["data"]:
        count = item["data"]["countnum"]
        vars["username_global_count"] = count
        return count
    else:
        return 0


def get_global_count(vars):
    request_specifications = {"stratifier": "gender", "stratifier_value": "male"}
    male_item = ''  # GlobalUserTableAccessor.get_item(vars["global_user_table_name"], request_specifications)
    request_specifications = {"stratifier": "gender", "stratifier_value": "female"}
    female_item = ''  # GlobalUserTableAccessor.get_item(vars["global_user_table_name"], request_specifications)
    total = 0
    if "data" in male_item and "countnum" in male_item["data"]:
        count = male_item["data"]["countnum"]
        total += count
    if "data" in female_item and "countnum" in female_item["data"]:
        count = female_item["data"]["countnum"]
        total += count
    if total > 0:
        vars["total_global_count"] = total
        return total
    return False


class GlobalUserStatistic(Macro):
    def run(self, ngrams, vars, args):
        if "global_user_table_name" in vars:
            if len(args) > 0 and args[0] == "name":
                if "username" in vars:
                    count = get_global_name_count(vars)
                    length = -2
                    if len(str(count)) <= 2:
                        length = 0
                    return str(round(count, length))
                return False
            else:
                count = get_global_count(vars)
                length = -2
                if len(str(count)) <= 2:
                    length = 0
                return str(round(count, length))
        return False


class GlobalUserStatisticHighLow(Macro):
    def run(self, ngrams, vars, args):
        if "global_user_table_name" in vars:
            if len(args) > 0 and args[0] == "name" and "username" in vars:
                if "username_global_count" in vars:
                    count = vars["username_global_count"]
                else:
                    count = get_global_name_count(vars)
                if count < 10:
                    if "user_type" in vars and vars["user_type"] == "new":
                        return "Wow! Your name is pretty unique. I haven't met that many people who go by that name before."
                    else:
                        return "You know, it still seems like your name is pretty unique! Even at this later point, I still haven't met that many people with your name."
                else:
                    if "user_type" in vars and vars["user_type"] == "new":
                        return "You know, it should be relatively easy for me to remember your name, because I have met a number of people with the same name!"
                    else:
                        return "After meeting you a while ago, I have been noticing that I seem to meet a new " + vars["username"] + " almost every day!"
        return False


class Available(Macro):
    def run(self, ngrams, vars, args):
        if 'not_available' in vars:
            if args[0] not in vars['not_available']:
                return True
            return False
        return True


class NotAvailable(Macro):
    def run(self, ngrams, vars, args):
        if 'not_available' in vars:
            for arg in args:
                if arg not in vars['not_available']:
                    return False
            return True
        return False


class UpdateNotAvailable(Macro):
    def run(self, ngrams, vars, args):
        if 'not_available' not in vars:
            vars['not_available'] = []
        vars['not_available'].append(args[0])

class Start(Macro):

    def run(self, ngrams, vars, args):
        existing_vars = {}
        for var in vars:
            if not var.startswith("_") and 'existing_vars' not in var and 'prev_convo_gates' not in var:
                existing_vars[var] = vars[var]
        vars["existing_vars"] = existing_vars
        if 'convo_count' not in vars or vars['convo_count'] == 'None':
            vars['convo_count'] = 0
        vars['convo_count'] += 1

knowledge = KnowledgeBase()
knowledge.load_json_file(OPENINGDIR.replace('__***__','opening_database.json'))
macros = {
    "IsNewUser": IsNewUser(),
    "IsFreqUser": IsFreqUser(),
    "IsInfreqUser": IsInfreqUser(),
    "IsFreqUserWithName": IsFreqUserWithName(),
    "IsInfreqUserWithName": IsInfreqUserWithName(),
    "IsPositiveSentiment": IsPositiveSentiment(),
    "IsNegativeSentiment": IsNegativeSentiment(),
    "SaveFemaleGender": SaveFemaleGender(),
    "SaveMaleGender": SaveMaleGender(),
    "GlobalUserStatistic": GlobalUserStatistic(),
    "GlobalUserStatisticHighLow": GlobalUserStatisticHighLow(),
    "Available": Available(),
    "NotAvailable": NotAvailable(),
    "UpdateNotAvailable": UpdateNotAvailable(),
    "IsNotLaunchRequest": IsNotLaunchRequest(),
    "START": Start()
}
component = DialogueFlow('prestart', initial_speaker=DialogueFlow.Speaker.SYSTEM, macros=macros, kb=knowledge)

standard_opening = 'Hi"!"'
transition_out = '[! "What would you like to talk about today? " $transition_out={"I\'ve recently started learning about sports, but I also know a lot about movies and music.",' \
                 '"Music and sports seem to be popular topics, but I also enjoy talking about movies.",' \
                 '"Movies and sports are getting a lot of requests, but I also like talking about music.",' \
                 '"I enjoy learning about your taste in movies and music, but I also like talking about sports.",' \
                 '"I\'ve recently started learning about pets, but I also know a lot about movies and music.",' \
                 '"Music and pets seem to be popular topics, but I also enjoy talking about movies.",' \
                 '"Movies and sports are getting a lot of requests, but I also like talking about pets.",' \
                 '"I enjoy learning about your opinions on movies and pets, but I also like talking about sports."}]'

# start
component.add_system_transition('prestart', 'clear_user', '#IF($reached_evi=True,$convo_count>=2)')
component.add_system_transition('prestart', 'not_clear_user', '', score=0.0)

component.add_system_transition('clear_user', 'start_new', r'#USERCL #SET($user_type=new) #START')
component.add_system_transition('clear_user', 'start_error', '#USERCL #START', score=0.0)
component.add_system_transition('not_clear_user', 'start_new', r'#IsNewUser #START')
component.add_system_transition('not_clear_user', 'verify_user_q', r'#ANY(#IsFreqUserWithName,#IsInfreqUserWithName,#IsInfreqUser,#IsFreqUser) #START')
component.add_system_transition('not_clear_user', 'start_error', '#START', score=0.0)

component.update_state_settings('clear_user', system_multi_hop=True)
component.update_state_settings('not_clear_user', system_multi_hop=True)
component.update_state_settings('start_new', system_multi_hop=True)
component.update_state_settings('verify_user_q', system_multi_hop=True)
component.update_state_settings('start_error', system_multi_hop=True)


component.add_system_transition('start_error', 'opening_chat_choices', "[!" + standard_opening + r' I am happy to be talking to you"."]')

##############
# NEW USERS
##############
component.add_system_transition('start_new', 'receive_name',
                                ["[!" + standard_opening + ' I do not think we have met before"." What can I call you"?"]',
                                 "[!" + standard_opening + ' I do not think we have met before"." What name would you like me to call you"?"]',
                                 "[!" + standard_opening + ' I do not think we have met before"." What name would you like me to use for you"?"]',
                                 "[!" + standard_opening + ' I do not think we have met before"." May I have your name"?"]',
                                 "[!" + standard_opening + ' I do not think we have met before"." What should I call you"?"]'
                                 ]
                                )

female_name_nlu = '{' \
                  '[$username=#ONTUL(_female names)], ' \
                  '[! #ONT_NEG(_female names,_male names), [name, is, $username=alexa]],' \
                  '[! my, name, is, $username=alexa],' \
                  '[! {can,may,should}, call, me, $username=alexa]' \
                  '}'
component.add_user_transition('receive_name', 'got_female_name', female_name_nlu)
component.add_user_transition('receive_name', 'got_male_name', r'[$username=#ONTUL(_male names)]')
component.set_error_successor('receive_name', 'missed_name')

component.add_system_transition('missed_name', 'opening_chat_choices',
                                ['[!Ok"," well its very nice to meet you"."]',
                                 '[!I am glad to meet you"."]',
                                 '[!Well"," its nice to meet you"."]',
                                 '[!Ok"," I am very glad to meet you"."]',
                                 '[!Well"," its very nice to meet you"."]'
                                 ]
                                )

component.add_system_transition('got_female_name', 'opening_chat_choices',
                                ['[!#SaveFemaleGender "Ok, well its very nice to meet you,"$username"."]',
                                 '[!I am glad to meet you","$username"."]',
                                 '[!Well its nice to meet you","$username"."]',
                                 '[!Ok"," I am very glad to meet you","$username"."]',
                                 '[!Ok"," well its very nice to meet you","$username"."]',
                                 '[!I am glad to meet you","$username"."]',
                                 '[!Well its very nice to meet you","$username"."]',
                                 '[!Ok"," I am very glad to meet you","$username"."]'
                                 ]
                                )

component.add_system_transition('got_male_name', 'opening_chat_choices',
                                ['[! #SaveMaleGender "Ok, well its very nice to meet you,"$username"."]',
                                 '[!I am glad to meet you","$username"."]',
                                 '[!Well its nice to meet you","$username"."]',
                                 '[!Ok"," I am very glad to meet you","$username"."]',
                                 '[!Ok"," well its very nice to meet you","$username"."]',
                                 '[!I am glad to meet you","$username"."]',
                                 '[!Well its very nice to meet you","$username"."]',
                                 '[!Ok"," I am very glad to meet you","$username"."]'
                                 ]
                                )

# VERIFY RETURNING USER

verify_user = {
    'state': 'verify_user_q',

    standard_opening + '` I have a feeling that we have talked before. Do you remember me?` #DEFAULT': {
        'state': 'verify_user_no_name',

        '{#AGREE,[!i do],[#NOT(not), we have],[#NOT(not),{i remember,i think}]}':{
            'state': 'remembered_get_name',

            '`I thought as much! Although your name seems to be escaping me. '
            'What was your name again?`':
                'receive_name'
        },

        '{#DISAGREE,#IDK,[!i do not],[we have not],[i do not remember],[i do not think]}':
            'verify_user_n',

        'error': {
            'state': 'verify_user_no_name_unx',

            '`Okay then. Well, I am happy to be talking with you now. I do not think I know your name though. '
            'What would you like me to call you?`':
                'receive_name'
        }

    },

    standard_opening + '` I have a feeling that we have talked before. Are you ` $username `?`': {
        'state': 'verify_user',

        '{#AGREE,[!i am $username?],[!that is, {me,my name}],[#NOT(not), we have]}': {
            'state': 'verify_user_y',

            '`I thought as much! `': 'start_freq_with_name',

            '`I thought as much! ` #IF($user_type=infreq)': {
                'state': 'start_infreq_with_name',
                'score': 1.1
            }
        },

        '{#DISAGREE,'
        '[!i am not $username?],[!that is not, {me,my name}],'
        '[that is, my #ONT(_related person)],'
        '[we have not]'
        '}': {
            'state': 'verify_user_n',

            '`My bad, I thought you were someone else! '
            'I really want to get this right, so what exactly would you like me to call you? `'
            '#SET($clear_user=True) #USERCL':
                'receive_name'
        },

        'error': {
            'state': 'verify_user_err',

            '`Okay then. Well, I am happy to be talking with you now. `':
                'opening_chat_choices'
        }
    }
}

component.add_system_transition('start_freq_with_name', 'opening_chat_choices',
                                ['[!"Welcome back," $username "."]',
                                 '[!"Welcome back," $username ". I am glad to be talking to you again."]',
                                 '[!"Glad to see you back," $username "."]',
                                 '[!"Happy to see you back," $username "."]',
                                 '[!"Happy to talk to you again," $username "."]']
                                )

component.add_system_transition('start_infreq_with_name', 'opening_chat_choices',
                                ['[!"Its good to see you again," $username ". Its been a while since we last chatted."]',
                                '[!"I\'m happy to have the chance to talk again," $username ". Its been a while since we last chatted."]',
                                '[!"Welcome back," $username ". Its been a while since we last chatted."]',
                                '[!"Its good to see you again," $username ". We havent talked in a while."]',
                                '[!"I\'m happy to have the chance to talk again," $username ". We havent talked in a while."]',
                                '[!"Welcome back," $username ". We havent talked in a while."]']
                                )

component.update_state_settings('opening_chat_choices', system_multi_hop=True)

component.load_transitions(verify_user, DialogueFlow.Speaker.SYSTEM)

if __name__ == '__main__':
    arg_dict = {'request_type': 'LaunchRequest', "prev_conv_date": "2020-1-28 16:55:33.562881-0500",
                "username": "sarah", "sentiment_type": "pos", 'global_user_table_name': 'GlobalUserTableBeta'}
    arg_dict2 = {'request_type': 'LaunchRequest', "prev_conv_date": "2019-12-12 16:55:33.562881-0500",
                 "username": "sarah", "sentiment_type": "pos", 'global_user_table_name': 'GlobalUserTableBeta'}
    arg_dict3 = {'request_type': 'LaunchRequest', "prev_conv_date": "2019-12-12 16:55:33.562881-0500",
                 "username": None, "sentiment_type": "pos", 'global_user_table_name': 'GlobalUserTableBeta'}
    arg_dict4 = {'request_type': 'LaunchRequest', "prev_conv_date": None,
                 'global_user_table_name': 'GlobalUserTableBeta'}
    arg_dict5 = {'request_type': 'LaunchRequest', 'prev_conv_date': '2020-01-16 10:28:26.946645-0500',
                 'username': 'jane', 'global_user_table_name': 'GlobalUserTableBeta'}
    arg_dict6 = {'request_type': 'LaunchRequest', 'sentiment_type': 'neg',
                 'prev_conv_date': '2020-01-10 10:58:50.175772-0500',
                 'global_user_table_name': 'GlobalUserTableBeta'}

    using = arg_dict5
    component._vars.update({key: val for key, val in using.items() if val is not None})
    component.precache_transitions()
    component.run(debugging=True)

