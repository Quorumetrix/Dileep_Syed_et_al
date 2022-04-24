#main.py

'''
This is the script to be run from the Python console in Blender.

Note: You must have installed the all necessary dependencies within the Blender
    Python installation - it is not sufficient for them to be installed in your
    System Python installation.

'''

# Ensure that the folder containing this Blender Python module is added to system path
import sys
sys.path.append('E://Documents/Professional/Quorumetrix_Studio/Github_projects/Dileep_Syeed_et_al/''

# Import the scripts from this module
from heart_vis.config import *
from heart_vis.load_data import *
from heart_vis.convenience_funcs import *
from heart_vis.data_processing import *
from heart_vis.blender_draw import *

# Other useful Python imports
import os
import time

def main():

    # Load data
    volume = load_tif(IMAGE_DEPTH)
    mask = load_tif(IMAGE_DEPTH, mask=True)
    field = load_field_data()

    # Standardize arrays
    volume, mask, field = standardize_arrays(volume, mask, field)

    if(FULL_STREAMLINES): # Streamlining in entire field (not subvolume)

        bi_streamlining(field, mask, label=FILE+'_all_'+SUPP_DESC)

    # Define the subvolume
    cube_dims = (x,y,z,window_x, window_y, depth)
    subfield, cube = get_subvolume(field,cube_dims)

   if(VOLUMETRIC): # Create a volumetric representation of the tissue using shader nodes
       make_volumetric_cube(volume, cube_dims)
       make_volumetric_cube(field,cube_dims, isfield=True)

   # Create a 3D grid of glyphs that fills the volume of the specified cube (subvolume)
   dense_glyph_volume(field, cube, mask,dims=cube_dims, downsample=True,label='glyphs')

   if(SUBVOL_STREAMLINES): # Create streamlines originating in the subvolume
       bi_streamlining(field,mask, cube, label=str(cube_dims)+SUPP_DESC)

   bpy.ops.wm.save_mainfile(filepath=BLEND_FILEPATH+'.blend')


if __name__ == '__main__':

    main()
