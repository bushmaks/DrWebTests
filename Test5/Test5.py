from json import load
from re import match, IGNORECASE

with open('Test5Example2.json') as file:
    data = load(file)

def urlPriority(data):
    if not data:
        print("Нет входных данных data!")


    prioritySettings = []
    for line in open('Test5prioritySettings.conf', encoding="utf-8"):
        if line.startswith('if '): prioritySettings.append(line)

    counterPriorities = 0

    argTemplate = '[\w\]\[\"]+'
    matchStringsTemplate = '[\w\d\.\",/\s]+'
    hostTemplate = '[\.\w\d]+'
    try:
        urlPath = match('https?://%s/([\w\d\._/-]+)?' % hostTemplate, data['url']).group(1)
        host = match('https?://(%s)/' % hostTemplate, data['url']).group(1)
    except AttributeError:
        print("Непрвильно указан url в data.")
        return False

    paramsIndex = data['url'].find('?')+1
    if paramsIndex:
        params = data['url'][paramsIndex:]
    else:
        params = ''


    args = {'urlPath': urlPath,'host': host, 'params': params}
    args.update(data["info"])
    priorityCounter = 0
    for priority in prioritySettings:
        counterPriorities += 1
        # TODO: упростить код, сделать более читаемым
        
        # Проверка правила со скобками
        if match('if (\(.+\))', priority):
            try:
                firstArg = match('if \((%s) has' % argTemplate, priority, IGNORECASE).group(1)
                firstArg = firstArg.replace('"', '')
                firstMatchStrings = match('.+has (%s):' % matchStringsTemplate, priority).group(1)
                firstMatchStrings = [x.replace('"', '') for x in firstMatchStrings.split(', ')]
            except AttributeError:
                print("Вы неправильно указали 1 выражение в {0} правиле.".format(counterPriorities))
                return False
            try:
                secondArg = match('.+and (%s) has'% argTemplate, priority, IGNORECASE).group(1)
                secondArg = secondArg.replace('"', '')
                secondMatchStrings = match('.+and.+has (%s):' % matchStringsTemplate, priority).group(1)
                secondMatchStrings = [x.replace('"', '') for x in secondMatchStrings.split(', ')]
            except AttributeError:
                print("Вы неправильно указали 2 выражение в {0} правиле.".format(counterPriorities))
                return False

            if type(args[firstArg]) is not str: args[firstArg] = str(args[firstArg])
            if type(args[secondArg]) is not str: args[secondArg] = str(args[secondArg])

            firstCheck = any(string in args[firstArg] for string in firstMatchStrings)
            secondCheck = any(string in args[secondArg] for string in secondMatchStrings)

            if firstCheck and secondCheck:
                priorityCounter += int(match('.+\):\s+([-?+?\d]+)', priority).group(1))
            elif firstCheck:
                priorityCounter += int(match('.+:\s+([-+\d]+)', priority).group(1))
            elif secondCheck:
                priorityCounter += int(match('.+and.+:\s+([-+\d]+)\)', priority).group(1))

        # Проверка правила с оператором and без скобок
        elif match('if [\w\d_\+\"\'\s\.,/-]+(and)', priority):
            try:
                firstArg = match('if (%s) has' % argTemplate, priority, IGNORECASE).group(1)
                firstArg = firstArg.replace('"', '')
                firstMatchStrings = match('if %s has (%s)\s+and' % (argTemplate, matchStringsTemplate),
                                          priority).group(1)
                firstMatchStrings = [x.replace('"', '') for x in firstMatchStrings.split(', ')]
            except AttributeError:
                print("Вы неправильно указали 1 выражение в {0} правиле.".format(counterPriorities))
                return False
            try:
                secondArg = match('.+and (%s) has'% argTemplate, priority, IGNORECASE).group(1)
                secondArg = secondArg.replace('"', '')
                secondMatchStrings = match('.+and.+has (%s):' % matchStringsTemplate, priority).group(1)
                secondMatchStrings = [x.replace('"', '') for x in secondMatchStrings.split(', ')]
            except AttributeError:
                print("Вы неправильно указали 2 выражение в {0} правиле.".format(counterPriorities))
                return False

            if type(args[firstArg]) is not str: args[firstArg] = str(args[firstArg])
            if type(args[secondArg]) is not str: args[secondArg] = str(args[secondArg])

            firstCheck = any(string in args[firstArg] for string in firstMatchStrings)
            secondCheck = any(string in args[secondArg] for string in secondMatchStrings)

            if firstCheck and secondCheck:
                priorityCounter += int(match('.+:\s+([-?+?\d]+)', priority).group(1))
        else:
            try:
                firstArg = match('if (%s) has' % argTemplate, priority, IGNORECASE).group(1)
                firstArg = firstArg.replace('"', '')
                firstMatchStrings = match('if %s has (%s)' % (argTemplate, matchStringsTemplate), priority).group(1)
                firstMatchStrings = [x.replace('"', '') for x in firstMatchStrings.split(', ')]
            except AttributeError:
                print("Вы неправильно указали выражение в {0} правиле.".format(counterPriorities))
                return False

            if type(args[firstArg]) is not str: args[firstArg] = str(args[firstArg])

            if any(string in args[firstArg] for string in firstMatchStrings):
                priorityCounter += int(match('.+:\s+([-?+?\d]+)', priority).group(1))


    return priorityCounter


print(urlPriority(data))
