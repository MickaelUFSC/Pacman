# core/game_state.py

class GameState:
    def __init__(self, pacman_pos, food_positions):
        self.pacman_pos = pacman_pos
        self.food_positions = set(food_positions)
        self.initial_food_positions = list(food_positions)  # <- Adicionado!


    def is_goal_state(self):
        return len(self.food_positions) == 0

    def move_pacman(self, new_pos):
        self.pacman_pos = new_pos
        if new_pos in self.food_positions:
            self.food_positions.remove(new_pos)

    def copy(self):
        return GameState(self.pacman_pos, self.food_positions.copy())
