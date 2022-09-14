from emora_stdm import DialogueFlow, Macro
from enum import Enum
import json, os
import random
from _globals import TRAVELDIR

# Zahara
# 04/09/2020

# bug fixed, added dialogue to a previous end


class State(Enum):
    START = 0
    OUTDOOR_START = 1
    START_TRAVEL = 2
    END = 100
    ROBOT = 3
    ROBOT_TRAVEL = 4

    ASK_TRAVEL = 5
    GROCERY_STORE = 6
    TRAVEL_N = 7
    TRAVEL_Y = 8
    ROBOT_FOOD = 9

    CITY_DISLIKE = 10
    CITY_NOT_TRAVELED = 11
    CITY_TRAVELED = 12
    ASK_OPINION_REASON = 13
    CITY_DISCUSS = 14

    REASON_NOT_SURE = 15
    REASON_N = 16
    REASON_Y = 17
    ROBOT_FOOD_OPINION = 18

    CITY_TOURISM = 20
    OK_THE_CITY = 21
    NOT_THE_CITY = 22

    ATTRACTION_OPINION = 25
    ATTRACTION_OPINION_D = 26
    ATTRACTION_OPINION_N = 27
    ATTRACTION_OPINION_Y = 28

    CITY_RECOMMEND = 30
    CITY_RECOMMEND_N = 31
    CITY_RECOMMEND_Y = 32

    FOOD_RECOMMEND = 35
    FOOD_RECOMMEND_N = 36
    FOOD_RECOMMEND_Y = 37

    FOOD_OPINION = 40
    FOOD_NOT_KNOW = 41
    FOOD_DISLIKE = 42
    FOOD_LIKE = 43

    ATTRACTION_RECOMMEND = 45
    ATTRACTION_RECOMMEND_D = 46
    ATTRACTION_RECOMMEND_N = 47
    ATTRACTION_RECOMMEND_Y = 48

    USER_REC_CITY = 50
    USER_REC_ANSWER = 51
    USER_REC_NO = 52

    MOVIE_REC = 55
    MOVIE_REC_N = 56
    MOVIE_REC_HAVE_WATCHED = 57
    MOVIE_REC_Y = 58

    MUSIC_REC = 60
    MUSIC_REC_N = 61
    MUSIC_REC_HAVE_HEARD = 62
    MUSIC_REC_Y = 63

    ASK_FAV_CITY = 66
    FAV_SAME = 67
    FAV_END = 68
    FAV_NO = 69
    NO_MATCH = 70

    TRAVEL_PLAN = 75
    TRAVEL_PLAN_D = 76
    TRAVEL_PLAN_Y = 77
    TRAVEL_PLAN_N = 78

    TRAVEL_PET = 80

    TRAVEL_TIME = 81
    TRAVEL_TIME_D = 82
    TRAVEL_TIME_E = 83
    TRAVEL_TIME_L = 84

    TRAVEL_EAT = 86
    TRAVEL_EAT_D = 87
    TRAVEL_EAT_Y = 88
    TRAVEL_EAT_N = 89

    TRAVEL_PET_Y = 92
    TRAVEL_PET_N = 91

    TRAVEL_N_PET = 95
    TRAVEL_N_PET_Y = 97
    TRAVEL_N_PET_N = 96

    # ASK_TRAVEL_CITY = 5
    # ASK_TRAVEL_CITY_DONTKNOW = 6
    # ASK_TRAVEL_CITY_UNKNOWN = 7
    # ASK_TRAVEL_CITY_UNKNOWN_INLIST = 8

    # CITY_TOURISM = 10
    # CITY_TOURISM_Y = 11
    # CITY_TOURISM_UNKNOWN = 12
    # CITY_TOURISM_CERTAIN = 13
    # CITY_TOURISM_CERTAIN_Y = 14
    # CITY_TOURISM_CERTAIN_N = 15

    # CITY_FOOD = 20
    # CITY_FOOD_Y = 21
    # CITY_FOOD_UNKNOWN = 22
    # CITY_FOOD_CERTAIN = 23
    # CITY_FOOD_CERTAIN_Y = 24
    # CITY_FOOD_CERTAIN_N = 25

    # CITY_SPORTS = 30
    # CITY_SPORTS_Y = 31
    # CITY_SPORTS_N = 32

    # CITY_EVENTS = 40
    # CITY_EVENTS_Y = 41
    # CITY_EVENTS_UNKNOWN = 42
    # CITY_EVENTS_CERTAIN = 43
    # CITY_EVENTS_CERTAIN_Y = 44
    # CITY_EVENTS_CERTAIN_N = 45

    # CITY_CULTURE = 50
    # CITY_CULTURE_Y = 51
    # CITY_CULTURE_N = 52

    # CITY_REASON = 60
    # CITY_REASON_POSITIVE = 61
    # CITY_REASON_NEGATIVE = 62
    # CITY_REASON_UNKNOWN = 63
    # CITY_REASON_ANS = 64


class TRAVEL_CATCH(Macro):
    """Catch user utterance

    Attribute:
        path: Path of database.
    """

    def __init__(self, path):
        self.path = path
        with open(self.path, 'r') as f:
            self.db = json.load(f)

    def run(self, ngrams, vars, args):
        # Catch user utterance in first key
        if len(args) == 0:
            return ngrams & self.db.keys()

        # Catch the user utterance in the third key
        if len(args) == 1:
            return ngrams & self.db[vars[args[0]]].keys()

        # Catch the user utterance in the third key
        if len(args) == 2:
            return ngrams & self.db[vars[args[0]]][vars[args[1]]].keys()


class TRAVEL_RANDOM(Macro):
    """Random generate keys

    Attribute:
        path: Path of database.
    """
    def __init__(self, path):
        self.path = path
        with open(self.path, 'r') as f:
            self.db = json.load(f)

    def run(self, ngrams, vars, args):
        # Random generate the first key
        name = 'db_keys' + self.path
        name_1 = 'db_keys_1' + self.path
        name_2 = 'db_keys_2' + self.path
        name_3 = 'db_keys_3' + self.path

        if len(args) == 0:
            if vars.get(name) is None or len(vars[name]) == 0:
                vars[name] = list(self.db.keys())
            key = random.choice(vars[name])
            vars[name] = vars[name].remove(key)
            return key

        # Random generate unduplicated the first key
        elif len(args) == 1:
            if vars.get(name_1) is None or len(vars[name_1]) <= 1:
                vars[name_1] = list(self.db[vars[args[0]]].keys())
            if vars[args[0]] in vars[name_1]:
                vars[name_1].remove(vars[args[0]])
            key_1 = random.choice(vars[name_1])
            vars[name_1] = vars[name_1].remove(key_1)
            return key_1

        # Random generate the third key
        elif len(args) == 2:
            if vars.get(name_2) is None or len(vars[name_2]) <= 1:
                vars[name_2] = list(self.db[vars[args[0]]][args[1]].keys())
            key_2 = random.choice(vars[name_2])
            vars[name_2] = vars[name_2].remove(key_2)
            return key_2

        # Random generate unduplicated the third key
        elif len(args) == 3:
            if vars.get(name_3) is None or len(vars[name_3]) <= 1:
                vars[name_3] = list(self.db[vars[args[0]]][vars[args[1]]].keys())
            if vars[args[-1]] in vars[name_3]:
                vars[name_3].remove(vars[args[0]])
            key_3 = random.choice(vars[name_3])
            vars[name_3] = vars[name_3].remove(key_3)
            return key_3


