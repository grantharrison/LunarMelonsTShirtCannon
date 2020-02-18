import numpy as np
import cv2, time

# Takes two sequential images from the camera and saves them into numpy arrays
# \param wait_time the amount of time to wait between video captures
# \return an object containing the two numpy arrays, None on failure
def load_images(wait_time : int) -> tuple:
    video = None
    video = cv2.VideoCapture(0)
    for i in range(5):
        if not video.isOpened():
            video = cv2.VideoCapture(0)
            if(i == 4):
                return None
    frames = []
    for i in range(2):
        ret, frame = video.read()
        frames.append(frame)
        if(i == 0):
            time.sleep(wait_time)
    for frame in frames:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    video.release()
    return tuple(frames)

def main():
    load_images(5)

if __name__ == "__main__":
    main()