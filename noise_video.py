import numpy as np
import utils
import random


def create_adv_vid_slow_fast(vid_name, start_frame, duration):
	print('create_adv_vid')

	vid_frames = utils.vid_to_frames(vid_name)
	print(vid_frames.shape)

	duration_slow = int(duration / 3)
	duration_freeze = int(duration / 6)

	saved_slow = utils.slow_down(vid_frames, start_frame, duration_slow)
	saved_freeze = utils.vid_freeze(vid_frames, start_frame + duration_slow, duration_freeze)
	saved = np.concatenate((saved_slow, saved_freeze), axis=0)

	utils.speed_up(vid_frames, start_frame + duration_slow + duration_freeze, saved)

	print(vid_frames.shape)

	new_vid_name = 'avenue_dataset_slow_fast/' + vid_name
	utils.frames_to_vid(vid_frames, 25, None, new_vid_name)
	return vid_frames


def create_adv_vid_low_resolution(vid_name, start_frame, duration):
	vid_frames = utils.vid_to_frames(vid_name)
	utils.lower_res_frames(vid_frames, start_frame, duration)

	new_vid_name = 'avenue_dataset_low_resolution/' + vid_name
	utils.frames_to_vid(vid_frames, 25, None, new_vid_name)


def create_adv_vid_combine(vid_name, start_frame, duration):
	frames = create_adv_vid_slow_fast(vid_name, start_frame, duration)
	utils.lower_res_frames(frames, start_frame, duration)

	new_vid_name = 'avenue_dataset_combine/' + vid_name
	utils.frames_to_vid(frames, 25, None, new_vid_name)


def noise_avenue_dataset(duration_secs, vid_fps):
	duration_frames = int(duration_secs * 25)
	for i in range(19, 22, 1):
		if i < 10:
			vid_name = '0' + str(i) + '.avi'
		else:
			vid_name = str(i) + '.avi'

		vidinf = utils.vid_info(vid_name)

		if vidinf[0] >= duration_frames + vid_fps:
			secs = int(vidinf[0] / vid_fps)
			secs = secs - duration_secs + 1
			start_sec = random.randint(1, secs)
			start_frame = start_sec * vid_fps

			create_adv_vid_slow_fast(vid_name, start_frame, duration_frames)
			create_adv_vid_low_resolution(vid_name, start_frame, duration_frames)
			create_adv_vid_combine(vid_name, start_frame, duration_frames)


#noise_avenue_dataset(8, 25)


def create_adv_frames_slow_fast(vid_frames, start_frame, duration):
	duration_slow = int(duration / 3)
	duration_freeze = int(duration / 6)

	saved_slow = utils.slow_down(vid_frames, start_frame, duration_slow)
	saved_freeze = utils.vid_freeze(vid_frames, start_frame + duration_slow, duration_freeze)
	saved = np.concatenate((saved_slow, saved_freeze), axis=0)

	utils.speed_up(vid_frames, start_frame + duration_slow + duration_freeze, saved)
	print(vid_frames.shape)

	return vid_frames


def noise_shanghai_dataset():
	# 1) get original data folder names
	original_data_path = 'shanghaitech'
	folders = utils.list_subfolders(original_data_path)

	# 2) create folders for newly generated data
	adv_data_path_slow_fast = 'shanghaitech_slow_fast'
	utils.create_folders(folders, adv_data_path_slow_fast)

	adv_data_path_lower_resolution = 'shanghaitech_lower_resolution'
	utils.create_folders(folders, adv_data_path_lower_resolution)

	adv_data_path_combine = 'shanghaitech_combined'
	utils.create_folders(folders, adv_data_path_combine)

	# 3) attack for each video
	for i in range(0, len(folders), 1):
		# 3.1) low-res attack
		print('low-res attack for: ' + folders[i])
		frames_1 = utils.folder_to_frames(folders[i], original_data_path)
		utils.lower_res_frames(frames_1, 100, 100)  # start / duration
		utils.frames_to_jpg(frames_1, adv_data_path_lower_resolution + '/' + folders[i])

		# 3.2) slow-fast attack
		print('slow-fast attack for: ' + folders[i])
		frames_2 = utils.folder_to_frames(folders[i], original_data_path)
		create_adv_frames_slow_fast(frames_2, 100, 100)
		utils.frames_to_jpg(frames_2, adv_data_path_slow_fast + '/' + folders[i])

		# 3.3) combined attack
		print('combined attack attack for: ' + folders[i])
		create_adv_frames_slow_fast(frames_1, 100, 100)  # frames1 already has low quality, just apply slow-fast
		utils.frames_to_jpg(frames_1, adv_data_path_combine + '/' + folders[i])


noise_shanghai_dataset()