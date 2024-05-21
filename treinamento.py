import sys
sys.path.append("./gym-examples")
import gym_examples
import gymnasium as gym
import numpy as np
import random
from IPython.display import clear_output
import pickle

env = gym.make('gym_examples/JogoDaVelha-v0')
qTabela = {}
gamma = 0.6
alpha = 0.1
probabilidade = 0.1

for i in range(10000):
    recompensa = 0
    terminated = False
    estado, info = env.reset()
    estadoTupla = tuple(map(tuple, estado['preenchido']))
    if (not estadoTupla in qTabela.keys()):
        qTabela[estadoTupla] = np.zeros(shape=9)

    while not terminated:
        if (random.uniform(0, 1) > probabilidade):
            acao = np.argmax(qTabela[estadoTupla])
        else:
            acao = env.action_space.sample()

        qAntigo = qTabela[estadoTupla][acao]
        estado, recompensa, terminated, truncated, info = env.step(acao)
        proximoEstadoTupla = tuple(map(tuple, estado['preenchido']))
        if (not proximoEstadoTupla in qTabela.keys()):
            qTabela[proximoEstadoTupla] = np.zeros(shape=9)

        qProximo = np.max(qTabela[proximoEstadoTupla])
        qNovo = (1 - alpha) * qAntigo + alpha * (recompensa + gamma * qProximo)
        qTabela[estadoTupla][acao] = qNovo
        estadoTupla = proximoEstadoTupla
    
    if i % 100 == 0:
        clear_output(wait=True)
        print("Episódio: ", i)
    
with open("qValores.pkl", "wb") as arquivo:
    pickle.dump(qTabela, arquivo)

for i in range(10):
    terminated = False
    recompensa = 0
    penalidade = 0

    estado, info = env.reset()
    estadoTupla = tuple(map(tuple, estado['preenchido']))
    print(estadoTupla)

    while not terminated:
        acao = np.argmax(qTabela[estadoTupla])
        estado, recompensa, terminated, truncated, info = env.step(acao)
        estadoTupla = tuple(map(tuple, estado['preenchido']))
        print(estadoTupla)
        
        if (recompensa == -20):
            penalidade += 1
    
    print(penalidade)




    
    
