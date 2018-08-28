from os import listdir
import re

dirPath = "Test1FilesDir"

def fileNamesFromTemplate(dirPath="."):
    """Возвращает список имен файлов в заданной дериктории по шаблону
     'image-FILENAME-date.tar.gz'. Аргументы: dirPath - по умолчанию содержит '.',
      что означает: текущая дериктория.
     """

    listOfFiles = listdir(dirPath)
    result = re.findall('image-([\w\d_ -]+)-\d{4}\d{2}\d{2}T\d{6}\.tar\.gz', ', '.join(listOfFiles))
    return list(set(result))


print(fileNamesFromTemplate(dirPath))
