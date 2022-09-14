from emora_stdm import DialogueFlow, KnowledgeBase, Macro
from enum import Enum, auto
import json
from emora._students.dialogues import spec_Dict, dict_genre, mpMiniGames_dict, mpCharacter_dict, underChar_dict,\
acVillager_dict, pokeType_dict, smashStage_dict, smashfighter_dict, mkartChar_dict,\
leagueChamp_dict, dotaHeros_dict, r6sOperator_dict, overHero_dict, descripSpec_Dict, descriptionFull_dict,\
comp_Dict
from emora._students.classes import SPECIFIC1a, SPECIFIC2a, SPECIFIC2b, SPECIFIC3a, SPECIFIC3b, GENRE_OPINION,\
syn_det, like_macro, dislike_macro, game_desc, ontology2, list_items_one, list_items_two,\
GENRE_RECOMMENDER, explain_response, fave_games, genre_pivot, genre_pivot_learning, GENRE_STORY_OPINION
from fuzzywuzzy import fuzz
from _globals import STUDENTSDIR

# Opening the json dictionary
with open(STUDENTSDIR.replace("__***__",'ont_dict.json')) as json_file:
    ontology = json.load(json_file)
######################################################################################################

class State(Enum):
    # # Initialize
    
    # Social Gaming
    sS1a= auto()
    sS2a= auto()
    sS2b= auto()
    sS2c= auto()
    sS3a= auto()
    sS3b= auto()
    sS3c= auto()
    sU1a= auto()
    sU2a= auto()
    sU2b= auto()
    sS1aA= auto()

    # Learning module
    LS1a= auto()
    LS2a= auto()
    LS2aa= auto()
    LS3a = auto()
    LS3aa = auto()
    LU1a= auto()
    LU2a= auto()
    LU3a= auto()
    LS1b = auto()
    LS1 = auto()
    LS1c= auto()
    LS2b= auto()

    # Start state
    S0= auto()

    # Favorite gaming
    fS1a= auto()
    fS1aa= auto()
    fS1b= auto()
    fS1ba= auto()
    fS1bb= auto()
    fS1c= auto()
    fS1d= auto()
    fS2ab= auto()
    fS2ac= auto()
    fS2ba= auto()
    fS2bb= auto()
    fS2da= auto()
    fS2db= auto()
    fS2dc= auto()
    fS3ba= auto()
    fS3bb= auto()
    fS3bd = auto()
    fS4a= auto()
    fS4b= auto()
    fU0= auto()
    fU1d= auto()
    fU2a= auto()
    fU2aa= auto()
    fU2ac= auto()
    fU2b= auto()
    fU2da= auto()
    fU2db= auto()
    fU3b= auto()
    fU4a= auto()
    fU4b= auto()
    fS2bc = auto()
    fS3bc = auto()
    fS4bc = auto()
    fU5a= auto()
    fS1dc= auto()
    fS1dd=auto()
    fS1de= auto()
    fU2b2 = auto()
    fU3b2 =auto()
    fU2a2 =auto()



    # General Gaming
    gS1a= auto()
    gS1b= auto()
    gS1c= auto()
    gS1d= auto()
    gS1f= auto()
    gS2a= auto()
    gS2b= auto()
    gS2c= auto()
    gS2d = auto()
    gS3aa= auto()
    gS3ab= auto()
    gS3b= auto()
    gS3c= auto()
    gS4a= auto()
    gS4b = auto()
    gS5a= auto()
    gU0= auto()
    gU1aa= auto()
    gU1ac= auto()
    gU1ad= auto()
    gU2a= auto()
    gU2b= auto()
    gU2c= auto()
    gU2d= auto()
    gU3a= auto()
    gU3b= auto()
    gU4a= auto()
    gS1h= auto()
    gS1g= auto()
    gS2e= auto()

    g5a= auto()
    g5b= auto()
    g5c= auto()
    g5d= auto()
    gU6= auto()

    # Health Module
    hS0 = auto()
    hU0 = auto()
    hS0a =auto()

    hS1a = auto()
    hS1b = auto()
    hS1c = auto()
    hS1d = auto()

    hU1a = auto()
    hU1b = auto()
    hU1c = auto()
    hU1d = auto()

    END = auto()

    # Meta
    mS0 = auto()
    mU0 = auto()
    mS1a = auto()
    mS1b= auto()
    mS1c = auto()
    mS1d = auto()
    mS0a= auto()

    mU1a= auto()
    mU1b = auto()
    mU1c = auto()
    mU1d = auto()

    mS1aa= auto()
    mS1ab = auto()
    mS1ac = auto()

    mS1ba = auto()
    mS1bb = auto()
    mS1bc = auto()

    mS1ca = auto()
    mS1cb = auto()
    mS1cc = auto()


    mS2da = auto()
    mS2db = auto()
    mS2dc = auto()



    mU2a = auto()
    mU2b = auto()
    mU2d = auto()

    mS1db = auto()
    mS1da = auto()

    # Ending
    OOO = auto() #future health module
    ERR = auto()
    endChallenge= auto()
    endGen= auto()
    endGenre= auto()
    endMario= auto()
    endMeta= auto()
    endOtherGames= auto()
    endPuzzle= auto()
    endRec= auto()
    endSocial= auto()
    endSpecGame= auto()
