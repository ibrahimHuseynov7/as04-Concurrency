import cv2

FALLBACK_SCREEN_SIZE = (1280, 720) # I have put a fallback screen size in case the actual screen size cannot be determined
SCREEN_USAGE = 0.85
QUIT_KEYS = (27, ord("q"))   # Escape and 'q' keys
NO_KEY = 255

# It is function for getting the screen size using screeninfo library, if it fails, it returns the fallback screen size in our case
def get_screen_size():
    
    try:
        from screeninfo import get_monitors

        monitors = get_monitors()
        primary = next((m for m in monitors if getattr(m, "is_primary", False)),
                       monitors[0])
        return primary.width, primary.height
    except Exception:  
        return FALLBACK_SCREEN_SIZE
#An OpenCV window that can be refreshed while our image is processed
class ImageWindow:
   

    def __init__(self, title, image_shape):
        height, width = image_shape[:2]
        screen_width, screen_height = get_screen_size()

        self.title = title
        self.scale = min(1.0,
                         screen_width * SCREEN_USAGE / width,
                         screen_height * SCREEN_USAGE / height)
        self.display_size = (max(1, round(width * self.scale)),
                             max(1, round(height * self.scale)))
        self.closed = False
        self._has_been_visible = False

        cv2.namedWindow(self.title, cv2.WINDOW_AUTOSIZE)
    # It is our function to draw the current state of image. Returns False if the user closed the window
    def show(self, image):
        
        if self.closed:
            return False
        if self.scale < 1.0:
            frame = cv2.resize(image, self.display_size, interpolation=cv2.INTER_AREA)
        else:
            frame = image
        cv2.imshow(self.title, frame)
        return self._poll(wait_ms=1)
 # Show the final image until any key is pressed or the window is closed.
    def wait_for_close(self, image):
       
        if not self.show(image):
            return
        self._bring_to_front()
        while self._poll(wait_ms=100, any_key_quits=True):
            pass

    def close(self):
        cv2.destroyAllWindows()
        cv2.waitKey(1)  # lets the GUI backend actually remove the window
        for _ in range(5):
            cv2.waitKey(1)

    def _bring_to_front(self):
        try:
            cv2.setWindowProperty(self.title, cv2.WND_PROP_TOPMOST, 1)
        except (cv2.error, AttributeError):
            pass

# Process GUI event, I have used very naive way to detect quit keys
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