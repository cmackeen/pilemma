import gym
from gym import error, spaces, utils
from gym.utils import seeding
from marketh import *

# amount of ink (eth collat) that cannot be won in flipper auction
LIQUID_FEE=0.13

#annual interest (or disinitegration) of ink
STABILITY_FEE=0.06
YTH=24*365.25

class Urn():
    def __init__(self,dai_amount,collateral,num):
        self.art=amount
        self.crit_ratio=1.5
        self.ink=collateral
        self.id=num
        self.sf=STABILITY_FEE
        self.liquidate=False
        self.closed=False
    def bite(self,t):
        if  1.*marketh.conv(t,collat)/amount<1.5:
            self.liquidate=True
    def dent():
        # eventually Number of bids based on random possion distribution 
        
        # let's imagine initially best case
        # best case is you get your ink with no competition
        #hence you lose interest and liquidationfee
        haul=(1-t*sf/YTH)*self.ink
        self.closed=True
        return haul 


        
