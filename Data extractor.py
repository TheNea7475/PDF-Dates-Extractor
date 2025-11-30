import pdfplumber #type: ignore VENV
import re
import pickle
import os
import Visual_scritps

#Variables declaration
PDFDir="PDF"
DataDir="Extracted Data"
data={
    "Pages":[],
    "Lines":[],
    "Dates":[]
}

def HasYear(string):
    pattern = r"\b\d{4}\b"  # Anno tra 1900 e 2099
    return re.search(pattern, string) is not None

def AskUntil(Prompt,Options):
    Ans = None
    while not(Ans in Options):
        Ans=input(f"{Prompt}>")
        if not(Ans in Options):
            print("Wrong input\n")
    return Ans



FilesList = [f for f in os.listdir(PDFDir) if f.endswith(".pdf")]
options = FilesList
print("Select a file")
for i in range(len(options)):
    print(f"{i}. - {options[i]}")
IndxArr=list(range(len(options)))
StringIdxArray = [str(num) for num in IndxArr]
Index=AskUntil("",StringIdxArray)

PDFFileName=options[int(Index)]
FilePath=f"{PDFDir}/{PDFFileName}"

print(PDFFileName)

with pdfplumber.open(FilePath) as pdf:
    maxpages=len(pdf.pages)
    pagecounter=0
    datescounter=0
    for page in pdf.pages:
        page_text=page.extract_text()
        data["Pages"].append(page_text)
        lines=page_text.splitlines()

        linecounter=0
        for line in lines:
            data["Lines"].append(line)


            if HasYear(line):

                if linecounter>0:
                    Prevl=lines[linecounter-1]

                if linecounter<(len(lines)-1):
                    Nextl=lines[linecounter+1]

                Lin=line

                data["Dates"].append({"Prevl":Prevl,"L":Lin,"Nextl":Nextl,"Page":pagecounter,"LineNum":linecounter})

                Visual_scritps.cls()
                print(f"""Updated data with: \n\n{Prevl}\n{Lin}\n{Nextl}\nPage {pagecounter} line {linecounter}\n\n""")
                Visual_scritps.loading_bar_controlled(pagecounter,maxpages)
                Prevl=""
                Lin=""
                Nextl=""

                datescounter=datescounter+1
            linecounter=linecounter+1
        pagecounter=pagecounter+1


Visual_scritps.cls()
print(f"""Total pages extracted: {len(data["Pages"])}\nTotal lines extracted: {len(data["Lines"])}\nTotal dates extracted: {len(data["Dates"])}""")
Visual_scritps.loading_bar_controlled(pagecounter,maxpages)

with open(f"{DataDir}/{PDFFileName}.pickle","wb") as PickleFile:
    pickle.dump(data,PickleFile)