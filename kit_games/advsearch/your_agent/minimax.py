# advsearch/your_agent/minimax.py
import random
from typing import Tuple, Callable

def minimax_move(state, max_depth, eval_fn):
    """
    Retorna a melhor jogada (ação) para o jogador atual no estado fornecido,
    utilizando o algoritmo Minimax com poda Alfa-Beta.
    
    :param state: Estado atual do jogo (GameState).
    :param max_depth: Profundidade máxima de busca (-1 para ilimitada).
    :param eval_fn: Função de avaliação heurística ou de utilidade.
    :return: A melhor ação (tupla de coordenadas x, y).
    """
    root_player = getattr(state, 'player', None)
    best_score = float('-inf')
    best_action = None
    
    alpha = float('-inf')
    beta = float('inf')
    
    successors = get_successors(state)
    for action, successor in successors:
        score = _min_value(successor, max_depth - 1 if max_depth != -1 else -1, alpha, beta, eval_fn, root_player)
        if score > best_score:
            best_score = score
            best_action = action
        alpha = max(alpha, best_score)
        
    return best_action

def _max_value(state, depth, alpha, beta, eval_fn, root_player):
    """
    Função Maximizadora do Minimax com Alfa-Beta.
    """
    if is_terminal_state(state) or depth == 0:
        return eval_fn(state, root_player)
    
    successors = get_successors(state)
    if not successors:
        return eval_fn(state, root_player)
    
    value = float('-inf')
    for action, successor in successors:
        value = max(value, _min_value(successor, depth - 1 if depth != -1 else -1, alpha, beta, eval_fn, root_player))
        if value >= beta:
            return value
        alpha = max(alpha, value)
    return value

def _min_value(state, depth, alpha, beta, eval_fn, root_player):
    """
    Função Minimizadora do Minimax com Alfa-Beta.
    """
    if is_terminal_state(state) or depth == 0:
        return eval_fn(state, root_player)
        
    successors = get_successors(state)
    if not successors:
        return eval_fn(state, root_player)
    
    value = float('inf')
    for action, successor in successors:
        value = min(value, _max_value(successor, depth - 1 if depth != -1 else -1, alpha, beta, eval_fn, root_player))
        if value <= alpha:
            return value
        beta = min(beta, value)
    return value

def is_terminal_state(state):
    if hasattr(state, 'is_terminal') and callable(state.is_terminal):
        return state.is_terminal()
    if hasattr(state, 'terminal'):
        return state.terminal
    return False

def get_successors(state):
    if hasattr(state, 'successors') and callable(state.successors):
        res = state.successors()
        return _normalize_successors(res)
    if hasattr(state, 'successors'):
        res = state.successors
        return _normalize_successors(res)
    if hasattr(state, 'get_successors') and callable(state.get_successors):
        res = state.get_successors()
        return _normalize_successors(res)
    if hasattr(state, 'children'):
        return _normalize_successors(state.children)
    if hasattr(state, 'legal_moves') and callable(state.legal_moves):
        moves = state.legal_moves()
        successors = []
        for action in moves:
            if hasattr(state, 'next_state') and callable(state.next_state):
                successors.append((action, state.next_state(action)))
            elif hasattr(state, 'result') and callable(state.result):
                successors.append((action, state.result(action)))
            else:
                successors.append((action, action))
        return successors
    return []

def _normalize_successors(res):
    normalized = []
    for item in res:
        if isinstance(item, tuple) and len(item) == 2:
            normalized.append(item)
        else:
            normalized.append((None, item))
    return normalized