import numpy as np
import pandas as pd
import tracktor as tr
import cv2
import sys
import scipy.signal
from matplotlib.pyplot import imshow
from scipy.optimize import linear_sum_assignment
from scipy.spatial.distance import cdist


def fishtrack(n_inds, ind_id, colors, block_size, offset, min_area, max_area,
  vid_name, vid_loc, scaling = 1.0, mot = True, codec = 'mp4v'):

  input_vidpath = vid_loc + vid_name + '.mp4'
  output_vidpath = vid_loc + vid_name + '_tracked.mp4'
  output_filepath = vid_loc + vid_name + '_tracked.csv'

  ## Open video
  cap = cv2.VideoCapture(input_vidpath)
  if cap.isOpened() == False:
    sys.exit('Video file cannot be read! Please check input_vidpath to ensure it is correctly pointing to the video file.')

  ## Video writer class to output video with contour and centroid of tracked
  ## object(s). Make sure the frame size matches size of array 'final'.
  fourcc = cv2.VideoWriter_fourcc(*codec)
  output_framesize = (int(cap.read()[1].shape[1] * scaling),
    int(cap.read()[1].shape[0] * scaling))
  out = cv2.VideoWriter(filename = output_vidpath, fourcc = fourcc, fps = 60.0,
    frameSize = output_framesize, isColor = True)

  ## Individual location(s) measured in the last and current step
  meas_last = list(np.zeros((n_inds, 2)))
  meas_now = list(np.zeros((n_inds, 2)))

  df = []
  last = 0

  while(True):
    try:
      # Capture frame-by-frame
      ret, frame = cap.read()

      this = cap.get(1)
      if ret == True:
         # Preprocess the image for background subtraction
          frame = cv2.resize(frame, None, fx = scaling, fy = scaling,
            interpolation = cv2.INTER_LINEAR)
          imgplot = imshow(frame)
          print(imgplot)

          thresh = tr.colour_to_thresh(frame, block_size, offset)

          final, contours, meas_last, meas_now = tr.detect_and_draw_contours(frame,
            thresh, meas_last, meas_now, min_area, max_area)
          if len(meas_now) != n_inds:
              contours, meas_now = tr.apply_k_means(contours, n_inds, meas_now)

          row_ind, col_ind = tr.hungarian_algorithm(meas_last, meas_now)
          final, meas_now, df = tr.reorder_and_draw(final, colors, n_inds,
            col_ind, meas_now, df, mot, this)

          # Create output dataframe
          for i in range(n_inds):
              df.append([this, meas_now[i][0], meas_now[i][1], ind_id[i]])

        # Display the resulting frame
          out.write(final)
          cv2.imshow('frame', final)
          if cv2.waitKey(1) == 27:
              break

      if last >= this:
          break

      last = this

    except ValueError as error:
      cap.release()
      out.release()
      cv2.destroyAllWindows()
      cv2.waitKey(1)
      print('Tracking broke. Try adjusting block_size, offset, min_area, ' +
      'and/or max_area')


  ## Write positions to file
  df = pd.DataFrame(np.matrix(df), columns = ['frame','pos_x','pos_y', 'id'])
  df.to_csv(output_filepath, sep=',')

  ## When everything done, release the capture
  cap.release()
  out.release()
  cv2.destroyAllWindows()
  cv2.waitKey(1)
