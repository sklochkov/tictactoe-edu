from time import time

class Game:
    def __init__(self, first_player):
        self.first_player = first_player
        self.start = time()
        self.board = [[0,0,0],[0,0,0],[0,0,0]]
        self.second_player = None
        self.current_player = {'id': None, 'symbol': None}

    def gameOver(self):
        # обработка вертикалей и горизонталей
        for i in range(3):
            if (sum(self.board[i]) == 3) or ((self.board[0][i] + self.board[1][i] + self.board[2][i]) == 3):
                return 1
            elif (sum(self.board[i]) == -3) or ((self.board[0][i] + self.board[1][i] + self.board[2][i]) == -3):
                return -1
        # обратока диагоналей
        if ((self.board[0][0] + self.board[1][1] + self.board[2][2]) == 3) or ((self.board[2][0] + self.board[1][1] + self.board[0][2]) == 3):
            return 1
        elif ((self.board[0][0] + self.board[1][1] + self.board[2][2]) == -3) or ((self.board[2][0] + self.board[1][1] + self.board[0][2]) == -3):
            return -1
        # обратока продолжения игры
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return None
        # обработка ничьей
        return 0

    def setSecondPlayer(self, second_player):
        self.second_player = second_player

    def checkPlayer(self, player):
        if self.first_player == player:
            return 1
        elif self.second_player == player:
            return 2
        else:
            return 0

    def makeMove(self, col, row, symbol):
        self.board[row][col] = symbol
    