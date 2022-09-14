
import json
import os
import traceback
import re
import os,sys,inspect

import datetime
import nltk
# import spacy

# from RemoveSpecialCase import clean_text

# current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parent_dir = os.path.dirname(current_dir)
# sys.path.insert(0, parent_dir)

# from Sounds import Sounds
import feedparser
# from EntityIndex import EntityIndex
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import OrderedDict
stops = set(stopwords.words('english'))
# from GoogleTrends import GoogleTrends


# entityIndex = EntityIndex()
# google_trends = GoogleTrends()

#import Intents
#from Intents import Topics, Intents

class Topics:
    YES = '__label__yes'  #ours
    NO = '__label__no'   #ours
    STOP = '__label__stop'  #ours includes "i am tired of you", i want to stop talking
    GREETING = '__label__greeting'  #ours
    JOKE = '__label__joke'  #ours
    NEWS = '__label__news'  #ours
    CHAT = '__label__chitchat'   #ours: general chat, not specific topic?
    EVI = '__label__EVI'   # ###NOT USED
    MOVIE = '__label__movie'  #ours OR amazon?
    FOOD = '__label__food'  #ours  + AMAZON should check if need to add Amazon
    HOWTO = '__label__howto'  #ours
    FITNESS = '__label__fitness'  #ours exercise
    OPINION = '__label__opinion'  ####MOVED TO INTENT
    SPORTS = '__label__sports'  #ours OR amazon?
    MUSIC = '__label__music'  #ours
    WEATHER = '__label__weather'  #ours OR amazon
    CELEBS = '__label__celebrities'  #ours
    FACTS = '__label__wikipedia' #ours
    FASHION = '__label__fashion'  #ours
    ATTRACTIONS = '__label__attraction'  #ours + amazon?
    LITERATURE = '__label__literature' #not working  only Amazon
    EDUCATION = "__label__education"  #get from Amazon
    PETSANIMALS = "__label__pets_animals" #get from amazon
    POLITICS = "__label__politics"  #get from amazon
    SCITECH = "__label__scitech" #get from Amazon
    BUSINESS = "__label__business" #amazon
    DRUG = "__label__drug"  #amazon -- maybe ours (add list of common medicine
    GAMES = "__label__games" #amazon
    HEALTH = "__label__health" #amazon  disease
    HISTORY = "__label__history" #amazon
    MATH = "__label__math" #amazon
    SHOPPING = "__label__shopping" #amazon
    RELIGION = "__label__religion" #amazon
    PSYCHOLOGY = "__label__psychology" #amazon
    ARTEVENT = "__label__art_event" #amazon
    RELATIONSHIP = "__label__relationship" #amazon
    WORLDCUP = "__label__worldcup" # worldcup
    CARS = "__label__cars"  # cars
    OPENING= "Greetings and small talk",
    SUICIDE="Talk about emotions",  # actual suicide
    EMOTIONALSUPPORT="Talk about emotions",
    GREETING="Greetings and small talk",
    OTHER= "Other topics"


TopicNames = {
    Topics.JOKE: 'Jokes',  # ours
    Topics.NEWS : 'News',  # ours
    Topics.CHAT : 'Small talk',  # ours: general chat, not specific topic?
    Topics.MOVIE : 'Movies and Shows',  # ours OR amazon?
    Topics.FOOD : 'Food and Restaurants',  # ours  + AMAZON should check if need to add Amazon
    Topics.HOWTO : 'Advice and Instructions',  # ours
    Topics.FITNESS : 'Exercise and Fitness',  # ours exercise
    Topics.OPINION : 'Personal Opinions',  ####MOVED TO INTENT
    Topics.SPORTS : 'Sports',  # ours OR amazon?
    Topics.MUSIC : 'Music and Concerts',  # ours
    Topics.WEATHER : 'Weather',  # ours OR amazon
    Topics.CELEBS : 'People',  # ours
    Topics.FACTS : 'Interesting facts',  # ours
    Topics.FASHION : 'Fashion',  # ours
    Topics.ATTRACTIONS : 'Travel and Tourism',  # ours + amazon?
    Topics.LITERATURE : 'Literature',  # not working  only Amazon
    Topics.EDUCATION : "Education",  # get from Amazon
    Topics.PETSANIMALS : "Animals",  # get from amazon
    Topics.POLITICS : "Politics",  # get from amazon
    Topics.SCITECH : "Science and Technology",  # get from Amazon
    Topics.BUSINESS : "Business news",  # amazon
    Topics.DRUG : "Medicine",  # amazon -- maybe ours (add list of common medicine
    Topics.GAMES : "Video Games",  # amazon
    Topics.HEALTH : "Health",  # amazon  disease
    Topics.HISTORY : "History",  # amazon
    Topics.MATH : "Math",  # amazon
    Topics.SHOPPING : "Shopping",  # amazon
    Topics.RELIGION : "Religion",  # amazon
    Topics.PSYCHOLOGY : "Psychology",  # amazon
    Topics.ARTEVENT : "Events and Shows",  # amazon
    Topics.RELATIONSHIP : "Relationships",  # amazon
    Topics.WORLDCUP : "Worldcup",  # worldcup
    Topics.CARS : "Cars",  # cars
    Topics.OPENING: "Greetings and small talk",
    Topics.SUICIDE: "Talk about emotions",  # actual suicide
    Topics.EMOTIONALSUPPORT:"Talk about emotions",
    Topics.GREETING: "Greetings and small talk",
    Topics.OTHER: "Other topics",
    "__label__WORLDNEWS": "World News",
    "__label__USNEWS": "U.S. Domestic News"
}



