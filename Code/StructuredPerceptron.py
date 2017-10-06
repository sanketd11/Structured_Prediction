
# coding: utf-8

# In[14]:

from random import shuffle
import pandas as pd
import numpy as np
from stemming.porter2 import stem


# In[341]:

class structuredPerceptron():
    def __init__(self,learningRate=0.001,C=0.1):
        self.weight={}
        self.avg={}
        self.gamma=learningRate
        self.C=C
        
    """sentence and label will be the lists""" 

    def featureExt(self,sentence,label):           
        featureVect={}
        #emission features
        if (not isinstance(sentence,list)):
            sentence=[''.join(sentence)]
        if (not isinstance(label,list)):
            label=[''.join(label)]
#         print sentence, label
        if len(label)==len(sentence):
#             print sentence, label
            emission=zip(sentence,label)
#             print emission
            for feat in emission:
#                 print 'feat tuple: ', feat
                key =str(feat[0]+'_'+feat[1])
                if featureVect.has_key(key):
                    featureVect[key]+=1
                else:
                    featureVect[key]=1
                
            #transition features
            transitionsLavel1=[]
#             print 'label: ', label
            if len(label)==1:
                transitionsLavel1.append('start'+'_'+label[0])
            else:
                transitionsLavel1=[str(label[i]+'_'+label[i+1]) for i in range(len(label)-1)]
                transitionsLavel1.append('start'+'_'+label[0])
                transitionsLavel1.append('end'+'_'+label[-1])

            for trans in transitionsLavel1:
                key = trans
                if featureVect.has_key(key):
                    featureVect[key]+=1
                else:
                    featureVect[key]=1
            
        return featureVect
    
    def score(self,featureVect):
        summ=0
        for key, value in featureVect.iteritems():
            if self.weight.has_key(key):
                summ+=self.weight[key]*featureVect[key]
            else:
                self.weight[key]=0
        return summ
    
    
    def findQty(self,inp):
        qtySFound=False
        qtyEFound=False
        fractions={'1/2':0.5,'3/4':0.75,'1/4':0.25,'1/8':0.125,'1/3':0.33,'2/3':0.66}
        qtys=0
        qtye=0
        word=inp
        i=0
    #     print inp
        label_array=[None]*len(inp)
        while(i < len(inp)):
            if not qtySFound and i<len(inp)-1:
                if word[i].isdigit() or word[i] in fractions.keys():
                    qtySFound=True
                    if word[i] in fractions.keys():
                        qtys=fractions[word[i]]
                        index=i
                        label_array[i]='qtys'
                    else:
                        qtys=int(word[i])
                        label_array[i]='qtys'
                        if word[i+1] in fractions.keys():
                            qtys=qtys+fractions[word[i+1]]
                            label_array[i+1]='qtys'
                            i=i+1   
                            index=i+1
                        else:
                            index=i


                    i=i+1
                    continue

            if not qtyEFound and i<len(inp)-1 and qtySFound:
                if i>(index+1):
                    break

                if word[i].isdigit() or word[i] in fractions.keys() :
                    qtyEFound=True
                    if word[i] in fractions.keys():
                        qtye=fractions[word[i]]
                        label_array[i]='qtye'
                    else:
                        qtye=int(word[i])
                        label_array[i]='qtye'
                        if word[i+1] in fractions.keys():
                            qtye=qtye+fractions[word[i+1]]
                            label_array[i+1]='qtye'

            if qtySFound and qtyEFound:
                break

            i=i+1
        return label_array

    
    def viterbiRaw(self,inp,DEBUG=False):
        alpha1=[]
        alpha2=[]
        alpha3=[]
        
        labelmap={
            0:'name',
            1:'unit',
            2:'comment'        
        }
        alphamap={
            0:alpha1,
            1:alpha2,
            2:alpha3        
        }
        
        label=self.findQty(inp)
