
from parlai.core.agents import Agent, create_agent_from_model_file, create_agent
from parlai.core.opt import Opt
from parlai.core.params import ParlaiParser

from emora import dialogue_manager
from emora_stdm import DialogueFlow
untextify_input = dialogue_manager.untextify_input
build_dialogue_manager = dialogue_manager.build_dialogue_manager


class EmoraAgentAgent(Agent):

    def __init__(self, opt, shared=None, precache=True):
        super().__init__(opt, shared)
        self.serialized_state = None
        if shared is None:
            self.emora = build_dialogue_manager(precache)
        else:
            self.emora = shared['emora']

    def share(self):
        shared = super().share()
        shared['emora'] = self.emora
        return shared

    def observe(self, obs):
        obs = super().observe(obs)
        user_utterance = obs['text']
        if self.serialized_state is None: # reset emora
            self.emora.new_turn()
        else:
            self.emora.deserialize(self.serialized_state)
        self.emora.controller().set_speaker(DialogueFlow.Speaker.USER)
        self.emora.user_turn(untextify_input(user_utterance))
        self.serialized_state = self.emora.serialize()
        return obs

    def act(self):
        if self.serialized_state is None: # reset emora
            self.emora.new_turn()
        else:
            self.emora.deserialize(self.serialized_state)
        self.emora.controller().set_speaker(DialogueFlow.Speaker.SYSTEM)
        response = self.emora.system_turn()
        self.serialized_state = self.emora.serialize()
        return {'text': response}


if __name__ == '__main__':
    opt = ParlaiParser().parse_args()
    agent = EmoraAgentAgent(opt, precache=False)
    inp = 'How many siblings do you have?'
    while not 'quit'.startswith(inp.strip().lower()):
        agent.observe({'text': inp, 'episode_done': False})
        response = agent.act()['text']
        print('System:', response)
        inp = input('User:  ')
