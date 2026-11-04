from ..othello.gamestate import GameState
from .minimax import minimax_move

def make_move(state: GameState):
    """
    Retorna a melhor jogada utilizando Minimax com poda alfa-beta
    e a heurística de contagem de peças. Profundidade limitada a 4.
    """
    return minimax_move(state, 4, evaluate_count)

def evaluate_count(state: GameState, player: str) -> float:
    """
    Retorna a diferença entre o número de peças do jogador e do oponente.
    """
    board = state.board
    # Descobre quem é o oponente
    opponent = 'W' if player == 'B' else 'B'
    
    player_count = 0
    opponent_count = 0
    
    # Percorre o tabuleiro contando as peças
    for row in board.tiles:
        for tile in row:
            if tile == player:
                player_count += 1
            elif tile == opponent:
                opponent_count += 1
                
    return float(player_count - opponent_count)