###########################################################################
## NaTex - Affirmation / Denial / Question
affirm = r"[{#ONT(positive), #ONT(agree), #ONT(like), #ONT(interested)}]"
deny = r"[{#ONT(negative), #ONT(disagree), #ONT(dislike)}]"
general = r"[$generalG={#ONT(largeGameList)} -#ONT(specificGame)]"
dont_know = '[{' \
            'dont know,do not know,unsure,[not,{sure,certain}],hard to say,no idea,uncertain,[!no {opinion,opinions,idea,ideas,thought,thoughts,knowledge}],' \
            '[{dont,do not}, have, {opinion,opinions,idea,ideas,thought,thoughts,knowledge}],' \
            '[!{cant,cannot,dont} {think,remember,recall}]' \
            '}]'
#### Module - General Gaming / Experience Gaming
# Regularly used natex inputs
# Anything: '/.*/'
# Affirm: '<[#ONT(positive)]>'
# Deny: '<[#ONT(negative)]>'
#######################################################################################
# CLASSES

class game_catcher(Macro):
    def run(self, ngrams, vars, args):
        global catch_flag
        try:
            vars['catch_flag'] = '2'
            return_dialogue = ""
            temp = vars['inquiry']
            high_r = -1
            for j in genG:
                for i in ontology["ontology"][j]:
                    if 100 > fuzz.ratio(i, temp) > 50:
                        if fuzz.ratio(i, temp) > high_r:
                            high_r = fuzz.ratio(i, temp)
                            return_dialogue += "i didnt quite catch that! did you mean " + i + "?"
                            if j == "specificGame":
                                vars['specG'] = i
                                catch_flag = 1
                                vars['catch_flag'] = '1'
                            else:
                                vars['generalG'] = i
                                catch_flag = 0
                                vars['catch_flag'] = '0'
                            return return_dialogue
            vars['catch_flag'] = '2'
            return "i have not heard of that game before. do you know a lot about it?"
        except:
            vars['catch_flag'] = '2'
            return "i have not heard of that game before. do you know a lot about it?"

class game_catcher_parttwo(Macro):
    def run(self, ngrams, vars, args):
        try:
            if catch_flag == 1:
                talked.append(vars['specG'])
                return "would you like to talk about " + vars['specG'] + "? i know a lot about the game!"
            else:

                return "oh! ive heard of " + vars['generalG'] + ". but i do not know very much about it. would you be willing to tell me about it?"
        except:
            return "wonderful, i love learning about new games. would you be willing to tell me about this game?"

class metaComp(Macro):
    def run(self, ngrams, vars, args) -> str:
        try:

             if len(vars['company']) > 0:
                c = vars['company']

                #make sure name is uniform
                playstation = ["ps", "sony"]
                fromsoftware = ["fromsoft","from software","from soft","dark souls"]
                riotgames = ["riot games","riot"],
                blizzard = ["blizard", "activision"]
                rockstar_games = ["rockstar", "rock star"]

                if c in playstation:
                    c = 'playstation'
                elif c in fromsoftware:
                    c = 'fromsoftware'
                elif c in riotgames:
                    c = 'riotgames'
                elif c in blizzard:
                    c = 'blizzard'
                elif c in rockstar_games:
                    c = 'rockstar games'


                #return s
                opinion = comp_Dict.get(c)

                return opinion + " as the industry grows as a whole, i know there is much debate over whether video games should be viewed as art, or merely entertainement. what do you think about video games as an art form?"
        except:
            return "i certainly see a lot of room for growth in that company. what do you think about video games as an art form?"
############################################################
#############################################################
#global list so that there is no repeat in conversation topic
genG = ["specificGame", "generalGame", "horror_games", "shooters_games","adventure_games", "racing_games", "rpg_games", "real-time strategy_games","party_games","roguelike_games", "survival_games","tbt_games", "tbs_games", "platformer_games", "beat-em-up_games","stealth_games", "rhythm_games", "metroidvania_games", "visual novels_games", "role-playing games_games", "tactical rpg_games", "sandbox rpg_game", "tower defense_games", "puzzle_games", "idle_games",  "casual_games", "educational_games"]
talked = []
not_talked = ontology["ontology"]["specificGame"].copy()
# if catch_flag is 0 -> genGame, if catch_flag is 1 -> specific Game
catch_flag = -1 # default flag is 0 because default flag of -1 crashes program
############################################################


