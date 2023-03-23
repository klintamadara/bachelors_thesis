#testing accuracy of page segmentation modes (PSMs)
import Levenshtein
import string

def Jaccard_similarity(x,y):
    if(len(x) == 0 or len(y) == 0):
        return 0
    z=set(x).intersection(set(y))
    a=float(len(z))/(len(x)+len(y)-len(z))
    return a

def overlap_coefficient(x,y):
    if(len(x) == 0 or len(y) == 0):
        return 0
    z=set(x).intersection(set(y))
    a=float(len(z))/min(len(x),len(y))
    return a

TXT_DIR_PSM1 = 'texts_raw/psm1/' # directory storing OCR result using PSM 1
TXT_DIR_PSM3 = 'texts_raw/psm3/' # directory storing OCR result using PSM 3
TXT_DIR_PSM6 = 'texts_raw/' # directory storing OCR result using PSM 6
TXT_DIR_PSM11 = 'texts_raw/psm11/' # directory storing OCR result using PSM 11
TXT_DIR_PSM12 = 'texts_raw/psm12/' # directory storing OCR result using PSM 12
TXT_DIR_PSM13 = 'texts_raw/psm13/' # directory storing OCR result using PSM 13
TXT_DIR_TRU = 'texts_actual/' #directory storing manually prepared correct ingredients lists -> for testing
TXT_DIR_RSLTS = 'results/' #directory storing all of the results

#code compares results from OCR to the correct ingredients list and returns Levenshtein and Jaccard similarity, as well as overlap coefficient
#for each test case, saves it in the result txt file
results = 'PSMs'

#erase if there was content in the text files before and write title
result_file_psm3 = open(TXT_DIR_RSLTS + results + "_psm3.txt", 'w')
print("PSM3 Levenshtein; PSM3 Jaccard; PSM3 Overlap", file = result_file_psm3)

result_file_psm6 = open(TXT_DIR_RSLTS + results + "_psm6.txt", 'w')
print("PSM6 Levenshtein; PSM6 Jaccard; PSM6 Overlap", file = result_file_psm6)

result_file_psm1 = open(TXT_DIR_RSLTS + results + "_psm1.txt", 'w')
print("PSM1 Levenshtein; PSM1 Jaccard; PSM1 Overlap", file = result_file_psm1)

result_file_psm11 = open(TXT_DIR_RSLTS + results + "_psm11.txt", 'w')
print("PSM11 Levenshtein; PSM11 Jaccard; PSM11 Overlap", file = result_file_psm11)

result_file_psm12 = open(TXT_DIR_RSLTS + results + "_psm12.txt", 'w')
print("PSM12 Levenshtein; PSM12 Jaccard; PSM12 Overlap", file = result_file_psm12)


result_file_all = open(TXT_DIR_RSLTS + results + ".txt", 'w')
print("ID;PSM1 Lev;PSM1 Jac;PSM1 Ove;PSM3 Lev;PSM3 Jac;PSM3 Ove;PSM6 Lev;PSM6 Jac;PSM6 Ove;PSM11 Lev;PSM11 Jac;PSM11 Ove;PSM12 Lev;PSM12 Jac;PSM12 Ove", file = result_file_all)

result_file_psm3.close()
result_file_psm6.close()
result_file_psm1.close()
result_file_psm11.close()
result_file_psm12.close()
result_file_all.close()

result_file_psm3 = open(TXT_DIR_RSLTS + results + "_psm3.txt", 'a')
result_file_psm6 = open(TXT_DIR_RSLTS + results + "_psm6.txt", 'a')
result_file_psm1 = open(TXT_DIR_RSLTS + results + "_psm1.txt", 'a')
result_file_psm11 = open(TXT_DIR_RSLTS + results + "_psm11.txt", 'a')
result_file_psm12 = open(TXT_DIR_RSLTS + results + "_psm12.txt", 'a')
result_file_all = open(TXT_DIR_RSLTS + results + ".txt", 'a')


