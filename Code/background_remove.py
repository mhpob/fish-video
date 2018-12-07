
import numpy as np
import cv2 as cv
cap = cv.VideoCapture('p:/obrien/biotelemetry/darpa/fish-video/bsb_vid.mp4')
fgbg = cv.createBackgroundSubtractorMOG2(detectShadows = False)

fourcc = cv.VideoWriter_fourcc(*'mp4v')
output_framesize = (int(cap.read()[1].shape[1] ),
  int(cap.read()[1].shape[0] ))

out = cv.VideoWriter(filename = 'p:/obrien/biotelemetry/darpa/fish-video/tshort_bg.mp4',
  fourcc = fourcc, fps = 24.0, frameSize = output_framesize, isColor = False)

while(1):
  ret, frame = cap.read()
  if ret == True:
    fgmask = fgbg.apply(frame)
    # out.write(fgmask)
    cv.imshow('frame',fgmask)

    k = cv.waitKey(30) & 0xff
    if k == 27:
      break


cap.release()
cv.destroyAllWindows()


