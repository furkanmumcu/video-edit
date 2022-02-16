import utils
import cv2


def vid_to_jpg(vid_name):
	vid_name_ext = vid_name + '.avi'
	vid_frames = utils.vid_to_frames(vid_name_ext)

	for i in range(vid_frames.shape[0]):
		if i < 10:
			frame_index_str = '0' + str(i)
		else:
			frame_index_str = str(i)

		path = vid_name + '/'
		frame_name = frame_index_str + ".jpg"
		cv2.imwrite(path + frame_name, vid_frames[i])


def vids_to_jpg():
	for i in range(1, 22, 1):
		if i < 10:
			vid_to_jpg('0' + str(i))
		else:
			vid_to_jpg(str(i))


#vidname = '01'
#vid_to_jpg(vidname)

vids_to_jpg()