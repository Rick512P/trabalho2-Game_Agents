from ..othello.gamestate import GameState
from ..othello.board import Board
from .minimax import minimax_move

# Usamos a matriz exata esperada pelo teste de avaliação posicional
POS_MASK = [
    [100, -30,  6,  2,  2,  6, -30, 100],
    [-30, -50,  1,  1,  1,  1, -50, -30],
    [  6,   1,  1,  1,  1,  1,   1,   6],
    [  2,   1,  1,  3,  3,  1,   1,   2],
    [  2,   1,  1,  3,  3,  1,   1,   2],
    [  6,   1,  1,  1,  1,  1,   1,   6],
    [-30, -50,  1,  1,  1,  1, -50, -30],
    [100, -30,  6,  2,  2,  6, -30, 100]
]

def make_move(state: GameState):
    """
    Retorna a melhor jogada utilizando Minimax com poda alfa-beta
    e a heurística de valor posicional (máscara). Profundidade limitada a 4.
    """
    return minimax_move(state, 4, evaluate_mask)

def evaluate_mask(state: GameState, player: str) -> float:
    """
    Retorna a avaliação posicional compatível com o teste unitário.
    """
    board = state.board
    opponent = 'W' if player == 'B' else 'B'
    
    player_score = 0.0
    opponent_score = 0.0
    
    for y in range(8):
        for x in range(8):
            tile = board.tiles[y][x]
            weight = POS_MASK[y][x]
            if tile == player:
                player_score += weight
            elif tile == opponent:
                opponent_score += weight
                
    return float(player_score - opponent_score)