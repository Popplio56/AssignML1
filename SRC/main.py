import os
import uuid
import cv2
import time
import json

# --- 1. THE BLUEPRINT (The Class) ---
class CaptureImages:
    def __init__(self, base_path, classes):
        self.base_path = base_path
        self.classes = classes
        self.cap = cv2.VideoCapture(0)
        
        if not os.path.exists(base_path):
            os.makedirs(base_path)

    def capture_single_image(self, class_name):
        ret, frame = self.cap.read()
        if not ret:
            return False, None
        
        raw_frame = frame.copy()

        # Draw the label so you know what to sign
        display_frame = cv2.putText(frame, f'Sign: {class_name}', (50, 50), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.imshow('Collector', display_frame)
        
        # Save logic
        folder_path = os.path.join(self.base_path, class_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            
        filename = f"{class_name}_{uuid.uuid4().hex[:8]}.jpg"
        cv2.imwrite(os.path.join(folder_path, filename), raw_frame)
        
        return True, raw_frame

    def run(self, num_images=20, sleep_time=0.5):
        
        
        for item in self.classes:
            # NEW: Pause and wait for you to be ready for the NEXT class
            print(f"\nNEXT UP: '{item}'")
            print("Position your hands. Press 's' to START capturing this sign, or 'q' to QUIT.")
            
            while True:
                ret, frame = self.cap.read()
                # Show a "Waiting" screen
                waiting_frame = cv2.putText(frame.copy(), f"Ready for: {item}?", (50, 50), 
                                          cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.imshow('Collector', waiting_frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('s'): # Press 's' to start the loop for this specific class
                    break
                elif key == ord('q'): # Press 'q' to stop everything
                    self.cap.release()
                    cv2.destroyAllWindows()
                    return

            # This is the actual data taking loop
            for i in range(num_images):
                success, _ = self.capture_single_image(item)
                
                if not success:
                    break
                
                # Tiny sleep so it doesn't take 20 photos in 1 second
                time.sleep(sleep_time)
            
            print(f"Finished capturing {item}!")

        self.cap.release()
        cv2.destroyAllWindows()
        print("All classes complete!")

# --- 2. THE EXECUTION (The Main Part) ---
if __name__ == '__main__':
    # Load your JSON
    try:
        # Get the directory where main.py is actually located
        script_dir = os.path.dirname(os.path.abspath(__file__))
# Create the full path to classes.json
        json_path = os.path.join(script_dir, 'config.json')

        with open(json_path, 'r') as f:
            data = json.load(f)
            my_classes = data['Classes']
        
        # Start the tool
        # We save to './dataset' 
        collector = CaptureImages('./dataset', my_classes)
        collector.run(num_images=10, sleep_time=0.3)
        
    except FileNotFoundError:
        print("Error: 'config.json' not found! Make sure it is in the same folder.")