#calculate scores for 200 images, both non-vegan (n) and vegan (v) products (100 samples each)
product_type = ["n", "v"]
for t in product_type:
    for x in range(1, 101):
        img_name = t + str(x)

        #prepare the correct ingredients list for testing purposes
        txt_tru = open(TXT_DIR_TRU + img_name + ".txt", "r", encoding='UTF-8')
        txt_tru_content = txt_tru.read()

        #prepare the OCR result from psm3 for testing purposes
        txt_psm3 = open(TXT_DIR_PSM3 + img_name + ".txt", "r", encoding='UTF-8')
        txt_psm3_content = txt_psm3.read()
        #prepare the OCR result from psm6 for testing purposes
        txt_psm6 = open(TXT_DIR_PSM6 + img_name + ".txt", "r", encoding='UTF-8')
        txt_psm6_content = txt_psm6.read()
        #prepare the OCR result from psm13 image for testing purposes
        txt_psm1 = open(TXT_DIR_PSM1 + img_name + ".txt", "r", encoding='UTF-8')
        txt_psm1_content = txt_psm1.read()
        #prepare the OCR result from psm13 image for testing purposes
        txt_psm11 = open(TXT_DIR_PSM11 + img_name + ".txt", "r", encoding='UTF-8')
        txt_psm11_content = txt_psm11.read()
        #prepare the OCR result from psm13 image for testing purposes
        txt_psm12 = open(TXT_DIR_PSM12 + img_name + ".txt", "r", encoding='UTF-8')
        txt_psm12_content = txt_psm12.read()

        #create lists, separating text in words. Remove unnecessary spaces and other redundant characters
        words_separate_psm3 = [s.strip(string.punctuation) for s in txt_psm3_content.split()]
        words_separate_psm3 = [s.strip() for s in words_separate_psm3 if s != '' and s!= ' ']

        words_separate_psm6 = [s.strip(string.punctuation) for s in txt_psm6_content.split()]
        words_separate_psm6 = [s.strip() for s in words_separate_psm6 if s != '' and s!= ' ']

        words_separate_psm1 = [s.strip(string.punctuation) for s in txt_psm1_content.split()]
        words_separate_psm1 = [s.strip() for s in words_separate_psm1 if s != '' and s!= ' ']

        words_separate_psm11 = [s.strip(string.punctuation) for s in txt_psm11_content.split()]
        words_separate_psm11 = [s.strip() for s in words_separate_psm11 if s != '' and s!= ' ']

        words_separate_psm12 = [s.strip(string.punctuation) for s in txt_psm12_content.split()]
        words_separate_psm12 = [s.strip() for s in words_separate_psm12 if s != '' and s!= ' ']

        words_separate_tru = [s.strip(string.punctuation) for s in txt_tru_content.split()]
        words_separate_tru = [s.strip() for s in words_separate_tru if s != '' and s!= ' ']

        #calculate similarity scores and write them to file 
        Levenshtein_psm3 = str(Levenshtein.distance(txt_psm3_content, txt_tru_content))
        Levenshtein_psm6 = str(Levenshtein.distance(txt_psm6_content, txt_tru_content))
        Levenshtein_psm1 = str(Levenshtein.distance(txt_psm1_content, txt_tru_content))
        Levenshtein_psm11 = str(Levenshtein.distance(txt_psm11_content, txt_tru_content))
        Levenshtein_psm12 = str(Levenshtein.distance(txt_psm12_content, txt_tru_content))

        Jaccard_psm3 = str(Jaccard_similarity(words_separate_psm3, words_separate_tru))
        Jaccard_psm6 = str(Jaccard_similarity(words_separate_psm6, words_separate_tru))
        Jaccard_psm1 = str(Jaccard_similarity(words_separate_psm1, words_separate_tru))
        Jaccard_psm11 = str(Jaccard_similarity(words_separate_psm11, words_separate_tru))
        Jaccard_psm12 = str(Jaccard_similarity(words_separate_psm12, words_separate_tru))

        overlap_psm3 = str(overlap_coefficient(words_separate_psm3, words_separate_tru))
        overlap_psm6 = str(overlap_coefficient(words_separate_psm6, words_separate_tru))
        overlap_psm11 = str(overlap_coefficient(words_separate_psm11, words_separate_tru))
        overlap_psm12 = str(overlap_coefficient(words_separate_psm12, words_separate_tru))
        overlap_psm1 = str(overlap_coefficient(words_separate_psm1, words_separate_tru))
        
        """
        Jaccard_psm3 = str(round(Jaccard_similarity(words_separate_psm3, words_separate_tru),4))
        Jaccard_psm6 = str(round(Jaccard_similarity(words_separate_psm6, words_separate_tru),4))
        Jaccard_psm13 = str(round(Jaccard_similarity(words_separate_psm13, words_separate_tru),4))

        overlap_psm3 = str(round(overlap_coefficient(words_separate_psm3, words_separate_tru),4))
        overlap_psm6 = str(round(overlap_coefficient(words_separate_psm6, words_separate_tru),4))
        overlap_psm13 = str(round(overlap_coefficient(words_separate_psm13, words_separate_tru),4))
        """
        print(img_name + ";" + Levenshtein_psm3 + ";" + Jaccard_psm3 + ";" + overlap_psm3, file = result_file_psm3)
        print(img_name + ";" + Levenshtein_psm6 + ";" + Jaccard_psm6 + ";" + overlap_psm6, file = result_file_psm6)
        print(img_name + ";" + Levenshtein_psm1 + ";" + Jaccard_psm1 + ";" + overlap_psm1, file = result_file_psm1)
        print(img_name + ";" + Levenshtein_psm11 + ";" + Jaccard_psm11 + ";" + overlap_psm11, file = result_file_psm11)
        print(img_name + ";" + Levenshtein_psm12 + ";" + Jaccard_psm12 + ";" + overlap_psm12, file = result_file_psm12)

        print(img_name + ";" + Levenshtein_psm1 + ";" + Jaccard_psm1 + ";" + overlap_psm1 + ";" + Levenshtein_psm3 + ";" + Jaccard_psm3 + ";" + overlap_psm3 + ";" + Levenshtein_psm6 + ";" + Jaccard_psm6 + ";" + overlap_psm6 + ";" + Levenshtein_psm11 + ";" + Jaccard_psm11 + ";" + overlap_psm11 + ";" + Levenshtein_psm12 + ";" + Jaccard_psm12 + ";" + overlap_psm12, file = result_file_all)


txt_tru.close()
txt_psm1.close()
txt_psm6.close()
txt_psm3.close()
txt_psm11.close()
txt_psm12.close()
result_file_psm3.close()
result_file_psm6.close()
result_file_psm1.close()
result_file_psm11.close()
result_file_psm12.close()
result_file_all.close()