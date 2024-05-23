import csv

with open('zdania.csv', encoding="utf-8") as input, open('zdania_cut.csv', 'w', encoding="utf-8", newline='') as output:
    csv_reader = csv.reader(input, delimiter=',')
    csv_writer = csv.writer(output)
    min = 3
    max = 6
    count = 0
    for row in csv_reader:
        words = len(row[0].split())
        if min <= words <= max:
            print(row[0] + "  " + str(words))
            csv_writer.writerow(row)
            count +=1
    print(count)
        

