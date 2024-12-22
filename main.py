import mediapipe as mp
import cv2
import math
import pyautogui
import requests
from bs4 import BeautifulSoup
import tkinter as tk
import webbrowser
import time


link_opened = False

######################
## HELPER FUNCTIONS ##
######################
# gets orientation of hand
def orientation(coordinate_landmark_0, coordinate_landmark_9): 
    wristX = coordinate_landmark_0[0] # wrist area x
    wristY = coordinate_landmark_0[1] # wrist area y
    
    middleX = coordinate_landmark_9[0] # middle joint x
    middleY = coordinate_landmark_9[1] # middle joint y
    
    if abs(middleX - wristX) < 0.05:      
        m = 1000000000
    else:
        m = abs((middleY - wristY) / (middleX - wristX))       
        
    if m >= 0 and m <= 1:
        if middleX > wristX:
            return "right"
        else:
            return "left"
    
    if m > 1:
        if middleY < wristY:       
            return "up"
        else:
            return "down"

# distance func
def dist(point1, point2):
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)


# get the x of a landmark
def x_coordinate(landmark):
    return landmark.x

# get the y of a landmark
def y_coordinate(landmark):
    return landmark.y

# checks which fingers are closed
# landmarks: list containing landmark coords
# z: sring that specifies desired operation to be done
def finger(landmarks, z):
    try:
        wrist_X = x_coordinate(landmarks[0]) # wrist
        wrist_Y = y_coordinate(landmarks[0])
        
        mid_index_X = x_coordinate(landmarks[7]) # mid index
        mid_index_Y = y_coordinate(landmarks[7])
        wrist_to_mid_index = dist([wrist_X, wrist_Y], [mid_index_X, mid_index_Y])
        
        top_index_X = x_coordinate(landmarks[8]) # top index
        top_index_Y = y_coordinate(landmarks[8])
        wrist_to_top_index = dist([wrist_X, wrist_Y], [top_index_X, top_index_Y])
        
        mid_middle_X = x_coordinate(landmarks[11]) # mid middle finger
        mid_middle_Y = y_coordinate(landmarks[11])
        wrist_to_mid_midfinger = dist([wrist_X, wrist_Y], [mid_middle_X, mid_middle_Y])
        
        top_middle_X = x_coordinate(landmarks[12]) # top middle finger
        top_middle_Y = y_coordinate(landmarks[12])                    
        wrist_to_top_midfinger = dist([wrist_X, wrist_Y], [top_middle_X, top_middle_Y])
        
        mid_ring_X = x_coordinate(landmarks[15]) # mid ring
        mid_ring_Y = y_coordinate(landmarks[15])                    
        wrist_to_mid_ring = dist([wrist_X, wrist_Y], [mid_ring_X, mid_ring_Y])
        
        top_ring_X = x_coordinate(landmarks[16]) # top ring
        top_ring_Y = y_coordinate(landmarks[16])
        wrist_to_top_ring = dist([wrist_X, wrist_Y], [top_ring_X, top_ring_Y])
        
        mid_pinky_X = x_coordinate(landmarks[19]) # mid pinky
        mid_pinky_Y = y_coordinate(landmarks[19])                    
        wrist_to_mid_pinky = dist([wrist_X, wrist_Y], [mid_pinky_X, mid_pinky_Y])
        
        top_pinky_X = x_coordinate(landmarks[20]) # top pinky
        top_pinky_Y = y_coordinate(landmarks[20])                    
        wrist_to_top_pinky = dist([wrist_X, wrist_Y], [top_pinky_X, top_pinky_Y])
        
        close = []
        
        # this operation gets the specific fingers that are currently closed
        if z == "finger":    
            if wrist_to_mid_index > wrist_to_top_index:
                close.append(1)
            if wrist_to_mid_midfinger > wrist_to_top_midfinger:
                close.append(2)
            if wrist_to_mid_ring > wrist_to_top_ring:
                close.append(3)
            if wrist_to_mid_pinky > wrist_to_top_pinky:
                close.append(4)
            return close
        
        # this operation gets the coordinates of the specific finger
        if z == "true coordinate":
            return (wrist_X, wrist_Y)
        
    except:
        pass
    
def display_coordinates(img, x, y):
    # convert coordinates to string
    coordinates_str = f"Coordinates: ({x}, {y})"
    
    # put text on video feed
    cv2.putText(img, coordinates_str, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)



#################
## MANGA STUFF ##
#################
def get_chapter_links():

    url = "https://readchainsaw-man.com/" # UPDATE LINK IF NEEDED

    response = requests.get(url)

    if response.status_code == 200:
        # parse the HTML content of the webpage
        soup = BeautifulSoup(response.content, "html.parser")
        
        # find all the links in there
        all_links = soup.find_all("a")
        
        # extract href attribute (link) from each anchor tag and store them in an array
        chapter_links_array = [link['href'] for link in all_links if 'chapter' in link.text.lower()]

        # remove duplicates
        no_dup_chapters = []
        
        for chapter in chapter_links_array:
            if chapter not in no_dup_chapters:
                no_dup_chapters.append(chapter)

        no_dup_chapters.reverse()

        return no_dup_chapters

    else:
        print("Failed to retrieve webpage.")