knowledge = KnowledgeBase()
knowledge.load_json(ontology)
df = DialogueFlow('start', initial_speaker=DialogueFlow.Speaker.SYSTEM, kb=knowledge,
                  macros={"syn_det":syn_det(), "fave_games":fave_games(), "SPECIFIC1a": SPECIFIC1a(),
                          "SPECIFIC2a": SPECIFIC2a(), "SPECIFIC2b": SPECIFIC2b(),"SPECIFIC3a":SPECIFIC3a(),
                          "SPECIFIC3b": SPECIFIC3b(), "GENRE_OPINION": GENRE_OPINION(), "GENRE_RECOMMENDER": GENRE_RECOMMENDER(),
                          "like_macro": like_macro(), "dislike_macro":dislike_macro(), "game_desc":game_desc(),
                         "game_catcher":game_catcher(), "game_catcher_parttwo":game_catcher_parttwo(), "list_items_one":list_items_one(),
                         "list_items_two":list_items_two(), "explain_response":explain_response(), "genre_pivot":genre_pivot(),
                          "genre_pivot_learning": genre_pivot_learning(),"list_items_two":list_items_two(), "explain_response":explain_response(), "genre_pivot":genre_pivot(),
                         "metaComp":metaComp(), "GENRE_STORY_OPINION":GENRE_STORY_OPINION()})
### Main Prompt - Do you play video games?
df.add_system_transition('start', State.gU0, '"Do you play video games?" $empty=""')

df.add_system_transition('request', 'start', '', score=2.0)
df.add_system_transition('request', State.gU0, '"Do you play video games?" $empty=""')

df.update_state_settings('start', enter='#IF($vgamev!=True) #SET($vgamev=True)')

df.add_user_transition(State.gU0, 'yes_vgames', '[#ONT(agree)]', score = 2.0)
df.add_user_transition(State.gU0, State.gS1b, '[#ONT(negative)]', score=2.0)
df.add_user_transition(State.gU0, State.gS1h, dont_know, score=3.0)
df.add_user_transition(State.gU0, State.LS1, general, score = 3.0)
df.add_user_transition(State.gU0, State.fS1d, '[{$specG=#ONT(specificGame)}]', score=3.0)
df.set_error_successor(State.gU0, State.mS0)

#df.add_user_transition(State.gU0, State.gS1d, '[$word=#ONT(dislike), $dislike=/.*/]') #has pos tag DELETED
#df.add_user_transition(State.gU0, State.gS1c, '[[$word=#ONT(like), $like=/.*/], -#ONT(positive)]') #has pos tag DELETED
#df.add_system_transition(State.gS1c, State.gU1ac, '"why do you" $word #like_macro') #pos ner tags
#df.add_system_transition(State.gS1d, State.gU1ad, '"why do you" $word #dislike_macro') #pos ner tags
#df.add_user_transition(State.gU1ac, State.fS1d, '[{$specG=#ONT(specificGame)}]')#pos ner tags
#df.add_user_transition(State.gU1ac, State.gS2d, '[-{$specG=#ONT(specificGame)} $explain=/.*/]') # continues from why do you like #pos ner tags
#df.add_user_transition(State.gU1ad, State.gS2d, '$explain=/.*/') # continues from why do you dislike #part of pos tag
#df.add_system_transition(State.gS2d, State.gU2c, '[!#explain_response "are there maybe particular types of stories you enjoy like horror or adventure stories?"]') #pos ner


### responses to main question
df.add_system_transition('yes_vgames', State.fU0, '"i like to game in my free time, too. what\'s your favorite video game?" #SET($vgamev=True)')
df.add_system_transition(State.gS1b, State.gU1aa, '"i understand that video games do not have the same appeal to everyone. maybe together we can find one you would enjoy. in general would you prefer a game you can play by yourself, or with others?"')
df.add_system_transition(State.gS1h, State.gU1aa, '"it is very common to not know very much about video games. maybe together we can find one you would enjoy. in general would you prefer a game you can play by yourself, or with others?"')


#TODO: expand accepted phrases
###alone or with friends
df.add_user_transition(State.gU1aa, State.gS2a,"[{$response=#ONT(alone)}]") # alone
df.add_user_transition(State.gU1aa, State.gS2b, "[{$response=#ONT(team)}]") # with others
df.add_user_transition(State.gU1aa, State.gS2e, dont_know)
df.set_error_successor(State.gU1aa, State.gS2c)

df.add_system_transition(State.gS2a, State.gU2a, '"there are a lot of fun games for people that are more introverted. i highly recommend the" $specG=pokemon "franchise, it is very fun to play solo but has a multiplayer component for when you are feeling social! would you be interested in that?"')
df.add_system_transition(State.gS2b, State.gU2b, '"thats awesome! video games can be a very social activity. i highly recommend the" $specG=mario kart "games, there are great in a group setting! would you be interested in them?"')

df.add_user_transition(State.gU2a, State.g5a, '[{#ONT(agree)}]')
df.add_user_transition(State.gU2b, State.g5a, '[{#ONT(agree)}]')
df.add_user_transition(State.gU2a, State.g5c, '[{#ONT(question)}]')
df.add_user_transition(State.gU2b, State.g5c, '[{#ONT(question)}]')
df.add_user_transition(State.gU2a, State.g5d, dont_know, score = 3.0)
df.add_user_transition(State.gU2b, State.g5d, dont_know, score = 3.0)
df.add_user_transition(State.gU2a, State.g5b, '[{#ONT(negative)}]', score = 2.0)
df.add_user_transition(State.gU2b, State.g5b, '[{#ONT(negative)}]', score = 2.0)
df.set_error_successor(State.gU2b, State.g5b)
df.set_error_successor(State.gU2a, State.g5b)

