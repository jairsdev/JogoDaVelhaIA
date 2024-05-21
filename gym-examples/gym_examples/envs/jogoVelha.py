import gymnasium as gym
from gymnasium import spaces
import pygame
import numpy as np
from .verificacao import Verificacao

class JogoDaVelha(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, render_mode=None, size=3):
        self.size = size 
        self.window_size = 512
        
        self.observation_space = spaces.Dict(
            {
                "agent": spaces.Box(0, size - 1, shape=(2,), dtype=int),
                "target": spaces.Box(0, size - 1, shape=(2,), dtype=int),
                "preenchido": spaces.Box(0, 2, shape=(3,3), dtype=int)
            }
        )

        self.action_space = spaces.Discrete(9)

        self._action_to_direction = {
            0: np.array([0, 0]),
            1: np.array([0, 1]),
            2: np.array([0, 2]),
            3: np.array([1, 0]),
            4: np.array([1, 1]),
            5: np.array([1, 2]),
            6: np.array([2, 0]),
            7: np.array([2, 1]),
            8: np.array([2, 2])
        }

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        self.window = None
        self.clock = None

    def _get_obs(self):
        return {"agent": self._agent_location, "target": self._target_location, "preenchido": self.state["preenchido"]}

    def _get_info(self):
        return {
            "distance": np.linalg.norm(
                self._agent_location - self._target_location, ord=1
            )
        }

    def reset(self, seed=None, options=None):
    
        super().reset(seed=seed)

        self._agent_location = self.np_random.integers(0, self.size, size=2, dtype=int)

        self._target_location = self._agent_location
        while np.array_equal(self._target_location, self._agent_location):
            self._target_location = self.np_random.integers(
                0, self.size, size=2, dtype=int
            )
        
        self.state = {
            "preenchido": np.zeros((3,3), dtype=int)
        }
        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info

    def step(self, action):
        direction = self._action_to_direction[action]
        reward = 0
        terminated = False
        if self.state['preenchido'][direction[0]][direction[1]]:
            reward += -10
        else:
            self._agent_location = direction
            self.state['preenchido'][self._agent_location[0]][self._agent_location[1]] = 1
            jogo = Verificacao(self.state["preenchido"])
            terminated, reward = jogo.verificaoJogo(reward)
            if not terminated:
                while self.state['preenchido'][self._target_location[0]][self._target_location[1]]:
                    self._target_location = self.np_random.integers(
                        0, self.size, size=2, dtype=int
                    )
                self.state['preenchido'][self._target_location[0]][self._target_location[1]] = 2
                jogo = Verificacao(self.state["preenchido"])
                terminated, reward = jogo.verificaoJogo(reward)
        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, terminated, False, info

    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()

    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.window_size, self.window_size))
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        canvas = pygame.Surface((self.window_size, self.window_size))
        canvas.fill((255, 255, 255))
        pix_square_size = self.window_size // self.size 

        for row in range(self.size):
            for col in range(self.size):
                pygame.draw.rect(
                    canvas,
                    (0, 0, 0),
                    pygame.Rect(
                        col * pix_square_size,
                        row * pix_square_size,
                        pix_square_size,
                        pix_square_size,
                    ),
                    width=3,
                )

                if self.state["preenchido"][row][col] == 1:
            
                    pygame.draw.line(
                    canvas,
                    (0, 0, 0),
                    (col * pix_square_size, row * pix_square_size),
                    ((col + 1) * pix_square_size, (row + 1) * pix_square_size),
                    width=3,
                )
                    pygame.draw.line(
                    canvas,
                    (0, 0, 0),
                    ((col + 1) * pix_square_size, row * pix_square_size),
                    (col * pix_square_size, (row + 1) * pix_square_size),
                    width=3,
                )
                    
                elif self.state["preenchido"][row][col] == 2:
                    
                    pygame.draw.circle(
                    canvas,
                    (0, 0, 0),
                    ((col + 0.5) * pix_square_size, (row + 0.5) * pix_square_size),
                    pix_square_size // 3,
                    width=3,
                )

        if self.render_mode == "human":
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()
            self.clock.tick(self.metadata["render_fps"])
        else: 
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
            )
    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