GeneralNewsFeeds = {
    Topics.NEWS:['http://feeds.reuters.com/reuters/topNews', 'http://rss.cnn.com/rss/cnn_topstories.rss'],
}
#more feeds available
#https://www.reuters.com/tools/rss
NewsSummaryFeeds={
    Topics.NEWS:['http://feeds.reuters.com/reuters/topNews', 'http://rss.cnn.com/rss/cnn_topstories.rss'],
    Topics.CELEBS:['http://feeds.reuters.com/reuters/peopleNews'],
    Topics.SPORTS:['http://feeds.reuters.com/reuters/sportsNews'],
    Topics.BUSINESS:['http://feeds.reuters.com/reuters/businessNews'],
    Topics.ARTEVENT:['http://feeds.reuters.com/news/artsculture', 'http://feeds.reuters.com/reuters/entertainment'],
    Topics.POLITICS:['http://feeds.reuters.com/Reuters/PoliticsNews'],
    Topics.SCITECH: ['http://feeds.reuters.com/reuters/scienceNews',
                     'http://feeds.reuters.com/reuters/technologyNews', ],
    Topics.HEALTH:['http://feeds.reuters.com/reuters/healthNews',''],
    Topics.RELATIONSHIP:['http://feeds.reuters.com/reuters/lifestyle'],
    Topics.FOOD:['https://www.health.com/nutrition/feed', 'https://www.health.com/food/feed'],
    Topics.CARS:['http://rss.nytimes.com/services/xml/rss/nyt/Automobiles.xml'],
    Topics.EDUCATION:['https://www.realwire.com/rss/?id=237&row=&view=Synopsis','https://www.realwire.com/rss/?id=599&row=&view=Synopsis'],
    #Topics.FITNESS:['https://www.mensjournal.com/health-fitness/rss/'],
    Topics.PSYCHOLOGY: ['https://psychcentral.com/news/feed'],
    Topics.LITERATURE:['https://www.newyorker.com/feed/books'],
    Topics.ATTRACTIONS:['http://rss.cnn.com/rss/cnn_travel.rss','http://feeds.feedburner.com/breakingtravelnews/news/tourism'],
    Topics.FASHION:['https://www.instyle.com/feeds/all/ins.rss','https://wwd.com/custom-feed/fashion/'],
    #Topics.FACTS:['https://www.factcheck.org/feed/'],
    "__label__USNEWS": ['http://feeds.reuters.com/Reuters/domesticNews'],
    "__label__WORLDNEWS":['http://feeds.reuters.com/Reuters/worldNews']
}

def crawlFeeds(feedDict):
    result = {}

    for topic, urls in feedDict.items():

        result[topic] = list()
        for url in urls:
            try:
                d = feedparser.parse(url)
                try:
                    for post in d.entries:
                        # print post
                        if 'summary' in post:
                            summary = post['summary']
                        elif 'value' in post:
                            summary = post['summary']
                        else:
                            continue
                        summary = summary.split("<")[0]
                        # summary = clean_text(summary, ssml=False)


                        if 'link' in post:
                            link = post['link']
                        else:
                            link = ""

                        if 'published' in post:
                            date = post['published']
                        else:
                            date = ""

                        if 'title' in post:
                            title = post['title']
                        else:
                            title = ""

                        story = {
                            'title': title,
                            'summary':summary,
                            'url':link,
                            'date':date
                        }
                        result[topic].append(story)
                except:
                    pass

            except:
                traceback.print_exc()

    return result

# sounds = Sounds()

