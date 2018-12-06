import glob
import os

' a module for combining visiting logs through month'

__author__ = 'Ken'


def combine_files():
    years = ('2015', '2016', '2017', '2018')
    months = ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12')
    if not os.path.exists('./combine'):
        os.mkdir('./combine/')

    for year in years:
        for month in months:
            newfileName = './combine/' + year + '-' + month + '.log'
            newfile = open(newfileName, 'w')
            pattern = r'' + year + '-' + month + '-' + '*.log'
            for fileName in glob.glob(pattern):
                with open(fileName, 'r') as f:
                    for line in f.readlines():
                        newfile.write(line)
            newfile.close()
            if os.path.getsize(newfileName) == 0:
                os.remove(newfileName)


if __name__ == '__main__':
    combine_files()