# 👁️ Drowsiness & Gaze Tracking Web App

A real-time drowsiness and gaze tracking system for online exams or corporate meetings. Built with **Streamlit**, **dlib**, **OpenCV**, and **MediaPipe**, it provides:

- 🔐 User/admin login system
- 🧠 Eye Aspect Ratio (EAR) based drowsiness detection
- 👀 Gaze monitoring (center, left, right, down)
- 📊 Admin dashboard for session log analysis

---

## 🚀 Features

### 👤 User Side
- Live camera monitoring
- EAR + gaze tracking
- Real-time alerts
- Metric logging per session

### 🛠️ Admin Side
- Upload/browse session logs
- EAR graph over time
- Drowsiness event summary

---

## 📦 Requirements
```bash
pip install -r requirements.txt
```
Ensure you also have:
- `shape_predictor_68_face_landmarks.dat` in the root directory
- A working webcam

---

## 🏃‍♂️ Run the App
```bash
streamlit run app.py
```

---

## 📁 Project Structure
```
drowsy_webapp/
├── app.py                # Main routing script
├── login.py              # Login page
├── detection.py          # User webcam detection page
├── dashboard.py          # Admin session dashboard
├── utils/
│   └── session_logger.py # Logs EAR to CSV
├── data/                 # Session logs stored here
└── requirements.txt
```

---

## ✅ Demo Credentials
- User: `user` / `1234`
- Admin: `admin` / `admin123`

---

## 🌐 Deployment Ideas
- **Streamlit Cloud** (easy and free)
- **Render / Railway** (Flask version)
- **Docker + EC2** for production

---

## 📬 Contact / Ideas
Feel free to extend with:
- Audio alerts 🔊
- Face absence detection 🚫
- Detailed attention scorecard 📈
