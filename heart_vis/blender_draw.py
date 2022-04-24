#blender_draw.py
import bpy
import bmesh
from bpy.app.handlers import persistent # For the driver expression script

import numpy as np

from heart_vis.config import *
from heart_vis.data_processing import make_montage, get_subvolume,sample_field_vals
from heart_vis.convenience_funcs import *

'''
Blender draw and scene functions
'''

def get_materials(mat_path=BLEND_TEMPLATE):

    with bpy.data.libraries.load(mat_path) as (data_from, data_to):
        data_to.materials = data_from.materials

    for mat in data_to.materials:
        if mat is not None:
            print(mat.name)


def stream2curve(coords, collection_label, cmap_val=None):

    '''
    Accepts the coordinates and draws them into Blender
    '''

    # create the Curve Datablock
    curveData = bpy.data.curves.new('streamline', type='CURVE')
    curveData.dimensions = '3D'
    curveData.resolution_u = 2

    # map coords to spline
    polyline = curveData.splines.new(type='NURBS')
    polyline.points.add(len(coords[:,0])-1)
    polyline.use_endpoint_u = True

    for i in range(len(coords[:,0])):

        x = (coords[i][0])# * xy_scale
        y = (coords[i][1])# * xy_scale
        z = (coords[i][2])# * z_scale

        if(x + y + z > 0):

            polyline.points[i].co = (x, y, z, 1)

    # create Object
    curveOB = bpy.data.objects.new('myCurve', curveData)
    curveData.bevel_depth = TUBE_BEVEL#0.0005

    # For each object
    mat = bpy.data.materials.get('streamtube')
    curveOB.data.materials.append(mat)

    # Optional colormapping: use pass_index to set color in shader nodes (object index)
    if cmap_val is not None:

        # Assign pass_index to apply a colormap.
        curveOB.pass_index = cmap_val * 255 # Express in 0-255 color range.

    # Since 2.8, this is the way to link the curve object to the scene
    scn = bpy.context.scene
    bpy.data.collections[collection_label].objects.link(curveOB)
    bpy.context.view_layer.objects.active = curveOB

    return curveOB

def animate_curve(t0, t1,persistent=False):

    '''
    Animate the curve bevel of the SELECTED curve

    Input:
        t0: int, first frame of animation
        t1: int, last frame of animation
        persistent: boolean that controls whether the curves grow to completion,
        or show only a growing tip.

    returns:
        None
    '''
    scene = bpy.context.scene

    scene.frame_set(t0-1)

    # Segment moving along
    bpy.context.object.data.bevel_factor_start = 0 #set factor to 0
    bpy.context.object.data.bevel_factor_end = 0 #set factor to 0

    bpy.context.object.data.keyframe_insert(data_path='bevel_factor_start') #keyframe it
    bpy.context.object.data.keyframe_insert(data_path='bevel_factor_end') #keyframe it


    if not persistent:


        scene.frame_set(t0)

        # Segment moving along
        bpy.context.object.data.bevel_factor_start = 0 #set factor to 0
        bpy.context.object.data.bevel_factor_end = 0.001 #set factor to 0

        bpy.context.object.data.keyframe_insert(data_path='bevel_factor_start') #keyframe it
        bpy.context.object.data.keyframe_insert(data_path='bevel_factor_end') #keyframe it

        scene.frame_set(t1)

        # Segment moving along
        bpy.context.object.data.bevel_factor_start = 0.999 #set factor to 0
        bpy.context.object.data.bevel_factor_end = 1 #set factor to 0

        bpy.context.object.data.keyframe_insert(data_path='bevel_factor_start') #keyframe it
        bpy.context.object.data.keyframe_insert(data_path='bevel_factor_end') #keyframe it


        scene.frame_set(t1+1)

        # Segment moving along
        bpy.context.object.data.bevel_factor_start = 1#set factor to 0
        bpy.context.object.data.bevel_factor_end = 1 #set factor to 0

        bpy.context.object.data.keyframe_insert(data_path='bevel_factor_start') #keyframe it
        bpy.context.object.data.keyframe_insert(data_path='bevel_factor_end') #keyframe it

    else:

        scene.frame_set(t0)

        # Segment moving along
        bpy.context.object.data.bevel_factor_start = 0 #set factor to 0
        bpy.context.object.data.bevel_factor_end = 0.01 #set factor to 0

        bpy.context.object.data.keyframe_insert(data_path='bevel_factor_start') #keyframe it
        bpy.context.object.data.keyframe_insert(data_path='bevel_factor_end') #keyframe it


        scene.frame_set(t1)

        # Segment moving along
        bpy.context.object.data.bevel_factor_start = 0
        bpy.context.object.data.bevel_factor_end = 1

        bpy.context.object.data.keyframe_insert(data_path='bevel_factor_start') #keyframe it
        bpy.context.object.data.keyframe_insert(data_path='bevel_factor_end') #keyframe it



