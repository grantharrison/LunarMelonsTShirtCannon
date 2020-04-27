import cv2
import numpy as np
import load

# Adapted from https://nanonets.com/blog/optical-flow/#sparse-of

# Determines the area of highest motion from a pair of images.
# \param imgs the list of images that are to be compared
# \return (u, v) the pixel coordinates of the centroid of the area containing the largest "movement" between images
def detect_motion(imgs):
    if len(imgs) < 2:
        print("ERROR: Not enough images in input list.")
        return None
    
    feature_params = dict(maxCorners = 300, qualityLevel = 0.2, minDistance = 2, blockSize = 7)
    lk_params = dict(winSize = (15,15), maxLevel = 2, criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    color = (0, 255, 0)
    prev_gray = cv2.cvtColor(imgs[0], cv2.COLOR_BGR2GRAY)
    prev = cv2.goodFeaturesToTrack(prev_gray, mask=None, **feature_params)
    mask = np.zeros_like(imgs[0])
    
    for i in range(1, len(imgs)):
        frame = imgs[i]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        _next, status, error = cv2.calcOpticalFlowPyrLK(prev_gray, gray, prev, None, **lk_params)

        good_old = prev[status == 1]
        good_new = _next[status == 1]

        for i, (new,old) in enumerate(zip(good_new, good_old)):
            a, b = new.ravel()
            c, d = old.ravel()
            mask = cv2.line(mask, (a,b), (c,d), color, 2)
            frame = cv2.circle(frame, (a,b), 3, color, -1)
        output = cv2.add(frame, mask)                           # Add mask of lines to original image

        prev_gray = gray.copy()
        prev = good_new.reshape(-1, 1, 2)

        cv2.imshow("Sparse optical flow", output)
        cv2.waitKey()
        cv2.destroyAllWindows()

frames = load.load_images("../tests/test_videos/Mufasa.mp4", 10, 10)
# cv2.imshow("Frame 1", frames[1])
# cv2.waitKey()
# cv2.destroyAllWindows()
detect_motion(frames)