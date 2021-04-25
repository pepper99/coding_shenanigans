#@title Bad apple

fps = 30 #@param {type:"integer"} 
width = 80 #@param {type:"integer"}
video_file = 'badapple.mp4' #@param {type:"string"}
frames_folder = 'badapple_frames' #@param {type:"string"}

# thanks to https://github.com/haveyouwantto/python-bad-apple and https://github.com/reeesga/donut

delay =  1/fps

# !pip install youtube_dl

import sys, os, cv2
import colorama
from PIL import Image
from time import sleep
from IPython.display import clear_output

CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]


def process(image, width=100):
    w, h = image.size
    ratio = h/w
    height = int(width * ratio)
    # print(width, height)
    image = image.resize((width, height)) # resize
    image = image.convert("L") # grayscale

    pixels = image.getdata()
    chars = "".join([CHARS[pixel//25] for pixel in pixels]) # pixels to asciis
    return(chars)

colorama.init()

if not (os.path.exists(frames_folder) or os.path.exists('badapple_saved.txt')):
  vidcap = cv2.VideoCapture(video_file)
  success,image = vidcap.read()
  count = 0
  os.makedirs(frames_folder)
  print("Extracting frames..")
  while success:
    cv2.imwrite(frames_folder + "/%d.jpg" % count, image) # save frame as JPEG file      
    success,image = vidcap.read()
    count += 1
else:
  count = len([f for f in os.listdir(frames_folder)])

if not os.path.exists('badapple_saved.txt'):
  print("frames =", count)
  print('Processing...')
  frames = []
  for itt in range(count):
    # open image
    try:
      s = frames_folder + '/' + str(itt) + '.jpg'
      image = Image.open(s)
    except:
      print("Invalid path")
      sys.exit()
        
    asciis = process(image, width) # image to asciis

    frame = "\n".join([asciis[index:(index + width)] for index in range(0, len(asciis), width)]) # adding new line characters
    frames.append(frame) # frame to list

  # save result to file
  with open("badapple_saved.txt", "w") as f:
    for frame in frames:
      f.write(str(frame) + "XXX")

print('\x1b[2J') # save home cursor position
with open("badapple_saved.txt", "r") as f: # read the frames from the memory file
  frames = f.read().split("XXX")
  for frame in frames:
    print(frame)
    print('\x1b[H') # return cursor to home position
    sleep(delay)