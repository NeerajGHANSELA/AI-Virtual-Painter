import cv2
import cv2.text
import mediapipe as mp
import numpy as np
import os
import handTrackingModule as htm

video_cap = cv2.VideoCapture(0)
video_cap.set(3, 1280)
video_cap.set(4, 720)

asbPath = os.path.dirname(os.path.abspath(__file__))
folderPath = os.path.join(asbPath, 'images')

# get all the filename in the images folder
menuImages = os.listdir(folderPath)
menuOverlayList = []    # used to store loaded images(not just filenames)

# loading images from the folder
for imPath in menuImages:
    image = cv2.imread(os.path.join(folderPath, imPath))
    menuOverlayList.append(image)

if len(menuOverlayList) != 1:
    exit("Menu images not found in the specified folder.")

handDetector = htm.handDetector(detectionConfidence=0.85, maxHands=1)

modeList = []   # stores the mode of the previous frames: draw or select

selection = "white" # default color
drawColor = (255, 255, 255) # default color: white
eraserColor = (0, 0, 0) # black
brushThickness = 10
eraserThickness = 80

prev_x, prev_y = 0, 0

imageCanvas = np.zeros((720, 1280, 3), np.uint8)

while True:
    success, image = video_cap.read()
    if not success:
        break

    """
        flip the image horizontally because:
        when drawing on the right side of the screen, the hand moves to the left and draws to the left side of the canvas and vise versa
    """

    image = cv2.flip(image, 1)  # flip horizontally
    # 0: flip vertically
    # 1: flip horizontally
    # -1: flip both vertically and horizontally

    # Show the menu image onto the webcam
    image[0:125, 0:1280] = menuOverlayList[0]
    
    # Find hand landmarks
    image = handDetector.findHands(image)
    lmList = handDetector.findPosition(image, draw=False)

    # Check which fingers are up
    if len(lmList) != 0:
        fingersList = handDetector.trackingFingersUpOrClosed(image, lmList)

        # Tip of index and middle fingers
        indexTip_x, indexTip_y = lmList[8][1:]
        middleTip_x, middleTip_y = lmList[12][1:]

        # Draw when the index finger is up
        # select when 2 fingers are up, no drawing
        numOfFingersOpen = fingersList.count(1)

        isIndexFingerOpen = fingersList[1] == 1
        isMiddleFingerOpen = fingersList[2] == 1

        # Drawing Mode
        if isIndexFingerOpen and not isMiddleFingerOpen:
            modeList.append("draw")
            if len(modeList) > 2:
                # drawing after selection, resulted in unwanted line. therefore, resetting the point to 0,0
                modePrev = modeList[-2]
                if modePrev == "select":
                    prev_x, prev_y = 0, 0

            # Only draw if below the menu area (y > 125)
            if indexTip_y > 125:
                cv2.circle(image, (indexTip_x, indexTip_y), 15, drawColor, cv2.FILLED)

                # The very 1st iteration, don't want to create a line from (0,0) to the index finger tip
                if prev_x == 0 and prev_y == 0:
                    prev_x, prev_y = indexTip_x, indexTip_y

                if drawColor == eraserColor and selection == "eraser":
                    cv2.line(image, (prev_x, prev_y), (indexTip_x, indexTip_y), drawColor, eraserThickness)
                    cv2.line(imageCanvas, (prev_x, prev_y), (indexTip_x, indexTip_y), drawColor, eraserThickness)
                else:
                    # Draw using a line
                    cv2.line(image, (prev_x, prev_y), (indexTip_x, indexTip_y), drawColor, brushThickness)
                    cv2.line(imageCanvas, (prev_x, prev_y), (indexTip_x, indexTip_y), drawColor, brushThickness)

                # Drawing after using eraser, would create unwanted line because of the previous points
                if selection == "eraser":
                    prev_x, prev_y = 0, 0
                else:
                    # update the pervious points
                    prev_x, prev_y = indexTip_x, indexTip_y
            else:
                # Reset previous points when finger is in menu area
                prev_x, prev_y = 0, 0

        # Selection Mode
        elif isIndexFingerOpen and isMiddleFingerOpen:
            modeList.append("select")

            if (indexTip_y and middleTip_y) < 125:
    
                # White: 180 - 310
                if 180 < (indexTip_x or middleTip_x) < 310:
                    selection = "white"
                    drawColor = (255, 255, 255)
                    
                # Blue: 440 - 495
                elif 440 < (indexTip_x or middleTip_x) < 495:
                    selection = "blue"
                    drawColor = (255, 0, 0)

                # Red: 620 - 690
                elif 620 < (indexTip_x or middleTip_x) < 690:
                    selection = "red"
                    drawColor = (0, 0, 255)

                # Green: 840 - 890
                elif 840 < (indexTip_x or middleTip_x) < 890:
                    selection = "green"
                    drawColor = (0, 255, 0)

                # Eraser: 1035 - 1075
                elif 1035 < (indexTip_x or middleTip_x) < 1075:
                    selection = "eraser"
                    drawColor = (0, 0, 0)

    # create a line above the selected color or eraser for indication
    match selection:
        case "white":   # 180 - 310
            cv2.line(image, (250, 10), (290, 10), (0, 0, 0), 2)
        case "blue":    # 440 - 495
            cv2.line(image, (470, 10), (510, 10), (0, 0, 0), 2)
        case "red": # 620 - 690
            cv2.line(image, (660, 10), (700, 10), (0, 0, 0), 2)
        case "green":   # 840 - 890
            cv2.line(image, (860, 10), (900, 10), (0, 0, 0), 2)
        case "eraser":
            cv2.line(image, (1070, 10), (1110, 10), (0, 0, 0), 2)

    # In the canvas image, where there is black -> white, colored -> black
    # then overlay the canvas image onto the webcam image
    iamgeGray = cv2.cvtColor(imageCanvas, cv2.COLOR_BGR2GRAY)
    _, imageInverse = cv2.threshold(iamgeGray, 50, 255, cv2.THRESH_BINARY_INV) 

    imageInverse = cv2.cvtColor(imageInverse, cv2.COLOR_GRAY2BGR) 
    image = cv2.bitwise_and(image, imageInverse)
    image = cv2.bitwise_or(image, imageCanvas)

    # Combine both image and imageCanvas
    # image = cv2.addWeighted(image, 0.5, imageCanvas, 0.5, 0)
    cv2.imshow("Virtual Painter", image)
    # cv2.imshow("Canvas", imageCanvas)
    cv2.waitKey(1)