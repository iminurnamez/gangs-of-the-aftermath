from . import prepare,tools
from .states import splash, citymap_screen, player_hood_screen, enemy_hood_screen
from .states import train_units, build_screen, player_attack_screen, message_screen
from .states import main_menu, save_game, enemy_attack_screen



def main():
    """Add states to control here."""
    run_it = tools.Control(prepare.ORIGINAL_CAPTION)
    state_dict = {
            "SPLASH": splash.Splash(),
            "MAIN_MENU": main_menu.MainMenu(),
            "CITYMAP": citymap_screen.CityMapScreen(),
            "PLAYER_HOOD_SCREEN": player_hood_screen.PlayerHoodScreen(),
            "ENEMY_HOOD_SCREEN": enemy_hood_screen.EnemyHoodScreen(),
            "TRAIN_UNITS": train_units.TrainUnits(),
            "BUILD_SCREEN": build_screen.BuildScreen(),
            "PLAYER_ATTACK": player_attack_screen.PlayerAttackScreen(),
            "ENEMY_ATTACK": enemy_attack_screen.EnemyAttackScreen(),
            "MESSAGE_SCREEN": message_screen.MessageScreen(),
            "SAVE_GAME": save_game.SaveGame()
            }
    run_it.setup_states(state_dict, "SPLASH")
    run_it.main()
