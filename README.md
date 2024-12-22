# Hands-Free Manga Navigator

## Description

The **Hands-Free Manga Navigator** is a Python-based application that allows users to navigate through manga chapters using a webcam. The application employs computer vision techniques for hand detection, gesture recognition, and web browsing control, providing a hands-free manga reading experience.

The application uses the **MediaPipe Hands** library to accurately detect hand landmarks (locations of joints and fingertips). By leveraging these landmarks, the program determines the hand's orientation (up, down, left, or right) and tracks which fingers are held up. Using this information, it recognizes specific gestures and maps them to commands, allowing seamless manga navigation.

**Note**: The current manga website may be shut down - please verify before use.

---

## System Requirements

- **Python**
- **Required Libraries**:
  - OpenCV
  - MediaPipe Hands
  - PyAutoGUI
  - BeautifulSoup
  - Tkinter
- **Web Browser**: Chrome, Firefox, Brave, etc.
- **Hardware**: Webcam

---

## Usage

1. **Run the Program**:  
   Open a terminal and execute:

   ```bash
   python main.py
   ```

2. **Position Yourself**:  
   Sit in front of the webcam. Ensure proper lighting for accurate hand detection.

3. **GUI and Live Feed**:  
    A GUI will pop up along with a live webcam feed. Use the following gestures for navigation:
   ![imgs\nav.png](#)

---

### **Gestures and Controls**

#### **Navigate Between Chapters**

- **Tilt Hand Left/Right**:  
  Move to the previous or next chapter.

---

#### **Choose a Manga Chapter**

- **Close Your Fingers**:  
  The selected chapter will open in your browser.
  ![imgs\close.png](#)

---

#### **Scroll in the Browser**

- **Scroll Down**:  
  ![imgs\scroll_down.png](#)

- **Scroll Down Faster**:  
  ![imgs\scroll_down_faster.png](#)

- **Scroll Up**:  
  ![imgs\scroll_up.png](#)

- **Scroll Up Faster**:  
  ![imgs\scroll_up_faster.png](#)

---

#### **Next/Previous Chapter**

- **Next Chapter**:

  - Hold your hand sideways to the right and stick out your index and pinky fingers.
  - Two green `+` signs will appear.
  - Drag your hand past the signs to load the next chapter.

  ![imgs\next_chapter.png](#)

- **Previous Chapter**:

  - Perform the same gesture as above, but towards the left.
  - Two blue `+` signs will appear.

  ![imgs\prev_chapter.png](#)

---

#### **Switch Tabs (Go to MyWings)**

- **Upside-Down Peace Sign**:

  - Hold an upside-down peace sign to close the current chapter and open a **MyWings** tab.
  - _(Note: The Python script does not terminate in this version.)_

  ![imgs\peace.png](#)

---

## Notes

- Ensure your mouse is hovering over the browser for scroll gestures to work.
- Proper lighting and a stable hand position are critical for accurate gesture recognition.

---

## Future Improvements

- Make usable for universally any manga site.

---