def drawVerts(data,label = 'Vers',incr=1):

    '''
    Load point clouds into a non-mesh cloud of vertices.
    '''

    mesh = bpy.data.meshes.new("Mesh")  # add a new mesh
    obj = bpy.data.objects.new(label, mesh)  # add a new object using the mesh

    bpy.context.collection.objects.link(obj)   # Since 2.8, this is the way to do this
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    mesh = bpy.context.object.data
    bm = bmesh.new()

    for i in range(0,len(data[:,0]),incr):

        # NOTE the inversion OR LACK

        x = (data[i][0])# - x_offset) / xy_scale
        y = (data[i][1])# - y_offset) / xy_scale
        z = (data[i][2])# - z_offset) / z_scale

        bm.verts.new([x, y, z])  # add a new vert

    # make the bmesh the object's mesh
    bm.to_mesh(mesh)
    bm.free()  # always do this when finished


def draw_mask(mask,incr=100):

    '''
    Represent the volume of the input mask as a point cloud of sample vertices
    from within the mask.
    '''

    inds = np.where(mask > 0)
    mask_inds = np.transpose(np.asarray(inds))
    assert mask_inds.shape[1] == 3, 'Error, perhaps not properly rotated array?'

    drawVerts(mask_inds, label='Mask', incr=incr)


