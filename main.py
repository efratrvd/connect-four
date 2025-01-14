from pandas import json_normalize
from tqdm import tqdm

from board import Board
from game import Game
from player import PlayerAB, PlayerMM, PlayerBFMM


def simulate_games(first_player_class, second_player_class):
    depths = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    depths = [1, 2, 3, 4, 5, 6, 7]

    results = []
    for player_1_depth in tqdm(depths):
        for player_2_depth in tqdm(depths):
            player_1 = first_player_class(player_1_depth, True)
            player_2 = second_player_class(player_2_depth, False)

            game = Game(Board(), player_1, player_2)
            winner, num_moves, player_1_times, player_2_times = game.simulateLocalGame()
            results.append({'first_player': {'id': player_1.__class__.__name__,
                                             'depth': player_1_depth,
                                             'times': player_1_times,
                                             'num_nodes_gen': player_1.num_nodes_generated
                                             },
                            'second_player': {'id': player_2.__class__.__name__,
                                              'depth': player_2_depth,
                                              'times': player_2_times,
                                              'num_nodes_gen': player_2.num_nodes_generated
                                              },
                            'winner': winner,
                            'num_moves': num_moves})

    return results


def run_game():
    player_1 = PlayerBFMM(1, isPlayerOne=True)
    player_2 = PlayerBFMM(7, isPlayerOne=False)

    game = Game(Board(), player_1, player_2)
    winner, num_moves = game.simulateLocalGame()
    print(winner, num_moves)


if __name__ == "__main__":
    player_types = [PlayerBFMM, PlayerAB, PlayerMM]
    results = []
    for player_1_type in player_types:
        for player_2_type in player_types:
            results += simulate_games(player_1_type, player_2_type)
            results_df = json_normalize(results)
            results_df.to_csv('game_simulation_results.csv')
