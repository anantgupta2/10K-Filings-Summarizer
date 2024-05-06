from data_parser import return_dataparsed

path = ".\primary-document.html"

f = open("test_file.txt", "w+") #, encoding='utf-8', errors='ignore')
f.write(return_dataparsed(path))
f.close()


