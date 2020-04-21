from .generalization_grid_game import create_gym_envs
from generalization_grid_games.envs.playingXYZGeneralizationGridGame import PlayingXYZGeneralizationGridGame
from .utils import get_asset_path, changeResolution

from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.patches import RegularPolygon, FancyArrow
import matplotlib.pyplot as plt
import numpy as np
import os 

EMPTY = 'empty'
X = 'x'
Y = 'y'
Z = 'z'
START = 's'
PASS = 'pass'
ALL_TOKENS = [EMPTY, X, Y, Z, PASS, START]
ALL_ACTION_TOKENS = [X, Y, Z, PASS, EMPTY]

#Change image resolution
# for image in os.listdir(get_asset_path('raw/')):
#     if image == ".DS_Store":
#         continue
#     path = get_asset_path('raw/'+image)
#     changeResolution(path,get_asset_path('') + image)

#ALL_TOKENS = [EMPTY, X, Y, Z, PASS]
TOKEN_IMAGES = {
    X: plt.imread(get_asset_path('x.png')),
    Y: plt.imread(get_asset_path('y.png')),
    Z: plt.imread(get_asset_path('z.png')),
    START: plt.imread(get_asset_path('start.png')),
}

HAND_ICON_IMAGE = plt.imread(get_asset_path('hand_icon.png'))

class UnityGame(TwoPlayerGeneralizationGridGame):
    num_tokens = len(ALL_TOKENS)
    hand_icon = HAND_ICON_IMAGE

    def __init__(self, layout, interactive=False, record_video=False, video_out_path='out.mp4'):
        self.layout = np.array(layout, dtype=object)

        self.initial_layout = layout.copy()
        self.current_layout = layout.copy()

        # self.interactive = interactive
        self.action = []
        # self.layout_demo = []
        # if record_video:
        #     self.start_recording_video(video_out_path)
        # else:
        #     self.record_video = False
        
        # height, width = layout.shape
        # self.width, self.height = width, height

        # #self.observation_space = spaces.MultiDiscrete(self.num_tokens * np.ones((height, width)))
        # #self.action_space = spaces.MultiDiscrete([self.height, self.width])
        # self.counter = 0
        # if interactive:
        #     self.action_lock = False

        #     # # Create the figure and axes
        #     self.fig, self.ax, self.textbox = self.initialize_figure(height, width)
        #     self.drawings = []
        #     self.render_onscreen()
        #     self.current_text_value = None

        #     # Create event hook for mouse clicks
        #     self.fig.canvas.mpl_connect('pick_event', self.button_press)
            
        #     # Create event for keyboard
        #     self.textbox.on_submit(self.submit)

        #     print("Initial Step")
        #     plt.show()


    def transition(self,layout, action):
        cval, pos  = action #i.e. (x, (3,1))
        r, c = pos 
        height, width = layout.shape
        new_layout = layout.copy()
        token = layout[r, c]
        #cval = self.current_text_value
        if cval in ALL_ACTION_TOKENS:
            return PlayingWithXYZ.add(new_layout,cval,r, c)
        else: return new_layout
        # if token == EMPTY:
        #     return PlayingWithXYZ.add(new_layout,token,r, c)
        # if token == PASS:
        #     return new_layout
        # if token == X:
        #     return playing_with_XYZ.add(new_layout, token, r, c)
        # if token == Y:
        #     return playing_with_XYZ.add(new_layout, token, r, c)
        # if token == Z: 
        #     return playing_with_XYZ.add(new_layout, token, r, c)

        #if token == UP_ARROW:

    @staticmethod
    def add(layout, token, r, c):
        if token != "pass":
            layout[r,c] = token
        return layout

    @staticmethod
    def compute_reward(state0, action, state1): 
        if np.array_equal(state0,layout0) and action[0] == PASS:
            return 1 
        return 0   

    @classmethod
    def draw_token(cls, token, r, c, ax, height, width, token_scale=1.0):
        if token == EMPTY:
            edge_color = '#888888'
            face_color = 'white'
            
            drawing = RegularPolygon((c + 0.5, (height - 1 - r) + 0.5),
                                         numVertices=4,
                                         radius=0.5 * np.sqrt(2),
                                         orientation=np.pi / 4,
                                         ec=edge_color,
                                         fc=face_color)
            ax.add_patch(drawing)

            return drawing

        else:
            edge_color = '#888888'
            face_color = '#DDDDDD'
            
            drawing = RegularPolygon((c + 0.5, (height - 1 - r) + 0.5),
                                         numVertices=4,
                                         radius=0.5 * np.sqrt(2),
                                         orientation=np.pi / 4,
                                         ec=edge_color,
                                         fc=face_color)
            ax.add_patch(drawing)

            im = TOKEN_IMAGES[token]
            oi = OffsetImage(im, zoom = cls.fig_scale * (token_scale / max(height, width)**0.5))
            box = AnnotationBbox(oi, (c + 0.5, (height - 1 - r) + 0.5), frameon=False)

            ax.add_artist(box)
            return box
    # @classmethod
    # def visualize_demonstration(demonstration):


    # def initialize_figure(cls, height, width):
    #     fig, ax, textbox = PlayingXYZGeneralizationGridGame.initialize_figure(height, width)

    #     # Draw a white grid in the background
    #     for r in range(height):
    #         for c in range(width):
    #             edge_color = '#888888'
    #             face_color = 'white'
                
    #             drawing = RegularPolygon((c + 0.5, (height - 1 - r) + 0.5),
    #                                          numVertices=4,
    #                                          radius=0.5 * np.sqrt(2),
    #                                          orientation=np.pi / 4,
    #                                          ec=edge_color,
    #                                          fc=face_color)
    #             ax.add_patch(drawing)

    #     return fig, ax, textbox





rng = np.random.RandomState()
num_layouts = 3
# def create_random_layout():
#     height = rng.randint(2,4)
#     width = rng.randint(2,4)
#     layout = np.full((height,width), EMPTY, dtype=object)
#     return layout

#layouts = [create_random_layout() for _ in range(num_layouts)]
#create_gym_envs(PlayingWithXYZ, layouts, globals())

E = EMPTY
S = START
#Training
layout0 = [
    [X, X, E, E],
    [S, X, E, E],
    [X, X, E, E]
]

layout1 = [
    [E, X, S, E],
    [E, E, X, E],
    [E, E, E, E], 
    [E, E, E, E]
]

layout2 = [
    [X, X, E, E],
    [X, S, E, E],
    [X, X, X, E], 
    [E, E, E, E]
]


# layout3 = [
#     [E, E, X, E],
#     [E, E, Y, E],
#     [E, E, Z, E], 
#     [E, E, E, E]
# ]

#Testing
layout3 = [
    [S, E, E, E], 
    [E, E, E, E],
    [E, E, E, E],
    [E, E, E, E] 
]
layout4 = [
    [E, E, E, E, E],
    [E, X, X, E, E],
    [E, X, S, E, E],
    [E, E, E, E, E],

]

layout5 = [
    [E, E, E, E, E],
    [E, E, E, E, E],
    [E, E, E, S, E],
    [E, E, E, E, E],

]


layouts = [np.array(x) for x in [layout0,layout1,layout2, layout3, layout4, layout5]]
create_gym_envs(PlayingWithXYZ, layouts, globals())