# load_data.py
from heart_vis.config import *

# Standard Python imports
import os
import numpy as np
# Non-standard python imports (may need to be installed in Blender's Python)
from PIL import Image # For importing a tiff
import vtk
from vtk.util import numpy_support

def load_tif(image_depth, mask=False, method='PIL'):

    '''
    Used for loading a tif file and processing it, saving into a numpy array
    for faster loading.

    parameters:
        image_depth: Z-dimension of image stack. Number of slices in tif.
        mask: Boolean; if true, input volume expected to be binary
        method: Str: Tif loading method, 'PIL' or 'VTK'
    '''

    npy_file =  FILE+'_imstack.npy'
    tif_file = FILE+'.tif'

    if(mask):

        npy_file =  FILE+'_mask.npy'#'_mask_erode3x.npy'#
        tif_file = FILE+'mask.tif'#'mask_erode3x.tif'#

    imstack = []

    # Start by trying to load the preprocessed stack as a numpy file
    if os.path.isfile(LOAD_PATH + npy_file):

        imstack = np.load(LOAD_PATH + npy_file)
        print("Loaded numpy volume: ", npy_file)
        print("Numpy volume shape: ", np.shape(imstack))

    else:

        print('Did not find numpy file: ',LOAD_PATH + npy_file, ', loading TIF instead.')

        if(method == 'PIL'):
            # Create an array to hold values from multiple images of the stack (imstack)
            img = Image.open(RAW_PATH+tif_file)
            img.seek(0) # Get first page of multi-page tiff
            print('PIL loaded slice range: ', np.nanmin(img), np.nanmax(img))
            imstack = np.asarray(img) # Start the cumulative array of slices.
            print('Numpy array created from slice, range: ', np.nanmin(img), np.nanmax(img))
            print('Loaded first page of tif as numpy array with shape: ',np.shape(imstack))

            image_width = np.shape(imstack[0]) # pixels
            image_height = np.shape(imstack[1]) # pixels

            for i in range(0,image_depth):
                try:
                    img.seek(i)
                    this_array = np.asarray(img)
                    imstack = np.dstack((imstack,this_array))

                except EOFError:
                    # Not enough frames in img
                    break
                except MemoryError:
                    # Not enough memory to do more concatenating images
                    print('Memory error at slice: ' + str(i) +', imstack shape: '+ str(np.shape(imstack)))
                    image_depth = np.shape(imstack)[2]
                    break
                except ValueError:# Catches the case where a slice doesn't have the correct dimentions
                    i = i + 1
                    print("Slice skipped: " + str(i))


        elif(method=='VTK'):

            vtkimg = read_tiff_vtk(tif_file, RAW_PATH)
            imstack = vtk_image_to_numpy_array(vtkimg)

        # Save index positions to file
        np.save(LOAD_PATH + npy_file, imstack)
        print("Saved volume as numpy array: ", LOAD_PATH + npy_file)

    assert np.shape(imstack)[0] > 0, 'No stack loaded'

    print('Original volume shape: ', np.shape(imstack))
    imstack = np.transpose(imstack, (1,0,2))
    print('Transposed volume shape: ',np.shape(imstack))
    print('Tif value range (imstack) : ', np.nanmin(imstack), np.nanmax(imstack))

    return imstack



def load_tiff_inds():

    # Load the tiff data
    tif_inds = np.load(LOAD_PATH + FILE + '_thresh_tif.npy') # Note: This just loads the indices where signal above threshold.

    # Transpose it (consider removing if included in processing above)
    tif_inds = np.transpose(np.asarray(tif_inds))
    assert tif_inds.shape[1] == 3, 'Error, perhaps not properly rotated array?'

    # Use the thresholded tiff as location for the streamlines
    #tif_sample_inds = tif_inds[np.random.choice(tif_inds.shape[0], N_SAMPLES, replace=False), :]
    print('Tif inds loaded, shape: ',np.shape(tif_inds))

    return tif_inds


def load_field_data():

    field_name = '_field.npy'

    # Load the field data
    if(SMOOTH_FIELD):
        field_name = '_field_smooth.npy'

    field = np.load(LOAD_PATH + FILE + field_name)

    print('Loaded field, original shape: ', np.shape(field))

    field = np.transpose(field, (2,3,1,0))
    print('Transposed field, shape: ',np.shape(field))

    return field


def read_tiff_vtk(filename, folder='./', spacing=(1, 1, 1)):

    vtkDataReader = vtk.vtkTIFFReader()
    print('WARNING: using vtk tiff reader, may be issues depending onn vtk version.')
    vtkDataReader.SetFileName(os.path.join(folder, filename))
    print(os.path.join(folder, filename))
    vtkDataReader.Update()
    image = vtkDataReader.GetOutput()
    cols, rows, depth = image.GetDimensions()
    if spacing is None:
        spacing = image.GetSpacing()
    image.SetOrigin(-cols / 2, -rows / 2, 0)
    image.SetSpacing(spacing)

    print(' Loaded image data:' + str(type(image)))
    print(image.GetDimensions())

    return image

def vtk_image_to_numpy_array(vtk_image):
    dims = vtk_image.GetDimensions()
    scalar_data = vtk_image.GetPointData().GetScalars()
    numpy_image = numpy_support.vtk_to_numpy(scalar_data)
    numpy_image = numpy_image.reshape(dims[2], dims[1], dims[0])
    numpy_image = numpy_image.transpose(1, 2, 0)
    print('vtk image shape: ',numpy_image.shape)

    return numpy_image
