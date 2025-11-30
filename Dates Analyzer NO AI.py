import pickle
import random
import re
import msvcrt
import os
import time
import pyttsx3 # type: ignore VENV
import Visual_scritps

DataDir="Extracted Data"

# Function to convert text to speech
def SpeakTextConditional(command,UseVoice):
    # Initialize the engine
    if UseVoice:
        engine = pyttsx3.init()
        engine.say(command) 
        engine.runAndWait()

def ToggleVoice(UseVoice):
    print(UseVoice)
    UseVoice = not (UseVoice)
    print(UseVoice)
    return UseVoice

def AskUntil(Prompt,Options):
    Ans = None
    while not(Ans in Options):
        Ans=input(f"{Prompt}>")
        if not(Ans in Options):
            print("Wrong input\n")
    return Ans

def AskUntilK(Prompt,Options):
    Ans = None
    while not(Ans in Options):
        print(f"{Prompt}")
        Ans = str(msvcrt.getch().decode())
        if not(Ans in Options):
            print("Wrong input\n")
    return Ans


pickle_files = [f for f in os.listdir(DataDir) if f.endswith(".pickle")]
options = pickle_files
print("Select a file")
for i in range(len(options)):
    print(f"{i}. - {options[i]}")
IndxArr=list(range(len(options)))
StringIdxArray = [str(num) for num in IndxArr]
Index=AskUntil("",StringIdxArray)

Datafile=f"{DataDir}/{options[int(Index)]}"
print(options[int(Index)])

with open(Datafile,"rb") as File:
    Data=pickle.load(File)

Pages=Data["Pages"]
Lines=Data["Lines"]
YearData=Data["Dates"]

Menu=None
UseVoice=False
while Menu != 0:
    Menu=AskUntilK(f"1 - Complete phrase with year YYYY\n2 - What happend in YYYY?\n3 - Quit\n",["1","2","3"])
    print(Menu)
    match Menu:
        case "1":
            TotalQuests=len(YearData)
            NotAsked=YearData
            WrongCount=0
            CorrectCount=0
            NewQuestion=False
            QuestNum=random.randint(0, len(NotAsked))

            print("""Press any key to start!\n""")
            Ans=msvcrt.getch().decode()

            Visual_scritps.loading_bar(50,2)

            Ans=None
            while Ans != "0":
                
                if NewQuestion:
                    QuestNum=random.randint(0, len(NotAsked))
                Quest=NotAsked[QuestNum]

                match = re.search(r'\b\d{4}\b', Quest["L"])
                CorrectAns = match.group()
                MaskedQuest = Quest["L"].replace(CorrectAns, '■■■■', 1)

                Visual_scritps.cls()
                print(f"Correct {CorrectCount} - Wrong {WrongCount} - To do {len(NotAsked)} - Total {TotalQuests} - Text Reader: {UseVoice}")
                print("""0. Save and quit - e. Peek lines - v. Toggle text reader\n\n""")
                print(f"{MaskedQuest}\n")
                SpeakTextConditional(MaskedQuest,UseVoice)
                print(">",end='',flush=True)

                FirstKey=str(msvcrt.getch().decode())
                
                match FirstKey:
                    case "v":
                        UseVoice=ToggleVoice(UseVoice)
                        NewQuestion=False
                        continue
                    case "e":
                        MaskedQuest=f"""e\n\n{Quest["Prevl"]}\n{MaskedQuest}\n{Quest["Nextl"]}\n\n>"""
                        print(MaskedQuest,end='',flush=True)
                        SpeakTextConditional(MaskedQuest,UseVoice)
                        Ans=str(input())
                        if Ans=="0":
                            break
                        if Ans=="v":
                            UseVoice=ToggleVoice(UseVoice)
                            NewQuestion=False
                            continue
                    case "0":
                        break
                    case _:
                        print(FirstKey,end='',flush=True)
                        Ans=str(input())
                        Ans=FirstKey+Ans
    

                #Ans Analysis
                if Ans==CorrectAns:
                    print("Correct!")
                    CorrectCount=CorrectCount+1
                    print("Removing quest\n")
                    NotAsked.pop(QuestNum)
                    NewQuestion=True
                else:
                    print(f"Wrong, correct value: {CorrectAns}\n")
                    WrongCount=WrongCount+1
                    NewQuestion=True

                time.sleep(1.5)

            #Prevent div by 0 when quitting instantly
            if WrongCount+CorrectCount==0:
                WrongCount=WrongCount+1
            print(f"Questions asked: {WrongCount+CorrectCount} - Correct: {CorrectCount} - Wrong: {WrongCount} - Correct percentage: {CorrectCount*100/(WrongCount+CorrectCount)}%\n")

        case "2":
            continue
        case "3":
            break