def dense_glyph_volume(field, meshcube, mask, dims, driver=True, downsample=False, label=''):

    '''
    Draw Glyphs for every value from a volume.
    Input:
        field : (m*n*p*q) array (original sized field
        meshcube: tuple (xx,yy,zz) of the index psitions for each voxel of the subvolume
                with respect to the original field array.
        driver: Boolean, whether or not to apply a driver to the scale
    Q: Does it make sense to use the meshcube regerring to original field values?

    '''
    print('Creating dense glyph volume from subfield')

    # UNpack the dimensions tuple and input meshcube
    xpos,ypos,zpos,window_x, window_y,depth = dims

    xx = meshcube[0]
    yy = meshcube[1]
    zz = meshcube[2]

    # Calculate appropriate gkyph scaling based on downsampling.
    n_voxels = (window_x * window_y * depth)
    print('input volume n_voxels:', n_voxels)
    ds_fact = n_voxels / N_GLYPHS
    GLYPH_DIM_BASE = 0.05 #Works well for native resolution
    glyph_dim = GLYPH_DIM_BASE * ds_fact / 20

    # Use a Cylinder primitive as the Glyph
    bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, enter_editmode=False, location=(0, 0, 0))
    # bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(xpos,ypos,zpos))
    bpy.context.active_object.name = FILE +"_GlphCtl_"+label
    bpy.ops.transform.resize(value=(glyph_dim, glyph_dim, glyph_dim * 10))
    # ctrl = bpy.data.objects["Empty"]     #the control object
    ctrl = bpy.data.objects[FILE +"_GlphCtl_"+label]     #the control object

    #obj = bpy.context.selected_objects[0] # Object to be the glyph, must be selected
    obj = bpy.data.objects["Cylinder"]
    mat = bpy.data.materials.get('Glyph')
    obj.data.materials.append(mat)

    parent_coll = bpy.context.selected_objects[0].users_collection[0]
    coll = bpy.data.collections.new(FILE+"_Glyphs_"+label)
    parent_coll.children.link(coll)


    xarr = xx.ravel()
    yarr = yy.ravel()
    zarr = zz.ravel()

    # Downsample by skipping values when > 10K glyphs would be made.
    if(downsample):

        # Calculate starting number of voxels from dimensions

        if n_voxels > N_GLYPHS:

            print('n_voxels > N_GLYPHS, downsampling to < ', N_GLYPHS)

            x_z_ratio = window_x / depth
            x_y_ratio = window_x / window_y
            x_steps = int(window_x)
            # y_steps = window_y
            y_steps = int(round(x_steps / x_y_ratio))
            z_steps = int(round(x_steps / x_z_ratio))

            print('x_y_ratio:',x_y_ratio)
            print('x_z_ratio:',x_z_ratio)
            print('x_steps:',x_steps)
            print('y_steps:', y_steps)
            print('z_steps:',z_steps)


            assert abs(window_y - y_steps) < 1, 'y_step error'
            assert abs(depth - z_steps) < 1, 'z_step error'


            # progressively shrink until within appropriate size to draw
            while n_voxels > N_GLYPHS:

                x_steps = x_steps - 1
                # y_steps = y_steps - 1
                y_steps = int(round(x_steps / x_y_ratio))
                z_steps = int(round(x_steps / x_z_ratio))
                n_voxels = x_steps * y_steps * z_steps

            print('Post downsampling: ')
            print('x_steps:', x_steps)
            print('y_steps:', y_steps)
            print('z_steps:', z_steps)

            # Create a new range of values with this number of intervals.
            xs = np.linspace(xpos - window_x / 2,
                             xpos + window_x / 2,
                             x_steps)
            ys = np.linspace(ypos - window_y / 2,
                             ypos + window_y / 2,
                             y_steps)
            zs = np.linspace(zpos - depth / 2,
                             zpos + depth / 2,
                             z_steps)

            xx_, yy_, zz_ = np.meshgrid(xs,ys,zs)

            # fill the arrays with the raveled values of the new meshgrid.
            xarr = xx_.ravel()
            yarr = yy_.ravel()
            zarr = zz_.ravel()

            assert len(xarr) == n_voxels, 'Meshgrid not giving expected results'

    for i in range(0,len(xarr)):

        x = xarr[i]
        y = yarr[i]
        z = zarr[i]

        '''
        We don't want to use rounded ints for the object location (above),
        but need rounded values as indices to the field values below.
        '''
        # Round and int for indexing the field.
        xr = int(round(xarr[i]))
        yr = int(round(yarr[i]))
        zr = int(round(zarr[i]))

        if(mask[xr,yr,zr] > 0):

            # Calculate the rotation
            vect = field[xr,yr,zr,:] # updated to transposed array
            mat = rotation_matrix_from_vectors(vect, DEF_VECT)
            eul = rot2eul(mat)

            if not np.array_equal(vect, FILT_VECT): # Filter specific vector.

                # Set location based on stack index.
                new_obj = obj.copy()
                new_obj.animation_data_clear()
                coll.objects.link(new_obj)
                new_obj.location = (x,y,z)  #define arrows positions (here they are centered on the world origin)

                # print(field[xr,yr,zr,:])

                # Rotate the copied object
                new_obj.rotation_euler[0] = eul[0]
                new_obj.rotation_euler[1] = eul[1]
                new_obj.rotation_euler[2] = eul[2] + np.pi

                # Assign pass_index to apply a colormap.
                mapped_val = np.arccos(abs(field[xr,yr,zr, 2]))
                new_obj.pass_index = mapped_val * 255 # Express in 0-255 color range.

                # Apply a driver to the X,Y,Z scale of the glyph so that the scale
                # of the entire collection of glyphs can be controlled by the empty.
                if(driver):
                    for t, val in enumerate(['X', 'Y', 'Z']):

                        driv = new_obj.driver_add("scale", t).driver
                        driv.type = 'SCRIPTED'
                        driv.use_self = True

                        dist = driv.variables.new()
                        dist.name = "var"
                        dist.type = 'TRANSFORMS'

                        dist.targets[0].id = ctrl
                        dist.targets[0].transform_type = 'SCALE_'+ val
                        driv.expression = "var"

    print('Finished drawing dense cube of glyphs')



