\# Takes two sequential images from the camera and saves them into numpy arrays
\n\# \param wait_time the amount of time to wait between video captures
\n\# \return an object containing the two numpy arrays, None on failure
def load_images(wait_time : int) -> tuple:
1. Create a video object using OpenCV’s VideoCapture() method.
2. Check if the operation was successful using the isOpened() method and retry on failure.
  a. If it fails a set number of times (say 5), return None.
3. For i in range(2):
  a. Create a frame object using the video object’s read() method.
  b. If i == 0 (first iteration), wait a set amount of time (random?) to allow for change to occur.
4. Convert the frames into grayscale using OpenCv’s cvtColor method.
5. Shutdown the camera using the video object’s release() method.
6. Return the two grayscale images as a tuple (Immutable => Good).
Additional Info:
Images may be written to file if desired, to allow for later review. Not necessary, but could be useful for testing purposes.
Additional error checking may be employed.

\# Determines the area of highest motion from a pair of images. 
\n\# \param imgs the list of images that are to be compared
\n\# \return the 2D bounding box containing the largest “movement” between images
def detect_motion(imgs):
1. Check that len(imgs) > 1.
2. Use Lucas-Kanade Optical Flow (somehow?) to determine apparent motion in images.
  a. Assumes that images were taken from a static camera and were taken in short succession.
3. Calculate the area with the densest Optical Flow from results of Step 2 as a 2D bounding box (set of four corners). (Could potentially calculate top 3 and randomly pick one).
  a. Max area will be set beforehand.
4. Return the bounding box calculated in Step 3 as a tuple.                     

\# Calculates distance between current position and target. Moves cannon into position.
\# \param current_position The current coordinates of the cannon.
\# \param target The bounding box of the target area.
\# \return True on success, False otherwise.
def move_to_target(current_position, target):
1. Randomly choose a location within the target bounding box and set it as the coordinates to move to.
2. Calculate manhattan (or euclidean? Needs to be tested later.) distance between the current position and the target coordinates.
3. Connect to hardware and move cannon into position needed to hit target.


Usage in Final Product:

1. T-shirt will be loaded into the cannon and air tank will be pressurized.
2. Pictures of the crowd will be captured using load_images().
3. The image array generated in step 2 will be sent to detect_motion() in order to obtain the bounding box coordinates for the most motion in the crowd.
4. Next the current_position of the camera will be obtained and sent along with the target’s position (bounding box found in step 3) to move_to_target() in order to move the cannon into position.
5. Finally, once the cannon is moved in position, the user will push the fire button, launching the pre-loaded t-shirt into the crowd.
