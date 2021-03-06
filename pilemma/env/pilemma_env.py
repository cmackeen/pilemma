
import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import pandas as pd 

import gym
from gym import error, spaces, utils
from gym.utils import seeding
from pilemma.env.dai_auct import Urn
import glob
import os
import random

init_dai=1000
init_eth=0
ACTION_SKIP = 0
ACTION_MINT = 1
ACTION_CLOSE = 2
ACTION_BUY=3
ACTION_SELL=4
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

    def current_time(self):
        return self.df.ix[self.index, 'Deltat']

class DaiLemmaEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, datadir='./pilemma/data'):
        self.bound = 100000
        self.num = 0.10
        self.eth = init_eth
        self.dai = init_dai
        self.rowpick = 0
        self.meta_counter =0
        self.equity = 0
        self.states = []
        self.urns = 0
        self.state = None

        for path in glob.glob(datadir + '/ETHUSDT_long_simpdt.csv'):
            if not os.path.isfile(path):
                continue

            self.states.append(path)

        self.observation_space = spaces.Box(low=0, high=self.bound, shape=(6,))
        self.action_space = spaces.Discrete(5)
        self.episode_total_reward=0
        self.counter=0

        if len(self.states) == 0:
            raise NameError('Invalid empty directory {}'.format(dirname))

    def step(self, action):
        assert self.action_space.contains(action)

        prev_portfolio= 1.01*self.dai + 0.99*self.eth * self.state.current_price()
        price = self.state.current_price()
        fee = np.random.normal(4,.8)*(1./price)*0.50
        cost = price * self.num
        cdp = Urn()
        if action == ACTION_SELL:
            if self.eth >= (self.num+fee):
                self.eth-=(self.num+0*fee)
                self.dai+=price*self.num
            else:
                self.eth-=fee
        if action == ACTION_BUY:
            if self.dai >= price*self.num:
                self.eth+=(self.num-0*fee)
                self.dai-=price*self.num
            else:
                self.eth-=fee
		

        if action == ACTION_MINT:
            self.eth-=self.num+fee
            if self.urns == 0 and self.eth>self.num+fee:
                self.eth-=self.num+fee
                cdp.mint(1.52*self.num*price,self.num,self.state.current_time())
                self.dai += cdp.art
                self.urns = 1
            else:
                self.eth -= fee
        if action == ACTION_CLOSE:
            if self.urns == 1:
                self.dai-=cdp.art
                haul=(np.random.normal(.5,.1))*cdp.close(cdp.art,self.state.current_time())
                self.eth+=haul-fee
                self.urns=0
            else:
                self.eth -= fee

        state, done = self.state.next()

        new_price = price
        if not done:
            new_price = self.state.current_price()

        portfolio= 1.01*self.dai + 0.99*self.eth * self.state.current_price()
        reward = portfolio - prev_portfolio

        return state, reward, done, {}

    def reset(self):
        if self.meta_counter%1000==0:
            self.rowpick=np.random.choice(range(1,nr))
            print(self.meta_counter)
            print("new time series")

        self.state = SystemState(random.choice(self.states),skiprows=self.rowpick)

        self.eth = init_eth
        self.dai = init_dai
        self.equity = 0
        self.urns = 0
        self.counter = 0
        self.meta_counter += 1
        state, done = self.state.next()
        return state

    def render(self, mode='human', close=False):
        pass