df.add_system_transition(State.g5a, State.mU0, '"i look forward to talking to you about the " $specG " franchise in the future! in the mean time, what do you see for the future of gaming?"') #Todo: opening meta question needs to change
df.add_system_transition(State.g5b, State.mU0, '"i will brainstorm more games for you! in the mean time, what do you see for the future of gaming?"') #Todo: opening meta question needs to change

#game description
df.add_system_transition(State.g5c, State.gU6, '[!#game_desc]')
df.add_system_transition(State.g5d, State.gU6, 'well, #game_desc')

df.add_user_transition(State.gU6, State.g5a, '[{#ONT(agree)}]')
df.add_user_transition(State.gU6, State.g5b, '[{#ONT(negative)}]', score = 2.0)
df.set_error_successor(State.gU6, State.g5b)


##stories
df.add_system_transition(State.gS2c, State.gU2c, '"hmmmm....lets try another angle, there are many great stories in games! are there maybe particular types of stories you enjoy like horror or adventure stories?"' )
df.add_system_transition(State.gS2e, State.gU2c, '"a lot of people are a bit of both! lets try another angle, are there maybe particular types of stories you enjoy like horror or adventure stories?"' )
df.add_user_transition(State.gU2c, State.gS3aa, "[{$genreS=#ONT(genreStory)}]", score = 2.0)
df.add_user_transition(State.gU2c, State.g5b, dont_know)
df.set_error_successor(State.gU2c, State.sS1aA)

df.add_system_transition(State.gS3aa, State.gU3a, '[!#GENRE_STORY_OPINION]')
df.add_user_transition(State.gU3a, State.g5a, '[{#ONT(agree)}]')
df.add_user_transition(State.gU3a, State.g5b, '[{#ONT(negative)}]', score = 2.0)
df.add_user_transition(State.gU3a, State.g5d, dont_know, score = 3.0)
df.add_user_transition(State.gU3a, State.g5c, '[{#ONT(question)}]')
df.set_error_successor(State.gU3a, State.g5b)
##end general

# conversation about how great games are for social growth
# SOCIAL MODULE
df.add_system_transition(State.sS1a, State.sU1a, '"Do you think that " $genre " video games can help people learn better social skills?"')
df.add_system_transition(State.sS1aA, State.sU1a, '"It seems like games cover lots of stories, and help people build social skills. Do you think so too?"')
df.add_user_transition(State.sU1a, State.sS3a, '[{#ONT(agree), #ONT(positive), #ONT(like)}]') # contains the words agree, social?
df.add_user_transition(State.sU1a, State.sS3b, '[{#ONT(disagree), #ONT(negative), #ONT(dislike)}]', score =2) # contains negative words, disagree, antisocial
df.add_user_transition(State.sU1a, State.hS0, '[{#ONT(metaHealth), #ONT(healthExercise), #ONT(healthBreaks)}]', score = 2.0)
df.add_user_transition(State.sU1a, State.hS0a, dont_know, score=3)
df.set_error_successor(State.sU1a, State.hS0a)


df.add_system_transition(State.sS3a, State.hU0, '"im glad you agree that video games can provide a great avenue to connect with friends. its also important to stay healthy while gaming. how should people practice healthy gaming?"')
df.add_system_transition(State.sS3b, State.hU0, '"hmmm... i have actually made a lot of connections through video games. however a lot of people view gaming negatively due to health habits. how do you think people can practice healthy gaming? "')

##end Social

#HEALTH

df.add_system_transition(State.hS0, State.hU0, '"i personally like to stay healthy as i game. what are ways you think people can practice healthy gaming?"') #Could open the conversation for the user to either continue this conversation on healthy gaming or go to another conversation. Doesn't come off as preachy, just as a personal preference. The user could ask the bot to elaborate.
df.add_system_transition(State.hS0a, State.hU0, '"often times the portential social benefits of video gaming are outshadowed by ideas of people using video games to act in an unhealthy manner. what are ways you think people can practice healthy gaming?"') #Could open the conversation for the user to either continue this conversation on healthy gaming or go to another conversation. Doesn't come off as preachy, just as a personal preference. The user could ask the bot to elaborate.


df.add_user_transition(State.hU0, State.hS1a, '"[{how, you, your}, -#ONT("healthExcersise")]"') #If the user asks for the elaborate on how the bot likes to stay healthy as it games -- how
df.add_user_transition(State.hU0, State.hS1b, '"[{what, why, who}, -#ONT("healthExcersise")]"') #If the user asks for the elaborate on how the bot likes to stay healthy as it games -- why
df.add_user_transition(State.hU0, State.hS1c, '"[#ONT("healthExcersise"]"') #excersise
df.add_user_transition(State.hU0, State.hS1d, '"[#ONT("healthBreaks"]"') #breaks
df.set_error_successor(State.hU0, State.hS1a)


