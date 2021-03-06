import pyscreenshot
import pytesseract
import time
import keyboard
import os
import csv
from PIL import ImageEnhance

# border around frame counter (vertical = y)
leftLimit = 1208
rightLimit = 1395
topLimit = 721
bottomLimit = 773
markFrameKey = 'F8'
removeLastKey = 'F7'

# values that will be plotted against frame number
defaultVal = 0.3
blinkVal = 0.1

# for sharpening filter
enhancementFactor = 2

markFrameAlreadyPressed = False
removeLastAlreadyPressed = False
goodInput = False

listOfBlinkFrames = []

# set up where to save csv
dataPath = os.path.join(os.path.expanduser("~"), "Documents", "HMS-Blink-Data")
if not os.path.isdir(dataPath):
    os.mkdir(dataPath)

# path to tesseract exe
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def getFrameNumber():
    # take screenshot of window
    rawImage = pyscreenshot.grab(bbox=(leftLimit, topLimit, rightLimit, bottomLimit))

    # process image
    enhancer = ImageEnhance.Sharpness(rawImage)
    processedIm = enhancer.enhance(enhancementFactor)
    #processedIm.save('im.png')

    # extract text from image
    ocrString = pytesseract.image_to_string(processedIm)
    print("Raw Text: '" + ocrString +"' end")

    # remove possible characters from number
    ocrString = ocrString.replace(',', '')
    ocrString = ocrString.replace('.', '')
    ocrString = ocrString.replace(')', '')
    ocrString = ocrString.replace(']', '')

    # narrow string down to only frame number
    ocrStringList = ocrString.split()
    ocrString = ocrStringList[1]

    #print("Filtered Text: '" + ocrString +"' end")
    return int(ocrString)


# start of main
while True:
    # check if mark frame key is pressed
    if keyboard.is_pressed(markFrameKey) and not markFrameAlreadyPressed:
        markFrameAlreadyPressed = True

        try:
            frameNum = getFrameNumber()
            listOfBlinkFrames.append(frameNum)
            print('\nBlink #' + str(len(listOfBlinkFrames)) + ' recorded at frame #' + str(frameNum))
        except:
            print('Unable to read frame value! Check position of screen')

    elif not keyboard.is_pressed(markFrameKey):
        markFrameAlreadyPressed = False

    # check if remove last frame key is pressed
    if keyboard.is_pressed(removeLastKey) and not removeLastAlreadyPressed:
        removeLastAlreadyPressed = True

        try:
            listOfBlinkFrames.pop()
            print('Removed blink #' + str(len(listOfBlinkFrames)+1))
        except:
            print('Blink List is empty! Nothing to remove!')

    elif not keyboard.is_pressed(removeLastKey):
        removeLastAlreadyPressed = False
    time.sleep(0.01)

    if keyboard.is_pressed('ctrl+Q'):
        break

print('\nHere is the list of blink frames generated:')
print(listOfBlinkFrames)

# get the number of frames in the video
totalFrames = input('\nPlease enter the total number of frames in the video:\n')

while not goodInput:

    try:
        if int(totalFrames) != 0:
            goodInput = True
            totalFrames = int(totalFrames)
    except:
        totalFrames = input('\nError: Please enter a valid number:\n')


# write data to csv:
with open(os.path.join(dataPath, "GroundTruthData_" + str(int(time.time())) + ".csv"), "w", newline="") as f:
    writer = csv.writer(f)

    writer.writerow(['Frame', 'Approx EAR'])

    for frameCount in range(1, totalFrames+1):

        if frameCount in listOfBlinkFrames:
            rowToWrite = [frameCount, blinkVal]
        else:
            rowToWrite = [frameCount, defaultVal]

        writer.writerow(rowToWrite)

print('Data written successfully!')