# func to increase the counter
def increase_counter(event=None):
    global counter, link_opened
    if counter < len(chapter_links) and not link_opened:
        counter += 1
        counter_label.config(text="Chapter: " + str(counter))
        # print(f"Opening chapter {counter}: {chapter_links[counter - 1]}")
    
# func to decrease the counter
def decrease_counter(event=None):
    global counter, link_opened
    if counter > 1 and not link_opened:
        counter -= 1
        counter_label.config(text="Chapter: " + str(counter))
        # print(f"Opening chapter {counter}: {chapter_links[counter - 1]}")

# func to open the respective link
def open_link():
    global counter, chapter_links, link_opened
    if 0 < counter <= len(chapter_links) and not link_opened:
        webbrowser.open(chapter_links[counter - 1])
        link_opened = True




#####################
## STARTING CAMERA ##
#####################
# start capturing webcam video
cap = cv2.VideoCapture(0)

# initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


## MANGA STUFF
# get chapter links
chapter_links = get_chapter_links()

# counter variable
counter = 0

# create GUI
root = tk.Tk()
root.title("Counter GUI")


# label to display the counter value
counter_label = tk.Label(root, text="Chapter: " + str(counter))
counter_label.pack(pady=10)

# button to open the respective link
open_button = tk.Button(root, text="Open Link", command=open_link)
open_button.pack(pady=5)



with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:

    # these two variables are to set a cooldown timer for going to the next/prev chapter
    cooldown_duration = 5  # seconds
    last_triggered_time = time.time() 

    while cap.isOpened():
        # read frames from webcam
        success, img = cap.read()
        image = img.copy()

        # check for empty frames
        if not success:
            print("Ignoring empty camera frame.")
            break  # break the loop if frame is empty

        # flip the image
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

        # process image with MediaPipe Hands
        results = hands.process(image)

        # draw hand landmarks on the image
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


        # "results.multi_hand_landmarks" gets the normalized x, y, and z coordinates of each landmark
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # calculate the angle of hand
                angle_result = orientation((hand_landmarks.landmark[0].x, hand_landmarks.landmark[0].y), (hand_landmarks.landmark[9].x, hand_landmarks.landmark[9].y))
                # print("Angle:", angle_result)

                # Check which fingers are closed
                closed_fingers = finger(hand_landmarks.landmark, "finger")
                # print("Closed fingers:", closed_fingers)

                # if closed_fingers == [1, 2, 3, 4]:
                #     print("all fingers are closed")

                # if direction(angle_result) == "right":
                #     print("your hand is facing right")

                ## HERE, call function to choose chapter and show gui ##
                if angle_result == "right":
                    increase_counter()
                if angle_result == "left":
                    decrease_counter()

                # Choose chapters
                if closed_fingers == [1, 2, 3, 4]:
                    open_link()


                # ## HERE, we can navigate page and scroll up and down (has speed up mode)
                if link_opened and closed_fingers == [2, 3, 4] and angle_result == "up":
                    pyautogui.scroll(-90)
                if link_opened and closed_fingers == [] and angle_result == "up":
                    pyautogui.scroll(-250)
                
                if link_opened and closed_fingers == [3, 4] and (angle_result == "right" or angle_result == "left"):
                    pyautogui.scroll(90)
                if link_opened and closed_fingers == [] and (angle_result == "right" or angle_result == "left"):
                    pyautogui.scroll(250)

                
                ## HERE, we can go to the next chapter
                if closed_fingers == [2, 3] and angle_result == "right" and time.time() - last_triggered_time >= cooldown_duration:
                     # Check if the cooldown period has elapsed
                    cv2.putText(image, "+", (450, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(image, "+", (450, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    index_finger_tip = hand_landmarks.landmark[8]
                    pinky_finger_tip = hand_landmarks.landmark[20]
                    if x_coordinate(index_finger_tip) > 0.7 and x_coordinate(pinky_finger_tip) > 0.7:
                        # print(x_coordinate(index_finger_tip))
                        counter += 1
                        pyautogui.hotkey('ctrl', 'w')
                        webbrowser.open(chapter_links[counter - 1])
                        last_triggered_time = time.time()

                if closed_fingers == [2, 3] and angle_result == "left" and time.time() - last_triggered_time >= cooldown_duration:
                     # Check if the cooldown period has elapsed
                    cv2.putText(image, "+", (120, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    cv2.putText(image, "+", (120, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    index_finger_tip = hand_landmarks.landmark[8]
                    pinky_finger_tip = hand_landmarks.landmark[20]
                    if x_coordinate(index_finger_tip) < 0.25 and x_coordinate(pinky_finger_tip) < 0.25:
                        # print(x_coordinate(index_finger_tip))
                        counter = counter - 1
                        pyautogui.hotkey('ctrl', 'w')
                        webbrowser.open(chapter_links[counter - 1])
                        last_triggered_time = time.time()


                ## HERE, we can close out the browser and maybe go to Canvas
                if closed_fingers == [3, 4] and angle_result == "down" and time.time() - last_triggered_time >= cooldown_duration:
                    pyautogui.hotkey('ctrl', 'w')
                    last_triggered_time = time.time()
                    webbrowser.open("https://my.unf.edu/campusm/home#menu")
                    # break

        # display processed image with landmarks
        cv2.imshow('Hands-Free Manga Navigator', image)

        # update GUI
        root.update_idletasks()
        root.update()

        # break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        
# release webcam and close all windows
cap.release()
cv2.destroyAllWindows()

root.mainloop()