from gym.envs.registration import register

register(
    id='pilemma-v0',
    entry_point='pilemma.envs:DaiAuct',
)
register(
    id='pilemma_stoch_v0',
    entry_point='pilemma.envs:DaiAuctStoch',
)
