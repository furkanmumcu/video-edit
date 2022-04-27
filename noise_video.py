import utils
import random


# assumes you have 21 avenue dataset testing videos in project directory
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
		utils.create_adv_vid_low_resolution(vid_name, start_frame, active_duration)
		utils.create_adv_vid_combine(vid_name, start_frame, active_duration)  # this will generate slow/fast too

	print('videos created. now creating frame jpgs.')
	utils.avenue_to_frames()
	print('done.')


# assumes you have shanghai dataset(in a folder) in your project directory
def noise_shanghai_dataset(duration):
	print('noise_shanghai_dataset')
	# 1) get original data folder names
	original_data_path = '_shanghaitech'  # name of the shanghai dataset folder
	folders = utils.list_subfolders(original_data_path)

	# 2) create folders for newly generated data
	adv_data_path_slow_fast = 'shanghaitech_slow_fast'
	utils.create_subfolders(folders, adv_data_path_slow_fast)

	adv_data_path_lower_resolution = 'shanghaitech_lower_resolution'
	utils.create_subfolders(folders, adv_data_path_lower_resolution)

	adv_data_path_combine = 'shanghaitech_combined'
	utils.create_subfolders(folders, adv_data_path_combine)

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
		utils.create_adv_frames_slow_fast(frames_2, start_frame, active_duration)
		utils.frames_to_jpg(frames_2, adv_data_path_slow_fast + '/' + folders[i])

		# 3.3) combined attack
		print('combined attack attack for: ' + folders[i])
		utils.create_adv_frames_slow_fast(frames_1, start_frame, active_duration)  # frames1 already has low quality, just apply slow-fast
		utils.frames_to_jpg(frames_1, adv_data_path_combine + '/' + folders[i])


# assumes you have ucf-crime dataset in "source" folder located in project directory
def noise_ucf_crime(duration, source, dest):
	print('noise_ucf_crime')

	# 1) get original data folder names
	folders = utils.list_subfolders(source)

	# 2) create folders for newly generated data
	utils.create_subfolders(folders, dest)

	for folder in folders:
		video_names = utils.list_files(source + '/' + folder)
		for video_name in video_names:
			vid_frames1 = utils.vid_to_frames(source + '/' + folder + '/' + video_name)
			# vid_frames2 = utils.vid_to_frames(source + '/' + folder + '/' + video_name)

			if vid_frames1.shape[0] < duration:
				active_duration = vid_frames1.shape[0]
			else:
				active_duration = duration

			start_frame = random.randint(0, vid_frames1.shape[0] - active_duration)

			# 3) combined attack
			utils.lower_res_frames(vid_frames1, start_frame, active_duration)  # start / duration

			utils.create_adv_frames_slow_fast(vid_frames1, start_frame, active_duration)  # frames1 already has low quality, just apply slow-fast

			adv_video_name = dest + '/' + folder + '/' + video_name
			utils.frames_to_vid(vid_frames1, 25, None, adv_video_name)

	print('noise_ucf_crime done!')

