from time import time


class Game:
    def __init__(self, first_player_id, first_player_username):
        self.first_player = ({'id': first_player_id,
                              'username': first_player_username})
        self.start = time()
        self.board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.second_player = None
        self.symbols = {first_player_id: 1}

    def game_over(self):
        for i in range(3):
            # обработка горизонталей
            if (abs(sum(self.board[i * 3: i * 3 + 3])) == 3):
                return sum(self.board[i * 3: i * 3 + 3]) // 3
            # обработка вертикалей
            elif(abs(sum(self.board[i::3])) == 3):
                return sum(self.board[i::3]) // 3
        # обратока диагоналей
        if (abs(sum(self.board[::4])) == 3):
            return sum(self.board[::4]) // 3
        elif (abs(sum(self.board[2:7:2])) == 3):
            return sum(self.board[2:7:2]) // 3
        # обратока продолжения игры
        for i in range(9):
            if self.board[i] == 0:
                return None
        # обработка ничьей
        return 0

    def set_second_player(self, second_player_id, second_player_username):
        self.second_player = ({'id': second_player_id,
                               'username': second_player_username})
        self.symbols[second_player_id] = -1

    def check_player(self, player):
        if self.first_player['id'] == player:
            return 1
        elif self.second_player and self.second_player['id'] == player:
            return 2
        else:
            return 0

    def make_move(self, col, row, user_id):
        self.board[row * 3 + col] = self.symbols[user_id]

    def current_player(self):
        if sum(self.board) == 1:
            return self.second_player['id']
        else:
            return self.first_player['id']
