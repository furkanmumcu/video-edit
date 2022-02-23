import utils
import cv2


def vid_to_jpg(vid_name):
	vid_name_ext = vid_name + '.avi'
	vid_frames = utils.vid_to_frames(vid_name_ext)

	digits = len(str(vid_frames.shape[0]))
	for i in range(vid_frames.shape[0]):
		frame_index_str = '0' * (digits - len(str(i))) + str(i)

		path = vid_name + '/'
		frame_name = frame_index_str + ".jpg"
		cv2.imwrite(path + frame_name, vid_frames[i])


def vids_to_jpg():
	for i in range(1, 22, 1):
		if i < 10:
			vid_to_jpg('0' + str(i))
		else:
			vid_to_jpg(str(i))


#vidname = '10'
#vid_to_jpg(vidname)

vids_to_jpg()