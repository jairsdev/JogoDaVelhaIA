class Verificacao:
    def __init__(self, jogo):
        self.jogo = jogo
    
    def verificaoLinha(self):
        linha = len(self.jogo)
        coluna = 0

        for i in range(linha):
            if (self.jogo[i][coluna] == 0):
                continue
            if self.jogo[i][coluna] == self.jogo[i][coluna+1] and self.jogo[i][coluna+1] == self.jogo[i][coluna+2]:
                return (True, self.jogo[i][coluna])
        return (False, False)
    
    def verificaoColuna(self):
        coluna = len(self.jogo) - 1
        linha = 0

        for i in range(coluna):
            if (self.jogo[linha][i] == 0):
                continue
            if self.jogo[linha][i] == self.jogo[linha+1][i] and self.jogo[linha+1][i] == self.jogo[linha+2][i]:
                return (True, self.jogo[linha][i])
        return (False, False)
    
    def verificaoDiagonal(self):
        linha = 0
        coluna = 0
        if (self.jogo[linha][coluna] != 0):
            if self.jogo[linha][coluna] == self.jogo[linha+1][coluna+1] and self.jogo[linha+1][coluna+1] == self.jogo[linha+2][coluna+2]:
                return (True, self.jogo[linha][coluna])
            
        linha = 0
        coluna = len(self.jogo[0]) - 1
        if (self.jogo[linha][coluna] != 0):
            if self.jogo[linha][coluna] == self.jogo[linha+1][coluna-1] and self.jogo[linha+1][coluna-1] == self.jogo[linha+2][coluna-2]:
                return (True, self.jogo[linha][coluna])
        return (False, False)
    
    def verificaoJogo(self, reward):
        if (self.verificaoColuna()[0] or self.verificaoLinha()[0] or self.verificaoDiagonal()[0]):
            if (self.verificaoColuna()[0]):
                vencedor = self.verificaoColuna()[1]
            if (self.verificaoDiagonal()[0]):
                vencedor = self.verificaoDiagonal()[1]
            if (self.verificaoLinha()[0]):
                vencedor = self.verificaoLinha()[1]
            if (vencedor == 1):
                reward += 10
            else:
                reward -= 20
            terminated = True
        else:
            terminated  = all(not 0 in linha for linha in self.jogo)
        reward += -1
        return terminated, reward

