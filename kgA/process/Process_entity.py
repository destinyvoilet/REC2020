import csv
    
csv_files = [r"college.csv", r"displine.csv", r"major.csv", r"province.csv", r"subject.csv", r"year.csv"]
labels = ["college", "displine", "major", "province", "subject", "year"]    
title = [['College:ID','Name','985:int','211:int','top:int',':LABEL'],
         ['Displine:ID','Name',':LABEL'],
         ['Major:ID','Name','Province','Contributor',':LABEL'],
         ['Province:ID','Name',':LABEL'],
         ['Subject:ID','Name',':LABEL'],
         ['Year:ID','Name',':LABEL']]
i = 0    
for file in csv_files:
    input = open(file, 'r')
    output = open('./entity./'+file, 'w', newline='')

    data = csv.reader(input)
    writer = csv.writer(output)
        
    flag = 0
    for j in data:
            
        arr = j[:]
            
        if flag == 0:
            writer.writerow(title[i])
            flag += 1
            continue
            
        arr.append(labels[i])
        writer.writerow(arr)

    i += 1
    input.close()  
    output.close()
    
