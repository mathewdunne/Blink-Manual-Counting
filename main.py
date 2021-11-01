import pyscreenshot
import pytesseract
import time

# border around frame counter (vertical = y)
leftLimit = 1399
rightLimit = 1688
topLimit = 251
bottomLimit = 314

# path to tesseract exe
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

time.sleep(2)
# take screenshot of window
rawImage = pyscreenshot.grab(bbox=(leftLimit, topLimit, rightLimit, bottomLimit))

# extract text from image
ocrString = pytesseract.image_to_string(rawImage)
print(ocrString)
