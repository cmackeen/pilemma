
import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import pandas as pd 
#from dai_auct import Urn

import gym
from gym import error, spaces, utils
from gym.utils import seeding

import glob
import os
import random

init_money=10000
ACTION_SKIP = 0
ACTION_BUY = 1
ACTION_SELL = 2
csv_file='./pilemma/data/ETHUSDT_long_simpdt.csv'
nr=sum(1 for line in open(csv_file))-101
window=1000
random_row = 0

class SystemState:
    def __init__(self, equity_path=csv_file, sep=',',skiprows=random_row):
        df = self.read_csv(equity_path, sep=sep, skiprows=random_row)

        df = df.fillna(method='ffill')
        df = df.fillna(method='bfill')

        self.df = df
        self.index = 0

        print("Imported tick data from {}".format(equity_path))

    def read_csv(self, path, sep, skiprows):
        dtypes = {'Date': str, 'Time': str}
        df = pd.read_csv(path, sep=sep, header=0, skiprows=random_row, nrows=window, names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume','Deltat'], dtype=dtypes)
        dtime = df.Date + ' ' + df.Time
        df.index = pd.to_datetime(dtime)
        df.drop(['Date', 'Time'], axis=1, inplace=True)
        return df

    def reset(self):
        self.index = 0

    def next(self):
        if self.index >= len(self.df) - 1:
            return None, True

        values = self.df.iloc[self.index].values

        self.index += 1

        return values, False

    def shape(self):
        return self.df.shape

    def current_price(self):
        return self.df.ix[self.index, 'Close']

class DaiLemmaEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, datadir='./pilemma/data'):
        self.bound = 100000

        self.comission = 0.1 / 100.
        self.num = 1

        self.money = 0
        self.rowpick = 0
        self.meta_counter =0
        self.equity = 0
        self.states = []
        self.state = None

        for path in glob.glob(datadir + '/ETHUSDT_long_simpdt.csv'):
            if not os.path.isfile(path):
                continue

            self.states.append(path)

        self.observation_space = spaces.Box(low=0, high=self.bound, shape=(6,))
        self.action_space = spaces.Discrete(3)
        self.episode_total_reward=0
        self.counter=0

        if len(self.states) == 0:
            raise NameError('Invalid empty directory {}'.format(dirname))

    def step(self, action):
        assert self.action_space.contains(action)

        portfolio = self.money + (1. - self.comission) * self.equity * self.state.current_price()
        price = self.state.current_price()
        cost = price * self.num
        comission_price = cost * (1. + self.comission)
        equity_price = price * self.equity
        prev_portfolio = self.money + equity_price

        if action == ACTION_BUY:
            if self.money >= comission_price:
                self.money -= comission_price
                self.equity += self.num
        if action == ACTION_SELL:
            if self.equity > 0:
                self.money += (1. - self.comission) * cost
                self.equity -= self.num
                self.counter += 1

        state, done = self.state.next()

        new_price = price
        if not done:
            new_price = self.state.current_price()

        new_equity_price = new_price * self.equity
        reward = (self.money + 0.4*new_equity_price) - prev_portfolio
        #reward = self.money - init_money
        self.episode_total_reward=reward
        info=self.counter

        return state, reward, done, {}

    def reset(self):
        if self.meta_counter%30==0:
            self.rowpick=np.random.choice(range(1,nr))
            print(self.meta_counter)

        self.state = SystemState(random.choice(self.states),skiprows=self.rowpick)

        self.money = init_money
        self.equity = 0
        self.counter = 0
        self.meta_counter += 1
        state, done = self.state.next()
        return state

    def render(self, mode='human', close=False):
        pass
