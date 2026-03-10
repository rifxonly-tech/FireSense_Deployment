# 🔥 FireSense: Real-Time Edge AI Fire & Smoke Detection

![FireSense Banner](https://img.shields.io/badge/AI-FireSense-orange?style=for-the-badge&logo=firebase)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-4-red?style=for-the-badge&logo=raspberry-pi)
![YOLO](https://img.shields.io/badge/YOLO-Nano-yellow?style=for-the-badge)

**FireSense** is an optimized edge-computing AI system designed to detect fire and smoke in real-time. Built using a custom-trained YOLO model, this project is specifically engineered to run efficiently on a CPU-only **Raspberry Pi 4**. Upon detecting danger, the system automatically triggers hardware actuators (a Buzzer alarm and a Relay for power cutoff) to prevent further disaster.

---

## 📂 Repository Structure

The project is cleanly divided into two main environments to separate testing and actual hardware deployment:

~~~text
📦 FireSense
 ┣ 📂 Hardware                # Run this ONLY on the Raspberry Pi
 ┃ ┣ 📜 best_float32.tflite   # Lightweight Edge model (11.7 MB)
 ┃ ┗ 📜 main_pi.py            # Main script with RPi.GPIO integration
 ┣ 📂 Testing                 # Run this on Local PC for testing
 ┃ ┣ 📜 best.pt               # Standard PyTorch weights (6.3 MB)
 ┃ ┗ 📜 test.py               # Webcam simulation script
 ┣ 📜 .gitignore              # Ignores cache and unnecessary files
 ┣ 📜 requirements.txt        # Python dependencies
 ┗ 📜 FireTrainngModel.ipynb  # The original Colab Training Notebook
~~~

---

## 🧠 Model Training Pipeline & Google Colab

The AI model was trained using a customized dataset of over 12,000 images via Roboflow. The entire training process was executed on Google Colab to leverage cloud GPU acceleration. 

🔗 **[Click here to view/run the Training Notebook in Google Colab](https://colab.research.google.com/drive/1u2AIWxVxRNrgniQBb5OnW2qSBUC6vtDG?usp=sharing)**

### Training Highlights (`FireTrainngModel.ipynb`):
- **Dataset Integration:** Securely downloaded the annotated dataset directly from Roboflow via API.
- **Fail-Safe Execution:** The model was trained for a total of **200 epochs**. To mitigate Google Colab's GPU limitations, a checkpoint resume mechanism (`resume=True`) was utilized to successfully recover a disconnected session from epoch 136 and completed the training up to epoch 200.
- **Performance Evaluation:** The final model achieved a solid overall **mAP50 of 57.6%** (59.9% for fire detection and 55.2% for smoke detection), which is highly reliable for a Nano-sized architecture.
- **Edge Hardware Optimization:** The standard PyTorch model (`best.pt`) was automatically exported into a highly compressed TensorFlow Lite format (`best_float32.tflite`) to ensure real-time >30 FPS processing on the Raspberry Pi.

---

## ⚙️ Hardware Setup (Raspberry Pi 4)

This system uses the `RPi.GPIO` library with **BCM** pin numbering. Please connect your physical hardware components to the following GPIO pins:

| Component | Pin Type | BCM Pin Number | Function |
| :--- | :--- | :--- | :--- |
| **Buzzer** | OUTPUT | `GPIO 17` | Sounds an alarm when fire/smoke is detected. |
| **Relay** | OUTPUT | `GPIO 27` | Cuts off electrical power to prevent electrical fires. |
| **Camera** | USB / CSI | `Default (0)` | Captures real-time RGB video feed. |

---

## 🚀 Installation & Setup

1. **Clone this repository** to your local machine or Raspberry Pi:
~~~bash
git clone https://github.com/rifxonly-tech/FireSense_Deployment/
cd FireSense
~~~

2. **Install the required dependencies** using `pip`:
~~~bash
pip install -r requirements.txt
~~~
*Note: If you are running this on a Raspberry Pi, ensure you have the camera modules enabled in `raspi-config`.*

---

## 💻 Usage

### 1. Local PC Testing (Simulation)
Want to test the model using your laptop's built-in webcam before messing with the hardware? Run the simulation script:
~~~bash
cd Testing
python test.py
~~~
*Press `q` on your keyboard to exit the camera window.*

### 2. Raspberry Pi Deployment (Production)
Once the hardware components are wired correctly, run the main script to activate the full FireSense edge system:
~~~bash
cd Hardware
python main_pi.py
~~~
*The terminal will output `[SYSTEM] Running on Raspberry Pi. Hardware pins ACTIVE.` and the actuators will trigger automatically upon detection.*

---
