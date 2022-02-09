import cv2
import numpy as np


# input: video name
# output: numpy array that contains frames of video
def vid_to_frame(vidname):
	print('vid_to_frame')


# input: numpy array contains frames
# output: creates video


# input: video name
# output: video specs: frameCount, frameWidth, frameHeight, channel, fps, fourcc_string
def vid_info(vidname):
	cap = cv2.VideoCapture(vidname)
	frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
	frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
	frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
	channel = int(cap.get(cv2.CAP_PROP_CHANNEL))

	fps = int(cap.get(cv2.CAP_PROP_FPS))

	fourcc_hex = int(cap.get(cv2.CAP_PROP_FOURCC))
	fourcc_string = chr(fourcc_hex & 0xff) + chr((fourcc_hex >> 8) & 0xff) + chr((fourcc_hex >> 16) & 0xff) + chr(
		(fourcc_hex >> 24) & 0xff)
	cap.release()
	return frame_count, frame_width, frame_height, channel, fps, fourcc_string


print('here 1')

info_result = vid_info('big_buck_bunny_720p_5mb.mp4')
print(info_result)






# function to remove/replace frames to create frozen effect


# funtion to lower frame quality
