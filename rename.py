import os
import csv

inputCSV = "Seriennummern.csv"

# with open(inputCSV, "r", encoding="utf-8", errors="ignore") as scraped:
#         final_line = scraped.readlines()[-1]

with open(inputCSV) as csvfile:
    dialect = csv.Sniffer().sniff(csvfile.read(1024))
    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect)

    for row in reader:  
        SerialString = row[0]+"-"+row[1]+"-"+row[2]+"-"+row[3]

    print("Renaming To: "+ SerialString)   

    os.rename("Laser/typenschilder.pdf", "Laser/typenschilder-bis-"+SerialString+".pdf")

print("done")
