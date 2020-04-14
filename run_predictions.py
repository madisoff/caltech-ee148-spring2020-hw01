import os
import numpy as np
import json
from PIL import Image
from pathlib import Path
import time

def detect_red_light(I, number, comp):
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
    tic = time.perf_counter()
    min_frame = 8
    max_frame = 23
    thresh = 0.91
    y_thresh = 0.55

    I_x = np.shape(I)[1]                # image pixel width
    I_y = np.shape(I)[0]                # image pixel height
    #I = I / np.linalg.norm(I)           # normalize the image

    comp_x = np.shape(comp)[1]           # comparison image size
    comp_y = np.shape(comp)[0]
    used_boxes = np.zeros((I_y,I_x))
    print("image "+str(number))
    for i in range(max_frame,min_frame-1,-2):
        print("frame size: " + str(i))
        for j in range(0,I_x - i,2):
            for k in range(0,I_y - i - (int(I_y * y_thresh)),2):
                test_box = I[k:(k+i),j:(j+i)]     #single out the box to test
                test_box = [[test_box[int(i * r / comp_y)][int(i * c / comp_x)] for c in range(comp_x)] for r in range(comp_y)]
                test_box = np.asarray(test_box)
                test_box_1d = test_box.flatten()
                comp_1d = comp.flatten()
                corr = np.inner(test_box_1d/np.linalg.norm(test_box_1d),comp_1d/np.linalg.norm(comp_1d))
                if (corr > thresh) and (corr > used_boxes[k,j]):
                    bounding_boxes.append([k,j,k+i,j+i])
                    used_boxes[k:(k+i),j:(j+i)] = corr
                    print('box')
    toc = time.perf_counter()
    print("time: "+str(toc-tic))

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
samp_size = 7

# set the path to the downloaded data:
comp_path = 'C:\\Users\\madle\\Dropbox\\ee148\\RedLightBasis'
# get sorted list of files:
file_names = sorted(os.listdir(comp_path))
# remove any non-JPEG files:
file_names = [f for f in file_names if '.jpg' in f]
comp = np.zeros((len(file_names),samp_size,samp_size,3))
for i in range(len(file_names)):
    # read image using PIL:
    samp = Image.open(os.path.join(comp_path,file_names[i]))
    samp = np.asarray(samp)
    size = np.shape(samp)[0]
    samp = [[samp[int(size * r / samp_size)][int(size * c / samp_size)] for c in range(samp_size)] for r in range(samp_size)]
    # convert to numpy array:
    comp[i] = np.asarray(samp)

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

    preds[file_names[i]] = detect_red_light(I, i, comp)

    # save preds (overwrites any previous predictions!)
    with open(os.path.join(preds_path,'preds.json'),'w') as f:
        json.dump(preds,f)
