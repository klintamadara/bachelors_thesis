#testing efficiency in improving OCR accuracy of different image pre-processing techniques
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

TXT_DIR_RAW = 'texts_raw/' # directory storing OCR result from images without pre-processing
TXT_DIR_BGREM = 'texts_processed/BGremove/' # directory storing OCR result using PSM 13
TXT_DIR_BW = 'texts_processed/B&W/' # directory storing OCR result using PSM 3
TXT_DIR_GS = 'texts_processed/GS/' # directory storing OCR result using PSM 6
TXT_DIR_BW_BG = 'texts_processed/B&W+BGremove/' # directory storing OCR result using PSM 3
TXT_DIR_GS_BG = 'texts_processed/GS+BGremove/' # directory storing OCR result using PSM 6
TXT_DIR_NOISE = 'texts_processed/noise/' # directory storing OCR result using PSM 3
TXT_DIR_NOISE_GS = 'texts_processed/noiseGS/' # directory storing OCR result using PSM 6
TXT_DIR_NOISE_GS_BG = 'texts_processed/noiseGS/' # directory storing OCR result using PSM 6

TXT_DIR_TRU = 'texts_actual/' #directory storing manually prepared correct ingredients lists -> for testing
TXT_DIR_RSLTS = 'results/' #directory storing all of the results

#code compares results from OCR to the correct ingredients list and returns Levenshtein and Jaccard similarity, as well as overlap coefficient
#for each test case, saves it in the result txt file
results = 'IMAGES'

#erase if there was content in the text file before and write title
result_file_all = open(TXT_DIR_RSLTS + results + ".txt", 'w')
print("ID;original Lev;original Jac;original Ove; B&W Lev;B&W Jac;B&W Ove;GS Lev;GS Jac;GS Ove;GS noise remove Lev;GS noise remove Jac;GS noise remove Ove;BG remove Lev;BG remove Jac;BG remove Ove;BG remove + BW Lev;BG remove + BW Jac;BG remove + BW Ove;BG remove + GS Lev;BG remove + GS Jac;BG remove + GS Ove;Noise remove Lev;Noise remove Jac;Noise remove Ove;GS noise and BG rem Lev;GS noise and BG rem Jac;GS noise and BG rem Ove", file = result_file_all)
result_file_all.close()

result_file_all = open(TXT_DIR_RSLTS + results + ".txt", 'a')

def get_list(text): 
    list_new = [s.strip(string.punctuation) for s in text.split()]
    list_new = [s.strip() for s in list_new if s != '' and s!= ' ']
    return list_new

