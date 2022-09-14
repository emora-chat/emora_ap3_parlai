
from emora_stdm.state_transition_dialogue_manager.chat_flow import DialogueFlow
import emora_stdm.state_transition_dialogue_manager.natex_common as natexes
from _globals import ACTDIR
import os

df = DialogueFlow('ask_about_day', kb=ACTDIR.replace('__***__','general_activity.json'))

ask_recap_nlg = '[!{' \
                '"So, What did you do today?",' \
                '"So, What was something fun that you did today?"' \
                '"So, What did you get up to today?"' \
                '}]' \
                '#SET($activityv=True)'
decline_share = "{" \
                "[not, {talk, talking, discuss, discussing, share, sharing, tell, say}]," \
                "[none,your,business]," \
                "[!{[!that,is],thats},private]" \
                "}"
relax_plans_nlu = '[#NOT(not),{relax,chill,fun,enjoy,[#LEM(take),break]}]'
dont_know = '[{' \
            'dont know,do not know,unsure,[not,{sure,certain}],hard to say,no idea,uncertain,[!no {opinion,opinions,idea,ideas,thought,thoughts,knowledge}],' \
            '[{dont,do not}, have, {opinion,opinions,idea,ideas,thought,thoughts,knowledge}],' \
            '[!{cant,cannot,dont} {think,remember,recall}]' \
            '}]'
no_plans_nlu = '{' + dont_know + ',[{nothing,none,have not decided,havent decided, up in the air, undecided, not much,[not,anything]}]}'


