from .generalization_grid_game import create_gym_envs
from generalization_grid_games.envs.playingXYZGeneralizationGridGame import PlayingXYZGeneralizationGridGame
from .utils import get_asset_path, changeResolution
from UnityDemo.GetDemonstration import DemonstrationHandler, get_demonstrations_name
from UnityDemo.constants import *
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.patches import RegularPolygon, FancyArrow
import matplotlib.pyplot as plt
import numpy as np
import os 


# EMPTY = [None,""]
# P = 'P'
# P_Clicked = 'P_highlighted'
# S = 'S'
# S_CLicked = 'S_highlighted'
# B = 'B'
# START = 'start'
# PASS = 'pass'
# CLICK = 'click'
# ALL_TOKENS = [EMPTY, P, S, B, PASS, START]
# ALL_ACTION_TOKENS = [CLICK]

# TOKEN_IMAGES = {
#     P: plt.imread(get_asset_path('p.png')),
#     S: plt.imread(get_asset_path('s.png')),
#     B: plt.imread(get_asset_path('b.png')),
#     START: plt.imread(get_asset_path('start.png')),
#     P_Clicked: plt.imread(get_asset_path('P_highlighted.png')),
#     S_CLicked: plt.imread(get_asset_path('S_highlighted.png'))
# }

class UnityGame(PlayingXYZGeneralizationGridGame):
    num_tokens = len(ALL_TOKENS)
    fig_scale = 0.2
    def __init__(self, layout, interactive=False, record_video=False, video_out_path='out.mp4'):
        self.layout = np.array(layout, dtype=object)

        self.initial_layout = layout.copy()
        self.current_layout = layout.copy()

        # self.interactive = interactive
        self.action = []
        self.layout_demo = []
        if record_video:
            self.start_recording_video(video_out_path)
        else:
            self.record_video = False
        
        height, width = layout.shape
        self.width, self.height = width, height

        #self.observation_space = spaces.MultiDiscrete(self.num_tokens * np.ones((height, width)))
        #self.action_space = spaces.MultiDiscrete([self.height, self.width])
        self.interactive = False
        self.counter = 0
        self.returnfrom = self.dictionary_creator()
        
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
        pos  = action #i.e. (x, (3,1))
        r, c = pos 
        height, width = layout.shape
        new_layout = layout.copy()
        #token = layout[r, c]
        pick_state = np.argwhere((layout == P_Clicked) | (layout == S_CLicked))
        if len(pick_state) >= 1:
            if len(pick_state) > 1:
                print("ERROR: More than two objects picked at the same time")
            selected_piece = pick_state[0] 
            # if layout[tuple(selected_piece[0])] == P_Clicked:
            #     selected_piece = P
            # elif layout[tuple(selected_piece[0])] == S_CLicked:
            #     selected_piece = S
            return self.add(new_layout,r,c,selected_piece)
        else:
            return self.add(new_layout, r, c,None)
        # else: return new_layout
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
    def dictionary_creator():
        returnfrom = dict()
        returnfrom[P_Clicked] = P
        returnfrom[P] = P_Clicked
        returnfrom[S_CLicked] = S
        returnfrom[S] = S_CLicked
        return returnfrom

    def add(self,layout, r, c, pick_obj = None):
        if isinstance(pick_obj, np.ndarray):
            token = layout[tuple(pick_obj)]
            layout[tuple(pick_obj)] = None
            layout[r,c] = self.returnfrom[token] 
        else:
            token = layout[r,c]
            if token == None:
                return layout
            new_token = self.returnfrom[token] 
            layout[r,c] = new_token
        return layout

    @staticmethod
    def compute_reward(state0, action, state1): 
        if np.array_equal(state0,state1) and action[0] == PASS:
            return 1 
        return 0

    # def render(self):
    #     for drawing in self.drawings:
    #         drawing.remove()
    #     self.drawings = []

    #     for r in range(self.height):
    #         for c in range(self.width):
    #             # if r == 20 and c == 21:
    #             #     print("hello")
    #             token = self.dict_seq[self.curr_time][r][c]
    #             drawing = self.draw_token(token, r, c, self.ax, height = self.height,width=self.width)
    #             if drawing is not None:
    #                 self.drawings.append(drawing)   


    @classmethod
    def draw_token(cls,token, r, c, ax, height, width):
        if token in EMPTY:
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

            tk = token.split()[-1]
            im = TOKEN_IMAGES[tk]
            oi = OffsetImage(im, zoom = 1 * (cls.fig_scale*2  / max(height, width)**0.5))
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





# rng = np.random.RandomState()
# num_layouts = 3
# # def create_random_layout():
# #     height = rng.randint(2,4)
# #     width = rng.randint(2,4)
# #     layout = np.full((height,width), EMPTY, dtype=object)
# #     return layout

# #layouts = [create_random_layout() for _ in range(num_layouts)]
# #create_gym_envs(PlayingWithXYZ, layouts, globals())

# E = EMPTY
# S = START
# #Training
# layout0 = [
#     [X, X, E, E],
#     [S, X, E, E],
#     [X, X, E, E]
# ]

# layout1 = [
#     [E, X, S, E],
#     [E, E, X, E],
#     [E, E, E, E], 
#     [E, E, E, E]
# ]

# layout2 = [
#     [X, X, E, E],
#     [X, S, E, E],
#     [X, X, X, E], 
#     [E, E, E, E]
# ]


# # layout3 = [
# #     [E, E, X, E],
# #     [E, E, Y, E],
# #     [E, E, Z, E], 
# #     [E, E, E, E]
# # ]

# #Testing
# layout3 = [
#     [S, E, E, E], 
#     [E, E, E, E],
#     [E, E, E, E],
#     [E, E, E, E] 
# ]
# layout4 = [
#     [E, E, E, E, E],
#     [E, X, X, E, E],
#     [E, X, S, E, E],
#     [E, E, E, E, E],

# ]

# layout5 = [
#     [E, E, E, E, E],
#     [E, E, E, E, E],
#     [E, E, E, S, E],
#     [E, E, E, E, E],

# ]

names = ["layer1.json","layer2.json"]
#names.remove("matrix.json")
# if ".DS_Store" in names:
#     names.remove(".DS_Store")
layouts = [DemonstrationHandler(name)(only_initial_layer=True) for name in names]
print("hellowolrd")
# layouts = [np.array(x) for x in [layout0,layout1,layout2, layout3, layout4, layout5]]
create_gym_envs(UnityGame, layouts, globals())