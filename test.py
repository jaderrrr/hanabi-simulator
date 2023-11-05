from board import Board
from player import Player
from hand import Hand

def run_test():
    board = Board(False)

    hands = board.deal_cards(4)

    players = []
    for hand in hands:
        new_hand = Hand(hand)
        new_player = Player(new_hand, board)
        players.append(new_player)

    players[0].set_next_players([players[1], players[2], players[3]])
    players[1].set_next_players([players[2], players[3], players[0]])
    players[2].set_next_players([players[3], players[0], players[1]])
    players[3].set_next_players([players[0], players[1], players[2]])

    curr_player_idx = 0

    while board.explosions < 3 and len(board.deck) > 0:
        print(curr_player_idx)
        players[curr_player_idx].play_turn()
        
        curr_player_idx = (curr_player_idx + 1) % 4

        board.print_board()
        for player in players:
            player.print_hand()
        print("")
        input()

    # everyone should get one last turn 
    og_player_idx = curr_player_idx - 1
    if og_player_idx == -1:
        og_player_idx = 3

    while curr_player_idx != og_player_idx and board.explosions < 4:
        print(curr_player_idx)
        players[curr_player_idx].play_turn()
        curr_player_idx = (curr_player_idx + 1) % 4 
        board.print_board()
        for player in players:
            player.print_hand()
        print("")
        input()



    total_score = 0
    for stack in board.stacks:
        total_score += stack.score

    print(f"Final Result: {total_score}!")

    return total_score

if __name__ == "__main__":
    num_runs = 2

    result_total = 0
    min_score = 26
    max_score = 0
    for i in range(num_runs):
        result = run_test()
        if result < min_score:
            min_score = result
        if result > max_score:
            max_score = result
        
        result_total += result

    average = result_total / num_runs
    print(f"Average score {average:.2f}")
    print(f"Max score {max_score}")
    print(f"Min score {min_score}")
