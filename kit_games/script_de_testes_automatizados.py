import subprocess
import sys
import re
from collections import defaultdict

# Configurações dos testes
NUM_RUNS_PER_MATCHUP = 50  # Altere para 100, 500 ou 1000 conforme seu tempo disponível
TIMEOUT_SECONDS = 15

# Pares de agentes para o torneio de avaliação
MATCHUPS = [
    {
        "name": "Custom vs Count (Ida)",
        "p1": "advsearch/your_agent/othello_minimax_custom.py",
        "p2": "advsearch/your_agent/othello_minimax_count.py",
    },
    {
        "name": "Count vs Custom (Volta)",
        "p1": "advsearch/your_agent/othello_minimax_count.py",
        "p2": "advsearch/your_agent/othello_minimax_custom.py",
    },
    {
        "name": "Custom vs Mask (Ida)",
        "p1": "advsearch/your_agent/othello_minimax_custom.py",
        "p2": "advsearch/your_agent/othello_minimax_mask.py",
    },
    {
        "name": "Mask vs Custom (Volta)",
        "p1": "advsearch/your_agent/othello_minimax_mask.py",
        "p2": "advsearch/your_agent/othello_minimax_custom.py",
    },
    {
        "name": "Count vs Mask (Ida)",
        "p1": "advsearch/your_agent/othello_minimax_count.py",
        "p2": "advsearch/your_agent/othello_minimax_mask.py",
    },
    {
        "name": "Mask vs Count (Volta)",
        "p1": "advsearch/your_agent/othello_minimax_mask.py",
        "p2": "advsearch/your_agent/othello_minimax_custom.py",
    },
]

def parse_game_output(output):
    """
    Extrai as pontuações do log impresso pelo server.py
    """
    b_match = re.search(r"Player 1 \(B - .*?\):\s*(\d+)", output)
    w_match = re.search(r"Player 2 \(W - .*?\):\s*(\d+)", output)
    
    if b_match and w_match:
        return int(b_match.group(1)), int(w_match.group(1))
    return None, None

def run_single_game(agent1, agent2):
    cmd = [sys.executable, "server.py", "othello", agent1, agent2]
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=TIMEOUT_SECONDS
        )
        return parse_game_output(result.stdout)
    except subprocess.TimeoutExpired:
        print("[AVISO] Partida cancelada por Timeout.")
        return None, None
    except Exception as e:
        print(f"[ERRO] Falha ao executar partida: {e}")
        return None, None

def main():
    log_file = open("tournament_stats.log", "w", encoding="utf-8")
    
    def log_print(text):
        print(text)
        log_file.write(text + "\n")
        log_file.flush()

    log_print("==================================================")
    log_print(f"  INICIANDO AVALIAÇÃO AUTOMATIZADA DE OTHELLO    ")
    log_print(f"  Partidas por confronto: {NUM_RUNS_PER_MATCHUP}")
    log_print("==================================================\n")

    overall_stats = defaultdict(lambda: {"wins": 0, "losses": 0, "ties": 0, "total_pieces": 0, "games": 0})

    for match in MATCHUPS:
        name = match["name"]
        p1_path = match["p1"]
        p2_path = match["p2"]
        
        p1_name = p1_path.split("/")[-1].replace(".py", "")
        p2_name = p2_path.split("/")[-1].replace(".py", "")

        log_print(f"--- Executando: {name} ---")
        log_print(f"P1 (B): {p1_name}  x  P2 (W): {p2_name}")
        
        p1_wins = 0
        p2_wins = 0
        ties = 0
        p1_total_score = 0
        p2_total_score = 0
        completed_games = 0

        for i in range(1, NUM_RUNS_PER_MATCHUP + 1):
            score_b, score_w = run_single_game(p1_path, p2_path)
            
            if score_b is None or score_w is None:
                continue

            completed_games += 1
            p1_total_score += score_b
            p2_total_score += score_w

            if score_b > score_w:
                p1_wins += 1
            elif score_w > score_b:
                p2_wins += 1
            else:
                ties += 1

            if i % 10 == 0 or i == NUM_RUNS_PER_MATCHUP:
                print(f"  Progresso: {i}/{NUM_RUNS_PER_MATCHUP} partidas concluídas...")

        if completed_games > 0:
            p1_avg = p1_total_score / completed_games
            p2_avg = p2_total_score / completed_games
            p1_win_pct = (p1_wins / completed_games) * 100
            p2_win_pct = (p2_wins / completed_games) * 100

            log_print(f"\nResultados do Confronto ({completed_games} partidas válidas):")
            log_print(f"  P1 ({p1_name}): {p1_wins} vitórias ({p1_win_pct:.1f}%) | Média de peças: {p1_avg:.2f}")
            log_print(f"  P2 ({p2_name}): {p2_wins} vitórias ({p2_win_pct:.1f}%) | Média de peças: {p2_avg:.2f}")
            log_print(f"  Empates: {ties}\n")

            # Acumula estatísticas globais por agente
            overall_stats[p1_name]["wins"] += p1_wins
            overall_stats[p1_name]["losses"] += p2_wins
            overall_stats[p1_name]["ties"] += ties
            overall_stats[p1_name]["total_pieces"] += p1_total_score
            overall_stats[p1_name]["games"] += completed_games

            overall_stats[p2_name]["wins"] += p2_wins
            overall_stats[p2_name]["losses"] += p1_wins
            overall_stats[p2_name]["ties"] += ties
            overall_stats[p2_name]["total_pieces"] += p2_total_score
            overall_stats[p2_name]["games"] += completed_games

    log_print("==================================================")
    log_print("             ESTATÍSTICAS GERAIS                  ")
    log_print("==================================================")
    
    for agent, stats in overall_stats.items():
        total_g = stats["games"]
        if total_g > 0:
            win_pct = (stats["wins"] / total_g) * 100
            avg_pieces = stats["total_pieces"] / total_g
            log_print(f"Agente: {agent}")
            log_print(f"  - Jogos Totais: {total_g}")
            log_print(f"  - Vitórias: {stats['wins']} ({win_pct:.2f}%)")
            log_print(f"  - Derrotas: {stats['losses']}")
            log_print(f"  - Empates: {stats['ties']}")
            log_print(f"  - Média de Peças/Partida: {avg_pieces:.2f}")
            log_print("--------------------------------------------------")

    log_file.close()
    print("\nRelatório final gravado com sucesso em 'tournament_stats.log'.")

if __name__ == "__main__":
    main()