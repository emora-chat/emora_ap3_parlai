from emora_stdm import Macro
from emora_stdm import NatexNLU
import random

class DetectTravel(Macro):
    def __init__(self, keywords):
        self.keywords = keywords

    def run(self, ngrams, vars, args):
        match = ngrams & self.keywords
        return match


class DetectFamily(Macro):
    def __init__(self, keywords):
        self.keywords = keywords

    def run(self, ngrams, vars, args):
        match = ngrams & self.keywords
        return match


class DetectWork(Macro):
    def __init__(self, keywords):
        self.keywords = keywords

    def run(self, ngrams, vars, args):
        match = ngrams & self.keywords
        return match


class DetectSocial(Macro):
    def __init__(self, keywords):
        self.keywords = keywords

    def run(self, ngrams, vars, args):
        match = ngrams & self.keywords
        return match


class DetectVagueYes(Macro):
    def __init__(self, all_keywords):
        self.keywords = all_keywords
        self.yes = set(['sure', 'yes', 'yea', 'yup', 'yep', 'i do', 'yeah', 'okay', 'of course', 'please', 'ok'])

    def run(self, ngrams, vars, args):
        keyword_match = ngrams & self.keywords
        yes_match = ngrams & self.yes

        if len(yes_match) != 0 and len(keyword_match) == 0:
            return True
        else:
            return False


# detect location
class DetectLocation(Macro):
    def __init__(self, locations):
        self.locations = locations

    def run(self, ngrams, vars, args):
        match = ngrams & self.locations
        return match


class DummyTrue(Macro):
    def __init__(self):
        pass

    def run(self, ngrams, vars, args):
        utterance = sorted(list(ngrams), key=len, reverse=True)[0]
        return utterance


class TravelSummary(Macro):
    def __init__(self, stats):
        self.stats = stats

    def run(self, ngrams, vars, args):
        location = vars[args[0]]
        stats = self.stats[location]

        # response generation
        response = 'I believe you made the right decision. Compared to yesterday, there are {} new confirmed cases in {} with total of {} positive cases.' \
                   ' I hope travel businesses to come back to normal states soon.'.format(stats['diff_confirmed'], location, stats['confirmed_today'])
        return response


class InfoSummary(Macro):
    def __init__(self, stats):
        self.stats = stats

    def run(self, ngrams, vars, args):
        location = vars[args[0]]
        stats = self.stats[location]

        # response generation
        if stats['diff_confirmed'] > 1 or stats['diff_confirmed'] == 0:
            response = 'At {}, there are about {} confirmed and {} deaths so far. Compared to yesterday, there are {} more positive cases. '.format(location, stats['confirmed_today'], stats['deaths_today'], stats['diff_confirmed'])
        else:
            response = 'At {}, there are about {} confirmed and {} deaths so far. Compared to yesterday, there is {} more positive case. '.format(location, stats['confirmed_today'], stats['deaths_today'], stats['diff_confirmed'])
        return response


class NewsSummary(Macro):
    def __init__(self, news):
        self.news = news

    def run(self, ngrams, vars, args):
        x = random.choice(self.news)
        summary = x[0]['description']
        response = 'Hey, {}. How do you think about it'.format(summary)
        return response


class NewsResponseGenerator(Macro):
    def __init__(self):
        self.positive = ['yes', 'good', 'hope', 'like', 'great', 'nice', 'agree', 'cool', 'yeah']
        self.negative = ['no', 'not', 'nah', 'disagree', 'bad', 'awful', 'none', 'suck', 'sucks']
        self.scary = ['scary', 'shocking', 'crazy']
        self.vaccine = ['vaccine', 'cure', 'medicine']
        self.politics = ['politics', 'white house', 'government', 'trump', 'donald', 'china', 'law', 'bill', 'russia']
        self.unemployment = ['unemployment', 'job']

    def match(self, tokens, keywords):
        for x in keywords:
            if x in tokens:
                return True
        return False

    def run(self, ngrams, vars, args):
        utterance = vars[args[0]].lower()
        tokens = set(utterance.split())

        if self.match(tokens, keywords=self.negative):
            response = 'Yeah this is definitely not cool. How do you feel about listening to these bad news over and over'
        elif self.match(tokens, keywords=self.scary):
            response = 'I agree, this is very shocking. Do you think things will settle down soon'
        elif self.match(tokens, keywords=self.vaccine):
            response = 'Yeah, I do not doubt that mankind will eventually win this fight but for now we should stay safe. When do you think the real vaccine will come out'
        elif self.match(tokens, keywords=self.politics):
            response = 'Well, I believe people should stop using this virus politically. What is your opinion on this'
        elif self.match(tokens, keywords=self.unemployment):
            response = 'Yeah i know, unemployment is pretty shocking right now. How do you think about it'
        elif self.match(tokens, keywords=self.positive):
            response = 'Good to hear. Lets try our best to stay positive. Are you feeling well today'
        else:
            response = 'Okay. Do you think things will settle down soon by next couple months'
        return response



class AskSocialDistancing(Macro):
    def __init__(self, vader):
        self.vader = vader

    def run(self, ngrams, vars, args):
        utterance = vars[args[0]].lower()
        sentiment = self.vader.polarity_scores(utterance)

        if sentiment['pos'] >= 0.6:
            response = 'That is good to hear, we should stay positive and safe. Are you successfully keeping some distance from public these days'

        elif sentiment['neg'] >= 0.6:
            response = 'Dont worry, you are not the only one who is concerned. Meanwhile, we should try our best to stay safe. Are you successfully keeping some distance from public these days'

        else:
            response = 'Gotya, I hope things settle down soon. I have a quick question. I saw many people talking about public distancing in social media. Were you also following this trend recently'
        return response
