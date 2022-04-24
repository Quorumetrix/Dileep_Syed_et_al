import numpy as np
import os

'''
Configuration file that is loaded the first time the streamline and glyph script
is run in a Blender instance.

It contains:
    - Paths to data input and output folders
    - Global constants and variables that are parameters for the streamline
        and glyph generating algorithms.

Several of the constants and variables are grouped by scene, and controlled by
the SCENE global. Below is a description of the scene-specific constants:

    BLEND_FILENAME: Filename to be given to the generated .blend file

    FILE: reference to the dataset to be loaded

    TUBE_BEVEL: Thickness of the streamtubes

    SUBVOL_STREAMLINES: Boolean; if True, algorithm draws streamlines
    originating from the subvolume defined by the cube.

    FULL_STREAMLINES: Boolean; if True, algorithm draws streamlines originating
        from points throughout the starting tissue volume

    N_STREAMLINES: Number of streamlines to be drawn

    x,y,z: postional coordinates designating the center of the cube that defines
        a subregion of interest

    window_x, window_y, depth: The width of the 'window' for each dimension of
        the cube defining a subregion of interest

    SUPP_DESC: String; Optional supplemental description used when naming the
        generated collections.

    N_GLYPHS: Number of glyphs to draw

    VOLUMETRIC: Boolean; if True, algorithm will create a volumetric
        representation of the tissue volume using material shader nodes
'''

SCENE = 'apex' # 'schematic', 'short', 'long', 'apex', 'long_full','short_full', 'long_section', 'short_section'
IMAGE_DEPTH = 162 # Number of slices in the stack. Z-component of image

SAMPLING_VOXELS = 0
ANGLE_THRESH = 45 #60
STREAM_LENGTH = 10000# 10k,Number of points to draw along each direction of streamline


if (SCENE == 'schematic'):
    BLEND_FILENAME = 'schematic_scene'
    FILE = 'short17b1'

    # Streamlines
    TUBE_BEVEL = 0.4#0.3
    SUBVOL_STREAMLINES = True
    FULL_STREAMLINES = False
    N_STREAMLINES = 1000

    # A nice slab across the short section, tissue-end to tissue end
    x = 950 #- 500
    y = 1100
    z = 80

    window_x = 500
    window_y = 100
    depth = 20

    SUPP_DESC = ''
    N_GLYPHS = 5000

    VOLUMETRIC = True

elif (SCENE == 'short'):

    BLEND_FILENAME = 'shortaxis_scene'
    FILE = 'short17b1'

    # Streamlines
    TUBE_BEVEL = 0.2#0.3
    SUBVOL_STREAMLINES = False
    FULL_STREAMLINES = True
    N_STREAMLINES = 5000
    SUPP_DESC = ''
    N_GLYPHS = 20000

    VOLUMETRIC = False

    x = np.floor(1345 / 2)
    y = np.floor(2560 / 2)
    z = np.floor(IMAGE_DEPTH /2)

    window_x = x * 2 - 10
    window_y = y * 2 - 10
    depth = z * 2 - 10


elif (SCENE == 'long'):
    BLEND_FILENAME = 'longaxis_scene'
    FILE = 'long18b1'
    # Streamlines
    TUBE_BEVEL = 0.3#0.3
    SUBVOL_STREAMLINES = False
    FULL_STREAMLINES = True
    N_STREAMLINES = 5000

    # Cube dimensions for the subvolume
    # stack_x = np.round(1595*5/8)
    stack_x = np.floor(1595/2)
    stack_y = np.floor(3556/2)
    stack_z = np.floor(IMAGE_DEPTH /2)
    stack_window_x =stack_x * 2 - 10#1100
    stack_window_y =stack_y * 2 - 10#500
    stack_depth = stack_z * 2 - 10 # -10, #50

    SUPP_DESC = ''
    N_GLYPHS = 10000
    VOLUMETRIC = False

elif (SCENE == 'apex'):

    IMAGE_DEPTH = 216
    BLEND_FILENAME = 'full_apex' #'apex_scene'
    FILE = 'apex17A1S1' #'long18b1'
    # Streamlines
    TUBE_BEVEL = 1#0.3
    SUBVOL_STREAMLINES = False
    FULL_STREAMLINES = True
    N_STREAMLINES = 10000
    SUPP_DESC = ''
    N_GLYPHS = 75000
    VOLUMETRIC = False #True

    ANGLE_THRESH = 60 # For the apex, a less stringent angle cutoff is needed

    # Apex

    # Same as for short axis, using apex image dimensions
    x = np.floor(1153 / 2)
    y = np.floor(1141 / 2)
    z = np.floor(IMAGE_DEPTH /2)

    window_x = x * 2 - 10
    window_y = y * 2 - 10
    depth = z * 2 - 10





