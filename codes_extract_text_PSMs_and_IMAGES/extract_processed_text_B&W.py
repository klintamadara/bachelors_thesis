import cv2 
import pytesseract

def get_blackwhite(image):
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)
    return blackAndWhiteImage

IMG_DIR = 'images_raw/' # directory with the original images
IMG_DIR_AFTER = 'images_processed/B&W/' #directory storing pre-processed images
TXT_DIR = 'texts_processed/B&W/' # directory storing OCR result from the pre-processed images

#manipulate images from 1 to 100 for both non-vegan and vegan products
product_type = ["n","v"]
for t in product_type:
    for x in range(1, 101):
        img_name = t + str(x)

        #import image
        image = cv2.imread(IMG_DIR + img_name + '.jpg')

        #convert image to black and white, and store in a directory
        image2 = get_blackwhite(image)
        cv2.imwrite(IMG_DIR_AFTER + img_name + "_B&W.png", image2)

        #OCR configuration
        custom_config = r'--oem 3 --psm 6'

        #extract text from preprocesed image, and store in in a text file
        text = pytesseract.image_to_string(image2, config=custom_config, lang='lav')
        sourceFile2 = open(TXT_DIR + img_name + ".txt", 'w', encoding='UTF-8')
        print(text, file = sourceFile2)
        sourceFile2.close()