#         print label

        if label.count(None)<=len(inp):
            viterbi_table=np.zeros((3,len(inp)))
            backpointer=np.zeros((3,len(inp)))

            k=0;
            while(label[k]=='qtys' or label[k]=='qtye'):
                if label[k]=='qtys':
                        alpha1.append('qtys')
                        alpha2.append('qtys')
                        alpha3.append('qtys')
                        
                else:
                    alpha1.append('qtye')
                    alpha2.append('qtye')
                    alpha3.append('qtye')
                backpointer[0][k] = 0;
                backpointer[1][k] = 1;
                backpointer[2][k] = 2;
                k=k+1;

    #         print k, label[k]
           
            
            viterbi_table[0][k]= self.score(self.featureExt(inp[0:k+1],alpha1+['name']))
            alpha1.append('name')
            viterbi_table[1][k]= self.score(self.featureExt(inp[0:k+1],alpha2+['unit']))
            alpha2.append('unit')
            viterbi_table[2][k]= self.score(self.featureExt(inp[0:k+1],alpha3+['comment']))
            alpha3.append('comment')
            if DEBUG:
                print 'before: ', alpha1, alpha2,alpha3
            for j in range(k+1,len(inp)):
                
                #Assumes previous column was something else
                if label[j]=='qtys' or label[j]=='qtye':
                    if label[j]=='qtys':
                        alpha1.append('qtys')
                        alpha2.append('qtys')
                        alpha3.append('qtys')
                        
                    else:
                        alpha1.append('qtye')
                        alpha2.append('qtye')
                        alpha3.append('qtye')
                    viterbi_table[0][j] = viterbi_table[0][j-1];
                    viterbi_table[1][j] = viterbi_table[1][j-1];
                    viterbi_table[2][j] = viterbi_table[2][j-1];
                    backpointer[0][j] = backpointer[0][j-1];
                    backpointer[1][j] = backpointer[1][j-1];
                    backpointer[2][j] = backpointer[2][j-1];
                    
                else:
                    if(j!=0):                        
                        max1=[self.score(self.featureExt(inp[0:j+1],alpha1+['name'])), self.score(self.featureExt(inp[0:j+1],alpha2+['name'])),self.score(self.featureExt(inp[0:j+1],alpha3+['name']))]
                        viterbi_table[0][j]=max(max1)
                        backpointer[0][j]=max1.index(max(max1))
                        if DEBUG:
                            print 'input: \n',inp[0:j+1]
                            
                            print 'max1: \n',max1


                        max2=[self.score(self.featureExt(inp[0:j+1],alpha1+['unit'])), self.score(self.featureExt(inp[0:j+1],alpha2+['unit'])),self.score(self.featureExt(inp[0:j+1],alpha3+['unit']))]
                        viterbi_table[1][j]=max(max2)
                        backpointer[1][j]=max2.index(max(max2))
                        if DEBUG:
                            print 'max2: \n',max2


                        max3=[self.score(self.featureExt(inp[0:j+1],alpha1+['comment'])), self.score(self.featureExt(inp[0:j+1],alpha2+['comment'])),self.score(self.featureExt(inp[0:j+1],alpha3+['comment']))]
                        viterbi_table[2][j]=max(max3)
                        backpointer[2][j]=max3.index(max(max3))
                        if DEBUG:
                            print 'max3: \n',max3

                        alpha1=alphamap[max1.index(max(max1))]+['name']
                        alpha2=alphamap[max2.index(max(max2))]+['unit']
                        alpha3=alphamap[max3.index(max(max3))]+['comment'] 
                        if DEBUG:                 
                            print 'alpha at ',j,'th step: \n', alpha1, alpha2,alpha3
                   

            last_col=viterbi_table[:,-1]
            back=np.argmax(last_col)
            label[-1]=labelmap[np.argmax(last_col)]

            for h in range(len(inp)-2,-1,-1):
                if(label[h]==None):
                    label[h]=labelmap[backpointer[back][h+1]]
                back=backpointer[back][h]
        return viterbi_table,backpointer, label

    
    
    
   
    
    def predict(self,sentence,test=False):
        if test:
            DEBUG=True
