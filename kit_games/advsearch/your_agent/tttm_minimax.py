import random
from typing import Tuple
from ..tttm.gamestate import GameState
from .minimax import minimax_move

def make_move(state: GameState) -> Tuple[int, int]:
    """
    Retorna a jogada escolhida pelo algoritmo Minimax com poda alfa-beta para o Tic-Tac-Toe Misere.
    Como o espaço de busca é pequeno, utilizamos profundidade ilimitada (-1).
    """
    return minimax_move(state, -1, utility)

def utility(state: GameState, player: str) -> float:
    """
    Retorna a utilidade de um estado terminal para o jogador `player`.
    
    No Tic-Tac-Toe Misere:
    - Quem faz 3 em linha PERDE.
    - Se o vencedor (winner) for o jogador atual (`player`), ele ganha (+1.0).
    - Se o vencedor for o adversário, o jogador perdeu (-1.0).
    - Se for empate (winner is None ou 'draw'), retorna 0.0.
    """
    winner = state.winner()
    if winner == player:
        return 1.0
    elif winner is not None:
        return -1.0
    else:
        return 0.0