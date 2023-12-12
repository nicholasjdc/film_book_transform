from langdetect import detect
from BookEntry import BookEntry
import re
import json
LOG_STATUS = 1
LOG_LEVEL = 10
def checkDupField(targetvalue: str, field: str) -> list[str]:
    duplicateSubjectsSet = set()
    for be in finalData:
        tempdata = be
        if tempdata[field] == targetvalue:
            
            addSubjectList: list[str] = tempdata['subjects']
            for subject in addSubjectList:
                duplicateSubjectsSet.add(subject)
    return duplicateSubjectsSet
def notSillyDetect(msg: str):
    lc = "zh-cn"
    try:
        lc = detect(msg)
    except:
        logprint("LANGUAGE NOT DETECTED: " + msg, 2)
        
    return lc
def logprint(message, log_status: int):
    if log_status >= LOG_LEVEL:
        print(message)

def setAwaitingStatusBulk(status):
    global awaitingEntryNumber, awaitingAuthor, awaitingTitle, awaitingPublication, awaitingPageCount, awaitingISBN, awaitingNote, awaitingLanguageCodes, awaitingPageNumber, awaitingTitle2, awaitingAuthor2, awaitingSeriesTitle, awaitingSeriesTitlec
    awaitingEntryNumber = status
    awaitingAuthor = status
    awaitingTitle = status
    awaitingPublication= status
    awaitingPageCount = status
    awaitingISBN = status
    awaitingNote = status
    awaitingLanguageCodes = status
    awaitingPageNumber = status
    awaitingAuthor2 = status
    awaitingTitle2 = status
    awaitingSeriesTitle = status
    awaitingSeriesTitlec = status
    
FULL_MANUSCRIPT = 'film_taiwan_manuscript.txt'
TEST_MANUSCRIPT = 'test_manuscript.txt'
file1 = open(FULL_MANUSCRIPT, 'r')

languageCodes = ['chi', 'eng', 'worldcat','jpn', 'fre', 'ger', 'ita', 'kor', 'spn', 'rus','uig', 'ctfal', 'duxiu','ncl']

count = 0
awaitingEntryNumber = False
awaitingAuthor = False
awaitingAuthor2 = False
awaitingTitle = False
awaitingTitle2 = False
awaitingPublication = False
awaitingPageNumber = False
awaitingPageCount = False
awaitingISBN = False
awaitingNote = False
awaitingLanguageCodes = False
awaitingSeriesTitle = False
awaitingSeriesTitlec = False

subjectsRegex = re.compile(r"\d+\.\d*")
authorRegex = re.compile(r"\w+\,\s\.*")
authorRegexParen = re.compile(r".* \(.*\)\,* .*")
numberPeriodRegex = re.compile(r"\d+\.")
publicationRegex = re.compile(r".+\:.+\,.*")

finalDictionary = {'entries': []}
finalData = []
with open('data.json', 'w', encoding='utf-8') as f:
    pass
