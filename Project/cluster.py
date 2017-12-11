from sklearn.datasets import load_iris
from itertools import cycle
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn import preprocessing
from numpy.random import RandomState
import pylab as pl
import csv

class clustering:


    def __init__(self):
        #print(load_iris().data)

       self.plot(preprocessing.scale(read_in_data('Workbook1.csv')))





    def plot(self, X):
        pca = PCA(n_components=2, whiten=True).fit(X)
        X_pca = pca.transform(X)
        kmeans = KMeans(n_clusters=2, random_state=RandomState(42)).fit(X_pca)
        for num in str(kmeans.labels_).replace('[','').replace(']','').split(' '):
            print(num)
        plot_2D(X_pca, kmeans.labels_, ["c0", "c1", "c2","c3", "c4", "c5","c6"])


def plot_2D(data, target, target_names):
    colors = cycle('rgbcmykw')
    target_ids = range(len(target_names))
    pl.figure()
    for i, c, label in zip(target_ids, colors, target_names):
        pl.scatter(data[target == i, 0], data[target == i, 1],
                   c=c, label=label)
    pl.legend()
    pl.show()


def convertToDouble(string):

    try:
        return float(''.join([i if ord(i) < 128 else ' ' for i in string]))
    except ValueError:
        print('found string')
        print(string.replace('\xef',''))
        return string

def read_in_data(file_name):
    array=[]
    with open(file_name, 'rU') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            array.append([convertToDouble(numeric_string) for numeric_string in row])
        return (array)



if __name__ == '__main__':
    c = clustering()