class TRAVEL_DETAIL(Macro):
    """Get keys value

    Attribute:
        path: Path of database.
    """
    def __init__(self, path):
        self.path = path
        with open(self.path, 'r') as f:
            self.db = json.load(f)

    def run(self, ngrams, vars, args):
        # Get the value of the first key
        if len(args) == 1:
            return self.db[vars[args[0]]]

        # Get the value of the second key
        elif len(args) == 2:
            return self.db[vars[args[0]]][args[1]]

        # Catch the value of the third key
        elif len(args) == 3:
            return self.db[vars[args[0]]][args[1]][vars[args[2]]]


class CATCH_LIST(Macro):
    """Catch user utterance with list.

    Attribute:
        list: A list whether user utterance is in or not.
    """

    def __init__(self, list):
        """Inits CATCH with list"""
        self.list = list

    def run(self, ngrams, vars, args):
        """Performs operation"""
        return ngrams & self.list


# Database
travel_db = TRAVELDIR.replace('__***__','travel_database.json')
city_db = TRAVELDIR.replace('__***__','city_onto.json')

# Variables
TRANSITION_OUT = ["movies", "music", "sports"]
NULL = "NULL TRANSITION"
CITY_IN_THE_LIST = {"honolulu","chicago","miami","orlando","philadelphia","san francisco","new orleans", "washington dc","houston","san diego","las vegas","los angeles","atlanta","seattle","bangkok","london","hong kong","macau","singapore","paris","dubai","kuala lumpur"}
# The cities not in the database
CITY_LIST = {"tokyo","jakarta","chongqing","manila","delhi","seoul","mumbai","shanghai","sao paulo","beijing",
             "lagos","mexico city","guangzhou","dhaka","osaka","cairo","karachi","moscow","chengdu",
             "kolkata","buenos aires","tehran","tianjin","kinshasa","rio de janeiro",
             "baoding", "lahore", "lima", "bangalore", "ho chi minh", "harbin", "wuhan", "shijiazhuang", "bogota", "suzhou",
             "linyi", "chennai", "nagoya", "nanyang", "zhengzhou", "hyderabad", "surabaya", "hangzhou", "johannesburg",
             "quanzhou", "taipei", "dongguan", "bandung", "hanoi", "shenyang", "baghdad", "onitsha",
             "ahmedabad", "luanda", "dallas", "pune", "nanjing", "boston", "santiago",
             "riyadh", "dusseldorf", "madrid", "toronto", "surat"}
YES = {"yes", "yea", "yup", "yep", "i do", "yeah", "a little", "sure", "of course", "i have", "i am", "sometimes", "too", "as well", "also", "agree","good", "keep","why not", "ok", "okay", "fine", "continue", "go on", "definitely", "liked", "loved"}
NO = {"no", "nope", "dont", "nothing", "nuh", "not", "don't", "haven't", "didn't", "doesn't", "never", "shouldn't"}
DONT_KNOW =  {"didn't try", "not sure", "don't know", "wouldn't know", "didn't know", "no idea", "don't remember", "can't recall", "can't remember", "didn't remember", "couldn't recall"}
# Functions
macros = {
    'CATCH': TRAVEL_CATCH(city_db),
    'RANDOM': TRAVEL_RANDOM(travel_db),
    'RANDOM_TOURISM': TRAVEL_RANDOM(travel_db),
    'RANDOM_FOOD': TRAVEL_RANDOM(travel_db),
    'RANDOM_EVENT': TRAVEL_RANDOM(travel_db),
    'RANDOM_CULTURE': TRAVEL_RANDOM(travel_db),
    'CITY_DETAIL': TRAVEL_DETAIL(city_db),
    'DETAIL': TRAVEL_DETAIL(travel_db),
    'CATCH_CITY_LIST': CATCH_LIST(CITY_IN_THE_LIST),
    'CATCH_YES':CATCH_LIST(YES),
    'CATCH_NO':CATCH_LIST(NO),
    'CATCH_NOT_SURE':CATCH_LIST(DONT_KNOW),
    'RANDOM_MUSIC':TRAVEL_RANDOM(travel_db),
    'RANDOM_MOVIE':TRAVEL_RANDOM(travel_db)
}

###################### Initialization Part ####################################################################################################################
# Initialize the DialogueFlow object, which uses a state-machine to manage dialogue
# Each user turn should consider error transition

df = DialogueFlow(State.START, initial_speaker=DialogueFlow.Speaker.USER, macros=macros)

# df.add_state(State.START)
# For dialogue manager initialization
# test
# df.add_user_transition(State.START, State.START_TRAVEL, 'test')
df.add_system_transition(State.START, State.OUTDOOR_START, '"Now we are all going through a tough time. Since you like to go to "$dest", do you like to travel?"')
df.add_system_transition(State.START, State.START_TRAVEL,'"Now we are all going through a tough time. We should all stay at home and stay safe and healthy. But it is still nice to think about where we might travel to in the future. Do you like to travel?"')
#df.add_system_transition(State.START_TRAVEL, State.ASK_TRAVEL,'"I was planning to travel to"$city={seattle, houston, atlanta}". However, because of the global pandemic, I had to cancel my travel plan. I was curious about this. Which city do you wanna try to after everything gets better?"')

