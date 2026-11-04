from ..othello.gamestate import GameState
from .minimax import minimax_move

def make_move(state: GameState):
    """
    Retorna a melhor jogada utilizando Minimax com poda alfa-beta
    e a heurística customizada focada em quinas, mobilidade e estruturas de triângulos/cunhas.
    Profundidade limitada a 4 para rodar com folga no tempo limite de 5 segundos.
    """
    return minimax_move(state, 4, evaluate_custom)

def evaluate_custom(state: GameState, player: str) -> float:
    board = state.board
    opponent = 'W' if player == 'B' else 'B'
    
    # 1. Controle de Quinas (Cantos do tabuleiro)
    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
    corner_score = 0.0
    for cx, cy in corners:
        tile = board.tiles[cy][cx]
        if tile == player:
            corner_score += 35.0
        elif tile == opponent:
            corner_score -= 35.0

    # 2. Penalidade de X-Squares e C-Squares (evitar entregar quinas)
    x_squares = [(1, 1), (1, 6), (6, 1), (6, 6)]
    x_penalty = 0.0
    for x, y in x_squares:
        cx, cy = (0 if x < 4 else 7), (0 if y < 4 else 7)
        if board.tiles[cy][cx] == '.': # Se a quina estiver vazia
            if board.tiles[y][x] == player:
                x_penalty -= 20.0
            elif board.tiles[y][x] == opponent:
                x_penalty += 20.0

    # 3. Mobilidade (número de jogadas válidas disponíveis)
    try:
        player_successors = list(state.successors())
        player_mobility = len(player_successors)
    except:
        player_mobility = 0

    # 4. Estrutura de "Triângulos" e Blocos Densos (Conectividade Diagonal/Ortogonal)
    structure_score = 0.0
    for y in range(8):
        for x in range(8):
            tile = board.tiles[y][x]
            if tile != '.':
                same_color_neighbors = 0
                diagonal_neighbors = 0
                
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < 8 and 0 <= ny < 8:
                            neighbor_tile = board.tiles[ny][nx]
                            if neighbor_tile == tile:
                                same_color_neighbors += 1
                                if dx != 0 and dy != 0: # Foco especial nas diagonais (fechamento de triângulos)
                                    diagonal_neighbors += 1
                
                # Bonifica peças que formam aglomerações seguras e feixes diagonais
                weight = same_color_neighbors + (diagonal_neighbors * 1.5)
                if tile == player:
                    structure_score += weight
                else:
                    structure_score -= weight

    # Agrega todos os fatores ponderados
    total_score = (
        (corner_score * 5.0) + 
        x_penalty + 
        (player_mobility * 2.5) + 
        structure_score
    )
    
    return float(total_score)