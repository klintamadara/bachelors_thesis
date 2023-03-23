import cv2
import pytesseract

IMG_DIR = 'images_raw/' # directory with the original images
TXT_DIR = 'texts_raw/psm12/' # directory storing OCR result from the original images

#extract OCR result from raw images for samples 1-100 both non-vegan (n) and vegan (v) products
product_type = ["n","v"]
for t in product_type:
    for x in range(1, 101):
        img_name = t + str(x)

        #import image
        image = cv2.imread(IMG_DIR + img_name + '.jpg')
        #OCR configuration:
        #--psm -> page segmentation mode. 13 - "Raw line. Treat the image as a single text line, bypassing hacks that are Tesseract-specific."
        #--oem -> OCR Engine mode. 3 is default, based on what is available.
        custom_config = r'--oem 3 --psm 12'

        #extract text from the original image using PyTesseract, Latvian language
        text_original = pytesseract.image_to_string(image, config=custom_config, lang='lav')
        #save the result in a text file
        sourceFile = open(TXT_DIR + img_name + ".txt", 'w', encoding='UTF-8')
        print(text_original, file = sourceFile)
        sourceFile.close()