# User Turn
df.add_user_transition(State.OUTDOOR_START,State.TRAVEL_N,'[{#CATCH_NO(), hate, worst, dislike, tired, hated}]')
df.add_user_transition(State.OUTDOOR_START, State.TRAVEL_Y, '[{#CATCH_YES(), love, like, favorite, hobby, best, said}]')
df.add_user_transition(State.OUTDOOR_START, State.GROCERY_STORE, '[{grocery store, grocery, groceries, supermarket, walmart, publix, kroger, trader joes, safeway, sprouts, hmart, aldi, wholefoods}]')
# df.add_user_transition(State.START, State.ASK_TRAVEL_CITY, '[$city=#CATCH()]')
# df.add_user_transition(State.START, State.ASK_TRAVEL_CITY_UNKNOWN_INLIST, '[$city=#CATCH_CITY_LIST()]')
df.add_user_transition(State.OUTDOOR_START, State.ROBOT, '[{robot, bot}]')
df.set_error_successor(State.OUTDOOR_START, State.TRAVEL_Y)

df.add_user_transition(State.START_TRAVEL,State.TRAVEL_N,'[{#CATCH_NO(), hate, worst, dislike, tired, hated}]')
df.add_user_transition(State.START_TRAVEL, State.TRAVEL_Y, '[{#CATCH_YES(), love, like, favorite, hobby, best, said}]')
df.add_user_transition(State.START_TRAVEL, State.GROCERY_STORE, '[{grocery store, grocery, groceries, supermarket, walmart, publix, kroger, trader joes, safeway, sprouts, hmart, aldi, wholefoods}]')
# df.add_user_transition(State.START, State.ASK_TRAVEL_CITY, '[$city=#CATCH()]')
# df.add_user_transition(State.START, State.ASK_TRAVEL_CITY_UNKNOWN_INLIST, '[$city=#CATCH_CITY_LIST()]')
df.add_user_transition(State.START_TRAVEL, State.ROBOT, '[{robot, bot}]')

# Error Transition
df.set_error_successor(State.START_TRAVEL, State.TRAVEL_Y)
# df.add_system_transition(State.START, State.START, NULL)
df.set_error_successor(State.START, State.START)
# df.add_system_transition(State.START, State.START, NULL)

df.add_system_transition(State.TRAVEL_Y,State.TRAVEL_PET,'"so when you travel, will you bring "$name" with you?"')
df.add_system_transition(State.TRAVEL_N,State.TRAVEL_N_PET,'"yeah I get it. Travel is not for everybody. Plus you have to take care of "$name". isn\'t it sweet to have someone to keep you company?"')
# System Turn
df.add_system_transition(State.GROCERY_STORE, State.ASK_TRAVEL, '"yes of course, but please be cautious when you go there. I like to travel to different cities,One of my favorite cities is"$city={honolulu, chicago, miami, orlando, philadelphia, san francisco, new orleans, washington dc, houston, san diego, las vegas, los angeles, atlanta, bangkok, london, hong kong, macau, singapore, paris, dubai, kuala lumpur}"."#DETAIL(city, brief_intro)"I was planning on traveling to there but my trip was cancelled due to this pandemic. Have you ever been to this city before?"')
df.add_system_transition(State.ROBOT, State.END,'"i can be a robot, but I am also your companion and I do have my own preferences. why would you want an emotionless machine when you have me? "')
#df.add_system_transition(State.TRAVEL_Y, State.ASK_TRAVEL, '"Yay! We share the same view on this. One of my favorite cities is"$city={honolulu, chicago, miami, orlando, philadelphia, san francisco, new orleans, washington dc, houston, san diego, las vegas, los angeles, atlanta, bangkok, london, hong kong, macau, singapore, paris, dubai, kuala lumpur}"."#DETAIL(city, brief_intro)"I was planning on traveling to there but my trip was cancelled due to this pandemic. Have you ever been to this city before?"')
df.add_system_transition(State.TRAVEL_N, State.END,'"Okay. I understand everyone has different ways of spending their leisure time. I also like to spend time with my loved ones at home. Location doesnt matter as long as we are having fun. "')
df.add_system_transition(State.TRAVEL_Y, State.TRAVEL_TIME, '"yay! i also love to travel. Do you prefer to wake up late and travel during the night, or would you rather be up at dawn to get an early start?"')
#df.add_system_transition(State.TRAVEL_Y, State.ASK_TRAVEL, '"Awesome! Last year, one of my friends went to"$city={seattle, houston, atlanta}"and she liked there very much. I know several wonderful cities to travel to in the United States. Which city do you want to go in the United States?"')

df.add_user_transition(State.TRAVEL_PET, State.TRAVEL_PET_N,'[{#CATCH_NO(), leave, family, friend, friends, brother, sister, parents, dad, mom, father, mother, take care, stay}]')
df.add_user_transition(State.TRAVEL_PET, State.TRAVEL_PET_Y,'[{#CATCH_YES(), love, like}]')
df.set_error_successor(State.TRAVEL_PET, State.TRAVEL_PET_N)

df.add_user_transition(State.TRAVEL_N_PET, State.TRAVEL_N_PET_Y,'[{yes, sure}]')
df.set_error_successor(State.TRAVEL_N_PET, State.TRAVEL_N_PET_Y)

df.add_system_transition(State.TRAVEL_N_PET_Y,State.END,"ok.")

df.add_system_transition(State.TRAVEL_PET_N, State.TRAVEL_TIME,'"I guess it is sometimes better to leave them at home when you travel. It seems that most pets are not used to travel to new places. When you travel, Do you prefer to wake up late and trip the night fantastic, or would you rather be up at dawn? "')
df.add_system_transition(State.TRAVEL_PET_Y, State.TRAVEL_TIME,'"Wow I am kinda jealous of "$name" now. I want someone to take me to travel to different places. When you travel, Do you prefer to wake up late and trip the night fantastic, or would you rather be up at dawn?"')
# User Turn
df.add_user_transition(State.TRAVEL_TIME,State.TRAVEL_TIME_D,'[{#CATCH_NOT_SURE(), care, no difference, whatever, depends, change, changes, matter, sometimes, both, also}]')
df.add_user_transition(State.TRAVEL_TIME,State.TRAVEL_TIME_E, '[{former, early, save time, dawn, sun rise, morning, waste, first}]')
df.add_user_transition(State.TRAVEL_TIME,State.TRAVEL_TIME_L, '[{#CATCH_NO(), latter, second, late, stay, bed, afternoon, noon, hotel, night, nightlife, party, parties, partying, later, fantastic, evening, tired}]')
df.set_error_successor(State.TRAVEL_TIME,State.TRAVEL_TIME_D)

# System Turn
df.add_system_transition(State.TRAVEL_TIME_E, State.TRAVEL_PLAN, '"wow, I genuinely respect people who can get up early during vacations. Do you like to plan each step of your itinerary or leave it all to chance? "')
df.add_system_transition(State.TRAVEL_TIME_L, State.TRAVEL_PLAN, '"haha same here. I can sleep in the hotel till noon while traveling. Do you like to plan each step of your itinerary or leave it all to chance? "')
df.add_system_transition(State.TRAVEL_TIME_D, State.TRAVEL_PLAN, '"yeah I get it. It really depends on the mood and the places. Do you like to plan each step of your itinerary or leave it all to chance? "')


