import cv2
import mediapipe as mp
import time

OUTPUT_TXT_FILE = "./" + "hand.txt"

class globals:
    start_time = time.time()

# MediaPipeの手の検出モジュールを初期化
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# カメラのキャプチャを開始
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280/10)  # 幅を1280に設定
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720/3)

# じゃんけんの結果を決める関数
def get_hand_shape(hand_landmarks):
    # 親指、示指、中指、薬指、小指のそれぞれの先端ランドマークの座標を取得
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    # 各指が曲がっているか（折りたたまれているか）を判断
    thumb_folded = thumb_tip.x < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x
    index_folded = index_tip.y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y
    middle_folded = middle_tip.y < hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y
    ring_folded = ring_tip.y < hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y
    pinky_folded = pinky_tip.y < hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].y

    # グー、チョキ、パーを判断
    if not thumb_folded and not index_folded and not middle_folded and not ring_folded and not pinky_folded:
        return "Rock"
    elif not thumb_folded and index_folded and middle_folded and not ring_folded and not pinky_folded:
        return "Scissors"
    elif thumb_folded and index_folded and middle_folded and ring_folded and pinky_folded:
        return "Paper"
    else:
        return "None"

def hand():
    last_hand_shape = "None"
    count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("カメラからフレームを取得できませんでした。")
            break

        # フレームをRGBに変換
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 手の検出を実行
        results = hands.process(rgb_frame)

        #検出された手のランドマークを描画
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # 手の形を認識
                hand_shape = get_hand_shape(hand_landmarks)
                cv2.putText(frame, hand_shape, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                if hand_shape != "None":
                    count = count+1
                    with open(OUTPUT_TXT_FILE,'a') as f:
                        f.write(hand_shape)
                        f.write("\n")
                    print(count," 手の形:", hand_shape)

        # フレームを表示
        cv2.imshow('Hand Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    hand()
    cap.release()
    cv2.destroyAllWindows()
