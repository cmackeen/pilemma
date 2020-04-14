from gym.envs.registration import register

register(
    id='pilemma-v0',
    entry_point='pilemma.envs:DaiLemma',
)