# ADD SYSTEM ANSWERING SAME QUESTION TOO
ask_about_day = {
    'state': 'ask_about_day',
    'error': 'ask_about_day',
    ask_recap_nlg:
    {
        'state': 'learn_about_day',
        'score': 2,
        'error': {
            '"Okay, I see. Thanks for sharing that with me. "': {
                'score': 2.0,
                'state': 'transition_out'
            }
        },

        decline_share:{
            'score':3.0,
            '"Okay, it seems like you don\'t want to share that with me. That\'s alright, I hope we can find something '
            'interesting that you do want to talk about, instead. "': 'transition_out'
        },

        '[#NOT(not),$chore=#ONT(chore)]': {
            '"Oh, you did some chores? '
            'Now that we have all of this time on our hands, '
            'I can imagine it would be nice to tidy up!"': 'transition_from_chore'
        },

        '[#NOT(not),{#EXP(travel),#LEM(do)},$errand_dest=#ONT(errand)]': {
            'score': 2.0,
            '[!"You know, it may not be the most exciting thing, but '
            'I bet you are glad to be done with that errand for now."]':
            {
                'error': {
                    '"Well, okay. I just know that a lot of people are usually happy to be done with errands. '
                    'Anyways, "': 'transition_out'
                },
                "{%s,[!{[!i,am],im},#NOT(not)],[im,#NOT(not),#EXP(happy)]}"%natexes.agree: {
                    '"Great! Well, hopefully we can find something interesting to talk about to '
                    'spice up your day, something more exciting than errands. "': 'transition_out'
                },

                "{"
                "[i,#NOT(not),#EXP(like),{it,that,#LEM(chore),#ONT(errand)}],"
                "[{it,its,that,#LEM(chore),#ONT(errand),they},#NOT(not),{#EXP(fun),#EXP(break)}]"
                "}": {
                    '[!"You enjoy doing errands? I was not really expecting that! '
                    'Let\'s try to continue your pleasant day. "]': 'transition_out'
                },

                "{%s,[!{[!i,am],im},not],[im,not,#EXP(happy)]}"%natexes.disagree: {
                    '"I think I heard you say you are not glad to be done with your errands? Well, I am glad '
                    'they seem to bring you some sort of joy. "': 'transition_out'
                },

                "{"
                "[i,not,#EXP(like),{it,that,chore,#ONT(errand)}],"
                "[{it,its,that,#LEM(chore),#ONT(errand),they},not,{#EXP(fun),#EXP(break)}],"
                "[{#EXP(annoy),#EXP(hate)}]"
                "}": {
                    '[!"Yeah, errands can be a bit annoying, but you have to do them at some point, unfortunately. '
                    'Let\'s talk about something a bit more exciting, I am sure this is not a very interesting '
                    'topic for you! "]': 'transition_out'
                }
            }
        },

        '[#NOT(not),$homework=#EXP(homework)]': {
            'score': 3.0,
            '[!"That is a pretty good use of your time, keep up the good work! I know it might be kind of hard to stay motivated due to the current situation. Are you taking a break now?"]':
            {
                "{%s,[!{[!i,am],im},#NOT(not)]}"%natexes.agree:{
                    '"Awesome! I am glad you have decided to include me in your break. "': 'transition_from_homework'
                },
                "{%s,[!{[!i,am],im},not]}"%natexes.disagree:{
                    '"You aren\'t really taking a break, but you are talking to me right now? '
                    'Well, I am glad to be talking to you. "': 'transition_from_homework'
                },
                "{[should,still,#LEM(do,work)],"
                "[{shouldnt,should not},#LEM(stop,end,finish)]}":{
                    '"You feel like you still should be working on it? Sometimes, you will work even better after taking '
                    'a small break, but yeah, make sure you don\'t neglect your work, for sure. "': 'transition_from_homework'
                },
                "[{[!{sort,kind},of],maybe,a little,i guess}]":{
                    '"Even a small break can be helpful to refresh you. "': 'transition_from_homework'
                },
                'error': {
                    '"Regardless, I am glad you have decided to talk with me. It keeps my days interesting, and I hope '
                    'it brings something new and fun to your day too! "': 'transition_from_homework'
                }
            }

            # '#GATE(schoolv:None) #SET($schoolv=True) #IF($life_in=True) [!"Oh, cool. I\'m actually a student too. '
            # 'Personally, I think school is pretty frustrating, but I do love learning new things. '
            # 'Do you like school?"]': {
            #     'state': "school_new:ask_like_school",
            #     'score': 2.0
            # }
        },

        '[#NOT(not),#LEM(complete,finish),$homework=#EXP(homework)]': {
            '"It sounds like you finished some work. You should be proud! It feels good to be done, doesn\'t it?"':{
                'error': {
                    '"I see. It does seem like a lot of people are so relieved when they are done with some work. "': 'transition_from_finish_homework'
                },
                "{%s,[!{[!i,am],im},#NOT(not)],[im,#NOT(not),#EXP(happy)]}"%natexes.agree: {
                    '"I knew it! Well, hopefully we can find something interesting to talk about to '
                    'spice up your day, other than your homework. "': 'transition_from_finish_homework'
                },

                "{"
                "[i,#NOT(not),#EXP(like),{it,that,#EXP(homework)}],"
                "[{it,its,that,they,#EXP(homework)},#NOT(not),{#EXP(fun),#EXP(break)}]"
                "}": {
                    '"You enjoy doing some schoolwork? Yeah, I guess depending on the topic, it could be cool!"': 'transition_from_homework_topic'
                },

                "{%s,[!{[!i,am],im},not],[im,not,#EXP(happy)]}"%natexes.disagree: {
                    '"I think I heard you say you are not glad to be done with your work? Either you enjoy it or '
                    'you still have more to do. Regardless, I am happy to be talking to you now. So, "': 'transition_out'
                },

                "{"
                "[i,not,#EXP(like),{it,that,#EXP(homework)}],"
                "[{it,its,that,they,#EXP(homework)},not,{#EXP(fun),#EXP(break)}],"
                "[#EXP(annoy)]"
                "}": {
                    '"Yeah, I think most people find schoolwork to be annoying, but you have to do them at some point, unfortunately. "': 'transition_from_finish_homework'
                },

                "[{[!{sort,kind},of],maybe,a little,i guess}]": {
                    '"Even if it was just something small that you finished, you should feel proud of yourself! "': 'transition_from_finish_homework'
                }
            }

            # '#GATE(schoolv:None) #SET($schoolv=True) #IF($life_in=True) "It sounds like you finished some work. You should be proud! I\'m actually a student too. '
            # 'Personally, I think school is pretty frustrating, but I do love learning new things. '
            # 'Do you like school?"': {
            #     'state': "school_new:ask_like_school",
            #     'score': 2.0
            # }
        },

        '[#NOT(not),{#EXP(travel),#LEM(attend,do,have)},{school,#EXP(class)}]': {
            'score': 2.0,
            '"Attending class is pretty different at the moment, but I am glad to hear that they are at least '
            'still working for you. "': 'transition_from_class'

            # '#GATE(schoolv:None) #SET($schoolv=True) #IF($life_in=True) "I\'m glad to hear you can still attend class in some form. I\'m actually a student too. '
            # 'Personally, I think school is pretty frustrating, but I do love learning new things. '
            # 'Do you like school?"': {
            #     'state': "school_new:ask_like_school",
            #     'score': 2.0
            # }
        },

        '[#NOT(not),{[{#EXP(travel),#LEM(do,have)},#LEM(work,job)],#LEM(work)}]': {
            'score': 2.0,
            '"I am glad you are able to keep working in spite of everything that is going on. "'
            '#SET($is_employed=True)':
                'transition_from_work'

            # '#GATE(worklifev:None) #SET($worklifev=True) #IF($life_in=True) "I\'m glad you are able to keep working in spite of everything that is going on. "'
            # '#SET($is_employed=True)': {
            #     'state': "worklife:entry_to_happy_work",
            #     'score': 2.0
            # }
        },

        '[#NOT(not),#EXP(travel),$dest=#ONT(indoor_destination)]': {
            'score': 4.0,
            '[!"People haven\'t really been going to the "$dest" recently. It probably '
            'felt good to get out of the house, even for a little bit, but I hope you are staying safe. "]': 'transition_from_indoor_dest'
        },

        '[#NOT(not),{#EXP(travel),#LEM(play)},$dest=#ONT(outdoor_destination)]': {
            'score': 4.0,
            '[!"It is nice to get out of the house and spend some time outdoors in the "$dest", with everything '
            'that is going on. I hope you enjoyed yourself and are staying safe. "]'
            '#SET($likes_outdoors=True)': 'transition_from_outdoor_dest'
        },

        '[#NOT(not),{#EXP(travel),#LEM(play)},{outdoors,outdoor,outside}]': {
            'score': 4.0,
            '[!"It is nice to get out of the house and spend some time outdoors, with everything '
            'that is going on. I hope you enjoyed yourself and are staying safe. "]'
            '#SET($likes_outdoors=True)': 'transition_from_outdoor_dest'
        },

        '[#NOT(not),{#EXP(travel),#LEM(play)},{indoor,indoors,inside}]': {
            'score': 4.0,
            '[!"I hope you enjoyed your indoor activities, it is good to keep yourself entertained! "]': 'give_fun_activity'
        },

        '[#NOT(not),#LEM(play),{game,games,house,home,dolls,doll,barbie,barbies,toy,toys}]': {
            '[!"I hope you enjoyed playing with your toys, it is good to keep yourself entertained! "]': 'give_fun_activity'
        },

        '[#NOT(not),#LEM(play),$console=#ONT(game_console)]': {
            '[!"Oh, cool! You have a "$console"? I bet you are having a lot of fun playing video games to pass '
            'the time. Are you playing them more than usual nowadays?"]': {
                'error': {
                    '"I see. Video games do seem to be one popular activity to relax and have fun for a lot '
                    'of people. "': 'transition_to_vr'
                },
                "{%s,[!{[!i,am],im},#NOT(not)],[#NOT(not),{more,a lot,#EXP(frequently)}]}"%natexes.agree: {
                    '"That makes sense. They are one easy way to keep yourself busy at home. "': 'transition_to_vr'
                },

                "{%s,[!{[!i,am],im},not],[not,{more,a lot,#EXP(frequently)}]}"%natexes.disagree: {
                    '"Well, I am glad you are able to enjoy playing them at least some of the time. "': 'transition_to_vr'
                }
            },

            '#IF($vgame_in=True)': {
                'state': 'videogames:yes_vgames',
                'score': 2.0
            }
        },

        '[#NOT(not),#LEM(play),{#ONT(vgames),[!video, #LEM(game)]}]': {
            'score': 1.1,

            '[!"Oh, cool! I bet you are having a lot of fun playing video games to pass '
            'the time. Are you playing them more than usual nowadays?"]': {
                'error': {
                    '"I see. Video games do seem to be one popular activity to relax and have fun for a lot '
                    'of people. "': 'transition_to_vr'
                },
                "{%s,[!{[!i,am],im},#NOT(not)],[#NOT(not),{more,a lot,#EXP(frequently)}]}" % natexes.agree: {
                    '"That makes sense. They are one easy way to keep yourself busy at home. "': 'transition_to_vr'
                },

                "{%s,[!{[!i,am],im},not],[not,{more,a lot,#EXP(frequently)}]}" % natexes.disagree: {
                    '"Well, I am glad you are able to enjoy playing them at least some of the time. "': 'transition_to_vr'
                }
            },

            '#IF($vgame_in=True)': {
                'state': 'videogames:yes_vgames',
                'score': 2.0
            }
        },

        '[#NOT(not),{$exercise={#EXP(exercise),[!#LEM(work),out],#ONT(outdoor_exercise,indoor_exercise)},[#LEM(play),$exercise=#ONT(sports)]}]':{
            'score':3.0,
            '[!"Oh, "$exercise"? It seems like a lot of people are spending this extra time at home getting into a '
            'good exercise routine. Is that something you are trying to do too?"]':{
                'error': {
                    '"Ok, sure. Any exercise is better than none!"': 'transition_from_exercise'
                },
                "{"
                "%s,[!{[!i,am],im},#NOT(not)],"
                "[#NOT(not),{it,that,some,{#EXP(exercise),[!#LEM(work),out],#ONT(outdoor_exercise,indoor_exercise,sports)}},{more,a lot,#EXP(frequently)}]"
                "}" % natexes.agree: {
                    '"Wow, I admire you for doing that. It is important to stay healthy in times like this, for sure. "': 'transition_from_exercise'
                },

                "{"
                "%s,[!{[!i,am],im},not],"
                "[not,{it,that,some,{#EXP(exercise),[!#LEM(work),out],#ONT(outdoor_exercise,indoor_exercise,sports)}},{more,a lot,#EXP(frequently)}]"
                "}" % natexes.disagree: {
                    '"Well, you never know. You just might get into a really good routine anyways, without even trying. "': 'transition_from_exercise'
                },

                "[{[!{sort,kind},of],maybe,a little,i guess}]":{
                    '"Even doing just a little bit of exercise on a regular basis can help. "': 'transition_from_exercise'
                },
            }
        },

        '[#NOT(not),$watching={#EXP(television),#EXP(hbo),#LEM(movie,channel,show,cartoon),youtube,netflix,hulu}]': {
            '[!"Oh, "$watching"? That seems to be a good one. Watching movies and shows is always so fun, and '
            'an easy way to relax. "]': 'transition_to_movies'
        },

        '[#NOT(not),#LEM(see,talk,chat,call),$contact=#ONT(related_person)]': {
            '[!"It is good to hear that you are keeping in touch with the people in your life. '
            'Are you close to your"$contact"?"]':{
                'error': {
                    '"Okay. Well, I hope you are able to stay connected with everyone you want to, even in these weird times. "': 'transition_out'
                },
                "{%s,[!{[!i,am],im},#NOT(not)],[#NOT(not),{#LEM(close),intimate,inseparable,best}]}"% natexes.agree: {
                    '"Wow, you sound like you are really close to them. I am glad to hear that. "': 'transition_out'
                },

                "{%s,[!{[!i,am],im},not],[not,{#LEM(close),intimate,inseparable,best}]}"%natexes.disagree: {
                    '"You aren\'t that close to them? Well, I hope you are able to stay connected with the other people '
                    'who are important in your life. "': 'transition_out'
                }
            }
        },

        '[#NOT(not),#LEM(play),with,$contact=#ONT(related_person)]': {
            '[!"It is good to hear that you are spending time with the people in your life. '
            'Are you close to your"$contact"?"]': {
                'error': {
                    '[!"Okay. Well, playing with your" $contact "is a good way to pass the time and have some fun, I think."]': 'transition_out'
                },
                "{%s,[!{[!i,am],im},#NOT(not)],[#NOT(not),{#LEM(close),intimate,inseparable,best}]}" % natexes.agree: {
                    '"Wow, you sound like you are really close to them. I am glad to hear that. "': 'transition_out'
                },

                "{%s,[!{[!i,am],im},not],[not,{#LEM(close),intimate,inseparable,best}]}" % natexes.disagree: {
                    '"You aren\'t that close to them? Well, I hope you are able to spend time with the other people '
                    'who are important in your life, too. "': 'transition_out'
                }
            }
        },

        '[#NOT(not),#LEM(play),with,$animal=#ONT(animal)]': {
            '[!"It is good to hear that you are spending time with your animals. '
            'Do you play a lot with your "$animal"?"]': {
                'error': {
                    '[!"Okay. Well, playing with your" $animal "is a good way to pass the time and have some fun, I think."]': 'transition_out'
                },
                "{%s,[!{[!i,am],im},#NOT(not)],[#NOT(not),{#LEM(close),intimate,inseparable,best}]}" % natexes.agree: {
                    '"Wow, you sound like you really care for them. I am glad to hear that. "': 'transition_out'
                },

                "{%s,[!{[!i,am],im},not],[not,{#LEM(close),intimate,inseparable,best}]}" % natexes.disagree: {
                    '"You don\'t spend that much time playing with your " $animal "? Well, it is always good to give '
                    'them some attention when you can."': 'transition_out'
                }
            }
        },

        "[$hobby=#ONT(hobby)]": {
            '[!"Oh, okay. I heard you say"$hobby". That is a great thing to do to keep yourself busy, especially in these times! "]': 'transition_from_hobby'
        },

        no_plans_nlu:{
            '{"Yeah, sometimes it is hard to decide what to do.",'
            '"Sure, I know the feeling of not really doing too much."}': {
                'score': 2.0,
                'state': 'give_fun_activity'
            }
        },

        relax_plans_nlu:{
            '{"Its always good to take some time to relax.",'
            '"You can never underappreciate the value of taking some time for yourself."}':  {
                'score': 2.0,
                'state': 'give_fun_activity'
            }
        },

        "[{"
        "quarantine,quarantined,#LEM(isolate),"
        "shelter in place,"
        "[#LEM(stuck,stay,trap,confine) #LEM(home,inside,indoor,indoors,house,apartment,home)],"
        "#LEM(survive)"
        "}]":{
            'score':3.0,
            '"That sounds tough. "': 'SYSTEM:coronavirus_op_intro'
        },

        "[#LEM(stock,find,get,buy,purchase),#LEM(food,grocery,cleaning,supply,item,resource,necessity,essential)]":{
            'score':3.0,
            '[!#SET($shopping_challenge=True) "Oh, shopping is definitely not the same anymore."]': 'SYSTEM:coronavirus_op_intro'
        },

        "[#EXP(coronavirus)]":{
            'score':3.0,
            '"Oh, yes. I keep hearing about the coronavirus outbreak. "': 'SYSTEM:coronavirus_op_intro'
        },

        "[{#LEM(fart,poop,shit,crap,piss,pee,urinate,tinkle),pooped,[#LEM(take),dump]}]":{
            '"Okay, that is kind of gross for you to share with me, but good for you, I guess? '
            'I really would rather talk about something else, so we are moving on now. "': 'transition_out'
        },

        "{"
        "[#LEM(fuck)],"
        "[#LEM(jerk,suck,masturbate,eat),{#EXP(genitalia),off,me,myself,#ONT(related_person)}],"
        "[#LEM(have,do),#EXP(sex)],"
        "[{porn,xrated,x rated}],"
        "[#LEM(make),{love,sex}]"
        "}":{
            '"You seem to be sharing some pretty personal details of your life. I am not sure this is the best time or '
            'place for that, and I do not know anything about those activities. So, we should move on to a '
            'more appropriate topic. "': 'transition_out'
        }

    }
}


df.load_transitions(ask_about_day, DialogueFlow.Speaker.SYSTEM)

# df.update_state_settings("school_new:ask_like_school", system_multi_hop=True)
# df.update_state_settings("worklife:entry_to_happy_work", system_multi_hop=True)


# df.add_system_transition('transition_out','ask_about_day','" -- "')
# df.add_system_transition('transition_to_vr','ask_about_day','" -- "')
# df.add_system_transition('transition_to_movies','ask_about_day','" -- "')

if __name__ == '__main__':
    df.precache_transitions()
    df.run(debugging=True)