# User Turn
df.add_user_transition(State.TRAVEL_PLAN,State.TRAVEL_PLAN_D,'[{#CATCH_NOT_SURE(), not every step, not each step, between, mostly, sometimes, both, also}]')
df.add_user_transition(State.TRAVEL_PLAN,State.TRAVEL_PLAN_N,'[{#CATCH_NO(), latter, chance, flow, second}]')
df.add_user_transition(State.TRAVEL_PLAN,State.TRAVEL_PLAN_Y,'[{plan, ahead, planner, before, former, first, work}]')


df.set_error_successor(State.TRAVEL_PLAN, State.TRAVEL_PLAN_D)

# System Turn
df.add_system_transition(State.TRAVEL_PLAN_Y, State.TRAVEL_EAT, '"wow respect, i really wanna have a travel buddy that makes plans before traveling. I cant do it by myself. What about food? Would you rather linger over meals or scarf them down and get moving again? "')
df.add_system_transition(State.TRAVEL_PLAN_N, State.TRAVEL_EAT, '"yeah me too! but i really wanna have a travel buddy that makes some plans before traveling. What about food? Would you rather linger over meals or scarf them down and get moving again?"')
df.add_system_transition(State.TRAVEL_PLAN_D, State.TRAVEL_EAT,'"same! i would do some work before hand but not every step. What about food? Would you rather linger over meals or scarf them down and get moving again?"')

# User Turn
df.add_user_transition(State.TRAVEL_EAT,State.TRAVEL_EAT_D,'[{#CATCH_NOT_SURE(), depends, sometimes, quality, maybe, not sure, sometimes, both, also}]')
df.add_user_transition(State.TRAVEL_EAT,State.TRAVEL_EAT_Y,'[{first, linger, like, enjoy, local, try, former, food, foodie, all about, cuisine}]')
df.add_user_transition(State.TRAVEL_EAT,State.TRAVEL_EAT_N,'[{latter, finish, car, snack, second, moving, scarfing, swallow, swallowing, waste of time}]')
df.set_error_successor(State.TRAVEL_EAT, State.TRAVEL_EAT_D)

# System Turn
df.add_system_transition(State.TRAVEL_EAT_Y, State.ASK_TRAVEL, '"Same here, I am a giant foodie and every time I go to a new place I look for new foods to try. One of my favorite cities is"$city={honolulu, chicago, miami, orlando, philadelphia, san francisco, new orleans, washington dc, houston, san diego, las vegas, los angeles, atlanta, bangkok, london, hong kong, macau, singapore, paris, dubai, kuala lumpur}"."#DETAIL(city, brief_intro)"I was planning on traveling to there but my trip was cancelled due to this pandemic. Have you ever been to this city before?"')
df.add_system_transition(State.TRAVEL_EAT_N, State.ASK_TRAVEL, '"Oh ok. For some people, enjoy the scenery and local culture is more important. One of my favorite cities is"$city={honolulu, chicago, miami, orlando, philadelphia, san francisco, new orleans, washington dc, houston, san diego, las vegas, los angeles, atlanta, bangkok, london, hong kong, macau, singapore, paris, dubai, kuala lumpur}"."#DETAIL(city, brief_intro)"I was planning on traveling to there but my trip was cancelled due to this pandemic. Have you ever been to this city before?"')
df.add_system_transition(State.TRAVEL_EAT_D, State.ASK_TRAVEL,'"Yeah it really depends on the state of mind and time. One of my favorite cities is"$city={honolulu, chicago, miami, orlando, philadelphia, san francisco, new orleans, washington dc, houston, san diego, las vegas, los angeles, atlanta, bangkok, london, hong kong, macau, singapore, paris, dubai, kuala lumpur}"."#DETAIL(city, brief_intro)"I was planning on traveling to there but my trip was cancelled due to this pandemic. Have you ever been to this city before? "')

# User Turn
df.add_user_transition(State.ASK_TRAVEL, State.CITY_DISLIKE, '[{hate, worst, dislike, tired, hated, didnt}]')
df.add_user_transition(State.ASK_TRAVEL, State.CITY_NOT_TRAVELED, '[{#CATCH_NO(), havent, never}]')
df.add_user_transition(State.ASK_TRAVEL, State.CITY_TRAVELED, '[{#CATCH_YES(), love, like, favorite, hobby, best, good, hometown, grew up, work, live, here}]')
df.add_user_transition(State.ASK_TRAVEL, State.ROBOT_TRAVEL, '[{robot, bot}]')
# df.add_user_transition(State.ASK_TRAVEL, State.ASK_TRAVEL_CITY, '[$city=#CATCH()]')
# df.add_user_transition(State.ASK_TRAVEL, State.ASK_TRAVEL_CITY_DONTKNOW, '[{i dont know, have no idea, who knows, no, nope, not, no idea}]')
# df.add_user_transition(State.ASK_TRAVEL, State.ASK_TRAVEL_CITY_UNKNOWN_INLIST, '[$city=#CATCH_CITY_LIST()]')
df.set_error_successor(State.ASK_TRAVEL, State.CITY_NOT_TRAVELED)

# System Turn
df.add_system_transition(State.ROBOT_TRAVEL, State.ASK_TRAVEL,'"i can do things i like in my virtual world. have you been to "$city" before? "')
df.add_system_transition(State.CITY_DISLIKE, State.CITY_RECOMMEND, '"Oh really? Maybe I should consider a different city. Do you have any city in mind that you would recommend me to go to?"')
df.add_system_transition(State.CITY_NOT_TRAVELED, State.CITY_DISCUSS, '"Oh thats fine. I love it because I heard that"#DETAIL(city, reason_for_travel)" I also love its food, culture, and I even know some of its tourist attractions. do you want to go there one day?"')
df.add_system_transition(State.CITY_TRAVELED, State.ASK_OPINION_REASON, '{Thats nice, Yay}"! then I can ask you opinions on this before I go. I heard that "#DETAIL(city, reason_for_travel)" Is that right?"')
# df.add_system_transition(State.ASK_TRAVEL_CITY, State.CITY_TOURISM, '{Nice choice, Good choice, Cool, Wonderful, Wow, Awesome}"! I love"$city"!"#DETAIL(city, brief_intro)"I am familiar with many aspects of this city, like tourist attraction, famous food, sports, events or the culture there. Would you like to know about the tourist attraction first?"')
# df.add_system_transition(State.ASK_TRAVEL_CITY_DONTKNOW, State.CITY_TOURISM, '"That\'s OK! One of my favorite cities is"$city={#RANDOM()}". do you want to talk about this city?"')
# df.add_system_transition(State.ASK_TRAVEL_CITY_UNKNOWN, State.CITY_TOURISM, '"Oops, I\'m not quite familiar with this city. One of my favorite cities is"$city={#RANDOM()}". do you want to talk about city"')
# df.add_system_transition(State.ASK_TRAVEL_CITY_UNKNOWN_INLIST, State.CITY_TOURISM, '{Interesting, Cool, Wow, Awesome}".I heard"$city"is a good place to travel, but I know little about this place. One of my favorite cities is"$city={#RANDOM()}". do u want to talk about this city?"')