elif (SCENE == 'long_full'):

    BLEND_FILENAME = 'longaxis_full'
    FILE = 'longaxisfullview18b1'
    # Streamlines
    TUBE_BEVEL = 1.0#0.3
    SUBVOL_STREAMLINES = False
    FULL_STREAMLINES = True
    N_STREAMLINES = 25000

    # Cube dimensions for the subvolume
    stack_x = np.floor(3594/2)
    stack_y = np.floor(3556/2)
    stack_z = np.floor(IMAGE_DEPTH /2)
    stack_window_x =stack_x * 2 - 10#1100
    stack_window_y =stack_y * 2 - 10#500
    stack_depth = stack_z * 2 - 10 # -10, #50

    # Focus on the area generating the 'eddies' behavior
    stack_x = np.floor(3594/2)
    stack_y = np.floor(3556/2)
    stack_z = np.floor(IMAGE_DEPTH /2)
    stack_window_x =stack_x * 2 - 10#1100
    stack_window_y =stack_y * 2 - 10#500
    stack_depth = stack_z * 2 - 10 # -10, #50

    SUPP_DESC = ''
    N_GLYPHS = 75000
    VOLUMETRIC = False

elif (SCENE == 'short_full'):

    BLEND_FILENAME = 'shortaxis_scene_new'
    FILE = 'short17b1_full'

    # Streamlines
    TUBE_BEVEL = 1.0#0.3
    SUBVOL_STREAMLINES = False
    FULL_STREAMLINES = True
    N_STREAMLINES = 10000 # 5000
    SUPP_DESC = ''
    N_GLYPHS = 75000

    VOLUMETRIC = False

    x = np.floor(2844 / 2)
    y = np.floor(2560 / 2)
    z = np.floor(IMAGE_DEPTH /2)

    window_x = x * 2 - 10
    window_y = y * 2 - 10
    depth = z * 2 - 10

elif (SCENE == 'long_section'):

    BLEND_FILENAME = 'longaxis_full'
    FILE = 'longaxisfullview18b1'
    # Streamlines
    TUBE_BEVEL = 0.3#0.3
    SUBVOL_STREAMLINES = True
    FULL_STREAMLINES = False
    N_STREAMLINES = 1000

    stack_x = np.floor(3594/2)
    stack_y = np.floor(3556/2)
    stack_z = np.floor(IMAGE_DEPTH /2)
    stack_window_x = stack_x * 2 - 10#1100
    stack_window_y = stack_y * 2 - 10#500
    stack_depth = stack_z * 2 - 10 # -10, #50

    SUPP_DESC = ''
    N_GLYPHS = 5000
    VOLUMETRIC = True

elif (SCENE == 'short_section'):

    BLEND_FILENAME = 'shortaxis_section'
    FILE = 'short17b1_full'

    # Streamlines
    TUBE_BEVEL = 0.5
    SUBVOL_STREAMLINES = True
    FULL_STREAMLINES = False
    N_STREAMLINES = 1000
    SUPP_DESC = ''
    N_GLYPHS = 75000

    VOLUMETRIC = True

    x = 1950
    y = 2100
    z = int((156-84/2))

    window_x = 300
    window_y = 500
    depth = 156 - 84


'''
Remaining constants the are the same between all scenes/input datasets
'''

RAW_PATH = 'Z://Collaboration_data/Heart/' + FILE + '/' # Path to data
LOAD_PATH = 'Z://Collaboration_data/Heart/my_generated/' # Path to preprocessed data
BLEND_TEMPLATE = 'Z://Blender/Heart/template_parula.blend' # Path to .blend template
MAT_PATH = 'Z://Blender/heart/tif_voxel_volumetric_experiments.blend' # Materials
SAVE_PATH = 'Z://Blender/Heart/delivery/' # Path to save .blend file output
BLEND_FILEPATH = os.path.join(SAVE_PATH,BLEND_FILENAME)

# Field
SMOOTH_FIELD = True # Is the input data using a smoothed vector field

INIT_BLEND = True # Bool to determine whether to initialize the scene (template)
ANIMATE = False # Whether or not to animate the streamlines
ANIM_START = 0 # Animation start frame
ANIM_END = 500 # Animation end frame

MULTI_CUBE = False # Multiple subvolues indicated in CUBES

print(FILE)
print(BLEND_FILEPATH)

# Glyphs
N_SAMPLES = 1000
GLYPH_SCALE = 0.5 # For glyph drawn with curves

if((FILE == 'short17b1') or (FILE == 'apex17A1S1') or (FILE == 'short17b1_full')):

    DEF_VECT = [0,0,1] # Default vector orientation
#    FILT_VECT = None
    FILT_VECT = [0,0,1] # Vector orientation to be filterd
    ROTATE = False # Boolean indicating whether the sample is to be rotated.


elif((FILE == 'long18b1') or (FILE == 'longaxisfullview18b1')):

    DEF_VECT = [0,0,1]  # Default vector orientation
    FILT_VECT = [0,1,0]# Vector orientation to be filterd
    ROTATE = True # Boolean indicating whether the sample is to be rotated.


    if ROTATE:
        # Need to also swap axis for the sample volume being drawn
        x = stack_x
        y = stack_z
        z = stack_y

        window_x = stack_window_x
        window_y = stack_depth
        depth = stack_window_y

    else:
        x = stack_x
        y = stack_y
        z = stack_z
        window_x = stack_window_x
        window_y = stack_window_y
        depth = stack_depth
