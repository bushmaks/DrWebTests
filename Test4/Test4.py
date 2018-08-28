from re import findall, search

def logPidParser(logFileName):
    logFile = open(logFileName)
    logText = logFile.read()
    pidList = sorted(list(set(findall('\[err\]:.-(\d+):', logText))))
    if not pidList:
        print("Не найдено ни одиного PID'а")
    resultList = []
    for pidIndex in range(len(pidList)):
        resultList.append({'pid': pidList[pidIndex], 'sf_at': '', 'sf_text': '', 'eax': 'test', 'ebx': '',
                    'ecx': '', 'edx': '', 'esi': '', 'edi': '', 'ebp': '',
                     'efl': '', 'esp': '','eip': ''})
        try:
            resultList[pidIndex]['sf_at'] = search('\[err\]:.-%s: Dump: Segmentation fault at (\d{8})'
                                                   % resultList[pidIndex]['pid'], logText).group(1)
        except AttributeError:
            resultList[pidIndex]['sf_at'] = 'Не найден'
        # TODO: Узнать откуда парсить sf_text
        resultList[pidIndex]['sf_text'] = ''

        for keyIndex in range(3, len(resultList[pidIndex].keys())-2):
            key = list(resultList[pidIndex].keys())[keyIndex]
            try:
                resultList[pidIndex][key] = search('\[err\]:.-%s: Dump:[\w\d\s=]+%s=(.{8})'
                                                   % (resultList[pidIndex]['pid'], key.upper()), logText).group(1)
            except AttributeError:
                resultList[pidIndex][key] = 'Не найден'
        try:
            resultList[pidIndex]['esp'] = search('\[err\]:.-%s: Dump: ESP=(.{8} \(.+\))'
                                                 % resultList[pidIndex]['pid'], logText).group(1)
        except AttributeError:
            resultList[pidIndex]['esp'] = 'Не найден'
        try:
            resultList[pidIndex]['eip'] = search('\[err\]:.-%s: Dump: EIP=(.{8} \(.+\))'
                                                 % resultList[pidIndex]['pid'], logText).group(1)
        except AttributeError:
            resultList[pidIndex]['eip'] = 'Не найден'

    return resultList

for pid in logPidParser('log.txt'):
    print("""PID: {pid}
    SF_AT: {sf_at}
    SF_TEXT: {sf_text}
    EAX={eax} EBX={ebx} ECX={ecx} EDX={edx}
    ESI={esi} EDI={edi} EBP={ebp} EFL={efl}
    ESP={esp}
    EIP={eip}
    """.format(**pid))
