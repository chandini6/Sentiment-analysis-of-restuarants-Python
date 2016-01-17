from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.lda import LDA
from numpy import array
import re



def readLexicon(file_name):
    lexicon = open(file_name)       
    build_lexicon = set()
    for line in lexicon:
        build_lexicon.add(line.strip())
    return build_lexicon
    
    lexicon.close()



#read the reviews and their polarities
def loadReviews(fname):
    
    reviews=[]
    polarities=[]
    print type(reviews)
    f=open(fname)
    for line in f:
        #line  = unicode(line, errors='replace')
        review,rating=line.strip().split('\t')    
        reviews.append(review.lower())    
        polarities.append(int(rating))
        print type(reviews)
    f.close()

    return reviews,polarities


def readReviews(fname):
    file_write = open('output.txt','w')
    f=open(fname)    
    new_reviews=[]
    modified_reviews = []
    polarities=[]    
    for line in f:
        
        #print type(new_reviews)        
        #line  = unicode(line, errors='replace')
        custReviews,rating=line.strip().split('\t')  
        polarities.append(int(rating))
        new_reviews.append(custReviews.lower())
        #print new_reviews        
        for review in new_reviews:
           #print review
            for not_word in notlex :
                if review in review:   
                    #print "inside"
                    print not_word            
                    wrd=not_word.split(' ')
                    wordNew=wrd[0]+wrd[1]
                    print wordNew
                    review1 = re.sub(not_word,wordNew,review)
                    #a_new.append(review1)
                    #print review
                    #print review1
                    #print a
                    new_reviews.remove(review)
                    new_reviews.append(review1)
            
    print new_reviews
        
    return modified_reviews,polarities
    
    f.close()
    file_write.close()        
                
        
    

poslex = readLexicon('positive-words.txt')
neglex = readLexicon('negative-words.txt')    
#rev_train,pol_train=readReviews('reviews.txt')
pos_neg_lex = poslex.union(neglex) 
notlex = set()
for word in pos_neg_lex:
    word = 'not'+' '+word
    notlex.add(word)
rev_train,pol_train=readReviews('test1.txt')
rev_test,pol_test=readReviews('testFile1.txt')



count the number of times each term appears in a document and transform each doc into a count vector
counter = CountVectorizer()
counts_train = counter.fit_transform(rev_train)
print type(counts_train)
#
##transform the counts into the tfidfd format. http://en.wikipedia.org/wiki/Tf%E2%80%93idf
transformer = TfidfTransformer()
transformed_train = transformer.fit_transform(counts_train)
#
##apply the same transformation on the test datqs
counts_test=counter.transform(rev_test)
transformed_test=transformer.transform(counts_test)
#
##make ane empty model
#
classifier=LogisticRegression(penalty='l1',C=5.0) #0.75
classifier=LogisticRegression(penalty='l1',C=5.0)
classifier=KNeighborsClassifier(n_neighbors=4, weights='uniform', algorithm='auto', leaf_size=30, p=2, metric='minkowski', metric_params=None)
classifier=SGDClassifier(loss='hinge', penalty='l2', alpha=0.0001, l1_ratio=0.15, fit_intercept=True, n_iter=5, shuffle=True, verbose=0, epsilon=0.1, n_jobs=1, random_state=None, learning_rate='optimal', eta0=0.0, power_t=0.5, class_weight=None, warm_start=False) #0.65
classifier=LDA(n_components=None, priors=None, shrinkage=None,store_covariance=False, tol=0.0001)
#
##fit the model on the training data
classifier.fit(transformed_train,pol_train)
#
##get the accuracy on the test data
print 'ACCURACY:\t',classifier.score(transformed_test,pol_test)
#
print 'PREDICTED:\t',classifier.predict(transformed_test)
print 'CORRECT:\t', array(pol_test)
