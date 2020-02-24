from generalization_grid_games.envs import playing_with_XYZ
from generalization_grid_games.envs.utils import run_random_agent_demo


def run_interactive_demos():
    playing_with_XYZ.PlayingWithXYZGymEnv0(interactive=True)
    playing_with_XYZ.PlayingWithXYZGymEnv1(interactive=True)
    playing_with_XYZ.PlayingWithXYZGymEnv2(interactive=True)
    #playing_with_XYZ.PlayingWithXYZGymEnv4(interactive=True)


if __name__ == "__main__":
    run_interactive_demos()
    # run_random_agent_demo(stf.StopTheFallGymEnv1)
