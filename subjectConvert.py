import re
import json
#CHECK FOR DUPLICATES, COLLATE ALL TOGETHER, GET RID OF ENDING PERIOD

entryCodeOne = re.compile(r"\s*[0-9][0-9][0-9][0-9]")

outputJSON = {}
currentLine = ""
OUTPUT_MANUSCRIPT = "subjectresult.json"
MANUSCRIPT = "subjectlist2.txt"
file1 = open(MANUSCRIPT, "r")
while True:
    line = file1.readline().strip()
    if line:
        if entryCodeOne.match(line):
            pastEntryCodes=[]

            if currentLine.strip() in outputJSON:
                print("WAAOH")
                pastEntryCodes = outputJSON[currentLine.strip()]
            if "," in line:
                separated = line.split(",")
                allEntryNumbers = []
                for s in separated:
                    if "-" in s:
                        sep2 =s.split("-")
                        allEntryNumbers.extend(list(
                            range(int(sep2[0]), int(sep2[1]) + 1))
                        )
                    else:
                        allEntryNumbers.append(s)
                outputJSON[currentLine.strip()] = allEntryNumbers
            elif "-" in line:
                separated = line.split("-")
                if "s" in line or separated[1]=='':
                    outputJSON[currentLine.strip()] = ["---"]

                elif len(separated) > 1:
                    outputJSON[currentLine.strip()] = list(
                        range(int(separated[0]), int(separated[1]) + 1)
                    )
                else:
                    outputJSON[currentLine.strip()] = ["---"]
            
            else:
                outputJSON[currentLine.strip()] = [line]
            currentLine = ""
            outputJSON[currentLine.strip()].extend()
        else:
            currentLine += " " + line
            if "See" in line:
                currentLine = ""
    else:
        break

with open(OUTPUT_MANUSCRIPT, "w", encoding="utf-8") as file2:
    json.dump(outputJSON, file2, ensure_ascii=False, indent=4)
file1.close()