def makeSummary(headlines, topic = None, limit=1600, storyLen=150, maxStories=5, preface = ""):
    numTokens=5
    numStories = 0
    entities = list()

    tokenSet = {} #want to diversify summary - if too much overlap, skip


    res = preface + " "
    for story in headlines[topic]:
        if 'summary' not in story or len(story['summary'])<20:
            continue

        if len(res)>=limit:
            break

        summary = story['summary']

        summary=re.sub(r'\<.*?\>', ' ', summary)
        summary = re.sub(r'\s+', ' ', summary)

        if len(summary) > storyLen:
            pos = summary.find(".", storyLen)
            chopped = summary
            if pos >=0:
                chopped = summary[:pos]
            #else:
            #    pos = summary.find(", ", storyLen)
            #    if pos>=0:
            #        summary = summary[:pos] + "."
            if len(chopped)> storyLen+50:
                continue
            #summary = summary.strip() + ". "
            summary=chopped
        try:
            overlap = 0
            tokens = nltk.tokenize.casual.casual_tokenize(summary)
            prefix = ""
            lemmas = list()
            end_cap = -1

            for i in range(0, min(len(tokens), numTokens)):
                if tokens[i][0].isupper():
                    end_cap = summary.find(tokens[i])+len(tokens[i])

                prefix = prefix + " " + tokens[i]
                lemma = tokens[i].lower().strip()
                lemmas.append(lemma)

            for lemma in lemmas:
                if lemma in tokenSet:
                    overlap+=1
            if overlap >=3:
                # print "repeated story skipped: " + summary
                continue #

            for lemma in lemmas:
                tokenSet[lemma]=1

            prefix = prefix.strip()
            foundEntity = None
            #longest_match = ""
            if len(prefix) < 2:
                continue
            ents = entityIndex.get_all_entities(prefix)
            if not ents: continue
            # inks': [{u'Lord of the Rings': {'score': 1.0,
            entities_response = entityIndex.get_all_entities(prefix)
            # pprint(entities_response)
            spots = []
            for text in entities_response:
                for link in text['links']:
                    for key in link:
                        # print link[key]
                        if link[key]['score'] > 0.0:
                            for d_type in link[key]['types']:
                                if d_type['type'] in ['wp_location','wp_person','wp_organization'] and link[key]['score'] == 1.0:
                                    if key.lower() not in spots:
                                        spots.append(key.lower())
                                    break

                                # if self.id_regex.match(d_type['id']):
                                #     entity_ids.append(d_type['id'])
            # spots = [x for x in google_trends.get_trends() if x in prefix] + spots

            for entry in ents:
                for ent, scores in entry['links'][0].items():
                    if scores['score'] == 1.0 and len(ent) > 1 and ent not in stops:
                        foundEntity = ent
                        if ent not in entities:
                            entities.append(ent)
                        #print entry
                        foundEntity = True
                        break

            res = res + " " + sounds.pause(250)

            if end_cap>0 and end_cap > 3:
                entity = summary[:end_cap]
                entities.append(entity)
                summary = sounds.emphasis( entity ) + ", " + sounds.rate( summary[end_cap+1:], 1.05)
            else:
                summary = sounds.rate( summary[end_cap+1:], 1.05)
            numStories +=1
            res = res + " " + summary
            if len(res) > limit or numStories >= maxStories: break
        except:
            traceback.print_exc()
            continue

        #if not foundEntity:
        #    continue
        #if foundEntity is not None and foundEntity in entities:
        #    continue #probably same/similar story

    if numStories < 3:
        return None, list()
    res = res + sounds.pause(250) + ", "# + " " + sounds.whew
    #if entities and len(entities)>0:
    #res = res + " Would you like to hear more about any of these or other topics?"
        #for i in range (0, min( len(entities), 3 )):
        #    if i==0: res = res + entities[i]
        #    elif i>0 and i < len(entities)-1: res = res + ", " + entities[i]
        #    elif i==min( 2, len(entities)-1): res = res + ", or " + entities[i]
        #    i+=1
        #    if i>=3: break
    # res = clean_text(res, ssml=False)
    entities = sorted(spots, key=lambda k: len(k.split()), reverse=True)
    entities = [x.lower() for x in entities]
    entities = list(set(entities))
    return res, entities

#main: crawl RSS feeds
if True:
    stories = crawlFeeds(NewsSummaryFeeds)
    # j = json.dumps(stories, indent=4)
    # json.dump(stories, open("news-feeds-data.json", "w"))
    open("news-feeds-data.json", "w").write(json.dumps(stories, indent=4))
    f2 = open("/usr/news_data/news-feeds-data.json", 'w')
    json.dump(stories, f2)
    # print >> f2, j
    f2.close()


# def write_news_to_file():
# #test: generate summaries from feeds
# #feeds = json.load(open(os.path.dirname(parent_dir) + "/Data/Facts/news-feeds-data.json", 'r'))

#     briefings = {}

#     for topic in stories.keys():
#         if topic != Topics.NEWS:
#             preface = "Today's top stories about {0}: ".format(TopicNames[ topic ])
#         else:
#             preface = "Today's top stories: ".format(TopicNames[ topic ])


#         summary, entities = makeSummary(stories, topic, limit=1600, maxStories=5, preface=preface)
#         # print "\ ----\n", summary, entities
#         if summary is None:
#             continue

#         briefings[topic]={
#             "briefing": summary,
#             "entities": entities
#         }


#     month = datetime.datetime.now().month
#     day = datetime.datetime.now().day
#     hour = datetime.datetime.now().hour
#     #output data
#     output = {
#         "{0}_{1}_{2}".format(month, day, hour): briefings
#     }

#     if briefings:
#         # j = json.dumps(briefings, indent=4)
#         f2 = open("/usr/news_data/news-briefings.json", 'w')
#         json.dump(briefings, f2)
#         # print >> f2, j
#         f2.close()
# write_news_to_file()

