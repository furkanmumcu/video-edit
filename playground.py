import utils


# To be deleted

'''
# DENEMELER

print('here 1')

vidname = '02.avi'
info_result = vid_info(vidname)
print(info_result[1])

buffer = vid_to_frames(vidname)
print(buffer.shape)

#
#lowered_frame = lower_res_frame(buffer[100])
#cv2.imshow('lowered_frame', lowered_frame)
#cv2.waitKey(0)
#

print('here 2')

#frames_to_vid(buffer, 25, None, 'adv.mp4')


## VID FREEZE & LOWER RES
#print('here 3')
#vid_freeze(buffer, 50, 100)
#lower_res_frames(buffer, 150, 75)

#frames_to_vid(buffer, 25, None, '02_adv.avi')



##SPEED UP
#a = speed_up(buffer, 100, 100)
#print(a.shape)
#frames_to_vid(a, 25, None, 'aaa.avi')


##SLOW DOWN & SAVED
svd_slow = slow_down(buffer, 100, 100)
print(buffer.shape)
print(svd_slow.shape)

frames_to_vid(buffer, 25, None, 'buffer_slowed.avi')
frames_to_vid(svd_slow, 25, None, 'svd_slowed.avi')


##VID FREEZE & SAVED
#svd_freeze = vid_freeze(buffer, 100, 100)
#print(buffer.shape)
#print(svd_freeze.shape)

#frames_to_vid(buffer, 25, None, 'buffer_frozen.avi')
#frames_to_vid(svd_freeze, 25, None, 'svd_frozen.avi')


"""
from moviepy.editor import VideoFileClip
import moviepy.video.fx.all as vfx


out_loc = 'dummy_out.avi'
clip = VideoFileClip("02_adv.avi")
clip = clip.subclip(4, 6)
final = clip.fx(vfx.speedx, 5)
final.write_videofile(out_loc, codec="libx264")

"""


'''