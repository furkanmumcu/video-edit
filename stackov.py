import cv2
import numpy as np

cap = cv2.VideoCapture('big_buck_bunny_720p_5mb.mp4')
frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
channel = int(cap.get(cv2.CAP_PROP_CHANNEL))

fps = int(cap.get(cv2.CAP_PROP_FPS))

fourcc_hex = int(cap.get(cv2.CAP_PROP_FOURCC))
fourcc_string = chr(fourcc_hex&0xff) + chr((fourcc_hex>>8)&0xff) + chr((fourcc_hex>>16)&0xff) + chr((fourcc_hex>>24)&0xff)

#duration = frameCount / fps

buf = np.empty((frameCount, frameHeight, frameWidth, 3), np.dtype('uint8'))

fc = 0
ret = True

while (fc < frameCount  and ret):
    ret, buf[fc] = cap.read()
    fc += 1

cap.release()

#cv2.namedWindow('frame 10')
#cv2.imshow('frame 10', buf[9])

#cv2.waitKey(0)


print('creating vid!')


#fourcc = cv2.VideoWriter_fourcc(*fourcc_string) # FourCC is a 4-byte code used to specify the video codec.
fourcc = cv2.VideoWriter_fourcc(*'MP4V') # FourCC is a 4-byte code used to specify the video codec.
video = cv2.VideoWriter('test.mp4', fourcc, float(fps), (frameWidth, frameHeight))

for frame_count in range(buf.shape[0]):
    video.write(buf[frame_count])