def draw_streamlines(streamlines,collection_label='stream'):

    '''
    Create a new collection and draw the streamlines.
    Converts list of streamlines to curves in Blender.

    Input:
        streamlines: list of streamline polyline objects
        collection_label: string
    '''

    # Create a collection and make it active to store curves
    collection = bpy.data.collections.new(collection_label)
    bpy.context.scene.collection.children.link(collection)
    layer_collection = bpy.context.view_layer.layer_collection.children[collection.name] # NOTE the use of 'collection.name' to account for potential automatic renaming
    bpy.context.view_layer.active_layer_collection = layer_collection

    # Convert streamlines to curves in Blender
    for  stream in streamlines:

        stream2curve(stream,collection_label)

    print('Finished loading ',len(streamlines), 'streamlines as curves.')



def stream_curves(field,mask,positions, sign, n_points=STREAM_LENGTH, window=None, angle_thresh=ANGLE_THRESH, label=''):

    '''
    Function to calculate streamline positions using custom algorithm

    Input:
        field: [m,n,p,3] array with x,y,z vector components
        mask
        positions: [n,3] array containing positions(= field indexes) of
                    starting point for each of the N_STREAMLINES streamlines
        sign: +-1, multiplier for the field vector to choose direction streamline is drawn.
        n_points: Number of points to draw along the streamline in either direction
        window: int. Number of voxels to average across in x,y,z. (smoothing)
    '''

    # Create the collections to hold them.
    if(ANIMATE):
        tip_label = 'streams_' + str(sign) + '_tip' + label # label allows unique collections
        create_collection(tip_label)

    persistent_label = 'streams_' + str(sign) + '_pers' + label
    create_collection(persistent_label)

    bpy.ops.object.empty_add(type='PLAIN_AXES')#, location=(xpos,ypos,zpos))
    bpy.context.active_object.name = 'streamline_ctl'
    ctrl = bpy.data.objects['streamline_ctl']     #the control object

    cmap_vals = []

    for n in range(N_STREAMLINES):

        x = (positions[n,0])
        y = (positions[n,1])
        z = (positions[n,2])

        # Colormap value for each streamline
        #cmap_val = abs(field[x,y,z, 2]) # Map the z axis (already 0 - 1) - updated to transposed array
        cmap_val = np.arccos(abs(field[x,y,z, 2])) # Map the z axis (already 0 - 1) - updated to transposed array
        cmap_vals.append(cmap_val)
        coord_list = []
        coord_list.append([x, y, z]) # Makes sure the first point is there

        for i in range(n_points):

            # Check whether positions are within bounds.
            condx = (x >= 0) and (x < field.shape[0])
            condy = (y >= 0) and (y < field.shape[1])
            condz = (z >= 0) and (z < field.shape[2])


            if(condx and condy and condz):

                # Get the component values at that position in the vector field
                dx = field[int(np.floor(x)), int(np.floor(y)), int(np.floor(z)),0]
                dy = field[int(np.floor(x)), int(np.floor(y)), int(np.floor(z)),1]
                dz = field[int(np.floor(x)), int(np.floor(y)), int(np.floor(z)),2]

            else:
                # print('Sample out of bounds (n, i): ',n, i, ' breaking loop')
                break

            if(i > 1): # You may only calculate the angle if there are enough points.

                # Calculate angle between segments.
                x1 = coord_list[-2][0]
                y1 = coord_list[-2][1]
                z1 = coord_list[-2][2]

                x2 = coord_list[-1][0]
                y2 = coord_list[-1][1]
                z2 = coord_list[-1][2]

                # Calculate both potential locations for the next point,

                xii= x + dx
                yii = y + dy
                zii = z + dz

                xiii= x - dx
                yiii = y - dy
                ziii = z - dz

                #and choose the one making the smallest angle
                x1 = coord_list[-2][0]
                y1 = coord_list[-2][1]
                z1 = coord_list[-2][2]

                x2 = coord_list[-1][0]
                y2 = coord_list[-1][1]
                z2 = coord_list[-1][2]

                angle_pos = calc_angle((x1,y1,z1),(x2,y2,z2),(xii,yii,zii))
                angle_neg = calc_angle((x1,y1,z1),(x2,y2,z2),(xiii,yiii,ziii))

                if(abs(angle_neg) > abs(angle_pos)):
                    xi = xii
                    yi = yii
                    zi = zii
                    seg_angle = angle_pos
                else:
                    xi = xiii
                    yi = yiii
                    zi = ziii
                    seg_angle = angle_neg

                cond_angle = abs(seg_angle) < angle_thresh

            else: # For the first two points, can't calculate angle, so bypass by defaulting cond_angle to true.

                cond_angle = True
                # Default xi,yi,zi
                xi = x + dx * sign
                yi = y + dy * sign
                zi = z + dz * sign


            # Check whether positions are within bounds.
            condxi = (xi >= 0) and (xi < field.shape[0])
            condyi = (yi >= 0) and (yi < field.shape[1])
            condzi = (zi >= 0) and (zi < field.shape[2])

            if(condxi and condyi and condzi):

                cond_mask = mask[int(xi),int(yi),int(zi)] > 0

                # Check that the vector value doesn't match the one we're filtering.
                # Needs to be inside the condition to avoid out of bounds errors
                vect = field[int(xi),int(yi),int(zi),:]

                if not np.array_equal(vect, FILT_VECT): # Filter specific vector.
                    # print(vect, FILT_VECT)
                    cond_filt = True
                else:
                    cond_filt = False

            else:
                cond_mask = False
                cond_filt = False

            if(cond_mask and cond_angle and cond_filt):#and cond_mask):

                coord_list.append([xi, yi, zi]) # Add new point

                # Update positions
                x = xi
                y = yi
                z = zi

            else:

                break

        coords = np.asarray(coord_list)

        if(coords.shape[0] > 1):

            # Persistent streamlines
            stream2curve(coords, persistent_label,cmap_val)


            if(ANIMATE):

                # Sample from a beta distribution (so all curves don't start at once)
                curve_anim_duration = 600
                func = np.random.beta(5, 1, 1)
                scale_func = func * (ANIM_END-ANIM_START) + ANIM_START

                t0 = scale_func
                t1 = scale_func + curve_anim_duration

                animate_curve(t0,t1,persistent=True)

                # Streamline tips - truncated version of the same streamline
                # (Only draw if animating the curves)
                stream2curve(coords, tip_label,cmap_val)
                animate_curve(t0,t1, persistent=False)

        else:
            print('Skipping n = ', n, ' from:  ', persistent_label)

    print('cmap_vals', np.min(cmap_vals), np.max(cmap_vals))