############################# Tourist Attraction Part ############################################################################################################
# User Turn
df.add_user_transition(State.ASK_OPINION_REASON,State.REASON_NOT_SURE,'[{#CATCH_NOT_SURE(), dont know, no idea, who knows, not sure, not quite sure}]')
df.add_user_transition(State.ASK_OPINION_REASON,State.REASON_N, '[{#CATCH_NO(), havent, never}]')
df.add_user_transition(State.ASK_OPINION_REASON,State.REASON_Y, '[{#CATCH_YES(), love, like, favorite, best, good}]')
df.add_user_transition(State.ASK_OPINION_REASON, State.ROBOT, '[{robot, bot}]')
df.set_error_successor(State.ASK_OPINION_REASON, State.REASON_NOT_SURE)

df.add_user_transition(State.CITY_DISCUSS,State.NOT_THE_CITY, '[{#CATCH_NO(), never}]')
df.add_user_transition(State.CITY_DISCUSS,State.OK_THE_CITY,'[{#CATCH_YES(), love, like, favorite, best, good, i would, maybe, might}]')
df.add_user_transition(State.CITY_DISCUSS, State.ROBOT, '[{robot, bot}]')
df.set_error_successor(State.CITY_DISCUSS, State.OK_THE_CITY)


df.add_user_transition(State.CITY_RECOMMEND,State.CITY_RECOMMEND_N,'[{#CATCH_NO(), never}]')
df.add_user_transition(State.CITY_RECOMMEND,State.CITY_RECOMMEND_Y,'[{#CATCH_YES(), love, like, favorite, best, good, i would}]')
df.add_user_transition(State.CITY_RECOMMEND, State.ROBOT, '[{robot, bot}]')
df.set_error_successor(State.CITY_RECOMMEND,State.CITY_RECOMMEND_N)
# df.add_user_transition(State.CITY_TOURISM, State.CITY_TOURISM_Y, '[{#CATCH_YES(),tourist attraction, tourist, tourism, attraction, tour}]')
# df.add_user_transition(State.CITY_TOURISM, State.ASK_TRAVEL_CITY, '[$city=#CATCH()]')
# df.add_user_transition(State.CITY_TOURISM, State.ASK_TRAVEL_CITY_UNKNOWN_INLIST, '[$city=#CATCH_CITY_LIST()]')
# df.add_user_transition(State.CITY_TOURISM, State.ASK_TRAVEL_CITY_DONTKNOW, '[[{no, nope, dont, nuh}] #NOT(know, idea)]')
# df.add_user_transition(State.CITY_TOURISM, State.CITY_TOURISM_DONTKNOW, '[{i dont know, have no idea, who knows}]')
# df.set_error_successor(State.CITY_TOURISM, State.CITY_TOURISM_UNKNOWN)
# df.set_error_successor(State.CITY_TOURISM, State.CITY_TOURISM_CERTAIN_N)

# System Turn
#df.add_system_transition(State.CITY_TOURISM_Y, State.CITY_TOURISM_CERTAIN, '"Good choice! I know several famous tourist attraction in"$city",Like"$tourism={#RANDOM_TOURISM(city, tourist_attraction)}".Would you like to know more detail about this tourist attraction?"')
df.add_system_transition(State.REASON_NOT_SURE,State.FOOD_OPINION, '"Ah ok. I will take that into consideration. Thanks! I also want to try out the food there. i know some of their popular cuisines such as "$food={#RANDOM_FOOD(city, famous_food)}". If you have tried it there, did you like it?"')
df.add_system_transition(State.REASON_N,State.CITY_RECOMMEND, '"Oh no, thats sad. I wanted to go because of that. Do you have any city in mind that you would recommend me to go to?"')
df.add_system_transition(State.REASON_Y,State.ATTRACTION_OPINION,'"Good to know! I know they have "$tourism={#RANDOM_TOURISM(city, tourist_attraction)}" which is quite popular. I actually wanna go there. Would you recommend the place?"')
df.add_system_transition(State.NOT_THE_CITY, State.FOOD_RECOMMEND,'"Ah thats okay. After all, it is better for us to stay home for now. One of my favorite cities also includes "$city={seattle, new york}", because"#DETAIL(city, reason_for_travel)" but it is undergoing a huge crisis right now. I hope everything will get better soon. Besides, I love their "$food={#RANDOM_FOOD(city, famous_food)}". Would you like to try that there one day."')
df.add_system_transition(State.OK_THE_CITY,State.FOOD_RECOMMEND,'"Yay! We have the same wishes now! But I bet I know more about this city than you do. For example, i know some of their popular cuisines such as "$food={#RANDOM_FOOD(city, famous_food)}". You should definitely try if you go there one day!"')
df.add_system_transition(State.CITY_RECOMMEND_N,State.END,'"Well thats fine. I am sure both of us will find a place that each will enjoy. "')
df.add_system_transition(State.CITY_RECOMMEND_Y,State.USER_REC_CITY,'"Thanks for your recommendation！I will take that into consideration. Do you want to tell me more about the city?"')
# df.add_system_transition(State.CITY_TOURISM_UNKNOWN, State.CITY_TOURISM, '"Interesting. I am not quite familiar with this aspect of"$city"What about talking about something that I know, like tourist attraction there?"')

# User Turn
df.add_user_transition(State.ATTRACTION_OPINION,State.ATTRACTION_OPINION_D,'[{#CATCH_NOT_SURE(), dont know, no idea, who knows, not sure, not quite sure, never been}]')
df.add_user_transition(State.ATTRACTION_OPINION,State.ATTRACTION_OPINION_N,'[{#CATCH_NO(), never, shouldnt}]')
df.add_user_transition(State.ATTRACTION_OPINION,State.ATTRACTION_OPINION_Y,'[{#CATCH_YES(), love, like, favorite, best, good, i would, fine}]')
df.add_user_transition(State.ATTRACTION_OPINION, State.ROBOT, '[{robot, bot}]')
df.set_error_successor(State.ATTRACTION_OPINION,State.ATTRACTION_OPINION_D)

