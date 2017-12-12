from sklearn.datasets import load_iris
from itertools import cycle
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn import preprocessing
from numpy.random import RandomState
import pylab as pl
import csv
import pandas as pd


class clustering:
    array = []
    k = 3
    pca = 30
    use_pca = False
    preprocess =False
    file_name = 'Workbook1.csv'
    headers = ['M01','M02','M03','M04','M05','M06','M07','M08','M09','M10','M11','M12','M13','M14','M15','M16','M17','M18','M19','M20','M21','M22','M23','M24','M25','M26','M27','M28','M29','M30','M31','M32','M33','M34','M35','M36','M37','M38','M39','M40','M41','M42','M43','M44','M45','M46','M47','M48','M49','M50','M51','M52','M53','M54','M55','M56','M57','M58','M59','M60','M61','M62','M63','M64','M65','M66','M67','M68','M69','M70','M71','M72','M73','M74']

    def __init__(self):
        print('started')
        for i in range(0,36):
            self.array.append([])

    def run(self):
        self.plot(self.setData())

    def setData(self):
        c = pd.DataFrame(read_in_data(self.file_name), columns=self.headers)
        if (self.preprocess):
            c = preprocessing.scale(c)
        return c

    def run_pca(self,c):
        pca = PCA(n_components=self.pca, whiten=False).fit(c)
        X = pca.transform(c)
        return {'fit':X,'pca':pca}

    def pca_components(self):
        c = self.setData()
        pc_labels = []
        pca = self.run_pca(c)['pca']
        for pc in range(1,self.pca+1):
            pc_labels.append('PC-'+str(pc))
        return pd.DataFrame(pca.components_, columns=c.columns, index=pc_labels)

    def plot(self, c):

        if(self.use_pca):
            X = self.run_pca(c)['fit']
        else:
            X = c
        kmeans = KMeans(n_clusters=self.k, random_state=RandomState(42)).fit(X)
        i = 2
        self.array[0].append(self.k)
        self.array[1].append(self.pca)
        for num in str(kmeans.labels_).replace('[','').replace(']','').split(' '):
            print(i)
            self.array[i].append(convertToDouble(num))
            i= i+1
        #plot_2D(X, kmeans.labels_, ["c0", "c1", "c2","c3", "c4", "c5","c6"])
    def printArray(self):
        f = open('loopResults.csv', 'w')
        f.write(str(self.array).replace('[','').replace('],',"\n").replace("]",''))
        f.close()



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

def test_pca(clust,pca_max):
    print_string = ''
    clust.preprocess = False

    for pc in range(1, pca_max):
        clust.pca = pc
        pca_c = clust.pca_components()
        pca_c = pca_c.abs()

        print_string = print_string + '\n' + str(pca_c.sort_values(by=pca_c.index[pc -1], ascending=False, axis=1).iloc[:,0:7].columns).replace('\n','').replace('Index([u','').replace('], dtype=\'object\')','')

    f = open('loopPCAC.csv', 'w')
    f.write(print_string)
    f.close()
    print(print_string)

if __name__ == '__main__':
    c = clustering()
    c.k = 2
    c.pca =7
    c.use_pca = True
    c.preprocess = False
    test_pca(c,10)
    #c.run()
    # for k in range(1,10):
    #       c.k = k
    #       for pc in range(0, 10):
    #           if (pc != 0):
    #               c.use_pca = True
    #           else:
    #               c.use_pca = False
    #           c.pca = pc
    #           c.run()
    # c.printArray()