import cv2 
import pytesseract

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

IMG_DIR = 'images_processed/cropped/' # directory with the original images
IMG_DIR_AFTER = 'images_processed/croppedGS/' #directory storing pre-processed images
TXT_DIR = 'texts_processed/croppedGS/' # directory storing OCR result from the pre-processed images

#prepare animal based ingredient check list for each product
txt_file = open("check_cropped.txt", "r", encoding='UTF-8')
file_content = txt_file.read()
list_cropped = file_content.split("\n") #each line format: nr
txt_file.close()
#print(list_cropped)

product_type = ["n"]#, "v"]
#test images from 1 to 20 for both non-vegan and vegan products
for t in product_type:
    for x in range(1, 101):

        if(str(x) not in list_cropped):
            continue

        img_name = t + str(x)
        #import image
        image = cv2.imread(IMG_DIR + img_name + '.jpg')

        #convert image to black and white, and store in a directory
        image2 = get_grayscale(image)
        cv2.imwrite(IMG_DIR_AFTER + img_name + ".png", image2)

        #OCR configuration
        custom_config = r'--oem 3 --psm 6'

        #extract text from preprocesed image, and store in in a text file
        text = pytesseract.image_to_string(image2, config=custom_config, lang='lav')
        sourceFile2 = open(TXT_DIR + img_name + ".txt", 'w', encoding='UTF-8')
        print(text, file = sourceFile2)
        sourceFile2.close()