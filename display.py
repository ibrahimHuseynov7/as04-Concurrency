
import cv2

QUIT_KEYS = (27, ord("q"))   # Escape and 'q' keys
NO_KEY = 255

#An OpenCV window that can be refreshed while our image is processed
class ImageWindow:
    

    def __init__(self, title):
        self.title = title
        self.closed = False
        self._has_been_visible = False

        cv2.namedWindow(self.title, cv2.WINDOW_AUTOSIZE)
    # It is our function to draw the current state of image. Returns False if the user closed the window
    def show(self, image):
       
        if self.closed:
            return False
        cv2.imshow(self.title, image)
        return self._poll(wait_ms=1)
 # Show the final image until any key is pressed or the window is closed.
    def wait_for_close(self, image):
        
        if not self.show(image):
            return
        while self._poll(wait_ms=100, any_key_quits=True):
            pass

    def close(self):
        cv2.destroyAllWindows()
        cv2.waitKey(1)  # lets the GUI backend actually remove the window
# Process GUI event, I have used very naive way to detect quit keys and the window's close button.
    def _poll(self, wait_ms, any_key_quits=False):
       
        key = cv2.waitKey(wait_ms) & 0xFF
        if key in QUIT_KEYS or (any_key_quits and key != NO_KEY):
            self.closed = True
        elif self._is_visible():
            self._has_been_visible = True
        elif self._has_been_visible:
            self.closed = True
        return not self.closed

    def _is_visible(self):
        try:
            return cv2.getWindowProperty(self.title, cv2.WND_PROP_VISIBLE) >= 1
        except cv2.error:
            return False
