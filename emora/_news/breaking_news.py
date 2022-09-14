from emora_stdm import DialogueFlow
from emora._news.news_macro import *
from enum import Enum

# states are typically represented as an enum
class State(Enum):
    START = 0
    ERROR = 1
    END = 2
    NEWS_AND_FOLLOWUP_QUESTION = 3  # this is like the start state

    USER_SAID_YES = 4
    USER_SAID_NO = 5
    USER_GAVE_UNEXPECTED_ANSWER = 6


# initialize objects
news_briefing = NewsBriefing()
custom_macros = {'GetNews': GetNews(news=news_briefing.news),
                 'AcknowledgeUsersNo': AcknowledgeUsersNo(news=news_briefing.news),
                 'AcknowledgeUsersYes': AcknowledgeUsersYes(news=news_briefing.news),
                 'GetGenericAcknowledgement': GetGenericAcknowledgement()
                 }
df = DialogueFlow(State.START, macros=custom_macros)

no_words = ['no', 'nope', 'nah', 'sorry', 'stop', 'exit', 'shut up', 'cancel']
yes_words = ['sure', 'yes', 'yea', 'yup', 'yep', 'i do', 'yeah', 'okay', 'of course', 'please']

# add transitions to create an arbitrary graph for the state machine
df.add_system_transition(State.START, State.NEWS_AND_FOLLOWUP_QUESTION, f"$news=#GetNews()")
df.add_user_transition(State.NEWS_AND_FOLLOWUP_QUESTION, State.USER_SAID_YES, f"[{{{', '.join(yes_words)}}}]")
df.add_user_transition(State.NEWS_AND_FOLLOWUP_QUESTION, State.USER_SAID_NO, f"[{{{', '.join(no_words)}}}]")
df.add_user_transition(State.NEWS_AND_FOLLOWUP_QUESTION, State.USER_GAVE_UNEXPECTED_ANSWER, f"#NOT([{', '.join(yes_words + no_words)}])")

df.add_user_transition(State.ERROR, State.USER_SAID_YES, f"[{{{', '.join(yes_words)}}}]")
df.add_user_transition(State.ERROR, State.USER_SAID_NO, f"[{{{', '.join(no_words)}}}]")
df.add_user_transition(State.ERROR, State.USER_GAVE_UNEXPECTED_ANSWER, f"#NOT([{', '.join(yes_words + no_words)}])")

df.add_system_transition(State.USER_SAID_YES, State.END, "#AcknowledgeUsersYes()")
df.add_system_transition(State.USER_SAID_NO, State.END, "#AcknowledgeUsersNo()")
df.add_system_transition(State.USER_GAVE_UNEXPECTED_ANSWER, State.END, f"#GetGenericAcknowledgement()")
# df.add_system_transition(State.USER_GAVE_UNEXPECTED_ANSWER, State.ERROR, f"#GetGenericAcknowledgement()")
df.add_system_transition(State.ERROR, State.ERROR, "Sorry I do not have any more news updates. What would you like to talk about next")

df.set_error_successor(State.NEWS_AND_FOLLOWUP_QUESTION, State.ERROR)
df.set_error_successor(State.USER_SAID_YES, State.ERROR)
df.set_error_successor(State.USER_SAID_NO, State.ERROR)
df.set_error_successor(State.USER_GAVE_UNEXPECTED_ANSWER, State.ERROR)
df.set_error_successor(State.ERROR, State.ERROR)


if __name__ == "__main__":
    df.check()
    df.run(debugging=False)