df.add_system_transition(State.hS1a, State.hU1a, '"i find that healthy gaming helps me mantain a positive lifestyle while enjoying video games. for me, this means taking breaks and going on walks!"') #Could open the conversation for the user to either continue this conversation on healthy gaming or go to another conversation. Doesn't come off as preachy, just as a personal preference. The user could ask the bot to elaborate.
df.set_error_successor(State.hU1a, State.END) #transition to end

df.add_system_transition(State.hS1b, State.hU1b, '"i think healthy gaming is important because before, i noticed i was prioritizing gaming over many other aspects of my life which was growing to be unhealthy."') #Could open the conversation for the user to either continue this conversation on healthy gaming or go to another conversation. Doesn't come off as preachy, just as a personal preference. The user could ask the bot to elaborate.
df.set_error_successor(State.hU1b, State.END) #transition to end

df.add_system_transition(State.hS1c, State.hU1c, '"exercise can be a great way to stay healthy! I really enjoy hiking."')
df.set_error_successor(State.hU1c, State.END) #transition to end


df.add_system_transition(State.hS1d, State.hU1d, '"taking breaks can be a great way to stay healthy! i like to talk breaks by making some delicious food."')
df.set_error_successor(State.hU1d, State.END) #transition to end

#end social


# Learning module this is used when we know they said a game but we did not know more about it
df.add_system_transition(State.fS2db, State.LU1a, '"i guess i have never heard of that game before. what is the genre?"')
df.add_system_transition(State.LS1, State.LU1a, '"ive heard of" $generalG " before but i do not know much about it. what is the genre?"')

df.add_user_transition(State.LU1a, State.LS1a, '[<$learned_genre=#ONT(genre), -#ONT(genreSpec)>]')
df.add_user_transition(State.LU1a, State.LS1b, '[$genre=#ONT(genreSpec)]')
df.add_user_transition(State.LU1a, State.LS1c, dont_know)
df.set_error_successor(State.LU1a, State.LS2aa)


df.add_system_transition(State.LS1c, State.LU2a, '"the best games fall into several genres, so its often hard to catagorize them. is that game single-player or multiplayer?"')
df.add_system_transition(State.LS2aa, State.LU2a, '"i never knew that was a genre. is that game single-player or multiplayer?"')
df.add_system_transition(State.LS1a, State.LU2a, '$learned_genre games can be a lot of fun"! is it single-player or multiplayer?"')

df.add_user_transition(State.LU2a, State.LS2a, r"$learned_type=[{#ONT(team)}]")
df.add_user_transition(State.LU2a, State.LS2b, r"$learned_type=[{#ONT(alone)}]")
df.set_error_successor(State.LU2a, State.LS3aa)

df.add_system_transition(State.LS2a, State.mU0, '"thank you for telling me about this multiplayer game! although i have consistantly loved playing video games with my friends, it is undeniable how much the industry has changed over the years. what do you see for the future of gaming?"') #todo: fix meta question
df.add_system_transition(State.LS2b, State.mU0, '"thank you for telling me about this single-player game! through all of the games i have played i see a lot of change in the gaming industry. what do you see for the future of gaming?"') #todo: fix meta question
df.add_system_transition(State.LS3aa, State.mU0, '"thank you for telling me about this game! what do you see for the future of gaming?"')#todo: fix meta question

df.add_system_transition(State.LS1b, State.fU5a, '[!#genre_pivot_learning]')
#todo: is there a way to redirect known games to their genre through a genre pivot esque thing

### end of learning

#### Favorite Gaming Conversation
df.add_user_transition(State.fU0, State.fS1a, '[!-{#ONT(specificGame), #ONT(largeGameList)} $inquiry=/.*/]', score = 0.5) #ToDo: fix
df.add_user_transition(State.fU0, State.fS1d, '[{$specG=#ONT(specificGame)}]', score=3.0) # If the user talks about a game we know about
df.add_user_transition(State.fU0, State.LS1,  general, score=2.0) # If the user has a specific game they like but it's not something we know a lot about
df.add_user_transition(State.fU0, State.fS1c, dont_know, score = 1.0)
df.set_error_successor(State.fU0, State.fS1c) # If user answers anything not in general game or specific game list

# sub dialogue
#df.add_system_transition(State.fS1b, State.fU2aa, '"oh! ive heard of "$generalG", but i have never played it. how would you describe the game?"')
#df.add_user_transition(State.fU2aa, State.fS1ba, '$input=/.*/')
#df.add_system_transition(State.fS1ba, State.fU2ac, '[!#syn_det()]')
#df.add_user_transition(State.fU2ac, State.fS1bb, '/.*/')
#df.add_system_transition(State.fS1bb, State.fU2a, '[!"thats really interesting."#fave_games]')
###

df.add_system_transition (State.fS1c, State.fU2a, '[!#fave_games]')