def create_collection(label, parent=None):
    '''
    Create a named collection

    input:
        label: str,name of collection
        parent: (optional) str, name of collection this collection is to be parented to.

    '''
    if parent is not None:
        # If setting to active collection
        # parent_coll = bpy.context.selected_objects[0].users_collection[0]
        parent_coll = bpy.data.collections[parent]
        collection = bpy.data.collections.new(label)
        parent_coll.children.link(collection)

    else:
        collection = bpy.data.collections.new(label)
        bpy.context.scene.collection.children.link(collection)


def bi_streamlining(field,mask, orig=None, label=''):

    '''
    Bi-directional streamline (streamtube) generating function

    Input:
        field: vector field [3,m,n,p] matrix where the first
                dimension is the x,y,z component
        orig: (xx,yy,zz) tuple (meshcube) Origin of the streamlines, defaults to a random sample of the entire field,
            But otherwise a sub-volume can be provided.
    TO DO: Draw glyphs at each position along the streamline
            - required modification of draw_glyphs() to accept predetermined
             glyph positions
    '''

    print('Drawing streamlines.')

    if orig is None: # If no subvolume os provided, use the whole one.

        orig = field

        # Standard way of visualizing start positions
        field_inds = sample_field_vals(field)
        pos = field_inds[np.random.choice(field_inds.shape[0], N_STREAMLINES, replace=False), :]

    else:

        xx = orig[0]
        yy = orig[1]
        zz = orig[2]

        xarr = xx.ravel()
        yarr = yy.ravel()
        zarr = zz.ravel()

        cube_coords = np.transpose(np.vstack([xarr,yarr,zarr]))
        pos = cube_coords[np.random.choice(cube_coords.shape[0], N_STREAMLINES, replace=False), :]

    drawVerts(pos, label='streamline_start_positions') # Useful to see where the streamlines originate

    # Bidirectional streamlines:
    # for each origin point, they are drawin in + (1) and - (1) direction
    stream_curves(field,mask,pos, 1, label=label)
    stream_curves(field,mask,pos, -1, label=label)

    print('Finished drawing ', N_STREAMLINES, ' bidirectional streamlines.')

