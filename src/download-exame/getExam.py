"""
    source: https://docs.python.org/3/library/urllib.parse.html
"""
import regex as re
from urllib import request

'''
    Finds the year's url in the IAVE website code (that's saved in the arquivoIAVE.html).

    @param ano year of the exam
'''
def findURLYear(ano):
    arquivo = open("arquivoIAVE.html", "r")

    lines = arquivo.readlines()
    arquivo.close()

    for line in lines:
        if(ano in line):
            #print(line)
            return line #URL do exame


'''
    Splits the ano's URL into a valid URL and then saves the 
    source code into a html file named the ano followed by
    .html, e.g. ano 2021 - "2021.html"
'''
def splitURLYear(URL, ano):

    #https://stackoverflow.com/questions/839994/extracting-a-url-in-python
    URL = re.search("https?://[^\s]+", URL).group(0) 

    print(URL)

    #FIXME aqui com regex 
    URL = URL[:-9]
    print(URL)

    request.urlretrieve(URL, str(ano) + ".html")


'''
    Returns the exam's URL.

    All of the parameters should be strings.
    @param codigoDisciplina 
'''
def findURLExam(codigoDisciplina, fase, ano):
    arquivo = open(str(ano) + ".html", "r")

    lines = arquivo.readlines()
    arquivo.close()

    fase = "F" + str(fase)

    for line in lines:
        if(".pdf" in line and codigoDisciplina in line and fase in line and "CC" not in line):
            print(line)
            return line #URL exam
    
'''
    Downloads the exam into a pdf file named with the course
    name followed by the year and the phase of the exam, 
    e.g. "MatemáticaA-2021-F1.pdf"
'''
def downloadExam(URL, nomeDisciplina, ano, fase):

    URL = re.search("https?://[^\s]+", URL).group(0) 

    print(URL)

    request.urlretrieve(URL, nomeDisciplina + "-" + ano + "-" + "F" + fase + ".pdf")


def main():
    pageYear = findURLYear("2021")
    splitURLYear(pageYear, 2021)
    URLExam = findURLExam("735", "2", "2021")
    if(URLExam is None):
        print("Something failed")
        return
    downloadExam(URLExam, "MatematicaA", "2021", "2")


main()
