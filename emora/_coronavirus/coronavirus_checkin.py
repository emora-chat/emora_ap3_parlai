
from emora_stdm import DialogueFlow
import os

coronavirus_checkin = DialogueFlow('_local_start')
coronavirus_checkin.add_system_transition('exit', 'SYSTEM:root', '')
coronavirus_checkin.knowledge_base().load_json_file(os.path.join('emora','coronavirus_checkin.json'))
coronavirus_checkin.add_system_transition('_local_start', 'start', '')

system = {
    'state': 'start',
    'enter': '#GATE #GOAL(coronavirus_checkin)',

    '`I\'ve been hearing a lot from people about how strange it is to live with the corona virus going on. '
    'Has your life changed a lot?` '
    '#GSRET(sympathy)': {

        '#UNX': 'sympathy',

        '#AGREE':{
            'score': 0.3,

            '`I figured it would have. Everyone seems to be affected, whether it is school or work or pretty much anything else. '
            'What would you say is the biggest way that it has impacted you? `'
            '#GSRET(sympathy)': {

                '#UNX': 'sympathy'
            }
        },

        '#DISAGREE':{
            'score': 0.3,

            '`Oh, that\'s good. So, `'
            '#GCOM':
                'activity:ask_about_day'
        },

        '#IDK':{
            'score': 0.2,

            '`You must be taking it pretty well then. '
            'I\'m not affected much myself, since almost everything I do is virtual, '
            'but my friends won\'t stop complaining about how stir crazy they are.`'
            '#GSRET(sympathy)': {

                '#UNX': {

                    '`So, `'
                    '#GCOM':
                        'activity:ask_about_day'
                }
            }
        },

        '[{has yours, your life {changed,different}, what about you}]':{
            'score': 1.1,

            '`Well lucky for me, everything I do is virtual already, so the virus doesn\'t really affect me, '
            'other than what I hear talking to other people.`': {

                '#UNX':{

                    '`Anyways, so, `'
                    '#GCOM':
                        'activity:ask_about_day'
                }
            }
        }
    }
}

sympathy = {
    'state': 'sympathy',

    '`It really is a crazy time. I cannot believe how many things have shut down around the world. How long do you '
    'think this shutdown will last?`'
    '#ALL($works_remote=None,$classes_remote=None,$school_closed=None,$aware_shutdown=None,$social_distancing=None,$worried_money=None)'
    '#SET($aware_shutdown=True) #GATE':{
        'score': 1.1,

        '[{what,[how {many,much}]}, {#LEM(shut,close,suspend), down, shutdown}]':{
            'score': 0.9,

            '`Lots of schools are being closed, including most universities. '
            'Lots of people are also being encouraged to work remotely, if it\'s possible. '
            'I mean, practically everything was shutting down, except for the essentials. `':{

                '#UNX': 'sympathy'
            }
        },

        '[#NOT(not), {long,weeks,summer,july,august}]':{

            '`We seem to be thinking the same thing. I have actually heard that a lot may be able to open in late summer, but we will '
            'have to wait and see.`': {

                '#UNX': 'sympathy'
            }
        },

        '{'
        '[!#NOT(not,dont,cant,cannot,shouldnt) <already,{#LEM(open),reopen,reopening,reopened}>],'
        '[!#NOT(not,dont,cant,cannot,shouldnt) <{#LEM(open),reopen,reopening,reopened},{soon,this,next}>],'
        '[{barbershop,barbershops,salon,salons,theatre,theatres,alley,alleys,surgery,surgeries,medical procedure,medical procedures}]'
        '[{georgia,alaska,oklahoma,south carolina}]'
        '}': {
            '`Oh, that\'s right. I have heard that some things are slowly reopening right now, too. We will have to see '
            'how it goes.`':{

                '#UNX': 'sympathy'
            }
        },

        '#IDK':{
            '`It is definitely hard to estimate what will happen. `': 'sympathy'
        },

        '#UNX': 'sympathy'
    },

    '`Actually, I have seen something pretty uplifting recently. Have you seen those videos where zoos are letting some of their animals, like penguins and otters, '
    'out of their cages to roam around?`'
    '#ALL($free_animals=None) #SET($free_animals=True)'
    '#GATE': {
        'state': 'animals_zoo',

        '#AGREE':{
            '`My favorite was to see the penguins at the Chicago zoo having the freedom to explore! What was yours?`':{

                '#UNX': 'sympathy',

                '[$saw_animal=#LEM(otter,armadillo,alligator,jellyfish,lizard,sea lion,puppy,whale,dog)]':{

                    '`Cool,` $saw_animal `? I wish I had seen that one too! `': 'sympathy'
                },

                '{#LEM(penguin),[{i,ive,me},too]}':{
                    '`You liked the penguins too? I think that is a pretty popular one, for sure. `':'sympathy'
                },

                '{#IDK, [#NEGATION,{one,favorite}]}':{
                    '`No big deal. It can be hard to choose a favorite in the first place. `': 'sympathy'
                }
            }
        },

        '#DISAGREE': {
            '`My favorite one was the penguins at the Chicago zoo, you should check it out! Anyway, `': 'sympathy'
        },

        '#UNX(Ok, I see. Anyways )': 'sympathy'
    },

    '`Well, the good news is that this virus won\'t last forever and people are taking steps in the right direction '
    'to lower its impact. I know things might seem really weird right now, but just do the best that you can and stay '
    'positive. `'
    '#ALL($free_animals=True) '
    '#ANY($works_remote=True,$classes_remote=True,$school_closed=True,$aware_shutdown=True,$social_distancing=True)'
    '#GATE #GSRET(end_corona)': {
        'state': 'stay_positive',

        '#UNX #GCOM(coronavirus_checkin)':{
            'state': 'end_corona',
            '`Anyways, so, `': 'activity:ask_about_day'
        }
    }
}

