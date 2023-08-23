from game import Game
from agent import Agent_AI


if __name__ == '__main__':
    game = Game()
    agent = Agent_AI(game)

    face = None
    while face != "cool":
        game.new_game()
        face = game.get_face()

        n_moves = 0
        while face == "happy" or face == "surprised":
            agent.play()
            n_moves += 1
            print("Moves:", n_moves)
            face = game.get_face()

    print("\nDu vann!")
    input("Press Enter to exit ")
