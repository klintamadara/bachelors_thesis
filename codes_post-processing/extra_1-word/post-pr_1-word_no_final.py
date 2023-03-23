import re

TXT_DIR_RAW = 'texts_processed/noiseGS/' # directory storing OCR result from the original images
TXT_DIR_TRU = 'texts_actual/' #directory storing manually prepared correct ingredients lists -> for testing
TXT_DIR_RSLTS = 'results/post-processing_none_1-word_final.txt' #location storing all of the results

exact_match_exception = ["bez", "nav", "saturēt", "nesatur", "var atrasties"]
exact_match_exception_longer = ["saturēt", "nesatur"]
exact_match_exception_ing = ["kakao sviests", "riekstu sviests", "riekstu piens", "zirņu piens", "cūku pupas", "kakao sviesta", "riekstu sviesta", "riekstu piena", "zirņu piena", "cūku pupu", "sēklu sviests", "sēklu sviesta"]
punctuation = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~”“''"
delimiters = ["(", ")", "[", "]", "{", "}", ":", "-", "—", ";", "."]

#prepare animal based ingredient list
txt_file = open("list.txt", "r", encoding='UTF-8')
file_content = txt_file.read()
list_ingredients = file_content.split("\n")
txt_file.close()

#prepare animal based ingredient check list for each product
txt_file = open("text_actual_animal_ingr_check.txt", "r", encoding='UTF-8')
file_content = txt_file.read()
list_ingredients_check = file_content.split("\n") #each line format: type;nr;nr;ingredients
txt_file.close()

#prepare document in which to write
txt_combined = open(TXT_DIR_RSLTS, 'w', encoding='UTF-8')
print("IMG;Ingr nr total - file;Ingr nr;Ingr nr identified;Ingr list;Ingr identified;Nr AB ingr - file;Nr AB ingr identified;AB ingr list - file;AB ingr list identified;Overlap (TP);Missed (FN);Extra (FP);AB ingr overlap (TP);AB ingr missed (FN);Wrongly flagged (FP)", 
file = txt_combined)

#get the actual ingredient list for validation
def clean_text_get_list(text):
    processed = re.sub("\d*[.,]?\d*\s*%", "", text) #remove 2,3% , 1.5 % utt.
    
    for char in delimiters:
        processed = processed.replace(char, ",")
    processed = processed.replace("-\n", "") #ignore "pārnesumi jaunā rindā"
    processed = processed.replace("–\n", "") #ignore "pārnesumi jaunā rindā"
    processed = processed.replace("\n", "") #ignore new lines
    processed = processed.replace("*", "") #ignore asterisks

    list_tru = processed.split(',') #make a list of all ingredients
    list_tru = [s.strip() for s in list_tru if s != '' and s!= ' '] #remove extra spaces
    return list_tru
    
    
#create a list of 1-word-long-ingredients from OCR text
def get_list(text):
    processed = re.sub("\d*[.,]?\d*\s*%", "", text) #remove 2,3% , 1.5 % utt.
    all_words_identified = [word.strip(punctuation) for word in processed.split()] #split into words and remove extra chars
    all_words_identified = [s.strip() for s in all_words_identified if s != '' and s!= ' '] #remove extra spaces and empty strings
    return all_words_identified


