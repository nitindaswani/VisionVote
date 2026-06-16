import json
import cv2
import mediapipe as mp
import face_recognition


def capture_face_encoding():

    cap = cv2.VideoCapture(0)

    while True:

        ret, frame = cap.read()

        if not ret:
            continue

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        encodings = face_recognition.face_encodings(
            rgb
        )

        cv2.imshow(
            "Face Registration",
            frame
        )

        if encodings:

            cap.release()
            cv2.destroyAllWindows()

            return json.dumps(
                encodings[0].tolist()
            )

        if cv2.waitKey(1) == 27:

            cap.release()
            cv2.destroyAllWindows()

            return None