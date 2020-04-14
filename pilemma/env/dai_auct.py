import gym
from gym import error, spaces, utils
from gym.utils import seeding
from marketh import *

LIQUID_FEE=0.13
STABILITY_FEE=0.06

class CDP():
    def __init__(self,amount,collateral,num):
        self.debt=amount
        self.crit_ratio=1.5
        self.collat=collateral
        self.id=num
        self.liquidate=False
    def bite(self,t):
        if  1.*marketh.conv(t,collat)/amount<1.5:
            self.liquidate=True
    def dent():
        # Number of bids based on random possion distribution 
        
