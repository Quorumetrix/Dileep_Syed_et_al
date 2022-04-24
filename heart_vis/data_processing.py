# data_processing.py
import numpy as np
import math
import skimage.io
from PIL import Image # For importing a tiff
from skimage.util import montage

from heart_vis.config import *
from heart_vis.convenience_funcs import *


def standardize_arrays(volume, mask, field):

    '''
    Standardize the input arrays so their dimensions are aligned.

    Input:
        volume: ndarray; reprenting intensity values of the tissue volume
        mask: ndarray; representing the mask to be used to constrain the streamlines
        field: ndarray; containing the orientation values for each dimension

    Returns:
        crop_volume
        crop_mask
        crop_field
    '''

    min_x = np.min([volume.shape[0], mask.shape[0], field.shape[0]])
    min_y = np.min([volume.shape[1], mask.shape[1], field.shape[1]])
    min_z = np.min([volume.shape[2], mask.shape[2], field.shape[2]])
    print('Minimum dimensions: ',min_x,min_y,min_z)

    assert volume.shape[1] == mask.shape[1], 'Mismatch between size of y axis'
    assert volume.shape[1] == field.shape[1], 'Mismatch between size of y axis'
    assert field.shape[1] == mask.shape[1], 'Mismatch between size of y axis'


    #volume, mask, field
    crop_volume = volume[:min_x,:min_y,:min_z]
    crop_mask  = mask[:min_x,:min_y,:min_z]
    crop_field   = field[:min_x,:min_y,:min_z,:]

    if(ROTATE):
        print('Shape of cropped arrays (before rotation): ')
        print(crop_volume.shape)
        print(crop_mask.shape)
        print(crop_field.shape)
        print('Shape of cropped arrays (after rotation): ')

        crop_volume = np.rot90(crop_volume, 1,(1, 2))
        crop_mask = np.rot90(crop_mask, 1,(1, 2))
        crop_field = np.rot90(crop_field, 1,(1, 2))
        crop_field[:,:,:,[1,2]] = crop_field[:,:,:,[2,1]]  # When rotating, also need to swap field values for y and z components


    print('Shape of cropped arrays: ')
    print(crop_volume.shape)
    print(crop_mask.shape)
    print(crop_field.shape)

    return crop_volume, crop_mask, crop_field



def sample_field_vals(field_array):

    '''
    Gets the value of the field that don't sum to 1 (Those in the tissue)

    '''

    # Find the array indexes where the fields don't add up to 1.
    sum_array = np.sum(field_array,axis=3)  # New orientation
    inds = np.where(sum_array != 1)
    field_inds = np.transpose(np.asarray(inds))
    assert field_inds.shape[1] == 3, 'Error, perhaps not properly rotated array?'


    return field_inds



def get_subvolume(field, cube_dims, isfield=True):

    '''
    Process a subvolume of the field for a given position and window.

    Input:
        field: ndarray
        cube_dims: tuple; (xpos, ypos, zpos,window, depth)
        isfield: boolean;determine whether to expect one or 3 values

    Returns:
        subfield: [3,m,n,p] array
        (xx,yy,zz): tuple, 3D meshgrid coordinates

    '''
    # Unpack the cube dimensions
    xpos,ypos,zpos,window_x, window_y, depth = cube_dims


    if(window_x * window_y * depth > 10000):

        print(' Warning, subvolume contains: ',str(window_x * window_y * depth),' voxels, may be difficult to draw them all.' )

    x_hi = int(xpos + window_x / 2)
    x_lo = int(xpos - window_x / 2)
    y_hi = int(ypos + window_y / 2)
    y_lo = int(ypos - window_y / 2)
    z_hi = int(zpos + depth / 2)
    z_lo = int(zpos - depth / 2)

    if(isfield):
        sub_field = field[x_lo:x_hi, y_lo:y_hi,z_lo:z_hi, :] # updated to transposed array
    else:
        sub_field = field[x_lo:x_hi, y_lo:y_hi,z_lo:z_hi]

    # Get the index positions for each of the Glyphs.
    xs = np.arange(x_lo,x_hi)
    ys = np.arange(y_lo,y_hi)
    zs = np.arange(z_lo,z_hi)

    xx,yy,zz = np.meshgrid(xs,ys,zs)

    print('Created subvolume of field, shape: ', np.shape(sub_field))

    return sub_field, (xx,yy,zz)


def make_montage(sub_vol, dimensions, label='', min_max=(0,4095)):

    '''
    Generate the montage that can be loaded into Blender as a 2D image texture.
    Since Blender does not accept a 3D image stack, it must be flattened into a 2D
    image, and subsequently re-sliced into 3D using the material shader nodes.

    Uses 'dimensions' tuple with the 'file' name to create a unique volume name.

    Inputs:
        sub_vol: m,n,p array containing raw staining values
        dimensions: tuple( xpos,ypos,zpos,window,depth )
    '''

    xpos,ypos,zpos,window_x,window_y,depth = dimensions

    print('Tif value range (sub_vol) : ', np.nanmin(sub_vol), np.nanmax(sub_vol))

    # Scale range to what the shaders in blender will expect.

    # min-max normalization to the range expected by the shaders
    sub_vol = (sub_vol - min_max[0]) /  (min_max[1] - min_max[0])  * 65535
    print('Scaled value range (sub_vol) : ', np.nanmin(sub_vol), np.nanmax(sub_vol))

    sub_vol = np.swapaxes(sub_vol,0,2)
    sub_vol = np.swapaxes(sub_vol,1,2)
    sk_montage = montage(sub_vol,grid_shape=(1,depth)).astype('uint16')

    max_proj = np.max(sub_vol, axis=2)
    
    print(' Created: ',np.shape(sk_montage), ' montage.')

    thisfile = LOAD_PATH + '/montages/' + FILE + str(dimensions)
    skimage.io.imsave(thisfile+label+'.tif', sk_montage, plugin='tifffile')
    skimage.io.imsave(thisfile+label+'_max.tif', max_proj, plugin='tifffile')

    print(' Saved Montage: ',thisfile)
