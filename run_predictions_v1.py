import os
import numpy as np
import json
from PIL import Image
from pathlib import Path

def isRed(rgb):
    red = int(rgb[0])
    blue = int(rgb[1])
    green = int(rgb[2])
    if (red > 245) and (green > 100) and (blue > 100):
        return True
    elif (red > 200) and (red - blue > 95):
        return True
    elif (red - blue > 75) and (red > 140):
        if (green > 40) and (green < 120):
            if (blue > 20) and (blue < 90):
                return True
    else:
        return False

def detect_red_light(I):
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
    min_frame = 3
    max_frame = 10
    I_x = np.shape(I)[0]
    I_y = np.shape(I)[1]
    red_arr = np.zeros((I_x, I_y))

    for i in range(I_x):
        for j in range(I_y):
            red_arr[i,j] = isRed(I[i,j])

    for k in range(max_frame, min_frame - 1, -1):
        buff = int(((np.sqrt(2) - 1) / 2) * k)
        for i in range(buff, I_x - k - buff):
            for j in range(buff, I_y - k - buff):
                if np.all(red_arr[i:i + k,j:j + k]):
                    red_arr[i:i + k,j:j + k] = False
                    bounding_boxes.append([i - buff,j - buff,i +k + buff,j + k + buff])

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

    preds[file_names[i]] = detect_red_light(I)

# save preds (overwrites any previous predictions!)
with open(os.path.join(preds_path,'preds.json'),'w') as f:
    json.dump(preds,f)

def isBlack(rgb):
    red = rgb[0]
    blue = rgb[1]
    green = rgb[2]
    if (red < 200) and (green < 200) and (blue < 200):
        if (abs(red - blue) < 30) and (abs(red - green) < 30) and (abs(blue - green) < 30):
            return true
    else:
        return false
