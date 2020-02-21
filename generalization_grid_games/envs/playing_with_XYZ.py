from .generalization_grid_game import GeneralizationGridGame, create_gym_envs
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

for images in os.listdir(get_asset_path('raw/')):
    raw_images = changeResolution(images)

ALL_TOKENS = [EMPTY, X, Y, Z]
TOKEN_IMAGES = {
}