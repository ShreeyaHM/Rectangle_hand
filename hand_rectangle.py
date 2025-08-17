import cv2
import mediapipe as mp
import math
import textwrap

def display_poem_in_rectangle(poem):
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
    mp_draw = mp.solutions.drawing_utils

    rect_width, rect_height = 100, 100
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

                h, w, _ = frame.shape
                x1, y1 = int(handLms.landmark[4].x * w), int(handLms.landmark[4].y * h)
                x2, y2 = int(handLms.landmark[8].x * w), int(handLms.landmark[8].y * h)

                dist = math.hypot(x2 - x1, y2 - y1)
                rect_width = int(max(100, dist * 2))
                rect_height = int(max(100, dist * 2))

        center_x, center_y = 300, 300
        top_left = (center_x - rect_width // 2, center_y - rect_height // 2)
        bottom_right = (center_x + rect_width // 2, center_y + rect_height // 2)
        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)

        line_height = 20
        text_x = top_left[0] + 10
        text_y = top_left[1] + 25

        chars_per_line = max(1, rect_width // 10)
        wrapped_lines = textwrap.wrap(poem, width=chars_per_line)

        for line in wrapped_lines:
            if text_y < bottom_right[1] - 10:
                cv2.putText(frame, line, (text_x, text_y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                text_y += line_height
            else:
                break

        cv2.imshow("Resizable Rectangle with Poem", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
