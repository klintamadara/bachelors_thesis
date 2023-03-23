import cv2 
import pytesseract

IMG_DIR = 'images_processed/GSpsm1_all/' # directory with the original images
IMG_DIR_AFTER = 'images_processed/noiseGSpsm1/' #directory storing pre-processed images
TXT_DIR = 'texts_processed/noiseGSpsm1/' # directory storing OCR result from the pre-processed images

product_type = ["n", "v"]

#test images from 1 to 20 for both non-vegan and vegan products
for t in product_type:
    for x in range(1, 101):
        img_name = t + str(x)
        #import image
        image = cv2.imread(IMG_DIR + img_name + '.png')

        #remove noise, and store in a directory
        image2 = cv2.fastNlMeansDenoising(image,None,10,7,21)
        cv2.imwrite(IMG_DIR_AFTER + img_name + ".png", image2)

        #OCR configuration
        custom_config = r'--oem 3 --psm 1'

        #extract text from preprocesed image, and store in in a text file
        text = pytesseract.image_to_string(image2, config=custom_config, lang='lav')
        sourceFile = open(TXT_DIR + img_name + ".txt", 'w', encoding='UTF-8')
        print(text, file = sourceFile)
        sourceFile.close()