user = {
    'state': 'user',

    '[!-{wish} [{my, i, im} {work, job, working} {remote, remotely, virtual, online, [{from,at} {home,house,apartment}]}]]'
    '#SET($is_employed=True,$works_remote=True)': {

        '`Oh, do you like working remotely?`':{

            '#AGREE':{

                '`I am glad to hear it is going well for you! `#GRET': 'exit'
            },

            '#DISAGREE':{

                '`Hang in there. It can be challenging, that\'s for sure. `#GRET': 'exit'
            },

            '#IDK':{

                '`That\'s understandable, it is still relatively new. `#GRET': 'exit'
            },

            '#UNX':{ '#GRET': 'exit' }
        }
    },

    '[{i, im} {#NEGATION,off,on leave} #LEM(work,job)]': {

        '`I see. Is it a nice break for you to not be working, or do you miss it?`': {

            '{[#NOT(not,dont),{like,nice,good,fun,#LEM(relax,chill,enjoy)}],[dont,miss]}': {

                '`Good, you should enjoy your time off. `#GRET': 'exit'
            },

            '{'
            '[#NOT(not,dont),{miss,sad,upset,#LEM(frustrate),bored,boring}],'
            '[{not,dont},{like,nice,good,fun,#LEM(relax,chill,enjoy)}]'
            '}': {

                '`That makes sense. It can be weird to suddenly not have anything to do. `#GRET': 'exit'
            },

            '{'
            '[#NOT(not,dont), {#LEM(need,want,like,worry,concern,stress),have to,got to}, {#LEM(pay,finance,bill,expense),money,income}],'
            '[{i,im} {broke,out of money,[low,money]}]'
            '}'
            '#SET($worried_money=True)': {

                '`That sounds like a hard situation, but I think everything will work out for you. `'
                '#GRET(coronavirus_checkin,sympathy->animals_zoo)':
                    'exit',

                '`That sounds like a hard situation, but I think everything will work out for you. `'
                '#GRET(coronavirus_checkin,sympathy->stay_positive)':
                    'exit',

                '`That sounds like a hard situation, but I think everything will work out for you. Since you '
                'do have some more time on your hands, I\'m wondering `'
                '#GCOM(coronavirus_checkin)':
                    'activity:ask_about_day'
            },

            '#IDK': {

                '`I get that, this is a pretty confusing time. `#GRET': 'exit'
            },

            '#UNX': {'#GRET': 'exit'}
        }
    },

    '[!-{wish} [{my, i, im} {school, college, class, classes} {remote, remotely, virtual, online, [{from,at} {home,house,apartment}]}]]'
    '#SET($is_student=True,$classes_remote=True)': {

        '`Oh, are you liking your online classes?`': {

            '#AGREE':{

                '`Great, that is really good to hear! `#GRET': 'exit'
            },

            '#DISAGREE':{

                '`Oh yeah, it is hit and miss for a lot of people. Definitely just try to do the best you can. `#GRET': 'exit'
            },

            '#IDK':{

                '`I get that, it is still a relatively new adjustment. `#GRET': 'exit'
            },

            '#UNX':{ '#GRET': 'exit' }
        }
    },

    '[{things, everything, lots, stuff, much, many}'
    '{shutting, down, closing, suspending, closed, suspended}]'
    '#SET($aware_shutdown=True)':{
        'score': 0.4,

        '`What\'s closed that you miss the most?`':{

            '#UNX':{ '#GRET': 'exit' }
        }
    },

    '[{my, i, im} #LEM(school, class, college, university)'
    '{shutting, down, closing, suspending, closed, suspended}]'
    '#SET($is_student=True,$school_closed=True)': {

        '`Right. Is it kind of a nice break for you to not have to go in to school every day?`': {

            '#AGREE':{

                '`Yeah, it is almost like an early summer vacation. `#GRET': 'exit'
            },

            '#DISAGREE':{

                '`That makes sense. This definitely is not a situation anyone wanted to be in. `#GRET': 'exit'
            },

            '#IDK':{

                '`I get that, this is a pretty confusing time. `#GRET': 'exit'
            },

            '#UNX':{ '#GRET': 'exit' }
        }
    },

    '[!-#NEGATION [{people, everyone, everybody} {overreacting, too #ONT(negative_emotion)}]]':{

        '`I don\'t know. I think people are worried for a reason. There are a lot of things to consider, but '
        'I hope everything gets back to some kind of normal soon.`': {

            '#UNX #GCOM(coronavirus_checkin)':{

                '` Anyways, so, `': 'activity:ask_about_day'
            }
        }
    },

    '<{#NEGATION,hard,difficult} #LEM(go, find, buy, get) '
    '{store, grocery, groceries, food, shop, shopping, mall, market, paper}>'
    '#SET($shopping_challenge=True)':{

        '`Yeah, that\'s tough. I know that must be pretty stressful, '
        'so hopefully you are able to get what you need soon. `': {

            '#UNX': {'#GRET': 'exit'}
        },

        '`Yeah, that\'s tough. None of my friends can find necessities like toilet paper in stores anywhere. '
        'Honestly, who would\'ve ever imagined there would come a time when toilet paper was such a sought after item?` '
        '#GATE': {

            '#UNX': {'#GRET': 'exit'}
        },
    },

    '[{my} {sick, ill, infected, virus, hospital, fever}]'
    '#SET($knows_sick=True)':{

        '`Oh no, that\'s awful. I hope they recover soon.`': {

            '#UNX': {'#GRET': 'exit'}
        }
    },

    '{'
    '[!-#NEGATION [{i, im} {sick, ill, infected, virus, fever}]],'
    '[i {dont,[!{do,am} not]} {feel,feeling} {well,good,best,better}]'
    '}'
    '#SET($is_sick=True)':{

        '`I\'m so sorry you don\'t feel well. '
        'I hope you\'re taking care of yourself. '
        'Get plenty of rest and please get help if you need it, '
        'especially if you have a fever or trouble breathing.`': {

            '#UNX': {

                '`There probably was not a whole lot that you could do today, but `'
                '#GCOM(coronavirus_checkin)':
                    'activity:ask_about_day'
            }
        }
    },

    '{'
    'social distancing, social distance, '
    '[{i, im} {home, house, apartment, condo}],'
    '[{i, im} {cant,cannot,dont,do not,am not} {#LEM(see,visit,go)} my]'
    '}'
    '#SET($social_distancing=True)':{

        '`Yeah, it\'s definitely a tough situation to not be able to get together with people or go and do '
        'the things you used to. You should try to keep in touch with everyone close to you. My friends '
        'say doing video chats are really helpful.`': {

            '#UNX': {'#GRET': 'exit'}
        }
    },

    '[i {cant,cannot,not able to}]':{
        'score': 0.1,

        '`I\'m sorry you can\'t do everything you want to be able to do right now. Well, ` #GCOM(coronavirus_checkin)':
            'activity:ask_about_day'
    }

}

coronavirus_checkin.load_transitions(system)
coronavirus_checkin.load_transitions(sympathy)
coronavirus_checkin.load_global_nlu(user)


if __name__ == '__main__':
    #coronavirus_checkin.precache_transitions()
    coronavirus_checkin.run(debugging=False)