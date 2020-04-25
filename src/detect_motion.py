import cv2

# Determines the area of highest motion from a pair of images.
# \param imgs the list of images that are to be compared
# \return (u, v) the pixel coordinates of the centroid of the area containing the largest "movement" between images
def detect_motion(imgs):
    if len(imgs) < 1:
        print("ERROR: Not enough images in input list.")
        return None
    