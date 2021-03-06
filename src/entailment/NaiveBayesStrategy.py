# Bismillahi-r-Rahmani-r-Rahim
#
# Naive Bayes Lexical strategy

from Strategy import Strategy
from nltk.classify.naivebayes import NaiveBayesClassifier
from nltk.classify.maxent import MaxentClassifier
from nltk import corpus

stopwords = set(corpus.stopwords.words('english'))

class NaiveBayesStrategy(Strategy):
    """Naive Bayes Lexical RTE strategy.
    >>> l = NaiveBayesStrategy()
    >>> l.train([('the cat','a dog',False),('the big cat','the cat',True)])
    >>> l.judge( [('the great big dog','the dog')] )
    [True]
    """
    def tokens(self, t):
        return set(t.lower().split()) - stopwords

    def features(self, text, hypothesis):
        t_tokens = self.tokens(text)
        h_tokens = self.tokens(hypothesis)
        features = {}
        for x in t_tokens & h_tokens:
            features['both(%s)' % x] = 1
        for x in h_tokens - t_tokens:
            features['missing(%s)' % x] = 1
        for x in t_tokens - h_tokens:
            features['additional(%s)' %x] = 1
        return features

    def train(self, pairs):
        features = [(self.features(x,y), judgment) for x,y,judgment in pairs]
        self.model = NaiveBayesClassifier.train(features)
        #self.model = MaxentClassifier.train(features, max_iter=10)
        print self.model.most_informative_features()
        #print dir(self.model)
        #print self.model

    def judge(self, pairs):
        features = [self.features(x,y) for x,y in pairs]
        return [self.model.classify(x) for x in features]


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
