import os
import cv2
import numpy
import numpy as np
from PIL import Image
import copy
import time


# input: video name
# output: numpy array that contains frames of video
def vid_to_frames(vid_name):
	print('func: vid_to_frame')
	cap = cv2.VideoCapture(vid_name)
	vid_inf = vid_info(vid_name)

	vid_frames = np.empty((vid_inf[0], vid_inf[1], vid_inf[2], 3), np.dtype('uint8'))
	fc = 0
	ret = True
	while fc < vid_inf[0] and ret:
		ret, vid_frames[fc] = cap.read()
		fc += 1

	cap.release()
	return vid_frames


# input: numpy array contains frames
# output: creates video
def frames_to_vid(frames_array, fps, fourcc, vid_name):
	print('func: frames_to_vid')
	# fourcc = cv2.VideoWriter_fourcc(*fourcc_string) # FourCC is a 4-byte code used to specify the video codec.
	# fourcc = cv2.VideoWriter_fourcc(*'MP4V')  # FourCC is a 4-byte code used to specify the video codec.
	fourcc = cv2.VideoWriter_fourcc(*'XVID')  # FourCC is a 4-byte code used to specify the video codec.
	video = cv2.VideoWriter(vid_name, fourcc, float(fps), (frames_array.shape[2], frames_array.shape[1]))

	for frame_count in range(frames_array.shape[0]):
		video.write(frames_array[frame_count])
	print('adv vid created')


# input: video name
# output: video specs: frameCount, frameWidth, frameHeight, channel, fps, fourcc_string
def vid_info(vidname):
	cap = cv2.VideoCapture(vidname)
	frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
	frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
	frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
	fps = int(cap.get(cv2.CAP_PROP_FPS))

	fourcc_hex = int(cap.get(cv2.CAP_PROP_FOURCC))
	fourcc = chr(fourcc_hex & 0xff) + chr((fourcc_hex >> 8) & 0xff) + chr((fourcc_hex >> 16) & 0xff) + chr(
		(fourcc_hex >> 24) & 0xff)
	cap.release()
	return frame_count, frame_height, frame_width, fps, fourcc


# function to remove/replace frames to create frozen effect
def vid_freeze(frames_array, frame_to_start, duration):
	print('func: vid_freeze')
	saved = []
	saved_copy = copy.deepcopy(frames_array)

	for i in range(duration):
		saved.append(saved_copy[frame_to_start + i])

	for i in range(duration):
		frames_array[frame_to_start+i] = frames_array[frame_to_start]

	saved_frz = numpy.asarray(saved, dtype=np.uint8)
	return saved_frz


# funtion to lower frame resolution
def lower_res_frame(frame):
	print('func: lower_frame_res')

	# create jpg file from frame array
	cv2.imwrite("temp_img/frame.jpg", frame)

	# lower the quality of jpg file
	image_file = Image.open("temp_img/frame.jpg")
	image_file.save("temp_img/frame_lower.jpg", quality=10)

	# lowered jpg -> np array
	frame_lower = cv2.imread('temp_img/frame_lower.jpg')

	#delete files
	image_file.close()
	os.remove("temp_img/frame.jpg")
	os.remove("temp_img/frame_lower.jpg")

	return frame_lower


def lower_res_frames(frames_array, frame_to_start, duration):
	print('func: lower_res_frames')
	for i in range(duration):
		temp = lower_res_frame(frames_array[frame_to_start + i])
		frames_array[frame_to_start + i] = temp


def speed_up_delete(frames_array, frame_to_start, duration):
	print('func: speed_up')
	delete_index = []
	for i in range(frame_to_start, frame_to_start + duration, 2):
		delete_index.append(i)

	#print(len(delete_index))
	new_frames_array = np.delete(frames_array, delete_index, axis=0)
	return new_frames_array


def speed_up(frames_array, frame_to_start, saved):
	print('func: speed_up_old')

	frames_copy = copy.deepcopy(frames_array)

	saved_fast = []

	for i in range(saved.shape[0]):
		saved_fast.append(frames_copy[frame_to_start + i])

	saved_fast = numpy.asarray(saved_fast, dtype=np.uint8)  # 125
	total_saved = np.concatenate((saved, saved_fast), axis=0)  # 250
	total_saved = speed_up_delete(total_saved, 0, total_saved.shape[0])

	for i in range(total_saved.shape[0]):
		frames_array[frame_to_start + i] = total_saved[i]

	return frames_array


def slow_down(frames_array, frame_to_start, duration):
	print('func: slow_down')

	saved = []
	saved_copy = copy.deepcopy(frames_array)

	cond = True
	end = frame_to_start + duration

	while cond:
		saved.append(saved_copy[frame_to_start + 1])
		frames_array[frame_to_start + 1] = frames_array[frame_to_start]

		saved.append(saved_copy[frame_to_start + 2])
		frames_array[frame_to_start + 2] = frames_array[frame_to_start]

		saved.append(saved_copy[frame_to_start + 3])
		frames_array[frame_to_start + 3] = frames_array[frame_to_start]

		frame_to_start = frame_to_start + 4

		if end <= frame_to_start:
			cond = False

	saved = numpy.asarray(saved, dtype=np.uint8)
	return saved
