import os
from supabase import create_client, Client
import json

url: str = "https://raifuhqmtrdvncpkonjm.supabase.co"
key: str = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJhaWZ1aHFtdHJkdm5jcGtvbmptIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcxMzY0ODk2MywiZXhwIjoyMDI5MjI0OTYzfQ.S5K7cViYytFYfFHe5w9PhunI6178tE_V8KPqny57VKQ"
)
supabase: Client = create_client(url, key)

with open("final.json") as subjects_file:
    s_file_contents = subjects_file.read()

parsed_subjects = json.loads(s_file_contents)

with open("data_test.json") as user_file:
    file_contents = user_file.read()

parsed_json = json.loads(file_contents)
for s in parsed_subjects:
    for en in parsed_subjects[s]:
        subjectList = set([s])
        currentSubjects = (
                supabase.table("entries")
                .select("entryNumber, subjects")
                .or_("entryNumber.eq." +en +", prev_entry_numbers.cs.{\"" + en +"\"}")
                .execute()
        )   
        if currentSubjects.data and currentSubjects.data[0]["subjects"]:
            subjectList.update(currentSubjects.data[0]["subjects"])
        finalList =list(filter(None, subjectList))
       
        response = (
                supabase.table("entries")
                .update({"subjects": finalList})
                .or_("entryNumber.eq." +en +", prev_entry_numbers.cs.{\"" + en +"\"}")
                .execute()
        )   
