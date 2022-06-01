import numpy
import numpy as np
import os
import cv2
import utils
import noise_video as nv
import pickle
from os import walk
import ffmpegio

#vid_name = '02.avi'

#nv.create_adv_vid_slow_fast(vid_name, 250, 200)

#nv.create_adv_vid_low_resolution(vid_name, 250, 200)

#nv.create_adv_vid_combine(vid_name, 250, 200)


#nv.create_adv_vid_fixed_fast(vid_name, 200, 200)

#nv.noise_avenue_dataset(12, 25)
#nv.noise_shanghai_dataset(500)
#utils.create_shanghai_training_frames('videos', 'training_frames')

#utils.vid_to_jpg('a', 'bb', 'aa')


#vid_frames = utils.vid_to_frames(vid_name)
#utils.vid_freeze(vid_frames, 250, 200)
#utils.frames_to_vid(vid_frames, 25, None, '02freeze.avi')
#utils.frames_to_jpg(vid_frames, 'freeze_frames')

#utils.replicate_avenue_frames_twice()

#nv.noise_ucf_crime(300, 'ucf-crime', 'ucf-crime-adv')

#nv.noise_ucf_crime(100, 'deneme', 'deneme-adv')
#utils.list_video_durations('ucf-crime')

def recreate():
	for i in range(1, 22, 1):
		if i < 10:
			vid_name = '0' + str(i) + '.avi'
		else:
			vid_name = str(i) + '.avi'

		frames = utils.vid_to_frames(vid_name)
		new_name = 'deneme/' + vid_name
		utils.frames_to_vid(frames, 25, None, new_name)

	print('done.')


#recreate()
#utils.vids_to_jpg('a', 'b')


print(utils.vid_info('deneme/sub1/1.mp4'))
nv.noise_ucf_crime('ucf-crime', 'ucf-crime-adv2')
print(utils.vid_info('deneme-adv/sub1/1.mp4'))