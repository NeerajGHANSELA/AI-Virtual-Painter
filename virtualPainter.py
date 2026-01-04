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

# Detection points for each color and eraser in the menu image
maxMenuHeight = 125
whiteMinDetect_x = 180
whiteMaxDetect_x = 310
blueMinDetect_x = 440
blueMaxDetect_x = 495
redMinDetect_x = 620
redMaxDetect_x = 690
greenMinDetect_x = 840
greenMaxDetect_x = 890
eraserMinDetect_x = 1035
eraserMaxDetect_x = 1075

# Line that are created above the selected color or eraser for indication
whiteLineMin_x = 250
whiteLineMax_x = 290
blueLineMin_x = 470
blueLineMax_x = 510
redLineMin_x = 660
redLineMax_x = 700
greenLineMin_x = 860
greenLineMax_x = 900
eraserLineMin_x = 1070
eraserLineMax_x = 1110
line_y = 10

# Variable to store previous points when drawing
prev_x, prev_y = 0, 0

imageCanvas = np.zeros((720, 1280, 3), np.uint8)
# Canvas is a black image. 8 bits: 0-255

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
            if indexTip_y > maxMenuHeight:  # was 125 originally
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

            if (indexTip_y and middleTip_y) < maxMenuHeight: # was 125 originally
    
                # White: 180 - 310
                if whiteMinDetect_x < (indexTip_x or middleTip_x) < whiteMaxDetect_x: 
                    selection = "white"
                    drawColor = (255, 255, 255)
                    
                # Blue: 440 - 495
                elif blueMinDetect_x < (indexTip_x or middleTip_x) < blueMaxDetect_x:
                    selection = "blue"
                    drawColor = (255, 0, 0)

                # Red: 620 - 690
                elif redMinDetect_x < (indexTip_x or middleTip_x) < redMaxDetect_x:
                    selection = "red"
                    drawColor = (0, 0, 255)

                # Green: 840 - 890
                elif greenMinDetect_x < (indexTip_x or middleTip_x) < greenMaxDetect_x:
                    selection = "green"
                    drawColor = (0, 255, 0)

                # Eraser: 1035 - 1075
                elif eraserMinDetect_x < (indexTip_x or middleTip_x) < eraserMaxDetect_x:
                    selection = "eraser"
                    drawColor = (0, 0, 0)

    # create a line above the selected color or eraser for indication
    match selection:
        case "white":
            cv2.line(image, (whiteLineMin_x, line_y), (whiteLineMax_x, line_y), (0, 0, 0), 2)
        case "blue":
            cv2.line(image, (blueLineMin_x, line_y), (blueLineMax_x, line_y), (0, 0, 0), 2)
        case "red":
            cv2.line(image, (redLineMin_x, line_y), (redLineMax_x, line_y), (0, 0, 0), 2)
        case "green":
            cv2.line(image, (greenLineMin_x, line_y), (greenLineMax_x, line_y), (0, 0, 0), 2)
        case "eraser":
            cv2.line(image, (eraserLineMin_x, line_y), (eraserLineMax_x, line_y), (0, 0, 0), 2)

    # In the canvas image, where there is black -> white, colored -> black
    # then overlay the canvas image onto the webcam image
    iamgeGray = cv2.cvtColor(imageCanvas, cv2.COLOR_BGR2GRAY)
    _, imageInverse = cv2.threshold(iamgeGray, 50, 255, cv2.THRESH_BINARY_INV) 

    imageInverse = cv2.cvtColor(imageInverse, cv2.COLOR_GRAY2BGR) 
    image = cv2.bitwise_and(image, imageInverse)
    image = cv2.bitwise_or(image, imageCanvas)

    cv2.imshow("Virtual Painter", image)
    cv2.imshow("Canvas", imageCanvas)
    cv2.waitKey(1)