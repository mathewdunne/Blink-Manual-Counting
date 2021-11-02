import pyscreenshot
import pytesseract
import time
import keyboard

# border around frame counter (vertical = y)
leftLimit = 1399
rightLimit = 1688
topLimit = 251
bottomLimit = 314

markFrameKey = 'F8'
removeLastKey = 'F7'

markFrameAlreadyPressed = False
removeLastAlreadyPressed = False

listOfBlinkFrames = []

# path to tesseract exe
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def getFrameNumber():
    # take screenshot of window
    rawImage = pyscreenshot.grab(bbox=(leftLimit, topLimit, rightLimit, bottomLimit))

    # extract text from image
    ocrString = pytesseract.image_to_string(rawImage)
    ocrString = ocrString[:-2] # remove blank characters from end of number

    return int(ocrString)


# start of main
while True:
    # check if mark frame key is pressed
    if keyboard.is_pressed(markFrameKey) and not markFrameAlreadyPressed:
        markFrameAlreadyPressed = True

        frameNum = getFrameNumber()
        listOfBlinkFrames.append(frameNum)

        print('Blink #' + str(len(listOfBlinkFrames)) + ' recorded at frame #' + str(frameNum))

    elif not keyboard.is_pressed(markFrameKey):
        markFrameAlreadyPressed = False

    # check if remove last frame key is pressed
    if keyboard.is_pressed(removeLastKey) and not removeLastAlreadyPressed:
        removeLastAlreadyPressed = True

        print('Removed blink #' + str(len(listOfBlinkFrames)))
        listOfBlinkFrames.pop()

    elif not keyboard.is_pressed(removeLastKey):
        removeLastAlreadyPressed = False
    time.sleep(0.01)

    if keyboard.is_pressed('ctrl+Q'):
        break

print(listOfBlinkFrames)





