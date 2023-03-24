import cv2 
import pytesseract

IMG_DIR = 'images_processed/croppednoiseGS/' #directory storing pre-processed images
TXT_DIR = 'texts_processed/croppednoiseGSpsm1/' # directory storing OCR result from the pre-processed images

txt_file = open("check_cropped.txt", "r", encoding='UTF-8')
file_content = txt_file.read()
list_cropped = file_content.split("\n") #each line format: nr
txt_file.close()

product_type = ["n"]#, "v"]
#test images from 1 to 20 for both non-vegan and vegan products
for t in product_type:
    for x in range(1, 101):

        if(str(x) not in list_cropped):
            continue
        
        img_name = t + str(x)
        #import image
        image = cv2.imread(IMG_DIR + img_name + '.png')

        #OCR configuration
        custom_config = r'--oem 3 --psm 1'

        #extract text from preprocesed image, and store in in a text file
        text = pytesseract.image_to_string(image, config=custom_config, lang='lav')
        sourceFile = open(TXT_DIR + img_name + ".txt", 'w', encoding='UTF-8')
        print(text, file = sourceFile)
        sourceFile.close()