df.add_user_transition(State.FOOD_RECOMMEND,State.FOOD_RECOMMEND_N, '[{#CATCH_NO(), never, shouldnt, wont, wouldnt}]')
df.add_user_transition(State.FOOD_RECOMMEND,State.FOOD_RECOMMEND_Y, '[{#CATCH_YES(), love, like, favorite, best, good, i would, fine, delicious, tasty, maybe}]')
df.add_user_transition(State.FOOD_RECOMMEND,State.ROBOT_FOOD, '[{robot, bot}]')
df.set_error_successor(State.FOOD_RECOMMEND,State.FOOD_RECOMMEND_N)



df.add_user_transition(State.USER_REC_CITY, State.USER_REC_ANSWER,'[{#CATCH_YES(), love, like, favorite, best, good, i would, fine, delicious, tasty, maybe, temperature, weather, beach, culture, event, people, nice}]')
df.add_user_transition(State.USER_REC_CITY, State.ROBOT, '[{robot, bot}]')
df.set_error_successor(State.USER_REC_CITY, State.USER_REC_NO)

# df.add_user_transition(State.CITY_TOURISM_CERTAIN, State.CITY_TOURISM_CERTAIN_N, '[#CATCH_NO()]')
# df.add_user_transition(State.CITY_TOURISM_CERTAIN, State.CITY_TOURISM_CERTAIN_Y, '[#CATCH_YES()]')
# # df.add_user_transition(State.CITY_TOURISM_CERTAIN, State.ASK_TRAVEL_CITY, '[$city=#CATCH()]')
# df.set_error_successor(State.CITY_TOURISM_CERTAIN, State.CITY_TOURISM_CERTAIN_N)

# System Turn
df.add_system_transition(State.ROBOT_FOOD, State.ATTRACTION_RECOMMEND,'"I may not live physically in your world, but I do eat food in mine. Anyways, I also know they have the tourist attraction "$tourism={#RANDOM_TOURISM(city, tourist_attraction)}"which is quite popular. I actually wanna go there. "$tourism","#DETAIL(city, tourist_attraction, tourism)" Would you consider this could be a good place to visit? "')
df.add_system_transition(State.USER_REC_ANSWER, State.END,'"Nice nice! I will definitely look into it. Thanks again! "')
df.add_system_transition(State.USER_REC_NO, State.END,'"Ok but still thanks again! "')
df.add_system_transition(State.ATTRACTION_OPINION_Y,State.FOOD_OPINION, '"Nice! I will definitely go one day once everything is fine. I also want to try out the food there. i know some of their popular cuisines such as "$food={#RANDOM_FOOD(city, famous_food)}", which, "#DETAIL(city, famous_food, food)". If you have tried it there, did you like it?"')
df.add_system_transition(State.ATTRACTION_OPINION_N,State.FOOD_OPINION, '"Ah ok. I will take that into consideration. Thanks! I also want to try out the food there. i know some of their popular cuisines such as "$food={#RANDOM_FOOD(city, famous_food)}", which, "#DETAIL(city, famous_food, food)". If you have tried it there, did you like it?"')
df.add_system_transition(State.ATTRACTION_OPINION_D,State.FOOD_OPINION, '"Okay, thats fine. I also want to try out the food there. i know some of their popular cuisines such as"$food={#RANDOM_FOOD(city, famous_food)}", which ,"#DETAIL(city, famous_food, food)". If you have tried it there, did you like it?"')

df.add_system_transition(State.FOOD_RECOMMEND_Y,State.ATTRACTION_RECOMMEND, '"Good to know! I also know they have the tourist attraction"$tourism={#RANDOM_TOURISM(city, tourist_attraction)}"which is quite popular. I actually wanna go there. "$tourism","#DETAIL(city, tourist_attraction, tourism)" Would you consider this could be a good place to visit?"' )
df.add_system_transition(State.FOOD_RECOMMEND_N,State.ATTRACTION_RECOMMEND,'"haha thats fine. maybe we dont share the same taste. I also know they have the tourist attraction"$tourism={#RANDOM_TOURISM(city, tourist_attraction)}"which is quite popular. I actually wanna go there. "$tourism","#DETAIL(city, tourist_attraction, tourism)" Would you consider this could be a good place to visit?"' )
# df.add_system_transition(State.CITY_TOURISM_CERTAIN_N, State.CITY_FOOD, '{Alright, Ok, Then}".I also know lots of famous food in"$city". Would you like to talk about the famous food in this city?"')
# df.add_system_transition(State.CITY_TOURISM_CERTAIN_Y, State.CITY_FOOD, '{Nice choice,Good choice, Wonderful,Awesome}"!"$tourism","#DETAIL(city, tourist_attraction, tourism)"I also know lots of famous food in"$city". Would you like to talk about it?"')

df.add_system_transition(State.FOOD_NOT_KNOW,State.MOVIE_REC,'"oh ok. I will try it myself then. Hopefully it will turn out to be good. I first heard about this city because of the movie "$movie={#RANDOM_MOVIE(city, movie)}". Do you know of this movie?"')
df.add_system_transition(State.FOOD_LIKE,State.MOVIE_REC,'"Awesome, I have found the right person to ask! I will try once I get there. I first heard about this city because of the movie "$movie={#RANDOM_MOVIE(city, movie)}". Do you know of this movie?"')
df.add_system_transition(State.FOOD_DISLIKE, State.MOVIE_REC,'"oh no. that\'s ok. i will look for something else to eat then. I first heard about this city because of the movie "$movie={#RANDOM_MOVIE(city, movie)}". Do you know of this movie?"')
############################# Famous Food Part #####################################################################################################################
# User Turn

df.add_user_transition(State.FOOD_OPINION,State.FOOD_NOT_KNOW,'[{#CATCH_NOT_SURE(), dont know, havent, no idea, who knows, not sure, not quite sure, never been, never tried, never had it}]')
df.add_user_transition(State.FOOD_OPINION,State.FOOD_DISLIKE,'[{#CATCH_NO(), never, shouldnt, wont, wouldnt, didnt, hated, not that good, gross, no}]')
df.add_user_transition(State.FOOD_OPINION,State.FOOD_LIKE,'[{#CATCH_YES(), love, like, favorite, best, good, i would, delicious, tasty, maybe, great, good, wonderful, should be}]')
df.add_user_transition(State.FOOD_OPINION,State.ROBOT_FOOD_OPINION, '[{robot, bot}]')
df.set_error_successor(State.FOOD_OPINION,State.FOOD_NOT_KNOW)

