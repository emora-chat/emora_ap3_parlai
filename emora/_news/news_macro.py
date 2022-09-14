from emora_stdm import Macro
from emora_stdm import NatexNLU

import pandas as pd
import numpy as np
import os, json, random
from pprint import pprint
import traceback
import random
from _globals import NEWSDIR

generic_acknowledgements = ['Right. I see. ', 'Oh. ok. ', 'Hmmm. ', 'I see. ']

class NewsBriefing():
    def __init__(self):
        self.path = NEWSDIR.replace('__***__','data')
        self.news = json.load(open(os.path.join(self.path,"news_briefing_short.json"), "r"))

class GetNews(Macro):
    def __init__(self, news):
        self.news = news
        self.intro_templates = ["I read in the news that ", "I read that ", "I learned that ",
                                "I saw in the news that ", "On {0}, {1} reported that "]
        self.number_of_news = len(self.news)

    def run(self, ngrams, vars, args):
        # pprint(vars)
        if 'told_news' not in vars:
            vars['told_news'] = 0
            vars['max_news'] = self.number_of_news
        index = vars['told_news']
        vars['told_news'] += 1
        if index < self.number_of_news:
            return f"{self.intro_templates[index%len(self.intro_templates)].format(self.news[index]['date'], self.news[index]['source'])}{self.news[index]['summary']}. {self.news[index]['follow_up_question']}"
        elif index == self.number_of_news:
            return f"What else would you like to talk about?"
        else:
            return f"I am sorry I don't have any more news updates. What else would you like to chat about?"

class AcknowledgeUsersNo(Macro):
    def __init__(self, news):
        self.news = news
        self.number_of_news = len(self.news)

    def run(self, ngrams, vars, args):
        index = vars['told_news']-1
        if index < self.number_of_news:
            if len(self.news[index]['follow_up_response_for_no']) > 0:
                return self.news[index]['follow_up_response_for_no']
            else:
                return generic_acknowledgements[index%len(generic_acknowledgements)]
        else:
            return f""

class AcknowledgeUsersYes(Macro):
    def __init__(self, news):
        self.news = news
        self.number_of_news = len(self.news)

    def run(self, ngrams, vars, args):
        index = vars['told_news']-1
        print('index:', index)
        if index < self.number_of_news:
            return f"{self.news[index]['follow_up_response_for_yes']}."
        else:
            return f""

class GetGenericAcknowledgement(Macro):
    def __init__(self):
        pass

    def run(self, ngrams, vars, args):
        return random.choice(generic_acknowledgements)