while True:
    global subject
    global nBE
    count += 1

    last_pos = file1.tell()
    line = file1.readline()

    
    LINE_MAX = 500000
    if not line or count > LINE_MAX:
        break
    
    strippedLine = line.strip()
    splitLine = strippedLine.split()
    
    if strippedLine == "":
        continue
    logprint("Line{}: {}".format(count, line.strip()), LOG_STATUS)

    if subjectsRegex.match(strippedLine):
        subject = " ".join(strippedLine.split()[1:])
    
    if strippedLine.isdigit():
        if 'nBE' in globals():
            logprint(nBE, 2)
            logprint((json.dumps(vars(nBE))), 2)
            if nBE.author == '' and nBE.authorc == '' and nBE.authorp == '':
                logprint("EMPTY AUTHOR", 2)
            if nBE.publication == '':
                logprint("EMPTY PUBLICATION", 2)
            if nBE.pageCount == '':
                logprint("EMPTY PAGE COUNT", 2)
            if nBE.note == '':
                logprint("EMPTY NOTE", 2)
            if len(nBE.subjects) == 0:
                logprint("EMpty Subject")
            if len(nBE.languageCode) ==0:
                logprint("EMPTY LANGUAGE CODES", 2)
            nBE.assignMissingFields()
            if nBE.ISBN != '':
                additionalSubjects = checkDupField(nBE.ISBN, 'ISBN')
                nBE.subjects += additionalSubjects
            elif nBE.title != '':
                additionalSubjects = checkDupField(nBE.title, 'title')
                nBE.subjects += additionalSubjects
            elif nBE.titlep != '':
                additionalSubjects = checkDupField(nBE.titlep, 'titlep')
                nBE.subjects += additionalSubjects
            elif nBE.titlec != '':
                additionalSubjects = checkDupField(nBE.titlec, 'titlec')
                nBE.subjects += additionalSubjects
            else: 
                pass
            with open('data.json', 'a', encoding='utf-8') as f:
                finalData.append(vars(nBE))                
        #Begin New Entry
        setAwaitingStatusBulk(True)


    if awaitingEntryNumber:
        if strippedLine.isdigit():
            logprint("ENTRY NUMBER", LOG_STATUS)
            nBE = BookEntry()
            nBE.subjects += [subject]
            nBE.entryNumber = strippedLine
            setAwaitingStatusBulk(True)
            logprint(nBE, LOG_STATUS)
            awaitingEntryNumber = False
    elif awaitingAuthor:
        if authorRegex.match(strippedLine) or authorRegexParen.match(strippedLine) or len(splitLine) < 3:#len(splitLine) <= 3 and strippedLine != ' ':
            logprint("author verified", LOG_STATUS)
            lc = notSillyDetect(strippedLine)
            logprint(lc, LOG_STATUS)
            if lc == 'en':
                nBE.author = strippedLine
            elif lc in {'zh-cn', 'ja', 'ko', 'zh-tw'}:
                nBE.authorc = strippedLine
            else:
                nBE.authorp = strippedLine
            logprint(nBE, LOG_STATUS)
        else:
            count -=1
            file1.seek(last_pos)
            awaitingAuthor2 = False
        awaitingAuthor = False   
        
    elif awaitingAuthor2:
        #lc = notSillyDetect(strippedLine)
        lc = notSillyDetect(splitLine[0])
        logprint(lc, LOG_STATUS)
        if lc in {'zh-cn', 'ja', 'ko', 'zh-tw'}:
            nBE.authorc = strippedLine
        else:
            count -=1
            file1.seek(last_pos)
        awaitingAuthor2 = False
    elif awaitingTitle:
        slashSplitLine = strippedLine.split('/')
        equalSplitLine = slashSplitLine[0].split('=')
        
        for title in equalSplitLine:
            lc = notSillyDetect(title)
            if lc == 'en':
                nBE.title = title
            elif lc in {'zh-cn', 'ja', 'ko', 'zh-tw'}:
                nBE.titlec = title
            else:
                nBE.titlep = title
        if len(slashSplitLine) >1 and not slashSplitLine[1].strip().strip('.').isdigit():
            tempAuthor = slashSplitLine[1]
            lc = notSillyDetect(tempAuthor)
            logprint(lc, LOG_STATUS)
            if lc == 'en':
                nBE.author = tempAuthor
            elif lc in {'zh-cn', 'zh-tw', 'ja', 'ko'}:
                nBE.authorc = tempAuthor
            else:
                nBE.authorp = tempAuthor
        logprint(nBE, LOG_STATUS)
        awaitingTitle = False
            
    elif awaitingTitle2:
        slashSplitLine = strippedLine.split('/')
        equalSplitLine = slashSplitLine[0].split('=')
        if '/' in strippedLine or '=' in strippedLine or notSillyDetect(equalSplitLine[0]) in {'zh-cn', 'ja', 'ko', 'zh-tw'}:
            for title in equalSplitLine:
                lc = notSillyDetect(title)
                if lc == 'en':
                    nBE.title = title
                elif lc in {'zh-cn', 'ja', 'ko', 'zh-tw'}:
                    nBE.titlec = title
                else:
                    nBE.titlep = title
            if len(slashSplitLine) >1 and not slashSplitLine[1].strip().strip('.').isdigit():
                tempAuthor = slashSplitLine[1]
                lc = notSillyDetect(tempAuthor)
                logprint(lc, LOG_STATUS)
                if lc == 'en':
                    nBE.author = tempAuthor
                elif lc in {'zh-cn', 'ja', 'ko', 'zh-tw'}:
                    nBE.authorc = tempAuthor
                else:
                    nBE.authorp = tempAuthor 
        else:
            count -=1
            file1.seek(last_pos)
        logprint(nBE, LOG_STATUS)
        awaitingTitle2 = False
    elif awaitingPublication:
        if (publicationRegex.match(strippedLine) and'series' not in strippedLine.lower() and 'Note:' not in strippedLine and 'ISBN' not in strippedLine.lower()) or not ('p.' in strippedLine or 'ISBN' in strippedLine or 'series' in strippedLine.lower() or 'note' in strippedLine.lower() or 'pages' in strippedLine or 'v.' in strippedLine or 'leaves' in strippedLine or 'l.' in strippedLine or numberPeriodRegex.match(strippedLine) ):
            
            if not publicationRegex.match(strippedLine):
                logprint("NOT PUB REGEX", 2)
            nBE.publication = strippedLine
            if '.' not in strippedLine:
                lineExtra = file1.readline()
                count+=1
                strippedLineExtra = lineExtra.strip()
                nBE.publication += strippedLineExtra
        else:  
            count -=1
            file1.seek(last_pos)
        awaitingPublication = False
    elif awaitingPageNumber:
        stupidOpenParenSplitLine = strippedLine.split('(')
        if ('pagings' in strippedLine.lower() or'unpaged' in strippedLine.lower() or 'p' in splitLine or 'p.' in strippedLine or 'pages' in strippedLine or 'v.' in splitLine or 'leaves' in strippedLine or 'l.' in strippedLine or 'pagination' in strippedLine.lower() or numberPeriodRegex.match(strippedLine)) and 'Note:' not in strippedLine:  
            nBE.pageCount = strippedLine
            
        else:
            count -=1
            file1.seek(last_pos)
        if nBE.publication == '':
                awaitingPublication = True
        awaitingPageNumber = False
    elif awaitingISBN:
        if 'ISBN' in strippedLine:
            logprint("ISBN FOUND", LOG_STATUS)
            nBE.ISBN = strippedLine.split("ISBN")[1].strip()
            last_pos = file1.tell()
            extraline = file1.readline()
            while 'series' not in extraline.lower() and 'note' not in extraline.lower():
                last_pos = file1.tell()
                nBE.ISBN += " " +extraline.strip()
                count+=1
                extraline = file1.readline()
            file1.seek(last_pos)
        else:
            count -=1
            file1.seek(last_pos)
        awaitingISBN = False
    elif awaitingSeriesTitle:
        if 'series' in splitLine[0].lower() :
            logprint("SERIES TITLE FOUND", LOG_STATUS)
            seriesStrippedLine = " ".join(strippedLine.split(':')[1:])
            nBE.seriesTitle = seriesStrippedLine.strip()
            last_pos = file1.tell()
            extraline = file1.readline()
            while 'note:' not in extraline.lower():
                last_pos = file1.tell()
                nBE.seriesTitle += extraline.strip()
                count+=1
                extraline = file1.readline()
            file1.seek(last_pos)
        else: 
            count -=1
            file1.seek(last_pos)
        awaitingSeriesTitle = False
    elif awaitingSeriesTitlec:
        if notSillyDetect(strippedLine) in {'zh-cn', 'ja', 'ko', 'zh-tw'}:
            nBE.seriesTitlec = strippedLine
        else:
            count -=1
            file1.seek(last_pos)
        awaitingSeriesTitlec = False
    elif awaitingNote:
        if 'Note:' in strippedLine:
            logprint("NOTE FOUND", LOG_STATUS)
            colonSplitLine = strippedLine.split('Note:')
            nBE.note = colonSplitLine[1].strip()
            last_pos = file1.tell()
            lineExtra = file1.readline()
            strippedLine = lineExtra.strip()
            count+=1
            while strippedLine!= '' and strippedLine[-1] == '.': 
                nBE.note += strippedLine
                last_pos = file1.tell()
                lineExtra = file1.readline()
                strippedLine = lineExtra.strip()
                count+=1
                
            file1.seek(last_pos)
            count -=1
        else:
            count -=1
            file1.seek(last_pos)
        awaitingNote = False
    elif awaitingLanguageCodes:
        for code in languageCodes:
            if code in strippedLine.lower():
                nBE.languageCode += [code]

logprint('Assigning data to dictionary', 100)
finalDictionary['entries'] = finalData

logprint('Opening file and dumping data', 100)
with open('data_test.json', 'w', encoding='utf-8') as file2:
    json.dump(finalDictionary, file2, ensure_ascii=False, indent=4)
file1.close()
