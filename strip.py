import csv


def main():
    desti = open('tiki-strip.txt', 'w', encoding='utf8')
    # write = csv.writer(desti)
    write = desti
    count = 0
    with open('tiki.csv') as file:
        reader = csv.reader(file)
        for row in reader:
            new_row = [row[2].strip(), row[4].strip(), row[3].strip(),
                       row[1].strip()]
            write.write("%s\n" % new_row)
            count += 1
    print(count)
    desti.close()


if __name__ == '__main__':
    main()
