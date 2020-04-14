import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
from dai_auct import Urn

class DaiLemma(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.ethprice=111
    def _seed():
        self.random_seed=np.random
    def step(self, action):

        #
    def reset(self):
        #
    def render(self, mode='human'):

    def close(self):
