class Game:
    def __init__(self, id: int):
        self.player1_made_move = False
        self.player2_made_move = False
        self.ready = False
        self.id = id
        self.moves = [None, None]

    def get_player_move(self, p):
        return self.moves[p]

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.player1_made_move = True
        else:
            self.player2_made_move = True

    def connected(self):
        return self.ready

    def both_made_move(self):
        return self.player1_made_move and self.player2_made_move

    def winner(self):

        player1 = self.moves[0]
        player2 = self.moves[1]

        winner = -1
        if player1 == 'Rock' and player2 == 'Scissors':
            winner = 0
        elif player1 == 'Scissors' and player2 == 'Rock':
            winner = 1
        elif player1 == 'Paper' and player2 == 'Rock':
            winner = 0
        elif player1 == 'Rock' and player2 == 'Paper':
            winner = 1
        elif player1 == 'Scissors' and player2 == 'Paper':
            winner = 0
        elif player1 == 'Paper' and player2 == 'Scissors':
            winner = 1

        return winner

    def reset(self):
        self.player1_made_move = False
        self.player2_made_move = False
