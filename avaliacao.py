import pickle
import sys
sys.path.append("./gym-examples")
import gym_examples
import gymnasium as gym
import numpy as np
from time import sleep

env = gym.make("gym_examples/JogoDaVelha-v0", render_mode="human")

with open("qValores.pkl", "rb") as arquivo:
    qTabela = pickle.load(arquivo)

for _ in range(2):
    terminated = False
    penalidade = 0
    estado, info = env.reset()
    sleep(1)
    estadoTupla = tuple(map(tuple, estado["preenchido"]))

    while not terminated:
        acao = np.argmax(qTabela[estadoTupla])
        estado, recompensa, terminated, truncated, info = env.step(acao)
        sleep(1)
        estadoTupla = tuple(map(tuple, estado["preenchido"]))
        if recompensa < -10:
            penalidade += 1
    
    print(penalidade)