#Catching unknown games or typos
#todo: use the catch flags to figure out which line of dialogue is happening, figure out if this is a game we know
###TODO: This is not working correctly!!!!!!
df.add_system_transition(State.fS1a, State.fU1d, '[!#game_catcher]')
df.add_user_transition(State.fU1d, State.fS2db, '[#ONT(negative)]', score=2.0) # i have not heard of that gen/spec game
df.add_user_transition(State.fU1d, State.LS1, general, score = 3.0) # caught a game that is general, learn about it
df.add_user_transition(State.fU1d, State.fS1d, '[$specG=#ONT(specificGame)]', score=3.0) # caught a game that is specific
df.add_user_transition(State.fU1d, State.fS1dd, '<[{#ONT(negative)}], #EQ($catch_flag,2)>', score=3.0) #idk the game, can i learn? YES
df.add_user_transition(State.fU1d, State.fS2da, '<[{#ONT(agree)}]>', score=3.0) #idk the game, can i learn? YES
#df.add_user_transition(State.fU1d, State.fS1dc, '<[{#ONT(agree)}], -#EQ($catch_flag,2)>', score=3.0) #idk the game, can i learn? YES
#df.add_user_transition(State.fU1d, State.fS2da, '<[{#ONT(agree)}], #EQ($catch_flag,2)>', score = 2.0) # caught the yes #todo: come back to this
df.set_error_successor(State.fU1d, State.fS2dc)


df.add_system_transition(State.fS2da, State.fU2da, '[!#game_catcher_parttwo]. the catch flag is $catch_flag')
df.add_user_transition(State.fU2da, State.fS1d, '<[{#ONT(agree)}], #EQ($catch_flag,1)>', score=3.0)
df.add_user_transition(State.fU2da, State.fS1de, '<[{#ONT(negative)}], #EQ($catch_flag,1)>', score=3.0)
df.add_user_transition(State.fU2da, State.fS1dc, '<[{#ONT(agree)}]>', score=2.0)  #teach me?
df.add_user_transition(State.fU2da, State.fS1dd, '<[{#ONT(negative)}]>', score=2.0)  #teach me?
df.set_error_successor(State.fU2da, State.fS2dc)

df.add_system_transition(State.fS2dc, State.fU2a, '[!#fave_games]')
df.add_system_transition(State.fS1dc, State.LU1a, '"wonderful! first, what genre would you consider that game to be?"')
df.add_system_transition(State.fS1dd, State.mU0, '"all well, in that case what can you tell me about the future of gaming?"') #todo: fix the meta question
df.add_system_transition(State.fS1de, State.mU0, '"thats too bad, well instead i would love some of your more broad video game opinons. what do you see for the future of gaming?"') #todo: fix the meta question


# Specific
df.add_system_transition(State.fS1d, State.fU2b, '[!#SPECIFIC1a]')
df.add_user_transition(State.fU2b, State.fS2ba, '[{$ans1=#ONT(specAnswer1), $ans_not1=#ONT(specAnswer2)}]') #Specific # answer not = for all coverage of misidentifying a game
df.add_user_transition(State.fU2b, State.fS2bc, '[{what, show, who, example, examples}, -#ONT(specAnswer1)]')
df.set_error_successor(State.fU2b, State.fS2bb)

df.add_system_transition(State.fS2bc, State.fU2b2, '[!#list_items_one]')
df.add_user_transition(State.fU2b2, State.fS2ba, '[{$ans1=#ONT(specAnswer1), $ans_not1=#ONT(specAnswer2)}]') #Specific # answer not = for all coverage of misidentifying a game
df.set_error_successor(State.fU2b2, State.fS2bb)

df.add_system_transition(State.fS2bb, State.fU3b, '[!#SPECIFIC2b]')
df.add_system_transition(State.fS2ba, State.fU3b, '[!#SPECIFIC2a]') #type / champion or something #initializing ans2 for later use

df.add_user_transition(State.fU3b, State.fS3bd, '[{$ans2=#ONT(specAnswer2), $ans_not2=#ONT(specAnswer1)}]')
df.add_user_transition(State.fU3b, State.fS3bc, '[<$temp=#ONT(agree), #EQ($switch,true)>]') #ooo
df.add_user_transition(State.fU3b, State.fS3ba, '[{what, show, who, example, examples}, -#ONT(specAnswer2)]') # asking for a list of the item we asked about
df.set_error_successor(State.fU3b, State.fS3bb)

df.add_system_transition(State.fS3ba, State.fU3b2, '[!#list_items_two]')
df.add_user_transition(State.fU3b2, State.fS3bd, '[{$ans2=#ONT(specAnswer2), $ans_not2=#ONT(specAnswer1)}]')
df.add_user_transition(State.fU3b2, State.fS3bc, '[<$temp=#ONT(agree), #EQ($switch,true)>]') #ooo
df.set_error_successor(State.fU3b2, State.fS3bb)

df.add_system_transition(State.fS3bc, State.fU2b, '$specG=$switch_game $ans1=$empty $ans2=$empty "is fun too." [!#SPECIFIC1a]') # if the user decides to switch game topics