df.add_user_transition(State.ATTRACTION_RECOMMEND,State.ATTRACTION_RECOMMEND_N,'[{#CATCH_NO(), shouldnt, wont, wouldnt, not really, else, elsewhere}]')
df.add_user_transition(State.ATTRACTION_RECOMMEND,State.ATTRACTION_RECOMMEND_Y,'[{#CATCH_YES(), love, like, favorite, best, good, i would, fine}]')
df.add_user_transition(State.ATTRACTION_RECOMMEND, State.ROBOT, '[{robot, bot}]')
df.set_error_successor(State.ATTRACTION_RECOMMEND, State.ATTRACTION_RECOMMEND_Y)
# df.add_user_transition(State.CITY_FOOD, State.CITY_FOOD_Y, '[#CATCH_YES()]')
# # df.add_user_transition(State.CITY_FOOD, State.CITY_FOOD_CERTAIN_N, '[[{no, nope, dont}] #NOT(know, idea)]')
# df.add_user_transition(State.CITY_FOOD, State.ASK_TRAVEL_CITY, '[$city=#CATCH()]')
# df.add_user_transition(State.CITY_FOOD, State.ASK_TRAVEL_CITY_UNKNOWN_INLIST, '[$city=#CATCH_CITY_LIST()]')
# # df.add_user_transition(State.CITY_TOURISM, State.CITY_TOURISM_DONTKNOW, '[{i dont know, have no idea, who knows}]')
# df.set_error_successor(State.CITY_FOOD, State.CITY_FOOD_CERTAIN_N)

# System Turn

df.add_system_transition(State.ROBOT_FOOD_OPINION,State.MOVIE_REC, '"I may not live physically in your world, but I do eat food in mine. Anyways, I first heard about "$city" because of the movie "$movie={#RANDOM_MOVIE(city, movie)}".have you heard about it?"')
df.add_system_transition(State.ATTRACTION_RECOMMEND_N,State.MOVIE_REC, '"Well, thats fine.  I first heard about it because of the movie "$movie={#RANDOM_MOVIE(city, movie)}".have you heard about it?"')
df.add_system_transition(State.ATTRACTION_RECOMMEND_Y,State.MOVIE_REC, '"Thanks for your suggestion. I first heard about it because of the movie "$movie={#RANDOM_MOVIE(city, movie)}".have you heard about it?"')

# df.add_system_transition(State.CITY_FOOD_Y, State.CITY_FOOD_CERTAIN, '"I like food! There are lots of famous food in"$city",Like"$food={#RANDOM_FOOD(city, famous_food)}".Would you like to know more detail about it?"')
# df.add_system_transition(State.CITY_FOOD_UNKNOWN, State.CITY_FOOD, '"Interesting. I am not quite familiar with this aspect of"$city"What about talking about something that I know, like famous food there?"')

# # User Turn
#df.add_user_transition(State.MOVIE_REC, State.MOVIE_NO, '[{}]')
df.add_user_transition(State.MOVIE_REC, State.MOVIE_REC_N, '[{#CATCH_NO(), music, songs, what is it, what was it, never heard, when, where}]')
df.add_user_transition(State.MOVIE_REC, State.MOVIE_REC_HAVE_WATCHED, '[{did watch, watched}]')
df.add_user_transition(State.MOVIE_REC, State.MOVIE_REC_Y, '[{#CATCH_YES(), did}]')
# df.add_user_transition(State.CITY_FOOD_CERTAIN, State.CITY_FOOD_CERTAIN_Y, '[#CATCH_YES()]')
df.set_error_successor(State.MOVIE_REC, State.MOVIE_REC_N)


# # System Turn
df.add_system_transition(State.MOVIE_REC_N, State.ASK_FAV_CITY, '"well,"$movie" "#DETAIL(city, movie, movie)" maybe you could check it out sometime. we have been talk about my favorite city, may i ask what is yours?"')
df.add_system_transition(State.MOVIE_REC_HAVE_WATCHED, State.MUSIC_REC, '"i am glad that we shared some similar experience. to be honest, "$city" always reminds me of the song "$music={#RANDOM_MUSIC(city, music)}". the song "#DETAIL(city, music, music)" you should check it out sometime."')
df.add_system_transition(State.MOVIE_REC_Y,State.MUSIC_REC,'"yay! by watching the movie i kinda feel like i am traveling. to be honest, "$city" always reminds me of the song "$music={#RANDOM_MUSIC(city, music)}". the song "#DETAIL(city, music, music)" you should check it out sometime."')


# ############################ Sports Part ###########################################################################################################################
# # User Turn
df.add_user_transition(State.MUSIC_REC, State.MUSIC_REC_HAVE_HEARD, '[{like, liked, love, loved, listened, good, great}]')
df.add_user_transition(State.MUSIC_REC, State.MUSIC_REC_Y, '[{#CATCH_YES(), ok, i might, maybe}]')
df.add_user_transition(State.MUSIC_REC, State.MUSIC_REC_N, '[{#CATCH_NO()}]')


# # df.add_user_transition(State.CITY_SPORTS, State.CITY_SPORTS_N, '[[{no, nope, dont}] #NOT(know, idea)]')
# df.add_user_transition(State.CITY_SPORTS, State.ASK_TRAVEL_CITY, '[$city=#CATCH()]')
# df.add_user_transition(State.CITY_SPORTS, State.ASK_TRAVEL_CITY_UNKNOWN_INLIST, '[$city=#CATCH_CITY_LIST()]')
# # df.add_user_transition(State.CITY_TOURISM, State.CITY_TOURISM_DONTKNOW, '[{i dont know, have no idea, who knows}]')
df.set_error_successor(State.MUSIC_REC, State.MUSIC_REC_N)



# # System Turn
df.add_system_transition(State.MUSIC_REC_HAVE_HEARD, State.ASK_FAV_CITY,'"wow nice! we have been talk about my favorite city, may i ask what is yours?"')
df.add_system_transition(State.MUSIC_REC_Y, State.ASK_FAV_CITY,'"good! we have been talk about my favorite city, what is your favorite city?"')
df.add_system_transition(State.MUSIC_REC_N, State.ASK_FAV_CITY,'"haha fine! we have been talk about my favorite city, what is your favorite city?"')