#do post-processing for images from 1 to 200 for both non-vegan and vegan products
product_type = ["n","v"]
for t in product_type:
    for x in range(1, 101):
        img_name = t + str(x)

        #prepare the actual ingredients list for testing purposes
        txt_tru = open(TXT_DIR_TRU + img_name + ".txt", "r", encoding='UTF-8')
        content_tru = str.lower(txt_tru.read()) #lowercase
        txt_tru.close()
        list_tru = clean_text_get_list(content_tru)

        #prepare the OCR result from original image for post-processing
        txt_raw = open(TXT_DIR_RAW + img_name + ".txt", "r", encoding='UTF-8')
        content_raw = txt_raw.read()
        txt_raw.close()
        raw_processed = str.lower(content_raw)
        raw_processed = raw_processed.replace(";", ",")
      
        
        #SPLITTING into a list of ingredients
        list_raw = get_list(raw_processed)

   
        #FEATURE
        list_raw_n = [] #animal based ingredients identified in the product
        #loop through all ingredients and check if they are animal based
        for ingredient in list_raw:
            if ingredient in list_ingredients:
                list_raw_n.append(ingredient)
                list_raw.remove(ingredient)

        
        #test the result, how correct it is (using prepared files fot checking accuracy)
        list_check_ingr_n = []
        ing_animal_overlap = []
        ing_animal_missed = []
        ing_animal_extra = []
        check_nr_total = 0
        check_nr_n = 0

        #extract check data from the manually prepared file
        if(t == "v"):
            ing_animal_extra = list_raw_n
            list_check = list_ingredients_check[x+100].split(";")
        else: #"n"
            list_check = list_ingredients_check[x].split(";")

        #make sure to look at the correct product(compare IDs)
        if(list_check[0] != img_name):
            print("Something doesn't add up. Can't check and compare animal ingredients list because samples are given different")
            print(list_check[0])
            print(img_name)
        else:
            check_nr_total = list_check[1] #total nr of ingredients check
            check_nr_n = list_check[2] #nr of animal based ingredients check
            if(t == "n"): #non-vegan product
                list_check_ingr_n = list_check[3].split(",") #check animal based ingredient list
                ing_animal_missed = list_check_ingr_n.copy() #missed - AB ingredients in the product not recognized by the solution
                list_raw_n_reduced = list_raw_n.copy()
                for detected_ingr in list_raw_n: #loop through all the AB ingreidents "found"
                    if detected_ingr in ing_animal_missed: #if they are actually in the product, it is a match (TP)
                        try:
                            ing_animal_missed.remove(detected_ingr)
                            ing_animal_overlap.append(detected_ingr)
                            list_raw_n_reduced.remove(detected_ingr)
                            continue
                        except ValueError: #sometimes there can be dublicates, if, e.g., word is the same in several languages. Only one of the times it is a correct identification
                            ing_animal_extra.append(detected_ingr) #add as wrongly flagged ingredient
                            list_raw_n_reduced.remove(detected_ingr)
                for detected_ingr in list_raw_n_reduced: #check ingredients left
                        found = 0 #to end a loop when ingredients match 
                        for ing in ing_animal_missed: #maybe identified ingredient contains extra words
                            if((ing in detected_ingr) or (detected_ingr in ing)): #if they overlap, it is a match
                                ing_animal_missed.remove(ing)
                                ing_animal_overlap.append(detected_ingr)
                                found = 1
                                break
                        if(found == 1): continue
                        """for tuple in list_similars: #because of OCR errors, correctly identified ingredients might have spelling mistakes
                            if(tuple[0] == detected_ingr and found == 0):                    
                                for ing in ing_animal_missed: #look at the AB ingredients in the product not yet matched
                                    if((tuple[1] in ing) or (ing in tuple[1])): #if identified ingredient is one of them
                                        ing_animal_missed.remove(ing)
                                        ing_animal_overlap.append(detected_ingr)
                                        list_similars.remove(tuple)
                                        found = 1
                                        break
                            if(found == 1): break"""
                        if(found == 0): ing_animal_extra.append(detected_ingr)

        print(img_name, check_nr_total, str(len(list_tru)), str(len(list_raw)), list_tru, [raw_processed], check_nr_n, str(len(list_raw_n)), list_check_ingr_n, list_raw_n, str(len(ing_animal_overlap)), str(len(ing_animal_missed)), str(len(ing_animal_extra)), ing_animal_overlap, ing_animal_missed, ing_animal_extra, sep = ";", file = txt_combined)

txt_combined.close()