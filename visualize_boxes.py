import os
import json
from PIL import Image, ImageDraw
# set the path to the downloaded data:
data_path = 'C:\\Users\\madle\\Dropbox\\ee148\\RedLights2011_Medium'

# set a path for saving predictions:
preds_path = '../data/hw01_preds'
os.makedirs(preds_path,exist_ok=True) # create directory if needed

# get sorted list of files:
file_names = sorted(os.listdir(data_path))

# remove any non-JPEG files:
file_names = [f for f in file_names if '.jpg' in f]
# save preds (overwrites any previous predictions!)
with open(os.path.join(preds_path,'preds.json'),'r') as f:
    boxes = json.load(f)
print(file_names)
for i in range(len(file_names)):
    coords = boxes[file_names[i]]
    I = Image.open(os.path.join(data_path,file_names[i]))
    for j in range(len(coords)):
        draw = ImageDraw.Draw(I)
        x0 = coords[j][1]
        y0 = coords[j][0]
        x1 = coords[j][3]
        y1 = coords[j][2]
        draw.rectangle([x0,y0,x1,y1],outline="green")
    I.save(os.path.join(preds_path,file_names[i]))
