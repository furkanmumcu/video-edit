import numpy as np
import utils
import random


def create_adv_vid_slow_fast(vid_name, start_frame, duration):
	print('create_adv_vid_slow_fast')

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


# duration: slow/fast & freeze
# fast part is fixed amount of time
def create_adv_vid_fixed_fast(vid_name, start_frame, duration):
	vid_frames = utils.vid_to_frames(vid_name)
	print(vid_frames.shape)

	duration_slow = int(duration / 4)
	duration_freeze = int((duration / 4) * 3)

	saved_slow = utils.slow_down(vid_frames, start_frame, duration_slow)
	saved_freeze = utils.vid_freeze(vid_frames, start_frame + duration_slow, duration_freeze)
	saved = np.concatenate((saved_slow, saved_freeze), axis=0)
	print('saved shape:' + str(saved.shape))

	# new speed method
	utils.speed_up_second(vid_frames, start_frame + duration_slow + duration_freeze, saved)

	print(vid_frames.shape)
	new_vid_name = 'fixed_fast/' + vid_name
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
	utils.create_avenue_video_folders()
	duration_frames = int(duration_secs * vid_fps)
	for i in range(1, 22, 1):
		if i < 10:
			vid_name = '0' + str(i) + '.avi'
		else:
			vid_name = str(i) + '.avi'

		vidinf = utils.vid_info(vid_name)

		if vidinf[0] < duration_frames:
			active_duration = vidinf[0]
		else:
			active_duration = duration_frames

		start_frame = random.randint(0, vidinf[0] - active_duration)
		# create_adv_vid_slow_fast(vid_name, start_frame, duration_frames)
		# create_adv_vid_fixed_fast(vid_name, start_frame, duration_frames)
		create_adv_vid_low_resolution(vid_name, start_frame, active_duration)
		create_adv_vid_combine(vid_name, start_frame, active_duration)  # this will generate slow/fast too

	print('videos created. now creating frame jpgs.')
	utils.avenue_to_frames()
	print('done.')


# Shanghai

def create_adv_frames_slow_fast(vid_frames, start_frame, duration):
	duration_slow = int(duration / 3)
	duration_freeze = int(duration / 6)

	saved_slow = utils.slow_down(vid_frames, start_frame, duration_slow)
	saved_freeze = utils.vid_freeze(vid_frames, start_frame + duration_slow, duration_freeze)
	saved = np.concatenate((saved_slow, saved_freeze), axis=0)

	utils.speed_up(vid_frames, start_frame + duration_slow + duration_freeze, saved)
	print(vid_frames.shape)

	return vid_frames


def create_adv_frames_fixed_fast(vid_frames, start_frame, duration):
	duration_slow = int(duration / 4)
	duration_freeze = int((duration / 4) * 3)

	saved_slow = utils.slow_down(vid_frames, start_frame, duration_slow)
	saved_freeze = utils.vid_freeze(vid_frames, start_frame + duration_slow, duration_freeze)
	saved = np.concatenate((saved_slow, saved_freeze), axis=0)

	# new speed method
	utils.speed_up_second(vid_frames, start_frame + duration_slow + duration_freeze, saved)

	return vid_frames


def noise_shanghai_dataset(duration):
	print('noise_shanghai_dataset')
	# 1) get original data folder names
	original_data_path = '_shanghaitech'
	folders = utils.list_subfolders(original_data_path)

	# 2) create folders for newly generated data
	adv_data_path_slow_fast = 'shanghaitech_slow_fast'
	utils.create_subfolders(folders, adv_data_path_slow_fast)

	adv_data_path_lower_resolution = 'shanghaitech_lower_resolution'
	utils.create_subfolders(folders, adv_data_path_lower_resolution)

	adv_data_path_combine = 'shanghaitech_combined'
	utils.create_subfolders(folders, adv_data_path_combine)

	unchanged = []

	# 3) attack for each video
	for i in range(0, len(folders), 1):
		frames_1 = utils.folder_to_frames(folders[i], original_data_path)
		frames_2 = utils.folder_to_frames(folders[i], original_data_path)

		if frames_1.shape[0] < duration:
			active_duration = frames_1.shape[0]
		else:
			active_duration = duration

		start_frame = random.randint(0, frames_1.shape[0] - active_duration)

		# 3.1) low-res attack
		print('low-res attack for: ' + folders[i])
		utils.lower_res_frames(frames_1, start_frame, active_duration)  # start / duration
		utils.frames_to_jpg(frames_1, adv_data_path_lower_resolution + '/' + folders[i])

		# 3.2) slow-fast attack
		print('slow-fast attack for: ' + folders[i])
		#create_adv_frames_slow_fast(frames_2, start_frame, active_duration)
		create_adv_frames_slow_fast(frames_2, start_frame, active_duration)
		utils.frames_to_jpg(frames_2, adv_data_path_slow_fast + '/' + folders[i])

		# 3.3) combined attack
		print('combined attack attack for: ' + folders[i])
		create_adv_frames_slow_fast(frames_1, start_frame, active_duration)  # frames1 already has low quality, just apply slow-fast
		utils.frames_to_jpg(frames_1, adv_data_path_combine + '/' + folders[i])


#noise_shanghai_dataset(300)