def make_volumetric_cube(volume, dimensions, isfield=False):

    '''
    Make a cube and position it at the same position as the subvolume with respect to the entire dataset.
    '''

    xpos,ypos,zpos,window_x, window_y,depth = dimensions
    label = ''
    min_max = (0,4095)
    print("dimensions: ",str(dimensions))


    sub_vol, cube = get_subvolume(volume, dimensions, isfield=isfield)
    print('sub_vol: ' ,np.shape(sub_vol))

    if isfield:
        sub_vol = np.arccos(abs(sub_vol[:,:,:,2]))
        label='_field'
        min_max = (-1,1)

    make_montage(sub_vol,dimensions, label=label, min_max=min_max)

    x_len = window_x
    y_len = window_y
    z_len = depth

    # Load the recently created montage
    new_img = bpy.data.images.load(filepath=LOAD_PATH + '/montages/'+FILE+str(dimensions)+label+'.tif')

    # Create, place and stretch the volumetric cube
    bpy.ops.mesh.primitive_cube_add(location=(xpos-0.5, ypos-0.5, zpos-0.5))
    bpy.ops.transform.resize(value=(x_len/2, y_len/2, z_len/2))


    # Get the cube as active object and get the volumetric material
    obj = bpy.context.active_object
    obj.name = 'volume_'+str(dimensions)+label # Rename uniquely
    mat = bpy.data.materials.get('new_volumetric'+label) #''' Add a second material with label attached into template, so both don't share the exact same material'''
    obj.data.materials.append(mat)

    # Assign material it to object
    if obj.data.materials:
        # assign to 1st material slot
        obj.data.materials[0] = mat
    else:
        # no slots
        obj.data.materials.append(mat)


    # Edit the node values

    # get the nodes
    nodes = mat.node_tree.nodes

    # Value node specifies how many slices in the subvolume.
    val_node = nodes.get("Value")
    val_node.outputs[0].default_value = depth

    nodes["Texture Coordinate"].object = obj# bpy.data.objects["texture control"]

    # Image texture node to control which image gets wrapped as a volume
    im_tex_node = nodes.get("Image Texture")#.002")
    im_tex_node.image = new_img


def load_collections(coll_to_add=None):

    '''
    Load collections from the BLEND_TEMPLATE file.
    '''

    with bpy.data.libraries.load(BLEND_TEMPLATE) as (data_from, data_to):
        data_to.collections = data_from.collections

    for col in data_to.collections:
        if col is not None:
            print(col.name)
            this_colletion = col

    # Link collection by name after loading
    this_colletion = bpy.data.collections.get(coll_to_add)
    bpy.context.scene.collection.children.link(this_colletion)


def load_worlds():

    '''
    Load the world from the blend template,
    but these still must be applied manually
    '''
    # Use an HDRI to give more realistic model lighting.
    HDRI_PATH = "Z:\\Blender\\hdri\\small_rural_road_4k.hdr"
    bpy.ops.image.open(filepath=HDRI_PATH)

    with bpy.data.libraries.load(BLEND_TEMPLATE) as (data_from, data_to):
        data_to.worlds = data_from.worlds

    for world in data_to.worlds:
        if world is not None:
            print('Loaded: ',world.name)
            this_world = world

def render_settings():

    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.device = 'GPU'
    bpy.context.scene.render.film_transparent = True


def init_blend():

    '''
    Initial set up of the scene by loading the relevant materials, worlds and collections
    '''

    # Set up the scene
    get_materials() # Should be inside getVolu,e, but test to see if already run.
    load_worlds()
    load_collections('Camera.collection')
    load_collections('Reference.collection')
    render_settings()
