import numpy as np

import utils


def create_adv_vid(vid_name, start_frame, duration):
    print('create_adv_vid')

    #info = utils.vid_info(vid_name)

    vid_frames = utils.vid_to_frames(vid_name)
    print(vid_frames.shape)

    duration_slow = int(duration / 3)
    duration_freeze = int(duration / 6)
    duration_fast = int(duration / 2)

    saved_slow = utils.slow_down(vid_frames, start_frame, duration_slow)
    saved_freeze = utils.vid_freeze(vid_frames, start_frame + duration_slow, duration_freeze)
    saved = np.concatenate((saved_slow, saved_freeze), axis=0)

    utils.speed_up(vid_frames, start_frame + duration_slow + duration_freeze, duration_fast, saved)

    #new_vid = utils.speed_up_old(vid_frames, start_frame + duration_slow + duration_freeze, duration_fast)
    #print(new_vid.shape)




    #new_vid_name = 'create.avi'
    #utils.frames_to_vid(new_vid, 25, None, new_vid_name)




vidname = '02.avi'
create_adv_vid(vidname, 100, 300)
