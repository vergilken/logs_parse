import glob
import csv
import json
import re

' a module for statistics of order logs'

__author__ = 'Ken'


def order_statistics():
    for fileName in glob.glob(r'*.log'):
        with open(fileName, 'r') as f:
            for lineIndex in f.readlines():
                try:
                    line = json.loads(lineIndex)
                except json.decoder.JSONDecodeError:
                    print(fileName, lineIndex)
                    continue
                if line.get("level") == 'info':
                    temp = line.get("message").find('/checkoutSuccess?on=')
                    if temp != -1:
                        arr = line.get('message').strip(' | ').split(' | ')[2:6]
                        orderId = re.search(r"\d*-?\d?", arr[0][len("/checkoutSuccess?on="):]).group(0)
                        session = arr[2]
                        timestamp = line.get("timestamp")
                        user = ''
                        if arr[3] != 'null':
                            user = arr[3]
                        with open("OrderTest.csv", "a", newline='') as dataCsv:
                            csv_writer = csv.writer(dataCsv, dialect="excel")

                            # key: session, value: (orderId, timestamp)
                            csv_writer.writerow([session, orderId, timestamp, user])


if __name__ == '__main__':
    order_statistics()
