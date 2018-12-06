import glob
import csv
import json
import re

' a module for statistics of product visiting logs'

__author__ = 'Ken'


def product_visiting_statistics():
    for fileName in glob.glob(r'*.log'):
        with open(fileName, 'r') as f:
            for lineIndex in f.readlines():
                try:
                    line = json.loads(lineIndex)
                except json.decoder.JSONDecodeError:
                    print(fileName, lineIndex)
                    continue

                '''
                    {"level":"info","message":"[21/Nov/2018:02:45:05 +0000] | GET | /product/sku407301/fried-egg-earrings | 
                    200 - 241.286 | 3NUDINAjO-8Ergce3npqMGot4vM55tU7 | null | 72.205.218.84 ","timestamp":"2018-11-21T02:45:05.760Z"}
                '''

                if line.get("level") == "info" and line.get("message").find('GET | /product/sku') != -1:
                    arr = line.get('message').strip(' | ').split(' | ')[2:6]
                    try:
                        productSku = 'sku' + re.search(r"\d*-?\d?", arr[0][len("/product/sku"):]).group(0)
                    except IndexError:
                        print("the line: ", line)
                        print("Unexpected error:", line.get("message"))
                        raise
                    session = arr[2]
                    timestamp = line.get("timestamp")
                    user = ''
                    if arr[3] != 'null':
                        user = arr[3]
                    with open("ProductTest.csv", "a", newline='') as dataCsv:
                        csv_writer = csv.writer(dataCsv, dialect="excel")
                        csv_writer.writerow([session, productSku, timestamp, user])  # key: session, value: (sku, timestamp)


if __name__ == '__main__':
    product_visiting_statistics()
