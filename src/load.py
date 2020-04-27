import numpy as np
import cv2, time

# Takes n sequential images from a video and saves them into numpy arrays
# \param video_src the file path of the video file to load from
# \param wait_time the amount of time to wait between video captures
# \return an object containing the two numpy arrays, None on failure
def load_images(video_src : str, n : int, wait_time : int) -> tuple:
    video = None
    video = cv2.VideoCapture(video_src)
    for i in range(5):
        if not video.isOpened():
            video = cv2.VideoCapture(video_src)
            if(i == 4):
                return None
    frames = []
    
    framespersec = 24     # video framerate
    videostart = 20       # want video capture to start at 20 seconds
    for i in range(framespersec * videostart):    # should be 288
        video.read()
    
    for i in range(n):
        ret, frame = video.read()
        frames.append(frame)
    video.release()
    return frames

def main():
    frames = load_images("../tests/test_videos/Mufasa.mp4", 10, 5)
    cv2.imshow("Frame 0", frames[0])
    cv2.waitKey()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
