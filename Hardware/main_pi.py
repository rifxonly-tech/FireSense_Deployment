import cv2
from ultralytics import YOLO

# -------------------------------------------------------------------
# 1. HARDWARE CONNECTOR SETUP (FOR HARDWARE TEAM)
# -------------------------------------------------------------------
# Try to import Raspberry Pi GPIO library gracefully.
# This prevents the script from crashing if tested on a normal PC.
try:
    import RPi.GPIO as GPIO
    IS_RASPBERRY_PI = True
    print("[SYSTEM] Running on Raspberry Pi. Hardware pins ACTIVE.")
except ImportError:
    IS_RASPBERRY_PI = False
    print("[WARNING] RPi.GPIO not found. Running in PC Simulation Mode.")

# Hardware Team: Change these variables based on your physical wiring!
# Using BCM pin numbering standard
BUZZER_PIN = 17
RELAY_PIN = 27

# Initialize Hardware Pins
if IS_RASPBERRY_PI:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    
    # Set pins as OUTPUT
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    GPIO.setup(RELAY_PIN, GPIO.OUT)
    
    # Set initial state to SAFE (OFF)
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    GPIO.output(RELAY_PIN, GPIO.LOW) # Assuming LOW means normal electrical flow


# -------------------------------------------------------------------
# 2. SOFTWARE & AI SETUP (FOR SOFTWARE TEAM)
# -------------------------------------------------------------------
# Load the highly optimized TFLite model for Raspberry Pi 4 CPU
model = YOLO('best_float32.tflite')

# Initialize RGB Camera (0 is usually the default USB/Pi camera)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("[SYSTEM] FireSense Camera Activated. Press 'q' to exit.")


# -------------------------------------------------------------------
# 3. MAIN DETECTION LOOP
# -------------------------------------------------------------------
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("[ERROR] Failed to grab frame from camera.")
        break

    # Run YOLOv11 inference with 50% confidence threshold
    results = model(frame, conf=0.5, verbose=False)
    
    # State variable for this current frame
    danger_detected = False

    # Check all detected objects in the frame
    for box in results[0].boxes:
        class_id = int(box.cls[0])
        class_name = model.names[class_id]
        
        # If the model sees fire or smoke, trigger the danger state!
        if class_name in ['fire', 'smoke']:
            danger_detected = True
            break # Exit loop early for speed, one fire is enough to trigger

    # --- HARDWARE TRIGGER LOGIC ---
    if danger_detected:
        # Action when Fire/Smoke is found!
        if IS_RASPBERRY_PI:
            GPIO.output(BUZZER_PIN, GPIO.HIGH) # Turn ON Siren
            GPIO.output(RELAY_PIN, GPIO.HIGH)  # Cut OFF Electricity (if using NC Relay)
        else:
            print("[SIMULATION] DANGER! Triggering Buzzer & Relay -> HIGH")
    else:
        # Action when the room is SAFE
        if IS_RASPBERRY_PI:
            GPIO.output(BUZZER_PIN, GPIO.LOW) # Turn OFF Siren
            GPIO.output(RELAY_PIN, GPIO.LOW)  # Restore Electricity
            
    # Draw boxes on the screen for monitoring
    annotated_frame = results[0].plot()
    cv2.imshow("FireSense - Edge Detection", annotated_frame)

    # Emergency manual exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# -------------------------------------------------------------------
# 4. CLEANUP (VERY IMPORTANT FOR HARDWARE)
# -------------------------------------------------------------------
cap.release()
cv2.destroyAllWindows()

if IS_RASPBERRY_PI:
    # Reset all GPIO pins to safe state before closing
    GPIO.cleanup()
    print("[SYSTEM] Hardware pins successfully reset.")