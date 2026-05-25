import cv2
def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Print the coordinate to the terminal
        print(f"[{x}, {y}],")
        
        # Draw a tiny red dot where you clicked so you don't lose track
        cv2.circle(img, (x, y), 3, (0, 0, 255), -1)
        cv2.imshow('Parking Map', img)

# Load the static map image we extracted earlier
img = cv2.imread('parking_map.png')

# Show the image
cv2.imshow('Parking Map', img)

# Listen for mouse clicks on the 'Parking Map' window
cv2.setMouseCallback('Parking Map', click_event)

print("Click on the corners of the parking spots. Press any key to exit.")
cv2.waitKey(0)
cv2.destroyAllWindows()