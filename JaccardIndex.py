minimum_similarity=0.05

import os
import time
t1=time.time()

file_loc =input("Enter file directory: ")
words_file_name=input("Enter name of words.txt file (include .txt): ")

print("Loading patents")
words_file=open(file_loc+"/"+words_file_name,"r")

patents={}

for row in words_file:
    split_row=row.split(":")
    keywords=split_row[1].replace(", \n","").split(', ')
    patents[split_row[0]]=keywords

print("Done loading patents. Calculating Jaccard similarities")
similarities_file_name="similarities.txt"
if os.path.exists(file_loc+"/"+similarities_file_name):
    os.remove(file_loc+"/"+similarities_file_name)
similarities_file=open(file_loc+"/"+similarities_file_name,"w")

counter=0
for first_patent in patents:
    for second_patent in patents:
        if first_patent != second_patent:
            first_patent_keywords=patents[first_patent]
            second_patent_keywords=patents[second_patent]

            all_words=second_patent_keywords.copy()
            shared_words=[]

            for word in first_patent_keywords:
                if word not in all_words:
                    all_words.append(word)

                if (word in second_patent_keywords) and (word not in shared_words):
                    shared_words.append(word)
            jaccard_index=len(shared_words)/len(all_words)
            if jaccard_index>=minimum_similarity:
                similarities_file.write(first_patent+","+second_patent+","+str(jaccard_index)+"\n")

            counter+=1
            if(counter%100000==0):
                print("calculated "+str(counter) +" Jaccard indexes")

similarities_file.close()

t2=time.time()
print("finished in "+str(t2-t1)+" seconds")
