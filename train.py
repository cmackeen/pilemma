import os
import time
import gym
import numpy as np
import matplotlib.pyplot as plt

from stable_baselines.bench import Monitor
from stable_baselines.results_plotter import load_results, ts2xy
from stable_baselines.ddpg import AdaptiveParamNoiseSpec
from stable_baselines import results_plotter
from stable_baselines import PPO2
import pilemma

best_mean_reward, n_steps = -np.inf, 0

def callback(_locals, _globals):
    """
    Callback called at each step (for DQN an others) or after n steps (see ACER or PPO2)
    :param _locals: (dict)
    :param _globals: (dict)
    """
    global n_steps, best_mean_reward
    # Print stats every 1000 calls
    if (n_steps + 1) % 1000 == 0:
        # Evaluate policy training performance
        x, y = ts2xy(load_results(log_dir), 'timesteps')
        if len(x) > 0:
            mean_reward = np.mean(y[-100:])
            std_reward = np.std(y[-100:])
            print(x[-1], 'timesteps')
            print("Best mean reward: {:.2f} - Last mean reward per episode: {:.2f}".format(best_mean_reward, mean_reward))

            # New best model, you could save the agent here
            if mean_reward+std_reward > best_mean_reward:
                best_mean_reward = mean_reward
                # Example for saving best model
                print("Saving new best model")
                _locals['self'].save(log_dir + str(time.strftime("%d_%b"))+'_best_model.pkl')
    n_steps += 1
    return True

# Create log dir
log_dir = "tmp/"
os.makedirs(log_dir, exist_ok=True)

# Create and wrap the environment
env = gym.make('pilemma-v0')
env = Monitor(env, log_dir, allow_early_resets=True)

# Because we use parameter noise, we should use a MlpPolicy with layer normalization
model=PPO2('MlpPolicy', env,verbose=0, n_cpu_tf_sess=18,tensorboard_log="./tmp/tboard/")
#model = DDPG('MlpPolicy', env, param_noise=param_noise, verbose=0, n_cpu_tf_sess=18, tensorboard_log="./tmp/ddpg_mlp_tboard/")
# Train the agent
time_steps = 1e5
model.learn(total_timesteps=int(time_steps), callback=callback)

results_plotter.plot_results([log_dir], time_steps, results_plotter.X_TIMESTEPS, "stock_ppo2")
plt.show()
