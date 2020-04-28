import numpy as np
import cv2, time

# Takes num_frames sequential images from a video and saves them into numpy arrays
# \param video_src the file path of the video file to load from
# \param video_start where the video should start in seconds
# \param num_frames the number of images to be loaded
# \param wait_time the amount of time to wait between video captures
# \return an object containing the two numpy arrays, None on failure
def load_images(video_src : str, video_start : float = 0, num_frames : int = 10, wait_time : int = 5) -> tuple:
    video = None
    video = cv2.VideoCapture(video_src)
    for i in range(5):
        if not video.isOpened():
            video = cv2.VideoCapture(video_src)
            if(i == 4):
                return None
    frames = []
    framespersec = video.get(cv2.CAP_PROP_FPS)

    for i in range(int(framespersec * video_start)):
        video.read()
    
    for i in range(num_frames):
        ret, frame = video.read()
        frames.append(frame)
    video.release()
    return frames

def main():
    frames = load_images("../tests/test_videos/Mufasa.mp4", video_start=12)
    cv2.imshow("Frame 0", frames[0])
    cv2.waitKey()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
