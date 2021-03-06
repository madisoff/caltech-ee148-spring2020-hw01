import os
import numpy as np
import json
from PIL import Image
from pathlib import Path
import time

def detect_red_light(I, comp):
    '''
    This function takes a numpy array <I> and returns a list <bounding_boxes>.
    The list <bounding_boxes> should have one element for each red light in the
    image. Each element of <bounding_boxes> should itself be a list, containing
    four integers that specify a bounding box: the row and column index of the
    top left corner and the row and column index of the bottom right corner (in
    that order). See the code below for an example.

    Note that PIL loads images in RGB order, so:
    I[:,:,0] is the red channel
    I[:,:,1] is the green channel
    I[:,:,2] is the blue channel
    '''


    bounding_boxes = [] # This should be a list of lists, each of length 4. See format example below.

    '''
    BEGIN YOUR CODE
    '''
    # Image search paramters
    min_frame = 8                       # smallest bounding_box size
    max_frame = 23                      # largest bounding_box size
    thresh = 0.91                       # correlation threshold
    y_thresh = 0.55                     # fraction of the rows to search in

    I_x = np.shape(I)[1]                # image pixel width
    I_y = np.shape(I)[0]                # image pixel height

    comp_x = np.shape(comp)[1]          # comparison image sizes
    comp_y = np.shape(comp)[0]
    used_boxes = np.zeros((I_y,I_x))    # array for storing/updating correlations

    # Check boxes of dimension i with upper left corner at row k and column j
    for i in range(max_frame,min_frame-1,-2):
        for j in range(0,I_x - i,2):
            for k in range(0,I_y - i - (int(I_y * y_thresh)),2):
                # Single out the part of the image to test
                test_box = I[k:(k+i),j:(j+i)]
                # Resize it to match the dimension of the comparison image
                test_box = [[test_box[int(i * r / comp_y)][int(i * c / comp_x)] for c in range(comp_x)] for r in range(comp_y)]
                test_box = np.asarray(test_box)

                # Turn the test box and comparison image into 1D arrays
                test_box_1d = test_box.flatten()
                comp_1d = comp.flatten()

                # Compute the correlation
                corr = np.inner(test_box_1d/np.linalg.norm(test_box_1d),comp_1d/np.linalg.norm(comp_1d))

                # Add the box if the new correlation exceeds the threshold
                # as well as any previous correlation at the coordinate.
                if (corr > thresh) and (corr > used_boxes[k,j]):
                    bounding_boxes.append([k,j,k+i,j+i])
                    used_boxes[k:(k+i),j:(j+i)] = corr

    '''
    As an example, here's code that generates between 1 and 5 random boxes
    of fixed size and returns the results in the proper format.
    '''
    '''
    box_height = 8
    box_width = 6

    num_boxes = np.random.randint(1,5)

    for i in range(num_boxes):
        (n_rows,n_cols,n_channels) = np.shape(I)

        tl_row = np.random.randint(n_rows - box_height)
        tl_col = np.random.randint(n_cols - box_width)
        br_row = tl_row + box_height
        br_col = tl_col + box_width

        bounding_boxes.append([tl_row,tl_col,br_row,br_col])
    '''
    '''
    END YOUR CODE
    '''

    for i in range(len(bounding_boxes)):
        assert len(bounding_boxes[i]) == 4

    return bounding_boxes

# Size of the comparison image to use (smaller => faster)
samp_size = 7

# set the path to the basis data:
comp_path = 'C:\\Users\\madle\\Dropbox\\ee148\\RedLightBasis'
# get sorted list of files:
file_names = sorted(os.listdir(comp_path))
# remove any non-JPEG files:
file_names = [f for f in file_names if '.jpg' in f]
comp = np.zeros((len(file_names),samp_size,samp_size,3))

# Open and resize all the basis images
for i in range(len(file_names)):
    # read image using PIL:
    samp = Image.open(os.path.join(comp_path,file_names[i]))
    samp = np.asarray(samp)
    size = np.shape(samp)[0]
    samp = [[samp[int(size * r / samp_size)][int(size * c / samp_size)] for c in range(samp_size)] for r in range(samp_size)]
    # convert to numpy array:
    comp[i] = np.asarray(samp)

# Compute the average of all the basis images.
comp = np.average(comp,0)

# set the path to the downloaded data:
data_path = 'C:\\Users\\madle\\Dropbox\\ee148\\RedLights2011_Medium'

# set a path for saving predictions:
preds_path = '../data/hw01_preds'
os.makedirs(preds_path,exist_ok=True) # create directory if needed

# get sorted list of files:
file_names = sorted(os.listdir(data_path))

# remove any non-JPEG files:
file_names = [f for f in file_names if '.jpg' in f]

preds = {}
for i in range(len(file_names)):

    # read image using PIL:
    I = Image.open(os.path.join(data_path,file_names[i]))

    # convert to numpy array:
    I = np.asarray(I)

    preds[file_names[i]] = detect_red_light(I, comp)

    # save preds (overwrites any previous predictions!)
    with open(os.path.join(preds_path,'preds.json'),'w') as f:
        json.dump(preds,f)
