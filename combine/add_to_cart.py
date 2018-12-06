import glob
import json
import csv

' a module for statistics of cart logs'

__author__ = 'Ken'


"""
    level: info
    message: [21/Nov/2018:01:49:51 +0000] | POST | /postAddToCart | 200 - 1673.312 | lTkFR7WmckOLJcg9HsmikGTyGdmZF7Gf | null | 174.56.118.203 
    timestamp: "2018-11-21T01:49:51.592Z"
"""


def cart_statistics():
    for fileName in glob.glob(r'*.log'):
        with open(fileName, 'r') as f:
            record = {}
            for lineIndex in f.readlines():
                try:
                    line = json.loads(lineIndex)
                except json.decoder.JSONDecodeError:
                    print(fileName, lineIndex)
                    continue
                if line.get("level") == 'info' and line.get("message").find('GET | /product/sku') != -1:
                    arr = line.get('message').strip(' | ').split(' | ')[2:6]
                    sku, session, timestamp = arr[0].strip('/').split('/')[1], arr[2], line.get('timestamp')
                    record[session] = (sku, timestamp)
                elif line.get("level") == 'info' and line.get("message").find('/postAddToCart') != -1:
                    session = line.get("message").strip(' | ').split(' | ')[2:6][2]
                    item = record.get(session, 'NA')
                    if item != 'NA':
                        user = ''
                        if arr[3] != 'null':
                            user = arr[3]
                        with open("cart_test.csv", "a", newline='') as dataCsv:
                            csv_writer = csv.writer(dataCsv, dialect="excel")
                            csv_writer.writerow([session, item[0], item[1], user])        # key: session, value: (sku, timestamp)
                        del record[session]


if __name__ == '__main__':
    cart_statistics()
