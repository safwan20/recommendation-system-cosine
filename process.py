import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict

class Process :
    def __init__(self):
        self.data = pd.read_csv('2010-2019/bollywood_2010-2019.csv')
        self.ratings = pd.read_csv('2010-2019/bollywood_meta_2010-2019.csv')
        self.data = self.data.fillna('https://upload.wikimedia.org/wikipedia/commons/f/fc/No_picture_available.png')
        self.tog = set()
        self.arr = []
        self.encoded = []
        self.movies = dict()
        self.encoded_dic = dict()

    def get_data(self) :
        return self.data.values
    
    def get_encoded(self) :
        genres = self.ratings['genres']
        h = self.ratings['imdb_id'].values
        for i in self.data.values :
            self.movies[i[1]] = i[2]
        for i in genres :
            split_genres = i.split('|')
            self.arr.append(split_genres)
            for j in split_genres :
                self.tog.add(j)
        flog = list(self.tog)
        flog.remove('\\N')
        cnt = 0
        for i in self.arr :
            temp = []
            for j in flog :
                if j in i :
                    temp.append(1)
                else :
                    temp.append(0)
            self.encoded_dic[h[cnt]] = temp
            self.encoded.append(temp)
            cnt+=1
        return self.encoded_dic
    
    def calculate(self,id) :
        results = defaultdict(list)
        cnt = 0
        ans = []
        try :
            for i in self.encoded :
                temp = []
                similar = cosine_similarity([self.encoded_dic[id]], [i])
                temp.append(self.ratings['title'][cnt])
                temp.append(self.movies[self.ratings['imdb_id'][cnt]])
                temp.append(self.ratings['imdb_id'][cnt])
                results[similar[0][0]].append(temp)
                cnt+=1
            for i in sorted(results.keys(),reverse=True) :  
                print(i)
                u = results[i]
                for j in u :
                    ans.append(j)
            return ans
        except :
            return None