df.add_system_transition(State.fS3bb, State.fU4a, r'[!#SPECIFIC3b]')
df.add_system_transition(State.fS3bd, State.fU4b, r'[!#SPECIFIC3a]')

df.add_system_transition(State.fS4bc, State.fU2b, '$specG=$switch_game $ans1=$empty $ans2=$empty "is also cool." [!#SPECIFIC1a]')


#to do: idk man
df.add_user_transition(State.fU4b, State.fS4bc, '[<$temp=#ONT(agree), #EQ($switch,true)>]', score= 3.00) #ooo
df.add_user_transition(State.fU4a, State.fS4a, '<[{#ONT(agree)}], #EQ($switchGP, false)>')  #todo: make broader
df.add_user_transition(State.fU4b, State.fS4a, '<[{#ONT(agree)}], #EQ($switchGP, false)>', score=2.00)  #todo: make broader
df.add_user_transition(State.fU4a, State.mS0a, '[{#ONT(disagree)}]')  #todo: make broader
df.add_user_transition(State.fU4b, State.mS0a, '[{#ONT(disagree)}]')  #todo: make broader
df.set_error_successor(State.fU4a, State.mS0)
df.set_error_successor(State.fU4b, State.mS0)

df.add_system_transition(State.fS4a, State.fU5a, '"i like them too. "[!#genre_pivot]') #todo: add a check here to make sure it is not an infinite loop
df.add_user_transition(State.fU5a, State.fS1d, affirm)
df.add_user_transition(State.fU5a, State.fS2ab, deny)
df.set_error_successor(State.fU5a, State.fS2ab)

# General
affirm = r"[{#ONT(positive), #ONT(agree), #ONT(like), #ONT(interested)}]"
df.add_system_transition(State.fS2ab, State.fU2a, '[!#fave_games]') # this loops from negative
df.add_system_transition(State.fS1aa, State.fU2a2, '[!#game_desc]') #TODO: link this back somewhere else this shoulw be  going somewhere else?

df.add_user_transition(State.fU2a2, State.fS2ab, '[<{#ONT(negative)},#EQ($switch3,false)>]', score =1.5) #negative
df.add_user_transition(State.fU2a2, State.fS1d, '[<{#ONT(positive), #ONT(agree), #ONT(like), #ONT(interested)}, #EQ($switch3,false)>]') #affirmative; this starts the conversation about specific games
df.add_user_transition(State.fU2a2, State.sS1a, '<[$genre=#ONT(genre)], #EQ($switch3,true)>', score=2.0)
df.set_error_successor(State.fU2a2, State.sS1aA) #TODO: change this later


df.add_user_transition(State.fU2a, State.fS2ab, '[<{#ONT(negative)},#EQ($switch3,false)>]', score =1.5) #negative
df.add_user_transition(State.fU2a, State.fS1d, '[<{#ONT(positive), #ONT(agree), #ONT(like), #ONT(interested)}, #EQ($switch3,false)>]') #affirmative; this starts the conversation about specific games
df.add_user_transition(State.fU2a, State.fS1aa, '<{what is}, #EQ($switch3,false)>')
df.add_user_transition(State.fU2a, State.sS1a, '<[$genre=#ONT(genre)], #EQ($switch3,true)>', score=2.0)
df.set_error_successor(State.fU2a, State.sS1aA) #TODO: change this later
#df.set_error_successor(State.fU2a, State.fS2bb)





##### meta module insertion
df.add_system_transition(State.mS0a, State.mU0, '"im sorry to hear that. video games have so much to offer from visual storylines to character arcs and from challenges to mediums of social interaction. what do you see for the future of gaming?"')
df.add_system_transition(State.mS0, State.mU0, '"video games have so much to offer from visual storylines to character arcs and from challenges to mediums of social interaction. what do you see for the future of gaming?"')
df.add_user_transition(State.mU0, State.mS1a, '[#ONT(metaArt)]')
df.add_user_transition(State.mU0, State.mS1b, '[#ONT(metaVR)]')
df.add_user_transition(State.mU0, State.mS1c, '[#ONT(metaBus)]')
df.set_error_successor(State.mU0, State.mS1d)
#BOOKMARK

###ART CONVERSATION ##########
df.add_system_transition(State.mS1a, State.mU1a, '"video game graphics are getting more advanced, as designers render more and more creative images. what do you think about video games as an art form?"')
df.add_user_transition(State.mU1a, State.mS1aa, '[#ONT(agree)]')#yes/like
df.add_user_transition(State.mU1a, State.mS1ab, '[#ONT(negative)]')#no/dislike
df.set_error_successor(State.mU1a, State.mS1ac) #error

#to do:

##Yes
# if the user has not done speific game module
#df.add_system_transition( State.mS1aa, State.fS1a, '"I think so too! what are some of your favorite story driven video games?"')
#else
df.add_system_transition( State.mS1aa, State.mU1d, '"I think so too! unfortunately, although more than a billion people play video games worldwide, many people view video games as a negative pastime. why do you think people feel this way?"')



