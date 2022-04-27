import os
import cv2
import numpy
import numpy as np
from PIL import Image
import copy
import time
from os import walk
from os import listdir
from os.path import isfile, join


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
# output: creates video #mp4v XVID
def frames_to_vid(frames_array, fps, fourcc, vid_name):
	print('func: frames_to_vid')
	# fourcc = cv2.VideoWriter_fourcc(*fourcc_string) # FourCC is a 4-byte code used to specify the video codec.
	# fourcc = cv2.VideoWriter_fourcc(*'MP4V')  # FourCC is a 4-byte code used to specify the video codec.
	fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # FourCC is a 4-byte code used to specify the video codec.
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
	image_file.save("temp_img/frame_lower.jpg", quality=5)

	# lowered jpg -> np array
	frame_lower = cv2.imread('temp_img/frame_lower.jpg')

	#delete files
	#os.remove("temp_img/frame.jpg")
	#os.remove("temp_img/frame_lower.jpg")
	safe_remove("temp_img/frame.jpg")
	safe_remove("temp_img/frame_lower.jpg")

	return frame_lower


def safe_remove(path, retries=3, sleep=0.1):
	for i in range(retries):
		try:
			os.remove(path)
		except WindowsError:
			if i == 2:
				Exception('removing still gives trouble')
			else:
				print('caught error while removing, going to sleep... ' + str(i))
			time.sleep(sleep)
		else:
			break


def lower_res_frames(frames_array, frame_to_start, duration):
	print('func: lower_res_frames')
	for i in range(duration):
		temp = lower_res_frame(frames_array[frame_to_start + i])
		frames_array[frame_to_start + i] = temp


def speed_up_delete(frames_array, frame_to_start, duration):
	print('func: speed_up_delete')
	delete_index = []
	for i in range(frame_to_start, frame_to_start + duration, 2):
		delete_index.append(i)

	#print(len(delete_index))
	new_frames_array = np.delete(frames_array, delete_index, axis=0)
	return new_frames_array


def speed_up(frames_array, frame_to_start, saved):
	print('func: speed_up')

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


def speed_up_second(frames_array, frame_to_start, saved):
	print('func: speed_up_second')
	frames_copy = copy.deepcopy(frames_array)
	saved_fast = []

	for i in range(25):
		saved_fast.append(frames_copy[frame_to_start + i])

	saved_fast = numpy.asarray(saved_fast, dtype=np.uint8)
	total_saved = np.concatenate((saved, saved_fast), axis=0)

	# pick 25 frames from total saved
	distilled = []
	distilled_rate = int(total_saved.shape[0] / 25)
	for i in range(25):
		distilled.append(total_saved[i * distilled_rate])

	distilled = numpy.asarray(distilled, dtype=np.uint8)

	for i in range(25):
		frames_array[frame_to_start + i] = distilled[i]

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


# saves the frames of a video as jpg
def vid_to_jpg(vid_name, source, dest):
	vid_name_ext = source + '/' + vid_name + '.avi'
	vid_frames = vid_to_frames(vid_name_ext)

	digits = len(str(vid_frames.shape[0]))
	for i in range(vid_frames.shape[0]):
		frame_index_str = '0' * (digits - len(str(i))) + str(i)

		path = dest + '/' + vid_name + '/'
		frame_name = frame_index_str + ".jpg"
		cv2.imwrite(path + frame_name, vid_frames[i])


# used for avenue dataset to jpg
def vids_to_jpg(source, dest):
	for i in range(1, 22, 1):
		if i < 10:
			vid_to_jpg('0' + str(i), source, dest)
		else:
			vid_to_jpg(str(i), source, dest)


def frames_to_jpg(vid_frames, path):
	digits = len(str(vid_frames.shape[0]))
	path = path + '/'
	for i in range(vid_frames.shape[0]):
		frame_index_str = '0' * (digits - len(str(i))) + str(i)

		frame_name = frame_index_str + ".jpg"
		cv2.imwrite(path + frame_name, vid_frames[i])