#             self.weight=self.avg
            viterbi_table,backpointer, labelPredicted=self.viterbiRaw(sentence,DEBUG)
            print 'viterbi table',viterbi_table
            print 'backpointer: ',backpointer
        else: 
            viterbi_table,backpointer, labelPredicted=self.viterbiRaw(sentence)
        return labelPredicted
            
    
    def train(self,data):        
        for j in range(20):  #Number of epochs=10 
            shuffle(data)
            i=1
            for sent in data:
                gamma_t=self.gamma*1.0/(1+self.gamma*self.C*i)
                i+=1
                
                sentence=sent[0]
                labelTrain=sent[1]
                labelPredicted=self.predict(sentence)                

                features1=self.featureExt(sentence,labelTrain) #correct
                features2=self.featureExt(sentence,labelPredicted) #prediction
                featureCombined={}
               
            #update on mistake
                for key,value in features1.iteritems():
                    if not self.weight.has_key(key):
                        self.weight[key]=0  #add to weight vector 
                    if features2.has_key(key):
                        featureCombined[key]=features1[key]-features2[key]
                    else:
                        featureCombined[key]=features1[key]

                for key,value in features2.iteritems():
                    if not self.weight.has_key(key):
                        self.weight[key]=0
                    if not features1.has_key(key) :
                        featureCombined[key]=-1*features2[key]

                
                for key,value in featureCombined.iteritems():
                    self.weight[key]+=gamma_t*featureCombined[key]
                
                for key,value in self.weight.iteritems():
                    if self.avg.has_key(key):
                        self.avg[key]+=self.weight[key]
                    else:
                        self.avg[key]=self.weight[key]
        
        
    
    def test(self,sentence,test=False):
        label=self.predict(sentence,test)
        return label
    


# # Input

# In[339]:

data= pd.read_csv('../nyt_training.csv')
with open('../stopwords.txt','r') as f:
    stopwords=f.readlines()
    stopwords=[word.strip('\n') for word in stopwords]

input_col=data['input']
input_col=[str(nm).lower() for nm in input_col]
input_col=[nm.split(' ') for nm in input_col]
input_col=[[stem(word.strip(",')( \n")) for word in ls if word not in stopwords  ] for ls in input_col]
# input_col

name_col=data['name']
nameCountMap={}
name_col=[str(nm).lower() for nm in name_col]
name_col=[nm.split(' ') for nm in name_col]
name_col=[[stem(word.strip(",')( \n")) for word in ls if word not in stopwords  ] for ls in name_col]
word_list_name=[word for ls in name_col for word in ls]


unit_col=data['unit']
unit_col=[str(nm).lower() for nm in unit_col]
unit_col=[nm.split(' ') for nm in unit_col]
unit_col=[[stem(word.strip(",')( \n")) for word in ls if word not in stopwords  ] for ls in unit_col]

word_list_unit=[word for ls in unit_col for word in ls]# unit_col


comment_col=data['comment']
comment_col=[str(nm).lower() for nm in comment_col]
comment_col=[nm.split(' ') for nm in comment_col]
comment_col=[[stem(word.strip(",')( \n")) for word in ls if word not in stopwords  ] for ls in comment_col]
word_list_comment=[word for ls in comment_col for word in ls]

qtys_col=data['qty']
qtys_col=[nm for nm in qtys_col]

qtye_col=data['range_end']
qtye_col=[nm for nm in qtye_col]


# In[246]:

def correctLabels(index,label):
    for i in range(len(label)):
        if label[i] not in ['qtys','qtye']:
            if input_col[index][i] in name_col[index]:
                label[i]='name'
            
            elif input_col[index][i] in unit_col[index]:
                label[i]='unit'
                
#             elif input_col[index][i] in comment_col[index]:
#                 label[i]='comment'
            else:
                label[i]='comment'
        
        
                
    return label


# In[342]:

sp= structuredPerceptron(learningRate=0.01)

datalabels=[sp.findQty(sent) for sent in input_col]
datalabels=[correctLabels(i,datalabels[i]) for i in range(len(datalabels))]
# print datalabels[4]                
data=zip(input_col,datalabels)

sp.train(data[0:10000])

# print sp.featureExt(['1/4', 'cup', 'extra-virgin', 'oliv', 'oil'], ['qtys', 'unit', 'comment', 'name', 'name'])
# print data[2:3]


# In[338]:

sp.weight
# for j in range(10):
print sp.test(data[7][0],test=True)
print data[7]


# In[343]:

with open('weight10000.text','w') as f:
    f.write(str(sp.weight))
# sp.weight


# In[346]:

def evaluate(label,given,qtys,qtye,name,unit,comment):
    global correct_sentence
    global heatmap
    correct_words=0
    _qtys=0
    _qtye=0
    flagqs=0
    flagqe=0
    fractions={'1/2':0.5,'3/4':0.75,'1/4':0.25,'1/8':0.125,'1/3':0.33,'2/3':0.66}
    for i in range(len(label)):
        if label[i]=='qtys':
            if fractions.has_key(given[i]):
                _qtys=_qtys+fractions[given[i]]
            else:
                _qtys=_qtys+int(given[i])
            correct_words=correct_words+1
            if label[i+1]=='qtys':
                if fractions.has_key(given[i]):
                    _qtys=_qtys+fractions[given[i]]
                else:
                    _qtys=_qtys+int(given[i])
                correct_words=correct_words+1
                i=i+2
                
            if _qtys==qtys:
                heatmap[0,0]=heatmap[0,0]+1

                
        if label[i]=='qtye':
            if fractions.has_key(given[i]):
                _qtye=_qtye+fractions[given[i]]
            else:
                _qtye=_qtye+int(given[i])
            
            correct_words=correct_words+1
            
            if label[i+1]=='qtys':
                if fractions.has_key(given[i]):
                    _qtye=_qtye+fractions[given[i]]
                else:
                    _qtye=_qtye+int(given[i])
                correct_words=correct_words+1
                i=i+2
                
            if _qtye==qtye:
                heatmap[1,1]=heatmap[1,1]+1

                
        
        if label[i]=='name':
            if given[i] in name:
                heatmap[3,3]=heatmap[3,3]+1
                correct_words=correct_words+1
            elif given[i] in unit :
                heatmap[3,2]=heatmap[3,2]+1
            elif given[i] in comment :
                heatmap[3,4]=heatmap[3,4]+1
        elif label[i]=='unit':
            if given[i] in name:
                heatmap[2,3]=heatmap[2,3]+1
            elif given[i] in unit :
                heatmap[2,2]=heatmap[2,2]+1
                correct_words=correct_words+1
            elif given[i] in comment :
                heatmap[2,4]=heatmap[2,4]+1
        elif label[i]=='comment':
            if given[i] in name:
                heatmap[4,3]=heatmap[4,3]+1
            elif given[i] in unit :
                heatmap[4,2]=heatmap[4,2]+1
            elif given[i] in comment :
                heatmap[4,4]=heatmap[4,4]+1
                correct_words=correct_words+1
      
#     print 'correct_words: ', correct_words, '  label Len: ', len(label)
    if correct_words==len(label):
        correct_sentence=correct_sentence+1


# In[350]:

test_input_col=input_col
test_name_col=name_col
test_comment_col=comment_col
test_unit_col=unit_col
test_qtys_col=qtys_col
test_qtye_col=qtye_col
heatmap=np.matrix(np.zeros((5,5)))
correct_sentence=0
result=[]
for i in range(0,len(test_input_col[0:10000])):
    label=sp.test(test_input_col[i])
    result.append({'Given':test_input_col[i],'QtyStart':test_qtys_col[i] ,'QtyEnd': test_qtye_col[i],'Name':test_name_col[i],'Unit':test_unit_col[i],'Comment':test_comment_col[i]})
#     print 'prediction: \n',label
#     print 'Given: \n',test_input_col[i],'\nQty Start: ', test_qtys_col[i] ,'\nQty End: ', test_qtye_col[i],'\n Name: ',test_name_col[i],'\n Unit:',test_unit_col[i],'\n Comment',test_comment_col[i]
    evaluate(label=label,given=test_input_col[i],qtys=test_qtys_col[i],qtye=test_qtye_col[i],name=test_name_col[i],unit=test_unit_col[i],comment=test_comment_col[i])

with open('trainResult.txt', 'w') as fb:
        fb.write(str(result))    
    
#Train Results
print heatmap
print correct_sentence
print len(test_input_col)
print 'Train Sentence Accuracy: ', 1.0*correct_sentence/len(test_input_col[0:10000])