# ############################# Events Part ##########################################################################################################################
# # User Turn
df.add_user_transition(State.ASK_FAV_CITY, State.FAV_SAME, '[$fav_city=#CATCH_CITY_LIST()]')
df.add_user_transition(State.ASK_FAV_CITY, State.FAV_END, '[$fav_city=#CATCH()]')
df.add_user_transition(State.ASK_FAV_CITY,State.FAV_NO,'[{#CATCH_NO(),#CATCH_NOT_SURE()}]')
df.set_error_successor(State.ASK_FAV_CITY,State.NO_MATCH)




# # df.add_user_transition(State.CITY_EVENTS, State.CITY_EVENTS_CERTAIN_N, '[[{no, nope, dont}] #NOT(know, idea)]')
# df.add_user_transition(State.CITY_EVENTS, State.ASK_TRAVEL_CITY, '[$city=#CATCH()]')
# df.add_user_transition(State.CITY_EVENTS, State.ASK_TRAVEL_CITY_UNKNOWN_INLIST, '[$city=#CATCH_CITY_LIST()]')
# # df.add_user_transition(State.CITY_TOURISM, State.CITY_TOURISM_DONTKNOW, '[{i dont know, have no idea, who knows}]')
# df.set_error_successor(State.CITY_EVENTS, State.CITY_EVENTS_CERTAIN_N)

# # System Turn
df.add_system_transition(State.FAV_SAME, State.END, '"wow "$fav_city" is also on the top of my list, maybe we should talk about it next time!"') #because "#DETAIL(city, reason_for_travel)" "$city=$fav_city"
df.add_system_transition(State.FAV_END,State.END,'"aww glad to know that. however, I do not know much about "$fav_city", i only know it is in "$fav_city_state=#CITY_DETAIL(fav_city, state)"."')
df.add_system_transition(State.FAV_NO,State.END,'"ah ok, thats fine"')
df.add_system_transition(State.NO_MATCH, State.END,'"I am not really familiar with it."')
# df.add_system_transition(State.CITY_EVENTS_Y, State.CITY_EVENTS_CERTAIN, '{Nice choice,Good choice}"! I enjoy festivals and events! There are different events in"$city",Like"$event={#RANDOM_EVENT(city, event)}".Would you like to know more detail about it?"')
# df.add_system_transition(State.CITY_EVENTS_UNKNOWN, State.CITY_EVENTS, '"Interesting. I am not quite familiar with this aspect of"$city"What about talking about something that I know, like interesting events there?"')

# # User Turn
# df.add_user_transition(State.CITY_EVENTS_CERTAIN, State.CITY_EVENTS_CERTAIN_Y, '[{yes, yea, yup, yep, i do, yeah, a little, sure, of course, i have, i am, sometimes, too, as well, also, agree, ok, fine, okay, famous food, food}]')
# # df.add_user_transition(State.CITY_TOURISM_CERTAIN, State.CITY_EVENTS_CERTAIN_N, '[{no, nope, dont}]')
# df.add_user_transition(State.CITY_EVENTS_CERTAIN, State.ASK_TRAVEL_CITY, '[$city=#CATCH()]')
# df.set_error_successor(State.CITY_EVENTS_CERTAIN, State.CITY_EVENTS_CERTAIN_N)

# # System Turn
# df.add_system_transition(State.CITY_EVENTS_CERTAIN_N, State.CITY_CULTURE, '{Alright, Ok, Then}".I am also familiar with the culture in"$city". Would you like to know about it?"')
# df.add_system_transition(State.CITY_EVENTS_CERTAIN_Y, State.CITY_CULTURE, '{Nice,Good,Great, Cool,Wonderful,Awesome}"!"$event","#DETAIL(city, event, event)"I am also familiar with the culture in"$city".Would you like to know about it?"')

# ############################# Culture Part #########################################################################################################################
# # User Turn
# df.add_user_transition(State.CITY_CULTURE, State.CITY_CULTURE_Y, '[#CATCH_YES()]')
# df.add_user_transition(State.CITY_CULTURE, State.ASK_TRAVEL_CITY, '[$city=#CATCH()]')
# df.add_user_transition(State.CITY_CULTURE, State.ASK_TRAVEL_CITY_UNKNOWN_INLIST, '[$city=#CATCH_CITY_LIST()]')
# df.set_error_successor(State.CITY_CULTURE, State.CITY_CULTURE_N)

# # System Turn
# df.add_system_transition(State.CITY_CULTURE_Y, State.CITY_REASON, '{Nice,Good, Great, Cool,Wonderful,Awesome}"!About the"$certain_culture={#RANDOM_CULTURE(city,culture)}","#DETAIL(city, culture, certain_culture)"So, why do you want to travel to"$city"?"')
# df.add_system_transition(State.CITY_CULTURE_N, State.CITY_REASON, '{Alright, Ok, Then}"So, why do you want to travel to"$city"?"')

# ############################# Travel Reason ##########################################################################################################
# # User Turn
# df.add_user_transition(State.CITY_REASON, State.CITY_REASON_NEGATIVE,'[#CATCH_NO()]')
# df.add_user_transition(State.CITY_REASON, State.CITY_REASON_POSITIVE, '[{interesting, beautiful, weather,love,temperature,like,good,nice}]')
# df.set_error_successor(State.CITY_REASON, State.CITY_REASON_UNKNOWN)

# # System Turn
# df.add_system_transition(State.CITY_REASON_POSITIVE, State.END, '{Nice,Good, Great, Cool,Wonderful,Awesome, I agree}"!I have to say"$city"is a wonderful city which is worth traveling to because it"#DETAIL(city, reason_for_travel)"!"')
# df.add_system_transition(State.CITY_REASON_NEGATIVE, State.END, '{Alright, Ok, Then}".But I think"$city"is a wonderful city which is worth traveling to because it"#DETAIL(city, reason_for_travel)"!"')
# df.add_system_transition(State.CITY_REASON_UNKNOWN, State.END, '{Interesting, I see}".In my opinion, I think"$city"is a wonderful city which is worth traveling to because it"#DETAIL(city, reason_for_travel)"!"')

####################### End Travel Component ##############################################################################################################################################
# # END
# df.set_error_successor(State.CITY_REASON_ANS, State.TRAVEL_END)
# df.add_system_transition(State.TRAVEL_END, State.END, '"I\'m glad to talk with you. What other topics would you like to talk about?"')

df.update_state_settings(State.END, system_multi_hop=True)
# df.add_system_transition(State.END, State.START, '" "')
# end (recurrent) the dialogue
# end (recurrent) the dialogue

if __name__ == '__main__':
    # automatic verification of the DialogueFlow's structure (dumps warnings to stdout)
    df.check()
    #df.precache_transitions()
    # run the DialogueFlow in interactive mode to test
    df.run(debugging=False)

