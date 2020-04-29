import cv2
import numpy as np
import load
import random
from matplotlib import pyplot as plt

# Adapted from https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_video/py_lucas_kanade/py_lucas_kanade.html

# Determines the area of highest motion from a pair of images.
# \return (u, v) the pixel coordinates of the centroid of the area containing the largest "movement" between images
def detect_motion():
    frames = load.load_images("../tests/test_videos/soccer_crowd.mp4", video_start=23, num_frames=30)
    # cv2.imshow("Frame 1", frames[1])
    # cv2.waitKey()
    # cv2.destroyAllWindows()

    flow_lines, image = sparse_optical_flow(frames)
    u, v = find_maximum(flow_lines)
    cv2.imwrite('motion_flow.png', flow_lines)

    # detect_motion(flow_lines)
    # rgb_frames = dense_optical_flow(frames)
    return (u, v)


# Runs optical flow over the list of input images
# \param imgs the list of sequential images that will be used to determine the optical flow vectors
# \return the mask of optical flow vectors and the last image with the optical flow vectors superimposed over it
def sparse_optical_flow(imgs):
    if len(imgs) < 2:
        print("ERROR: Not enough images in input list.")
        return None
    
    feature_params = dict(maxCorners = 300, qualityLevel = 0.03, minDistance = 3, blockSize = 10)
    lk_params = dict(winSize = (15,15), maxLevel = 2, criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255)]
    color = (255, 255, 255)
    prev_gray = cv2.cvtColor(imgs[0], cv2.COLOR_BGR2GRAY)                       # goodFeaturesToTrack requires a grayscale image, so we convert it
    prev = cv2.goodFeaturesToTrack(prev_gray, mask=None, **feature_params)
    mask = np.zeros_like(imgs[0])                                               # an empty mask is created to add motion lines to
    
    for i in range(1, len(imgs)):
        frame = imgs[i]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)                          # optical flow requires grayscale images also, so we convert this one too
        
        _next, status, error = cv2.calcOpticalFlowPyrLK(prev_gray, gray, prev, None, **lk_params)

        good_old = prev[status == 1]                                            # obtain the good pixels from the previous (old) image
        good_new = _next[status == 1]                                           # obtain the good pixels from the next (new) image

        for j, (new,old) in enumerate(zip(good_new, good_old)):
            a, b = new.ravel()                                                  # good pixel coordinates of new image
            c, d = old.ravel()                                                  # good pixel coordinates of old image
            # if i == 1:
            #     color = random.choice(color)
            mask = cv2.line(mask, (a,b), (c,d), color, 2)                       # draw the vector on the mask
            frame = cv2.circle(frame, (a,b), 3, color, -1)                      # circle the new point on the frame
        output = cv2.add(frame, mask)                                           # overlay mask of lines with original image

        prev_gray = gray.copy()                                                 # gray is now the previous image in the loop
        prev = good_new.reshape(-1, 1, 2)

        # cv2.imshow("Sparse optical flow", output)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
    return mask, output

def dense_optical_flow(imgs):
    frames = []
    frame1 = imgs[0]
    prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    hsv = np.zeros_like(frame1)
    hsv[...,1] = 255

    for i in range(1, len(imgs)):
        frame2 = imgs[i]
        _next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)

        flow = cv2.calcOpticalFlowFarneback(prvs,_next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

        mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
        hsv[...,0] = ang*180/np.pi/2
        hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
        rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

        frames.append(rgb)
        cv2.imshow('frame2',rgb)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
        elif k == ord('s'):
            cv2.imwrite('opticalfb.png',frame2)
            cv2.imwrite('opticalhsv.png',rgb)
        prvs = _next
    return frames

def find_maximum(flow_lines):
    gray = cv2.cvtColor(flow_lines, cv2.COLOR_BGR2GRAY)
    gray = (255-gray)

    params = cv2.SimpleBlobDetector_Params()
    params.filterByArea = True
    params.minArea = 150
    params.filterByConvexity = True
    params.minConvexity = 0.2
    params.filterByInertia = True
    params.minInertiaRatio = 0.05

    keypoints = cv2.SimpleBlobDetector_create(params).detect(gray)
    u, v = get_maximum(keypoints)
    
    image_key = cv2.drawKeypoints(flow_lines, keypoints, np.zeros((1,1)), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imwrite('max_circles.png', image_key)
    cv2.imshow("key points", image_key)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return (u, v)

def get_maximum(keypoints):
    maximum = -1
    max_coord = None
    for keypoint in keypoints:
        if keypoint.size > maximum:
            maximum = keypoint.size
            max_coord = keypoint.pt
    return max_coord

if __name__ == "__main__":
    detect_motion()