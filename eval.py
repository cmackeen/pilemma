import gym
import time
from stable_baselines import PPO2
from stable_baselines.common.evaluation import evaluate_policy
import numpy as np
import pilemma

# Create environment
env = gym.make('pilemma-v0')
env = gym.wrappers.Monitor(env, './tmp/eval', force=True)

data_out=[]
def evaluate(model, num_steps=1000):
  """
  Evaluate a RL agent
  :param model: (BaseRLModel object) the RL Agent
  :param num_steps: (int) number of timesteps to evaluate it
  :return: (float) Mean reward for the last 100 episodes
  """
  episode_rewards = [0.0]
  obs = env.reset()
  for i in range(num_steps):
      # _states are only useful when using LSTM policies
      action, _states = model.predict(obs)

      obs, reward, done, info = env.step(action)
      # Stats
      episode_rewards[-1] += reward
      data_out.append(obs)
      if done:
          obs = env.reset()
          episode_rewards.append(0.0)
  # Compute mean reward for the last 100 episodes
  mean_100ep_reward = round(np.mean(episode_rewards[-100:]), 1)
  print("Mean reward:", mean_100ep_reward, "Num episodes:", len(episode_rewards))
  
  return mean_100ep_reward,data_out



# anstantiate the agent
model = PPO2('MlpPolicy', env)
model.load_parameters(load_path_or_dict="tmp/17_Apr_best_model.pkl")

eval_model = evaluate(model, num_steps=1000)
mean_reward = eval_model[0]
system_acts=eval_model[1]