def folder_to_frames(folder_name, path):
	frames = []
	path = path + '/'
	folder_name = path + folder_name

	for filename in os.listdir(folder_name):
		img = cv2.imread(os.path.join(folder_name, filename))
		if img is not None:
			frames.append(img)

	frames = numpy.asarray(frames, dtype=np.uint8)
	return frames


def list_file_names(path):
	file_names = next(walk('videos'), (None, None, []))[2]
	return file_names


# list of subfolders of a directory
def list_subfolders(path):
	subfolders = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
	return subfolders


def create_subfolders(sub_folder_names, main_folder):
	#create main folder first
	if not os.path.exists(main_folder):
		os.makedirs(main_folder)

	#create folders
	for i in range(len(sub_folder_names)):
		subfolder_name = main_folder + '/' + sub_folder_names[i]
		if not os.path.exists(subfolder_name):
			os.makedirs(subfolder_name)


def list_files(path):
	arr = [f for f in listdir(path) if isfile(join(path, f))]
	return arr


def create_avenue_video_folders():
	slow_fast = 'avenue_dataset_slow_fast'
	combined = 'avenue_dataset_combine'
	low_res = 'avenue_dataset_low_resolution'
	if not os.path.exists(slow_fast):
		os.makedirs(slow_fast)
	if not os.path.exists(combined):
		os.makedirs(combined)
	if not os.path.exists(low_res):
		os.makedirs(low_res)


def create_avenue_frame_folders():
	slow_fast = 'frames_avenue_dataset_slow_fast'
	combined = 'frames_avenue_dataset_combine'
	low_res = 'frames_avenue_dataset_low_resolution'
	if not os.path.exists(slow_fast):
		os.makedirs(slow_fast)
	if not os.path.exists(combined):
		os.makedirs(combined)
	if not os.path.exists(low_res):
		os.makedirs(low_res)

	sub_folders = []
	for i in range(1, 22, 1):
		if i < 10:
			sub_folders.append('0' + str(i))
		else:
			sub_folders.append(str(i))

	create_subfolders(sub_folders, slow_fast)
	create_subfolders(sub_folders, combined)
	create_subfolders(sub_folders, low_res)


def avenue_to_frames():
	create_avenue_frame_folders()
	print('avenue_to_frames slow_fast')
	vids_to_jpg('avenue_dataset_slow_fast', 'frames_avenue_dataset_slow_fast')
	print('avenue_to_frames combine')
	vids_to_jpg('avenue_dataset_combine', 'frames_avenue_dataset_combine')
	print('avenue_to_frames low_resolution')
	vids_to_jpg('avenue_dataset_low_resolution', 'frames_avenue_dataset_low_resolution')


def create_shanghai_training_frames(source, dest):
	sub_folder_names = list_file_names(source)
	for i in range(len(sub_folder_names)):
		sub_folder_names[i] = sub_folder_names[i].split('.')[0]

	#create_subfolders(sub_folder_names, dest)

	for i in range(0, len(sub_folder_names), 1):
		print('current vid name: ' + sub_folder_names[i] + ' current index: ' + str(i))
		vid_to_jpg(sub_folder_names[i], source, dest)

	print('func: create_shanghai_training_frames done')


def replicate_frames(vid_name, dest):
	vid_frames = vid_to_frames(vid_name)
	print(vid_frames.shape)

	for i in range(0, vid_frames.shape[0], 10):
		if i < vid_frames.shape[0] - 10:
			vid_frames[i + 5] = vid_frames[i + 4]

	frames_to_jpg(vid_frames, dest)


def replicate_avenue_frames():
	for i in range(1, 22, 1):
		if i < 10:
			vid_name = '0' + str(i)
		else:
			vid_name = str(i)

		replicate_frames(vid_name + '.avi', vid_name)


def replicate_frames_twice(vid_name, dest):
	vid_frames = vid_to_frames(vid_name)
	print(vid_frames.shape)

	for i in range(0, vid_frames.shape[0], 10):
		if i < vid_frames.shape[0] - 10:
			vid_frames[i + 4] = vid_frames[i + 3]
			vid_frames[i + 9] = vid_frames[i + 8]

	frames_to_jpg(vid_frames, dest)


