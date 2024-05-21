import sys
sys.path.append("./gym-examples")
import gym_examples
import gymnasium
from time import sleep

env = gymnasium.make('gym_examples/JogoDaVelha-v0', render_mode="human")

observation, info = env.reset()
sleep(1)

reward = -1
for i in range(50):
    action = env.action_space.sample()
    observation, reward, terminated, truncated, info = env.step(action)
    sleep(1)

    if terminated:
        observation, info = env.reset()
        sleep(2)