#calculate scores for 200 images, both non-vegan (n) and vegan (v) products (100 samples each)
product_type = ["n", "v"]
for t in product_type:
    for x in range(1, 101):
        img_name = t + str(x)

        #prepare the correct ingredients list for testing purposes
        txt_tru = open(TXT_DIR_TRU + img_name + ".txt", "r", encoding='UTF-8')
        txt_tru_content = txt_tru.read()

        #prepare the OCR result from psm3 for testing purposes
        txt_bg_rem = open(TXT_DIR_BGREM + img_name + ".txt", "r", encoding='UTF-8')
        txt_bg_rem_content = txt_bg_rem.read()
        #prepare the OCR result from psm6 for testing purposes
        txt_bw = open(TXT_DIR_BW + img_name + ".txt", "r", encoding='UTF-8')
        txt_bw_content = txt_bw.read()
        #prepare the OCR result from psm13 image for testing purposes
        txt_gs = open(TXT_DIR_GS + img_name + ".txt", "r", encoding='UTF-8')
        txt_gs_content = txt_gs.read()
        #prepare the OCR result from psm3 for testing purposes
        txt_bwANDbg = open(TXT_DIR_BW_BG + img_name + ".txt", "r", encoding='UTF-8')
        txt_bwANDbg_content = txt_bwANDbg.read()
        #prepare the OCR result from psm6 for testing purposes
        txt_gsANDbg = open(TXT_DIR_GS_BG + img_name + ".txt", "r", encoding='UTF-8')
        txt_gsANDbg_content = txt_gsANDbg.read()
        #prepare the OCR result from psm13 image for testing purposes
        txt_noise = open(TXT_DIR_NOISE + img_name + ".txt", "r", encoding='UTF-8')
        txt_noise_content = txt_noise.read()
        #prepare the OCR result from psm13 image for testing purposes
        txt_noise_gs = open(TXT_DIR_NOISE_GS + img_name + ".txt", "r", encoding='UTF-8')
        txt_noise_gs_content = txt_noise_gs.read()


        #prepare the OCR result from psm13 image for testing purposes
        txt_raw = open(TXT_DIR_RAW + img_name + ".txt", "r", encoding='UTF-8')
        txt_raw_content = txt_raw.read()

        #create lists, separating text in words. Remove unnecessary spaces and other redundant characters
        words_separate_raw = get_list(txt_raw_content)
        words_separate_tru = get_list(txt_tru_content)
        words_separate_bw = get_list(txt_bw_content)
        words_separate_gs = get_list(txt_gs_content)
        words_separate_bgrem = get_list(txt_bg_rem_content)
        words_separate_noise = get_list(txt_noise_content)
        words_separate_noise_gs = get_list(txt_noise_gs_content)
        words_separate_gs_bg = get_list(txt_gsANDbg_content)
        words_separate_bw_bg = get_list(txt_bwANDbg_content)

        #calculate similarity scores and write them to file 
        Levenshtein_noise = str(Levenshtein.distance(txt_noise_content, txt_tru_content))
        Levenshtein_noise_gs = str(Levenshtein.distance(txt_noise_gs_content, txt_tru_content))
        Levenshtein_bg = str(Levenshtein.distance(txt_bg_rem_content, txt_tru_content))
        Levenshtein_bw = str(Levenshtein.distance(txt_bw_content, txt_tru_content))
        Levenshtein_gs = str(Levenshtein.distance(txt_gs_content, txt_tru_content))
        Levenshtein_gs_bg = str(Levenshtein.distance(txt_gsANDbg_content, txt_tru_content))
        Levenshtein_bw_bg = str(Levenshtein.distance(txt_bwANDbg_content, txt_tru_content))
        Levenshtein_raw = str(Levenshtein.distance(txt_raw_content, txt_tru_content))


        Jaccard_noise = str(Jaccard_similarity(words_separate_noise, words_separate_tru))
        Jaccard_noise_gs = str(Jaccard_similarity(words_separate_noise_gs, words_separate_tru))
        Jaccard_bg = str(Jaccard_similarity(words_separate_bgrem, words_separate_tru))
        Jaccard_bw = str(Jaccard_similarity(words_separate_bw, words_separate_tru))
        Jaccard_gs = str(Jaccard_similarity(words_separate_gs, words_separate_tru))
        Jaccard_gs_bg = str(Jaccard_similarity(words_separate_gs_bg, words_separate_tru))
        Jaccard_bw_bg = str(Jaccard_similarity(words_separate_bw_bg, words_separate_tru))
        Jaccard_raw = str(Jaccard_similarity(words_separate_raw, words_separate_tru))

        overlap_noise = str(overlap_coefficient(words_separate_noise, words_separate_tru))
        overlap_noise_gs = str(overlap_coefficient(words_separate_noise_gs, words_separate_tru))
        overlap_bg = str(overlap_coefficient(words_separate_bgrem, words_separate_tru))
        overlap_bw = str(overlap_coefficient(words_separate_bw, words_separate_tru))
        overlap_gs = str(overlap_coefficient(words_separate_gs, words_separate_tru))
        overlap_gs_bg = str(overlap_coefficient(words_separate_gs_bg, words_separate_tru))
        overlap_bw_bg = str(overlap_coefficient(words_separate_bw_bg, words_separate_tru))
        overlap_raw = str(overlap_coefficient(words_separate_raw, words_separate_tru))

        print(img_name + ";" + Levenshtein_raw + ";" + Jaccard_raw + ";" + overlap_raw + \
              ";" + Levenshtein_bw + ";" + Jaccard_bw + ";" + overlap_bw + \
                ";" + Levenshtein_gs + ";" + Jaccard_gs + ";" + overlap_gs + \
                ";" + Levenshtein_noise_gs + ";" + Jaccard_noise_gs + ";" + overlap_noise_gs + \
                ";" + Levenshtein_bg + ";" + Jaccard_bg + ";" + overlap_bg + \
                ";" + Levenshtein_bw_bg + ";" + Jaccard_bw_bg + ";" + overlap_bw_bg + \
                ";" + Levenshtein_gs_bg + ";" + Jaccard_gs_bg + ";" + overlap_gs_bg + \
                ";" + Levenshtein_noise + ";" + Jaccard_noise + ";" + overlap_noise, file = result_file_all)


txt_tru.close()
txt_noise_gs.close()
txt_noise.close()
txt_bw.close()
txt_gs.close()
txt_gsANDbg.close()
txt_bwANDbg.close()
txt_bg_rem.close()
result_file_all.close()