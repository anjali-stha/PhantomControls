![Image](https://github.com/user-attachments/assets/d3be0ba8-3001-4889-b0f7-fe146ae53238)
# Inspiration
It started as a simple thought—what if we could play a game without touching anything? No keyboard, no controller, just movement. We’ve all seen motion-controlled gaming in high-end VR systems, but what about something that works with just a webcam? That idea stuck with us. We wanted to see if we could take something as natural as raising a hand or making a fist and turn it into a way to control a game. No fancy equipment, no complicated setup—just movement, captured and translated into action.

# What it does
Phantom Controls turns your real-world movements into in-game actions using just a webcam. Raise your hand to move forward, give a thumbs down to move backward, or form an "okay" sign to shoot. Lean left or right to strafe, lift your elbow to reload, and touch your left hand to your right elbow for spike control. By tracking hand gestures and body positions in real time, it creates an intuitive way to interact with games, making gameplay feel more natural and immersive.

# How we built it
We combined computer vision and AI-driven gesture recognition to turn movement into game commands. Using MediaPipe for real-time body and hand tracking, OpenCV for video processing, and PyDirectInput for simulating key presses, we built a system that translates natural gestures into responsive in-game actions. The program detects hand positions, body tilts, and arm movements, ensuring smooth and intuitive gameplay—all powered by a simple webcam.

# Challenges we ran into
Natural Gestures: Achieving fluid, intuitive gestures was more challenging than anticipated. Variations in hand positioning sometimes resulted in incorrect actions being triggered.
Motion Sensitivity: Quick or subtle movements could confuse the system, leading to misreads or unintentional actions.
Gesture Differentiation: Fine-tuning was needed to distinguish between similar gestures, such as raising a hand to jump versus using the same motion for shooting.
Response Time: Minimizing any lag was critical to maintain immersion, as even slight delays could disrupt the gameplay experience.

# Learnings
Gained hands-on experience with computer vision to enable real-time interactions, making gameplay feel more intuitive.
Learned the importance of careful gesture calibration to ensure accurate and efficient tracking.
Realized how enhancing motion recognition can significantly improve the overall user experience, creating smoother and more responsive interactions.

# What’s next
Expanding gesture recognition to include more complex commands and refine the control system.
Exploring the possibility of integrating voice commands to make gameplay even more dynamic.
Working on enhancing compatibility with VR and AR to take the immersive experience to new levels.
Experimenting with machine learning techniques to adapt motion tracking for personalized gestures and refine performance over time.
