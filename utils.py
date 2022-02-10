import cv2
import numpy as np


# input: video name
# output: numpy array that contains frames of video
def vid_to_frames(vidname):
	print('func: vid_to_frame')
	cap = cv2.VideoCapture('big_buck_bunny_720p_5mb.mp4')
	vid_inf = vid_info(vidname)

	buf = np.empty((vid_inf[0], vid_inf[1], vid_inf[2], 3), np.dtype('uint8'))
	fc = 0
	ret = True
	while fc < vid_inf[0] and ret:
		ret, buf[fc] = cap.read()
		fc += 1

	cap.release()
	return buf


# input: numpy array contains frames
# output: creates video
def frames_to_vid():
	print('frames_to_vid')


# input: video name
# output: video specs: frameCount, frameWidth, frameHeight, channel, fps, fourcc_string
def vid_info(vidname):
	cap = cv2.VideoCapture(vidname)
	frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
	frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
	frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
	fps = int(cap.get(cv2.CAP_PROP_FPS))

	fourcc_hex = int(cap.get(cv2.CAP_PROP_FOURCC))
	fourcc_string = chr(fourcc_hex & 0xff) + chr((fourcc_hex >> 8) & 0xff) + chr((fourcc_hex >> 16) & 0xff) + chr(
		(fourcc_hex >> 24) & 0xff)
	cap.release()
	return frame_count, frame_height, frame_width, fps, fourcc_string


print('here 1')

vid_name = 'big_buck_bunny_720p_5mb.mp4'
info_result = vid_info(vid_name)
print(info_result[1])

buffer = vid_to_frames(vid_name)
print(buffer.shape)
print(buffer[1])



# function to remove/replace frames to create frozen effect


# funtion to lower frame quality
