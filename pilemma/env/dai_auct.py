import gym
from gym import error, spaces, utils
from gym.utils import seeding

# amount of ink (eth collat) that cannot be won in flipper auction
LIQUID_FEE=0.13

#annual interest (or disinitegration) of ink
STABILITY_FEE=0.06
YTH=24*365.25
YTms=24*365.25*60*60*1000

class Urn():
    def __init__(self):
        self.sf=STABILITY_FEE
        self.liquidate=False
        self.art=0
        self.time=0
        self.ink=0
        self.closed=False

    def mint(self,amount,collateral,dt):
        self.art=amount
        self.ink=collateral
        self.time=dt
        self.liq_ratio=1.5


    def bite(self,conv):
        if  1.*conv*self.ink/self.art<self.liq_ratio:
            self.liquidate=True
            return self.liquidate
    def close(self, dai_debt, current_t):
        if dai_debt>=self.art:
            self.closed=True
            return (1-(current_t-self.time)*self.sf/YTH)*self.ink
        else:
            pass

    def dent(current_t):
        # eventually Number of bids based on random possion distribution 
        
        # let's imagine initially best case
        # best case is you get your ink with no competition
        #hence you lose interest and liquidationfee
        haul=(1-(current_t-self.time)*self.sf/YTH)*self.ink
        self.closed=True
        return haul 


        
