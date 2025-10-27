import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Key, Controller
import time

def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, 320) 
    cap.set(4, 240)  

    detector = HandDetector(detectionCon=0.7, maxHands=1)
    keyboard = Controller()

    last_action = "NONE"
    cooldown = 0.5
    last_time = time.time()

    while True:
        success, img = cap.read()
        hands, _ = detector.findHands(img, draw=False)

        if hands:
            for hand in hands:
                lmList = hand["lmList"]   
                connections = detector.mpHands.HAND_CONNECTIONS
                for id, lm in enumerate(lmList):
                    cx, cy = lm[0:2]
                    cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
                for connection in connections:
                    start, end = connection
                    x1, y1 = lmList[start][0:2]
                    x2, y2 = lmList[end][0:2]
                    cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        action = "NONE"
        if hands:
            fingers = detector.fingersUp(hands[0])

            if fingers == [0, 0, 0, 0, 0]:
                action = "NEUTRAL"
            elif fingers == [1, 1, 1, 1, 1]:
                action = "LEFT"
            elif fingers == [0, 1, 0, 0, 0]:
                action = "UP"
            elif fingers == [0, 1, 1, 0, 0]:
                action = "DOWN"
            elif fingers == [0, 1, 1, 1, 0]:
                action = "RIGHT"

        current_time = time.time()

        if action != "NONE" and (action != last_action or current_time - last_time > cooldown):
            if action == "LEFT":
                keyboard.press(Key.left)
                keyboard.release(Key.left)
            elif action == "RIGHT":
                keyboard.press(Key.right)
                keyboard.release(Key.right)
            elif action == "UP":
                keyboard.press(Key.up)
                keyboard.release(Key.up)
            elif action == "DOWN":
                keyboard.press(Key.down)
                keyboard.release(Key.down)

            last_action = action
            last_time = current_time
            
        cv2.putText(img, f"Action: {action}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow("Gesture Game Control", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()