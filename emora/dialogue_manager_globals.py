from emora_stdm import Macro
from emora_stdm.state_transition_dialogue_manager.natex_nlu import NatexNLU
import random

# Macros

# class SetTrue(Macro):
#     def run(self, ngrams, vars, args):
#         vars[args[0]] = True


class SetTopicSuggestion(Macro):
    def run(self, ngrams, vars, args):
        vars['dm_suggested_topic'] = str(args[0])


class CheckExternalComp(Macro):
    def run(self, ngrams, vars, args):
        if 'chosenModule' in vars:
            if vars['chosenModule'] == args[0]:
                return True
        return False


TRANSITIONS = {"Music and sports seem to be popular topics, but I also enjoy talking about movies.",
               "Movies and sports are getting a lot of requests, but I also like talking about music.",
               "I enjoy learning about your taste in movies and music, but I also like talking about sports.",
               "I\'ve recently started learning about pets, but I also know a lot about movies and music.",
               "Music and pets seem to be popular topics, but I also enjoy talking about movies.",
               "Movies and sports are getting a lot of requests, but I also like talking about pets.",
               "I enjoy learning about your opinions on movies and pets, but I also like talking about sports.",
                "I\'ve recently started learning about different cities, but I also know a lot about movies and music.",
               "Music and pets seem to be popular topics, but I also enjoy talking about travelling.",
               "Virtual reality and sports are getting a lot of requests, but I also like talking about music.",
               "I enjoy learning about your opinions on virtual reality and movies, but I also like talking about sports."
               }


class ChooseTransitionOut(Macro):
    def run(self, ngrams, vars, args):
        opts = TRANSITIONS
        if 'transition_out' in vars:
            opts = opts - {vars['transition_out']}
        return random.choice(tuple(opts))


# MOVEON = {'You seem to want to change topics. I am happy to do so with you. ',
#           'You want to be done with this topic already? Well, alright. Let\'s talk about something else then. ',
#           'Ok, I am getting that sense that you want to move on from this topic. I am more than happy to talk about something different with you. '}
# SHORT_MOVEON = {'Okay,', 'Well, ', 'Well, ok.'}
#
#
# class ChooseMoveOn(Macro):
#     def run(self, ngrams, vars, args):
#         if 'move_on_count' not in vars:
#             vars['move_on_count'] = 0
#         vars['move_on_count'] += 1
#         if vars['move_on_count'] < 2:
#             opts = MOVEON
#         else:
#             opts = SHORT_MOVEON
#         if 'move_on_utt' in vars:
#             opts = opts - {vars['move_on_utt']}
#         return random.choice(tuple(opts))

BREAKING_INTRO = {'I just found out about this really cool thing I want to share with you. ',
                  'Oh, I don\'t know if you heard about this already. ',
                  'Hey, you know what, this is a pretty cool thing I just learned. '}
class ChooseBreakingNews(Macro):
    def run(self, ngrams, vars, args):
        opts = BREAKING_INTRO
        if 'breaking_news_intro' in vars:
            opts = opts - {vars['breaking_news_intro']}
        return random.choice(tuple(opts))


class IntLessThan(Macro):
    def run(self, ngrams, vars, args):
        if args[0] in vars and args[1] in vars:
            lhs = int(vars[args[0]])
            rhs = int(vars[args[1]])
            if lhs < rhs:
                return True
            else:
                return False
        return True