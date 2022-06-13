import os
from urllib.parse import parse_qs
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
import regex as re

def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + " (" + str(counter) + ")" + extension
        counter += 1

    return path

def save_json(year, subject, question, answers):
    path = uniquify("../jsons/question.json")
    file = open(path, "w")
    a = answers[0]
    b = answers[1]
    c = answers[2]
    d = answers[3]
    json = {"text": question,
        "answers": [
        {"id": 0,"text": a,"correct": True},
        {"id": 0,"text": b,"correct": True},
        {"id": 0,"text": c,"correct": True},
        {"id": 0,"text": d,"correct": True}],
        "subject": subject,
        "subsubject": "",
        "year": year
        }
    json = str(json).replace("True", "true")
    #print(json)
    file.write(json)
    file.close()

def extract_questions_pdf(filename, year, subject):
    doc = convert_from_path(filename)
    path, fileName = os.path.split(filename)
    fileBaseName, fileExtension = os.path.splitext(fileName)
    txt = ""
    for page_number, page_data in enumerate(doc):
        txt += pytesseract.image_to_string(page_data, lang = "por")
        #print("Page # {} - {}".format(str(page_number),txt))

    #print(txt)
    search = re.split("\d\. +", txt)
    #print(search)
    for i in search:
        # question = re.search("\d\.\d\. ", i)
        # if question is not None:
        #     print("Sub question:", i)

        search2 = re.split("\d\.\d\.\s+", i)
        #print(search2)
        try:
            intro_grupo = search2[-1].split("GRUPO")[-1][5:]
            if len(search2[-1].split("GRUPO")) != 1:
                group = "\nIntro do GRUPO " + search2[-1].split("GRUPO")[-1][0:3].split("\n")[0] + ": " + intro_grupo
                #print("\nIntro do GRUPO",search2[-1].split("GRUPO")[-1][0:4].split("\n")[0] + ":", intro_grupo)
            else:
                if len(search2[-1][:-3].split("(A)")) == 1:
                    main = search2[-1][:-3]
                    #print("\nMain question:", search2[-1][:-3])
        except:
            pass
        
        for j in search2:
            answer = re.search("\(A\)", j)
            if answer is not None:
                try:
                    question = j.split("(A)")[-2]
                #   print("Grupo:", group)
                #    print("Main Question:", main)
                #    print("\nSub-Question: ", question)
                except:
                    pass
                a = j.split("(A) ")[-1].split("(B)")[0]
                b = j.split("(B) ")[-1].split("(C)")[0]
                c = j.split("(C) ")[-1].split("(D)")[0]
                d = j.split("(D) ")[-1].split("\n\n")[0]

                answers = [a, b, c, d]
                question = group + "\n" + main + "\n" + question
                save_json(year, subject, question, answers)

               # print("\nOption A: (A)", j.split("(A) ")[-1].split("(B)")[0])
               # print("Option B: (B)", j.split("(B) ")[-1].split("(C)")[0])
               # print("Option C: (C)", j.split("(C) ")[-1].split("(D)")[0])
               # print("Option D: (D)", j.split("(D) ")[-1].split("\n\n")[0])



extract_questions_pdf("fisica.pdf", 11, "Física")
