import cv2
import mediapipe as mp
import time
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1200)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)
keys = [
    ["Q", "W", "E", "R", "T"],
    ["A", "S", "D", "F", "G"]
]

finalText = ""

mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0


def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img


class Button:
    def __init__(self, pos, text, size=[85, 85]):
        self.text = text
        self.pos = pos
        self.size = size


buttonList = []

for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))


while True:
    success, img = cap.read()
    hands, img = detector.findHands(img, draw=True)

    img = drawAll(img, buttonList)

    if len(hands) != 0:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            lmlist = hands[0]["lmList"]
            if x < lmlist[8][0] < x + w and y < lmlist[8][1] < y + h:
                cv2.rectangle(img, (x, y), (x + w, y + h), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                length, info, img = detector.findDistance(lmlist[8][0:2], lmlist[12][0:2], img)
                print(f"{length=}")

                if length < 30:
                    print("Clicking")
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                    finalText += button.text

    cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 425), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("image", img)
    cv2.waitKey(1)
