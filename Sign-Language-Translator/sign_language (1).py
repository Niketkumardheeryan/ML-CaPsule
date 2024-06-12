import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Set camera width to 1280 pixels
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Set camera height to 720 pixels

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils
fingercordinates=[(8,6),(12,10),(16,14),(20,18)]
thumbcordinate=(4,2)

while True:
    success,img=cap.read()
    if not cap.isOpened():
      print("Error: Camera not opened.")
      exit()
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(imgRGB)
    multiLandMarks=results.multi_hand_landmarks
    if multiLandMarks:
        handpoints=[]
        for handLms in multiLandMarks:
            mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)
            for idx, lm in enumerate(handLms.landmark):
                # print(id,lm)
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                handpoints.append((cx,cy))
        for point in handpoints:
            cv2.circle(img,point,10,(0,0,255),cv2.FILLED)

        upcount=0
        for cordinate in fingercordinates:
            if handpoints[cordinate[0]][1] < handpoints[cordinate[1]][1]:
                upcount+=1
        if handpoints[thumbcordinate[0]][0] >handpoints[thumbcordinate[1]][0]:
            upcount+=1

         #condition for victory
        if (handpoints[8][1] < handpoints[6][1]) and (handpoints[12][1] < handpoints[10][1]) :
            if upcount==2:
                cv2.putText(img, "VICTORY", (15, 250), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 5)


         # #condition for yo
         # if (handpoints[8][1] < handpoints[6][1]) and (handpoints[20][1] < handpoints[18][1]):
         #     if upcount==2:
         #         cv2.putText(img, "YO", (15, 250), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 5)

         #condition for ok
        if handpoints[4][1] < handpoints[2][1] and handpoints[4][1] < handpoints[5][1] and handpoints[8][1] > handpoints[5][1] and upcount == 1:
            cv2.putText(img, "OK", (15, 250), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 5)

         # Condition for hi
            if (distancey[4] < distancey[2] and distancey[8] < distancey[6]) and \
                    (distancey[20] < distancey[18] and distancey[12] < distancey[10]) and \
                    (distancey[16] < distancey[14]):
                cv2.putText(frame, txt9, (15, 250), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 5)

         # condition for smile
        if handpoints[4][1] < handpoints[2][1] and handpoints[8][0] < handpoints[6][0]:
            if upcount == 2:
                cv2.putText(img, "smile", (15, 250), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 5)

         # condition for call me
        if (handpoints[4][1] < handpoints[2][1] and handpoints[20][1] < handpoints[18][1]):
            if upcount == 2:
                cv2.putText(img, "call me", (15, 250), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 5)

         # condition for hot
        if (handpoints[8][1] < handpoints[6][1]) :
            if upcount == 1:
                cv2.putText(img, "HOT", (15, 250), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 5)

         # condition for lose
        if handpoints[thumbcordinate[0]][0] > handpoints[thumbcordinate[1]][0]:
           if upcount == 1:
                cv2.putText(img, "LOSE", (15,250), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 5)
         # #condition for thumbs up
         # if (handpoints[4][1] < handpoints[2][1] and handpoints[8][1] < handpoints[6][1]) and (handpoints[20][1] > handpoints[18][1] and handpoints[12][1] > handpoints[10][1]) and (handpoints[16][1] > handpoints[14][1]):
         #     if upcount == 1:
         #         cv2.putText(img, "THUMBS UP", (15,250), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 5)

         # condition for thief (thumb tip touching index finger tip and rest of fingers closed)
        dist_thumb_index = abs(handpoints[4][0] - handpoints[8][0]) + abs(handpoints[4][1] - handpoints[8][1])
        if dist_thumb_index < 60 and upcount==2:
            cv2.putText(img, "thief", (15, 250), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 5)



        cv2.putText(img,str(upcount),(100,150),cv2.FONT_HERSHEY_PLAIN,12,(255,0,0),12)


    cv2.imshow("finger counter",img)
    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' key to exit the loop and close the window
        break

cap.release()
cv2.destroyAllWindows()

