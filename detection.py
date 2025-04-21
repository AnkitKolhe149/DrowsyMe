# import streamlit as st
# from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
# import av
# import cv2
# import dlib
# import numpy as np
# from scipy.spatial import distance
# from utils.session_logger import log_metrics

# # Load dlib models only once
# face_detector = dlib.get_frontal_face_detector()
# landmark_model = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


# def eye_aspect_ratio(eye):
#     A = distance.euclidean(eye[1], eye[5])
#     B = distance.euclidean(eye[2], eye[4])
#     C = distance.euclidean(eye[0], eye[3])
#     return (A + B) / (2.0 * C)


# class DrowsinessDetector(VideoProcessorBase):
#     def __init__(self):
#         self.ear_history = []
#         self.frame_count = 0

#     def recv(self, frame):
#         img = frame.to_ndarray(format="bgr24")
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         faces = face_detector(gray)

#         for face in faces:
#             landmarks = landmark_model(gray, face)
#             left_eye = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(36, 42)]
#             right_eye = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(42, 48)]

#             left_ear = eye_aspect_ratio(left_eye)
#             right_ear = eye_aspect_ratio(right_eye)
#             avg_ear = (left_ear + right_ear) / 2.0
#             self.ear_history.append(avg_ear)

#             if len(self.ear_history) > 30:
#                 self.ear_history.pop(0)

#             cv2.putText(img, f"EAR: {avg_ear:.2f}", (20, 30),
#                         cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

#             # Drowsiness alert
#             if avg_ear < 0.21:
#                 cv2.putText(img, "DROWSINESS ALERT!", (20, 70),
#                             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

#             # Save metrics every 60 frames
#             self.frame_count += 1
#             if self.frame_count % 60 == 0:
#                 log_metrics(user_id="demo_user", ear=avg_ear)

#         return av.VideoFrame.from_ndarray(img, format="bgr24")


# def detection_page():
#     st.header("🧠 Real-Time Drowsiness Detection")
#     st.markdown("Live EAR tracking with drowsiness alerts and session logging.")

#     webrtc_streamer(
#         key="drowsiness",
#         video_processor_factory=DrowsinessDetector,
#         rtc_configuration=RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}),
#         media_stream_constraints={"video": True, "audio": False},
#     )


import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
import av
import cv2
import numpy as np
import mediapipe as mp
from utils.session_logger import log_metrics

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

class MediaPipeDrowsinessDetector(VideoProcessorBase):
    def __init__(self):
        self.face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)
        self.ear_history = []
        self.frame_count = 0

    def eye_aspect_ratio(self, landmarks, indices, frame_w, frame_h):
        points = [(int(landmarks[i].x * frame_w), int(landmarks[i].y * frame_h)) for i in indices]
        A = np.linalg.norm(np.array(points[1]) - np.array(points[5]))
        B = np.linalg.norm(np.array(points[2]) - np.array(points[4]))
        C = np.linalg.norm(np.array(points[0]) - np.array(points[3]))
        return (A + B) / (2.0 * C)

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb)

        frame_h, frame_w, _ = img.shape

        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
            left_eye_idx = [362, 385, 387, 263, 373, 380]  # Left eye
            right_eye_idx = [33, 160, 158, 133, 153, 144]  # Right eye

            left_ear = self.eye_aspect_ratio(landmarks, left_eye_idx, frame_w, frame_h)
            right_ear = self.eye_aspect_ratio(landmarks, right_eye_idx, frame_w, frame_h)
            avg_ear = (left_ear + right_ear) / 2.0
            self.ear_history.append(avg_ear)

            if len(self.ear_history) > 30:
                self.ear_history.pop(0)

            cv2.putText(img, f"EAR: {avg_ear:.2f}", (20, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            if avg_ear < 0.21:
                cv2.putText(img, "DROWSINESS ALERT!", (20, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            self.frame_count += 1
            if self.frame_count % 60 == 0:
                log_metrics(user_id="demo_user", ear=avg_ear)

        return av.VideoFrame.from_ndarray(img, format="bgr24")


def detection_page():
    st.header("🧠 Real-Time Drowsiness Detection (MediaPipe)")
    st.markdown("Live EAR tracking using MediaPipe with session logging.")

    webrtc_streamer(
        key="drowsiness_mediapipe",
        video_processor_factory=MediaPipeDrowsinessDetector,
        rtc_configuration=RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}),
        media_stream_constraints={"video": True, "audio": False},
    )
