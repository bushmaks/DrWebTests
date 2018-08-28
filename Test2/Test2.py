from subprocess import run, PIPE
from re import findall, IGNORECASE, DOTALL
from time import strptime
from random import randint

testDomains = ['drweb.ru', 'drweb.com', 'drweb.net', 'drweb.de', 'google.com']

domain = testDomains[randint(0, 4)]

def whois(domain):
    """Данная функция разбирает вывод штатную linux-утилиту "whois" для переданного доменного имени,
     разбирает вывод и возвращает:
        - дату создания домена в виде структуры данных struct_time
        - список name server'ов (если получены)
        - название организации (если есть)
    """
    # Запускаем штатную linux утилиту whois для домена domain
    whoisEcho = run(['whois', domain], stdout=PIPE).stdout.decode('utf-8')

    # Берем информацию только после домена
    whoisEcho = ''.join(findall('{0}(.+)'.format(domain), whoisEcho, IGNORECASE | DOTALL))

    creationTimeList = findall('creat[a-z ]+:\s+(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)', whoisEcho, IGNORECASE)

    if not creationTimeList:
        print("Не нашел даты создания!(whois)")
        return False
    else:
        creationTime = strptime(sorted(creationTimeList)[0], "%Y-%m-%dT%H:%M:%SZ")

    serverNamesList = findall('nserver:\s+([\w\d\.]+)\n', whoisEcho, IGNORECASE)
    if not serverNamesList:
        serverNamesList = findall('Name server:\s+([\w\d\.]+)\n', whoisEcho, IGNORECASE)

    serverNamesList = list(set([x.lower() for x in serverNamesList]))

    organizationName = ''.join(findall('org:\s+([\w\s]+)\n', whoisEcho, IGNORECASE))
    if not organizationName:
        organizationName = ''.join(findall('Registrant Organization:\s+([\w\s]+)\n', whoisEcho, IGNORECASE))

    return [creationTime, serverNamesList, organizationName]

print(whois(domain))