## no
# if the user has not done speific game module
#df.add_system_transition( State.mS1ab, State.fS1a, '"I entirely disagree! what are some of your favorite story driven video games?"')
#else
df.add_system_transition( State.mS1ab, State.mU1d, '"I entirely disagree! unfortunately, although more than a billion people playing video games world wide, many people view video games as a negative pastime. why do you  think people feel this way?"')

## error
# if the user has not done speific game module
#df.add_system_transition( State.mS1ac, State.fS1a, '"the artistic merit of video games is often questioned. what are some of your favorite story driven video games?"')
#else
df.add_system_transition( State.mS1ac, State.mU1d, '"the artistic merit of video games is often questioned. why do you think people view video games as a negative pastime?"')



###VR Conversation ####
df.add_system_transition(State.mS1b, State.mU1b, '"virtual reality is gaining traction right now! what do you think about virtual reality?"')
df.add_user_transition(State.mU1b, State.mS1ba, '[#ONT(agree)]')#yes/like
df.add_user_transition(State.mU1b, State.mS1bb, '[#ONT(negative)]')#no/dislike
df.set_error_successor(State.mU1b, State.mS1bb)



#to do: oooo
##Yes
# if the user has not done speific game module
#df.add_system_transition( State.mS1ba, State.fS1a, '"I think so too! what are some of your favorite story driven video games?"')
#else
df.add_system_transition( State.mS1ba, State.mU1c, '"virtual reality offers a beautiful addition to the video gaming world. unfortunately, it seems like some people think videogames are not good for kids. why do you think people feel this way?"')


## no
# if the user has not done speific game module
#df.add_system_transition( State.mS1bb, State.fS1a, '"I entirely disagree! what are some of your favorite story driven video games?"')
#else
df.add_system_transition( State.mS1bb, State.mU1d, '"virtual reality is a growing presence in gaming for sure. unfortunately, yeah, i mean, it seems like some people think videogames are not good for kids. why do you think people feel this way?"')




###INDUSTRY CONVERSATION ####
df.add_system_transition(State.mS1c, State.mU1c, '"the video game industry has grown tremendously in the past decade, however some people speculate that the success of these companies will not last. what video game companies do you think will endure?"')
df.add_user_transition(State.mU1c, State.mS1ca, '[$company=#ONT(metaComp)]')#catch from ontology
df.set_error_successor(State.mU1c, State.mS1cc)


##Yes
# if the user has not done speific game module
# df.add_system_transition( State.mS1ca, State.fS1a, '"#Metacomp what are some of your favorite games from $company?"')
#else
df.add_system_transition( State.mS1ca, State.mU1a, '[!#metaComp]')


## error
# if the user has not done speific game module
# df.add_system_transition( State.mS1cc, State.fS1a, 'it is hard to say what the industry will look like in the near future considering how much it has grown in the past fifteen years. what games would you say helped fuel that growth?"')
#else
df.add_system_transition( State.mS1cc, State.mS1a, '"it is hard to say what the industry will look like in the near future considering it grew a lot. what do you think about video games as an art form?"')


###### stigma #######


df.add_system_transition(State.mS1d, State.mU1d, '"a lot of people think video games are bad for kids. what do you think are the reasons people look down on playing video games?"')
df.add_user_transition(State.mU1d, State.mS1da, '[#ONT(metaEntertainment)]')# entertainmentMeta
df.add_user_transition(State.mU1d, State.mS1db, '[#ONT(metaHealth)]') #healthMeta
df.set_error_successor(State.mU1d, State.mS1db) #error




##entertainment
df.add_system_transition( State.mS1da, State.mU2d, '"thats true theyre a source of entertainment, but there are a lot of parallels that video games and sports share. do you think its unfair for the two to be seen as equals?"')
df.add_user_transition(State.mU2d, State.mS2da, '[#ONT(agree)]')#yes
df.add_user_transition(State.mU2d, State.mS2db, '[#ONT(negative)]')#no
df.set_error_successor(State.mU2d, State.mS2dc)

#no
df.add_system_transition( State.mS2da, State.hU0, '"i agree! however it is important to practice healthy gaming! what are ways do you think people can practice healthy gaming?"')

#yes
df.add_system_transition( State.mS2db, State.hU0, '"i disagree. video games can foster a lot of great skills similar to sports. in both sports and video games however, it is important to stay healthy. what are ways you can practice healthy gaming?"')

#error
df.add_system_transition( State.mS2dc, State.hU0, '"regardless of whether you play sports or video games, youve got to take care of yourself. what are ways do you think people can practice healthy gaming?"')


## healthy gaming
# transition into healthy gaming module
df.add_system_transition( State.mS1db, State.hU0, '"video games are often seen as unhealthy. They can lead to a lot of bad habits that all culminate to not taking care of yourself. what are ways do you think people can practice healthy gaming?"')


## end meta insertion



if __name__ == '__main__':
    #df.precache_transitions()
    df.run(debugging=False)
