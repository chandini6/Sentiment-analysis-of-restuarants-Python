"""
A simple script that demonstrates how we classify textual data with sklearn.
"""
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from numpy import array


#read the reviews and their polarities
def loadReviews(fname):
    
    reviews=[]
    polarities=[]
    f=open(fname)
    for line in f:
        review,rating=line.strip().split('\t')    
        reviews.append(review.lower())    
        polarities.append(int(rating))
    f.close()

    return reviews,polarities


rev_train,pol_train=loadReviews('publicremarks.csv')
#rev_test,pol_test=loadReviews('test1.txt')


#count the number of times each term appears in a document and transform each doc into a count vector
counter = CountVectorizer()
counts_train = counter.fit_transform(rev_train)

#transform the counts into the tfidfd format. http://en.wikipedia.org/wiki/Tf%E2%80%93idf
transformer = TfidfTransformer()
transformed_train = transformer.fit_transform(counts_train)

#apply the same transformation on the test datqs
counts_test=counter.transform(rev_test)
transformed_test=transformer.transform(counts_test)

#make ane empty model
classifier=LogisticRegression()

#fit the model on the training data
classifier.fit(transformed_train,pol_train)

#get the accuracy on the test data
print 'ACCURACY:\t',classifier.score(transformed_test,pol_test)

print 'PREDICTED:\t',classifier.predict(transformed_test)
print 'CORRECT:\t', array(pol_test)

cm = confusion_matrix(transformed_test,pol_test)
print cm






