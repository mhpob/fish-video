import numpy as np
import pandas as pd
# import tracktor as tr
import cv2
import sys
import scipy.signal
from scipy.optimize import linear_sum_assignment
from scipy.spatial.distance import cdist


# colours is a vector of BGR values which are used to identify individuals in the video
# t_id is termite id and is also used for individual identification
# number of elements in colours should be greater than n_inds (THIS IS NECESSARY FOR VISUALISATION ONLY)
# number of elements in t_id should be greater than n_inds (THIS IS NECESSARY TO GET INDIVIDUAL-SPECIFIC DATA)
n_inds = 8
t_id = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
colours = [(0,0,255),(0,255,255),(255,0,255),(255,255,255),(255,255,0),(255,0,0),(0,255,0),(0,0,0)]

# this is the block_size and offset used for adaptive thresholding (block_size should always be odd)
# these values are critical for tracking performance
block_size = 51
offset = 20

# the scaling parameter can be used to speed up tracking if video resolution is too high (use value 0-1)
scaling = 1.0

# minimum area and maximum area occupied by the animal in number of pixels
# this parameter is used to get rid of other objects in view that might be hard to threshold out but are differently sized
min_area = 500
max_area = 10000

# mot determines whether the tracker is being used in noisy conditions to track a single object or for multi-object
# using this will enable k-means clustering to force n_inds number of animals
mot = True

# in this example, we use a circular mask to ignore area outside the petri-dish
# mask_offset represents offset of circle from centre of the frame
mask_offset_x = -18
mask_offset_y = -5

# name of source video and paths
video = 'termite_video'
input_vidpath = 'c:/users/secor/desktop/tracktor/tracktor-master/videos/' + video + '.mp4'
output_vidpath = 'c:/users/secor/desktop/tracktor/tracktor-master/output/' + video + '_tracked2.mp4'
output_filepath = 'c:/users/secor/desktop/tracktor/tracktor-master/output/' + video + '_tracked2.csv'
codec = 'DIVX' # try other codecs if the default doesn't work ('DIVX', 'avc1', 'XVID') note: this list is non-exhaustive
