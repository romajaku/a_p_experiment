import csv

with open('zdania.csv', encoding="utf-8") as input, open('zdania_cut.csv', 'w', encoding="utf-8", newline='') as output:
    csv_reader = csv.reader(input, delimiter=',')
    csv_writer = csv.writer(output)
    count = 0
    for row in csv_reader:
        words = len(row[0].split())
        if 3 <= words <= 6:
            print(row[0] + "  " + str(words))
            csv_writer.writerow(row)
            count +=1
    print(count)
        

