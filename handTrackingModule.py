import cv2
import mediapipe as mp
import time # used to check the frame rate

class handDetector():
    # parameters include all the parameters of the Hands class
    def __init__(self, mode=False, maxHands=2, detectionConfidence=0.5, trackConfidence=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionConfidence = detectionConfidence
        self.trackConfidence = trackConfidence

        self.mpHands = mp.solutions.hands
        # Create an object of the Hands class
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionConfidence,
            min_tracking_confidence=self.trackConfidence
        ) # use the default values
        self.mpDraw = mp.solutions.drawing_utils # to draw the landmarks and connections onto the hands

        self.fingerTipsList = [8, 12, 16, 20] # index, middle, ring, pinky finger tips landmark ids
        self.fingerComparisonList = [6, 10, 14, 18]

    def findHands(self, image, draw=True):
        # send rgb image to the hands
        # Hands class only uses RGB object
        imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
        self.results = self.hands.process(imgRGB)

        # extract the information from the results
        # print(results)

        # To check whether hand is detected or not
        # print(results.multi_hand_landmarks)

        # if the hands are being detected
        if self.results.multi_hand_landmarks:
            # For each hand
            for handLms in self.results.multi_hand_landmarks:
                # Extract the information for each hand

                if (draw):
                    # We are drawing on the BGR format because that is what we are showing (cv2.imshow())
                    self.mpDraw.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS)
        return image
    
    def findPosition(self, image, handNo=0, draw=True):
        # handNo, is used to specify which hand we want to track if there are multiple hands

        lmList = [] # stores all the landmark positionss

        if self.results.multi_hand_landmarks:
            # get the information of the specified hand
            hand = self.results.multi_hand_landmarks[handNo]
            # For each landmark in the hand
            for id, lm in enumerate(hand.landmark):
                # lm gives us the location of each landmark in x,y,z format, which is the normalized value of the landmark
                # id gives us the index of the landmark. Each landmark is associated with an id

                height, width, channels = image.shape
                pixel_x, pixel_y = int(lm.x * width), int(lm.y * height)
                lmList.append([id, pixel_x, pixel_y])
                
                # if draw:
                #     cv2.circle(image, (pixel_x, pixel_y), 25, (255, 0, 255), cv2.FILLED)

        return lmList
    
    def getHandedness(self, image, handNo=0):
        # only one hand will be tracked, therefore, handNo = 0
        if self.results.multi_handedness:
            handedness = self.results.multi_handedness[handNo]
            return handedness.classification[0].label
        return None

    
    def trackingFingersUpOrClosed(self, image, lmList):
        """
            This function will only track the 2 fingers, index and middle finger
        """
        fingers = []    # 1: open, 0: closed

        # thumb
        handedness = self.getHandedness(image)

        thumbTip_x = lmList[4][1]
        thumbComparison_x = lmList[3][1]

        if handedness == "Right":
            if thumbTip_x < thumbComparison_x:
                fingers.append(1)
            else:
                fingers.append(0)
        
        elif handedness == "Left":
            if thumbTip_x > thumbComparison_x:
                fingers.append(1)
            else:
                fingers.append(0)

        for i in range(0, 4):
            fingerTip_y = lmList[self.fingerTipsList[i]][2]
            fingerComparison_y = lmList[self.fingerComparisonList[i]][2]

            if fingerTip_y <= fingerComparison_y:
                fingers.append(1)
            else:
                fingers.append(0)
        
        return fingers


        
        




