import json
with open("bespoke_result.json") as subjects_file:
    s_file_contents = subjects_file.read()

parsed_subjects = json.loads(s_file_contents)
newResults = {}
for key in parsed_subjects:
    if(parsed_subjects[key][0] and isinstance(parsed_subjects[key][0], int)):
        newList =[]
        for n in parsed_subjects[key]:
            s = str(n)
            for i in range(4-len(s)):
                s = "0" +s
            newList.append(s)
        newResults[key]=newList
    else:
        newResults[key] = parsed_subjects[key]
with open("final.json", "w", encoding="utf-8") as file2:
    json.dump(newResults, file2, ensure_ascii=False, indent=4)