def replicate_avenue_frames_twice():
	for i in range(1, 22, 1):
		if i < 10:
			vid_name = '0' + str(i)
		else:
			vid_name = str(i)

		replicate_frames_twice(vid_name + '.avi', vid_name)


#**** NOISE UTILS
def create_adv_vid_slow_fast(vid_name, start_frame, duration):
	print('create_adv_vid_slow_fast')

	vid_frames = vid_to_frames(vid_name)
	print(vid_frames.shape)

	duration_slow = int(duration / 3)
	duration_freeze = int(duration / 6)

	saved_slow = slow_down(vid_frames, start_frame, duration_slow)
	saved_freeze = vid_freeze(vid_frames, start_frame + duration_slow, duration_freeze)
	saved = np.concatenate((saved_slow, saved_freeze), axis=0)

	speed_up(vid_frames, start_frame + duration_slow + duration_freeze, saved)

	print(vid_frames.shape)

	new_vid_name = 'avenue_dataset_slow_fast/' + vid_name
	frames_to_vid(vid_frames, 25, None, new_vid_name)
	return vid_frames


# duration: slow/fast & freeze
# fast part is fixed amount of time
def create_adv_vid_fixed_fast(vid_name, start_frame, duration):
	vid_frames = vid_to_frames(vid_name)
	print(vid_frames.shape)

	duration_slow = int(duration / 4)
	duration_freeze = int((duration / 4) * 3)

	saved_slow = slow_down(vid_frames, start_frame, duration_slow)
	saved_freeze = vid_freeze(vid_frames, start_frame + duration_slow, duration_freeze)
	saved = np.concatenate((saved_slow, saved_freeze), axis=0)
	print('saved shape:' + str(saved.shape))

	# new speed method
	speed_up_second(vid_frames, start_frame + duration_slow + duration_freeze, saved)

	print(vid_frames.shape)
	new_vid_name = 'fixed_fast/' + vid_name
	frames_to_vid(vid_frames, 25, None, new_vid_name)
	return vid_frames


def create_adv_vid_low_resolution(vid_name, start_frame, duration):
	vid_frames = vid_to_frames(vid_name)
	lower_res_frames(vid_frames, start_frame, duration)

	new_vid_name = 'avenue_dataset_low_resolution/' + vid_name
	frames_to_vid(vid_frames, 25, None, new_vid_name)


def create_adv_vid_combine(vid_name, start_frame, duration):
	frames = create_adv_vid_slow_fast(vid_name, start_frame, duration)
	lower_res_frames(frames, start_frame, duration)

	new_vid_name = 'avenue_dataset_combine/' + vid_name
	frames_to_vid(frames, 25, None, new_vid_name)


#used in shanghai & ucf-crime
def create_adv_frames_slow_fast(vid_frames, start_frame, duration):
	duration_slow = int(duration / 3)
	duration_freeze = int(duration / 6)

	saved_slow = slow_down(vid_frames, start_frame, duration_slow)
	saved_freeze = vid_freeze(vid_frames, start_frame + duration_slow, duration_freeze)
	saved = np.concatenate((saved_slow, saved_freeze), axis=0)

	speed_up(vid_frames, start_frame + duration_slow + duration_freeze, saved)
	print(vid_frames.shape)

	return vid_frames


def create_adv_frames_fixed_fast(vid_frames, start_frame, duration):
	duration_slow = int(duration / 4)
	duration_freeze = int((duration / 4) * 3)

	saved_slow = slow_down(vid_frames, start_frame, duration_slow)
	saved_freeze = vid_freeze(vid_frames, start_frame + duration_slow, duration_freeze)
	saved = np.concatenate((saved_slow, saved_freeze), axis=0)

	# new speed method
	speed_up_second(vid_frames, start_frame + duration_slow + duration_freeze, saved)

	return vid_frames