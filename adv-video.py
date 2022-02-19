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


def noise_avenue_dataset(duration_secs, vid_frame):
	duration_frames = int(duration_secs * 25)
	for i in range(1, 22, 1):
		if i < 10:
			vid_name = '0' + str(i) + '.avi'
		else:
			vid_name = str(i) + '.avi'

		vidinf = utils.vid_info(vid_name)
		#print(vidinf[0])

		if vidinf[0] >= duration_frames + vid_frame:
			secs = int(vidinf[0] / vid_frame)
			secs = secs - duration_secs + 1
			start_sec = random.randint(1, secs)
			start_frame = start_sec * vid_frame
			#print(start_frame)

			create_adv_vid_slow_fast(vid_name, start_frame, duration_frames)
			create_adv_vid_low_resolution(vid_name, start_frame, duration_frames)
			create_adv_vid_combine(vid_name, start_frame, duration_frames)


noise_avenue_dataset(4, 25)