from .generalization_grid_game import PlayingXYZGeneralizationGridGame, create_gym_envs
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
PASS = 'pass'

#Fix image resolution
for image in os.listdir(get_asset_path('raw/')):
    if image == ".DS_Store":
        continue
    path = get_asset_path('raw/'+image)
    changeResolution(path,get_asset_path('') + image)

ALL_TOKENS = [EMPTY, X, Y, Z, PASS]
TOKEN_IMAGES = {
    X: plt.imread(get_asset_path('x.png')),
    Y: plt.imread(get_asset_path('y.png')),
    Z: plt.imread(get_asset_path('z.png'))
}

HAND_ICON_IMAGE = plt.imread(get_asset_path('hand_icon.png'))

class PlayingWithXYZ(PlayingXYZGeneralizationGridGame):
    num_tokens = len(ALL_TOKENS)
    hand_icon = HAND_ICON_IMAGE

    @staticmethod
    def transition(layout, action):

        r, c = action
        height, width = layout.shape
        new_layout = layout.copy()
        token = layout[r, c]
        new_layout = layout.copy()
        if token == EMPTY:
            return PlayingWithXYZ.add(new_layout,token,r, c)
        if token == PASS:
            return new_layout
        if token == X:
            return playing_with_XYZ.add(new_layout, token, r, c)
        if token == Y:
            return playing_with_XYZ.add(new_layout, token, r, c)
        if token == Z: 
            return playing_with_XYZ.add(new_layout, token, r, c)

        #if token == UP_ARROW:

    @staticmethod
    def add(layout, token, r, c):
        layout[r,c] == token

    @staticmethod
    def compute_reward(state0, action, state1):
        return 0.

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



    def initialize_figure(cls, height, width):
        fig, ax, textbox = PlayingXYZGeneralizationGridGame.initialize_figure(height, width)

        # Draw a white grid in the background
        for r in range(height):
            for c in range(width):
                edge_color = '#888888'
                face_color = 'white'
                
                drawing = RegularPolygon((c + 0.5, (height - 1 - r) + 0.5),
                                             numVertices=4,
                                             radius=0.5 * np.sqrt(2),
                                             orientation=np.pi / 4,
                                             ec=edge_color,
                                             fc=face_color)
                ax.add_patch(drawing)

        return fig, ax, textbox


    def button_press(self, event):
        if self.action_lock:
            return
        if (event.xdata is None) or (event.ydata is None):
            return
        i, j = map(int, (event.xdata, event.ydata))
    
        if (i < 0 or j < 0 or i >= self.width or j >= self.height):
            return

        self.action_lock = True
        c, r = i, self.height - 1 - j
        if event.button == 1:
            print(self.current_text_value)
            self.step((r, c))
        self.fig.canvas.draw()
        self.action_lock = False
    
    def value(self,text):
        self.currentvalue = text



rng = np.random.RandomState()
num_layouts = 3
def create_random_layout():
    height = rng.randint(2,20)
    width = rng.randint(2,20)
    layout = np.full((height,width), EMPTY, dtype=object)
    return layout

layouts = [create_random_layout() for _ in range(num_layouts)]
create_gym_envs(PlayingWithXYZ, layouts, globals())
