
# coding: utf-8

# In[73]:

import pandas as pd
import numpy as np
from stemming.porter2 import stem


# In[129]:

data= pd.read_csv('../nyt_training.csv')
with open('../stopwords.txt','r') as f:
    stopwords=f.readlines()
    stopwords=[word.strip('\n') for word in stopwords]


# In[144]:

input_col=data['input']
split_sents=[]
for sent in input_col:
    split_sents.append(str(sent).split(' '))


# In[145]:

input_col=data['input']
input_col=[str(nm).lower() for nm in input_col]
input_col=[nm.split(' ') for nm in input_col]
input_col=[[stem(word.strip(",')(")) for word in ls if word not in stopwords  ] for ls in input_col]
# input_col


# In[146]:

name_col=data['name']
nameCountMap={}
name_col=[str(nm).lower() for nm in name_col]
name_col=[nm.split(' ') for nm in name_col]
name_col=[[stem(word.strip(",')(")) for word in ls if word not in stopwords  ] for ls in name_col]
word_list_name=[word for ls in name_col for word in ls]
# word_list_name

# for word in word_list:
#     if not nameCountMap.has_key(word):
#         nameCountMap[word]=word_list.count(word)


# In[147]:

unit_col=data['unit']
unit_col=[str(nm).lower() for nm in unit_col]
unit_col=[nm.split(' ') for nm in unit_col]
unit_col=[[stem(word.strip(",')(")) for word in ls if word not in stopwords  ] for ls in unit_col]

word_list_unit=[word for ls in unit_col for word in ls]# unit_col
# for word in word_list:
#     if not nameCountMap.has_key(word):
#         nameCountMap[word]=word_list.count(word)


# In[148]:

comment_col=data['comment']
comment_col=[str(nm).lower() for nm in comment_col]
comment_col=[nm.split(' ') for nm in comment_col]
comment_col=[[stem(word.strip(",')(")) for word in ls if word not in stopwords  ] for ls in comment_col]
word_list_comment=[word for ls in comment_col for word in ls]


# # Emission Probability Calculations

# In[149]:

all_words=[]
all_words.extend(word_list_name)
all_words.extend(word_list_unit)
all_words.extend(word_list_comment)

all_words=set(all_words)

countMap={}
countMap['name']={}
countMap['unit']={}
countMap['comment']={}

for word in all_words:
    if word !='nan':
        countMap['name'][word]=1
        countMap['comment'][word]=1
        countMap['unit'][word]=1
        if word in word_list_name:
            countMap['name'][word]=word_list_name.count(word)+1
        if word in word_list_comment:
            countMap['comment'][word]=word_list_comment.count(word)+1
        if word in word_list_unit:
            countMap['unit'][word]=word_list_unit.count(word)+1
        



# In[252]:


totalCountMap={}

for key, value in countMap.iteritems():
    totalCountMap[key]=sum(value.values())
    
for key, value in countMap.iteritems():
    for key2, value2 in value.iteritems():
        countMap[key][key2]=1.0*countMap[key][key2]/totalCountMap[key] 

# print totalcountMap
# print countMap


# # Transition Probability Calculations

# In[280]:

# name
# qtys
# qtye
# unit
# comment
#name fist quantity second




start_name=0
start_qtys=0
start_qtye=0
start_unit=0
start_comment=0


name_qtys =0
name_qtye =0
name_name =0
name_unit =0
name_comment =0

qtys_name =0
qtys_qtys =0
qtys_qtye =0
qtys_unit =0
qtys_comment =0

qtye_name =0
qtye_qtys =0
qtye_qtye =0
qtye_unit =0
qtye_comment =0

unit_name =0
unit_qtys =0
unit_qtye =0
unit_unit =0
unit_comment =0

comment_name =0
comment_qtys =0
comment_qtye =0
comment_unit =0
comment_comment =0




def transitionProb(inp,indx):
    global start_name
    global start_qtys
    global start_qtye
    global start_unit
    global start_comment


    global name_qtys 
    global name_qtye 
    global name_name 
    global name_unit 
    global name_comment 

    global qtys_name 
    global qtys_qtys 
    global qtys_qtye 
    global qtys_unit 
    global qtys_comment 

    global qtye_name 
    global qtye_qtys 
    global qtye_qtye 
    global qtye_unit 
    global qtye_comment 

    global unit_name 
    global unit_qtys 
    global unit_qtye 
    global unit_unit 
    global unit_comment 

    global comment_name 
    global comment_qtys 
    global comment_qtye 
    global comment_unit 
    global comment_comment 


    qtySFound=False
    qtyEFound=False
    fractions={'1/2':0.5,'3/4':0.75,'1/4':0.25,'1/8':0.125,'1/3':0.33,'2/3':0.66}
    qtys=0
    qtye=0
    word=inp
    
    #Check for quantities Start and End
#     for i in range(0,len(inp)):
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
    
    for i in range(0, len(inp)):
        if label_array[i]==None:
            if word[i] in name_col[indx]:
                label_array[i]='name'
#                 print 'Label for',word[i],' is name\n'
                continue
            elif word[i] in unit_col[indx]:
                label_array[i]='unit'
#                 print 'Label for',word[i],' is unit\n'
                continue
            elif word[i] in comment_col[indx]:
                label_array[i]='comment'
#                 print 'Label for',word[i],' is comment\n'
                continue
        
    for i in range(0, len(inp)):
        if(i==0):
            if(label_array[0]=='name'):
                start_name = start_name + 1;
            elif(label_array[0]=='qtys'):
                start_qtys = start_qtys + 1;
            elif(label_array[0]=='qtye'):
                start_qtye = start_qtye + 1;
            elif(label_array[0]=='unit'):
                start_unit = start_unit+ 1;
            elif(label_array[0]=='comment'):
                start_comment = start_comment + 1;
        else:
            if(label_array[i-1]=='name' and label_array[i]=='name'):
                name_name = name_name + 1;
            elif(label_array[i-1]=='name' and label_array[i]=='qtys'):
                name_qtys = name_qtys + 1;
            elif(label_array[i-1]=='name' and label_array[i]=='qtye'):
                name_qtye = name_qtye + 1;
            elif(label_array[i-1]=='name' and label_array[i]=='unit'):
                name_unit = name_unit + 1;
            elif(label_array[i-1]=='name' and label_array[i]=='comment'):
                name_comment = name_comment + 1;
                
            elif(label_array[i-1]=='qtys' and label_array[i]=='name'):
                qtys_name = qtys_name + 1;
            elif(label_array[i-1]=='qtys' and label_array[i]=='qtys'):
                qtys_qtys = qtys_qtys + 1;
            elif(label_array[i-1]=='qtys' and label_array[i]=='qtye'):
                qtys_qtye = qtys_qtye + 1;
            elif(label_array[i-1]=='qtys' and label_array[i]=='unit'):
                qtys_unit = qtys_unit + 1;
            elif(label_array[i-1]=='qtys' and label_array[i]=='comment'):
                qtys_comment = qtys_comment + 1;
                
            elif(label_array[i-1]=='qtye' and label_array[i]=='name'):
                qtye_name = qtye_name + 1;
            elif(label_array[i-1]=='qtye' and label_array[i]=='qtys'):
                qtye_qtys = qtye_qtys + 1;
            elif(label_array[i-1]=='qtye' and label_array[i]=='qtye'):
                qtye_qtye = qtye_qtye + 1;
            elif(label_array[i-1]=='qtye' and label_array[i]=='unit'):
                qtye_unit = qtye_unit + 1;
            elif(label_array[i-1]=='qtye' and label_array[i]=='comment'):
                qtye_comment = qtye_comment + 1;
            
            elif(label_array[i-1]=='unit' and label_array[i]=='name'):
                unit_name = unit_name + 1;
            elif(label_array[i-1]=='unit' and label_array[i]=='qtys'):
                unit_qtys = unit_qtys + 1;
            elif(label_array[i-1]=='unit' and label_array[i]=='qtye'):
                unit_qtye = unit_qtye + 1;
            elif(label_array[i-1]=='unit' and label_array[i]=='unit'):
                unit_unit = unit_unit + 1;
            elif(label_array[i-1]=='unit' and label_array[i]=='comment'):
                unit_comment = unit_comment + 1;
                
            elif(label_array[i-1]=='comment' and label_array[i]=='name'):
                comment_name = comment_name + 1;
            elif(label_array[i-1]=='comment' and label_array[i]=='qtys'):
                comment_qtys = comment_qtys + 1;
            elif(label_array[i-1]=='comment' and label_array[i]=='qtye'):
                comment_qtye = comment_qtye + 1;
            elif(label_array[i-1]=='comment' and label_array[i]=='unit'):
                comment_unit = comment_unit + 1;
            elif(label_array[i-1]=='comment' and label_array[i]=='comment'):
                comment_comment = comment_comment + 1;
                     
# transitionProb([ '2','3/4', '3','3/4','tablespoon', 'veget', 'oil' ])     
# transitionProb([ '3/4', '3','3/4','tablespoon', 'veget', 'oil' ])     
# transitionProb([ '2','3/4', '3','tablespoon', 'veget', 'oil' ])     
# transitionProb([ '2','3','3/4','tablespoon', 'veget', 'oil' ])     
# transitionProb([ '3/4','3/4', 'tablespoon', 'veget', 'oil' ])
# transitionProb([ '3/4','tablespoon', 'veget', 'oil' ]) 
# transitionProb([ '3','tablespoon', 'veget', 'oil' ]) 
# transitionProb([ '2','3','tablespoon', 'veget', 'oil' ])
# transitionProb([ '2','3/4','tablespoon', 'veget', 'oil' ])
# transitionProb([ 'tablespoon', 'veget', 'oil' ]) 
print qtys_qtye





# In[284]:

for i in range(0,len(input_col)):
    transitionProb(input_col[i],i)

trans_prob=np.zeros((6, 5))
#start
#name
#qtys
#qtye
#unit
#comment
trans_prob[0][0] =  start_name
trans_prob[0][1] =  start_qtys
trans_prob[0][2] =  start_qtye
trans_prob[0][3] =  start_unit
trans_prob[0][4] =  start_comment

trans_prob[1][0] =  name_qtys 
trans_prob[1][1] =  name_qtye 
trans_prob[1][2] =  name_name 
trans_prob[1][3] =  name_unit 
trans_prob[1][4] =  name_comment 

trans_prob[2][0] =  qtys_name 
trans_prob[2][1] =  qtys_qtys 
trans_prob[2][2] =  qtys_qtye 
trans_prob[2][3] =  qtys_unit 
trans_prob[2][4] =  qtys_comment 

trans_prob[3][0] =  qtye_name 
trans_prob[3][1] =  qtye_qtys 
trans_prob[3][2] =  qtye_qtye 
trans_prob[3][3] =  qtye_unit 
trans_prob[3][4] =  qtye_comment 

trans_prob[4][0] =  unit_name 
trans_prob[4][1] =  unit_qtys 
trans_prob[4][2] =  unit_qtye 
trans_prob[4][3] =  unit_unit 
trans_prob[4][4] =  unit_comment 

trans_prob[5][0] =  comment_name 
trans_prob[5][1] =  comment_qtys 
trans_prob[5][2] =  comment_qtye 
trans_prob[5][3] =  comment_unit 
trans_prob[5][4] =  comment_comment 

print qtys_name, qtys_unit


# In[286]:

temp = 1.0*1.0*(start_name + start_unit + start_comment + start_qtys + start_qtye + 5);
start_name = 1.0*1.0*(start_name+1)/temp;
start_unit = 1.0*1.0*(start_unit+1)/temp;
start_comment = 1.0*1.0*(start_comment+1)/temp;
start_qtys = 1.0*1.0*(start_qtys+1)/temp;
start_qtye = 1.0*1.0*(start_qtye+1)/temp;

temp = 1.0*1.0*(name_name + name_unit + name_comment + name_qtys + name_qtye + 5);
name_name = 1.0*(name_name+1)/temp;
name_unit = 1.0*(name_unit+1)/temp;
name_comment = 1.0*(name_comment+1)/temp;
name_qtys = 1.0*(name_qtys+1)/temp;
name_qtye = 1.0*(name_qtye+1)/temp;

temp = 1.0*(unit_name + unit_unit + unit_comment + unit_qtys + unit_qtye + 5);
unit_name = 1.0*(unit_name+1)/temp;
unit_unit = 1.0*(unit_unit+1)/temp;
unit_comment = 1.0*(unit_comment+1)/temp;
unit_qtys = 1.0*(unit_qtys+1)/temp;
unit_qtye = 1.0*(unit_qtye+1)/temp;

temp = 1.0*(comment_name + comment_unit + comment_comment + comment_qtys + comment_qtye + 5);
comment_name = 1.0*(comment_name+1)/temp;
comment_unit = 1.0*(comment_unit+1)/temp;
comment_comment = 1.0*(comment_comment+1)/temp;
comment_qtys = 1.0*(comment_qtys+1)/temp;
comment_qtye = 1.0*(comment_qtye+1)/temp;


temp = 1.0*(qtys_name + qtys_unit + qtys_comment + qtys_qtys + qtys_qtye + 5);
print qtys_name, qtys_unit, temp
qtys_name = 1.0*(qtys_name+1)/temp;
qtys_unit = 1.0*(qtys_unit+1)/temp;
qtys_comment = 1.0*(qtys_comment+1)/temp;
qtys_qtys = 1.0*(qtys_qtys+1)/temp;
qtys_qtye = 1.0*(qtys_qtye+1)/temp;

temp = 1.0*(qtye_name + qtye_unit + qtye_comment + qtye_qtys + qtye_qtye + 5);
qtye_name = 1.0*(qtye_name+1)/temp;
qtye_unit = 1.0*(qtye_unit+1)/temp;
qtye_comment = 1.0*(qtye_comment+1)/temp;
qtye_qtys = 1.0*(qtye_qtys+1)/temp;
qtye_qtye = 1.0*(qtye_qtye+1)/temp;


print qtys_name, qtys_unit


# In[154]:

# Smoothing + Normalizing the transition probabilities
trans_prob_Nsmth=trans_prob+1 
for i in range(5):
    trans_prob_Nsmth[i]=1.0*trans_prob_Nsmth[i]/sum(trans_prob_Nsmth[i])
trans_prob_Nsmth


# # Inference Algorithm (Viterbi)
# 
# 
# 
# 

# In[287]:

def findQty(inp):
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
        
  
    


# In[288]:

def viterbi(inp):
    labelmap={
        0:'name',
        1:'unit',
        2:'comment'        
    }
    label=findQty(inp)
    
    if label.count(None)==len(inp):
        viterbi_table=np.zeros((3,len(inp)))
        backpointer=np.zeros((3,len(inp)))
        
        
        viterbi_table[0][0]=start_name*countMap['name'][inp[0]]
        viterbi_table[1][0]=start_unit*countMap['unit'][inp[0]]
        viterbi_table[2][0]=start_comment*countMap['comment'][inp[0]]
        
        for j in range(1,len(inp)):
            
            
            
            max1=[name_name*viterbi_table[0][j-1], unit_name*viterbi_table[1][j-1], comment_name*viterbi_table[2][j-1]]
            viterbi_table[0][j]=countMap['name'][inp[j]]*max(max1)
            backpointer[0][j]=max1.index(max(max1))
            
            max2=[name_unit*viterbi_table[0][j-1], unit_unit*viterbi_table[1][j-1], comment_unit*viterbi_table[2][j-1]]
            viterbi_table[1][j]=countMap['unit'][inp[j]]*max(max2)
            backpointer[1][j]=max2.index(max(max2))
            
            max3=[name_comment*viterbi_table[0][j-1], unit_comment*viterbi_table[1][j-1], comment_comment*viterbi_table[2][j-1]]
            viterbi_table[2][j]=countMap['comment'][inp[j]]*max(max3)
            backpointer[2][j]=max3.index(max(max3))
            
            
            
        last_col=viterbi_table[:,-1]
        back=np.argmax(last_col)
        label[-1]=labelmap[np.argmax(last_col)]
        
        for k in range(len(inp)-2,-1,-1):
            label[k]=labelmap[backpointer[back][k+1]]
            back=backpointer[back][k]
    return viterbi_table,backpointer, label


# In[299]:

# viterbi for qtys,qtye
def viterbi(inp):
    labelmap={
        0:'name',
        1:'unit',
        2:'comment'        
    }
    lmap={
        'qtys_name':qtys_name,
        'qtys_unit':qtys_unit,
        'qtys_comment':qtys_comment,
        'qtye_name':qtye_name,
        'qtye_unit':qtye_unit,
        'qtye_comment':qtye_comment,
        'start_name':start_name,
        'start_unit':start_unit,
        'start_comment':start_comment,
        
    }
    label=findQty(inp)
#     print label
    
    if label.count(None)<=len(inp):
        viterbi_table=np.zeros((3,len(inp)))
        backpointer=np.zeros((3,len(inp)))
        
        k=0;
        while(label[k]=='qtys' or label[k]=='qtye'):
            backpointer[0][k] = 0;
            backpointer[1][k] = 1;
            backpointer[2][k] = 2;
            k=k+1;
        
#         print k, label[k]
        
        if label[k]==None and k!=0:
            last_label = label[k-1];
        else:
            last_label='start'
            
        lab=[last_label+'_name',last_label+'_unit',last_label+'_comment']
#         print lab
        
        if (not countMap['name'].has_key(inp[k])or not countMap['unit'].has_key(inp[k]) or not countMap['comment'].has_key(inp[k])):
            name=1#(1.0/totalCountMap['name'])
            unit=1#(1.0/totalCountMap['unit'])
            comment=1#(1.0/totalCountMap['comment'])
        else:
            name=(countMap['name'][inp[k]])
            unit=(countMap['unit'][inp[k]])
            comment=(countMap['comment'][inp[k]])
        
        viterbi_table[0][k]=lmap[lab[0]]*name
        viterbi_table[1][k]=lmap[lab[1]]*unit
        viterbi_table[2][k]=lmap[lab[2]]*comment
        
        for j in range(k+1,len(inp)):
            if (not countMap['name'].has_key(inp[j])or not countMap['unit'].has_key(inp[j]) or not countMap['comment'].has_key(inp[j])):
                name=1#(1.0/totalCountMap['name'])
                unit=1#(1.0/totalCountMap['unit'])
                comment=1#(1.0/totalCountMap['comment'])
            else:
                name=(countMap['name'][inp[j]])
                unit=(countMap['unit'][inp[j]])
                comment=(countMap['comment'][inp[j]])
            #Assumes previous column was something else
            if label[j]=='qtys' or label[j]=='qtye':
                viterbi_table[0][j] = viterbi_table[0][j-1];
                viterbi_table[1][j] = viterbi_table[1][j-1];
                viterbi_table[2][j] = viterbi_table[2][j-1];
                backpointer[0][j] = backpointer[0][j-1];
                backpointer[1][j] = backpointer[1][j-1];
                backpointer[2][j] = backpointer[2][j-1];
            else:

                if(j!=0 and (label[j-1]=='qtys' or label[j-1]=='qtye')):
                    if label[j-1]=='qtys':
                        max1=[qtys_name*viterbi_table[0][j-1], qtys_name*viterbi_table[1][j-1], qtye_name*viterbi_table[2][j-1]]
                        viterbi_table[0][j]=name*max(max1)
                        backpointer[0][j]=max1.index(max(max1))

                        max2=[qtys_unit*viterbi_table[0][j-1], qtys_unit*viterbi_table[1][j-1], qtys_unit*viterbi_table[2][j-1]]
                        viterbi_table[1][j]=unit*max(max2)
                        backpointer[1][j]=max2.index(max(max2))

                        max3=[qtys_comment*viterbi_table[0][j-1], qtys_comment*viterbi_table[1][j-1], qtys_comment*viterbi_table[2][j-1]]
                        viterbi_table[2][j]=comment*max(max3)
                        backpointer[2][j]=max3.index(max(max3))
                    elif label[j-1]=='qtye':
                        max1=[qtye_name*viterbi_table[0][j-1], qtye_name*viterbi_table[1][j-1], qtye_name*viterbi_table[2][j-1]]
                        viterbi_table[0][j]=name*max(max1)
                        backpointer[0][j]=max1.index(max(max1))

                        max2=[qtye_unit*viterbi_table[0][j-1], qtye_unit*viterbi_table[1][j-1], qtye_unit*viterbi_table[2][j-1]]
                        viterbi_table[1][j]=unit*max(max2)
                        backpointer[1][j]=max2.index(max(max2))

                        max3=[qtye_comment*viterbi_table[0][j-1], qtye_comment*viterbi_table[1][j-1], qtye_comment*viterbi_table[2][j-1]]
                        viterbi_table[2][j]=comment*max(max3)
                        backpointer[2][j]=max3.index(max(max3))
                        
                else:
                    max1=[name_name*viterbi_table[0][j-1], unit_name*viterbi_table[1][j-1], comment_name*viterbi_table[2][j-1]]
                    viterbi_table[0][j]=name*max(max1)
                    backpointer[0][j]=max1.index(max(max1))

                    max2=[name_unit*viterbi_table[0][j-1], unit_unit*viterbi_table[1][j-1], comment_unit*viterbi_table[2][j-1]]
                    viterbi_table[1][j]=unit*max(max2)
                    backpointer[1][j]=max2.index(max(max2))

                    max3=[name_comment*viterbi_table[0][j-1], unit_comment*viterbi_table[1][j-1], comment_comment*viterbi_table[2][j-1]]
                    viterbi_table[2][j]=comment*max(max3)
                    backpointer[2][j]=max3.index(max(max3))
            
        last_col=viterbi_table[:,-1]
        back=np.argmax(last_col)
        label[-1]=labelmap[np.argmax(last_col)]
        
        for h in range(len(inp)-2,-1,-1):
            if(label[h]==None):
                label[h]=labelmap[backpointer[back][h+1]]
            back=backpointer[back][h]
    return viterbi_table,backpointer, label


# In[320]:

inp=['1','cup', '2098-pound','pea']
# inp=['fresh','cup','lemon','extract']
viterbi_table,back_table,label=viterbi(inp)
print label
print viterbi_table
print back_table
countMap['comment']['besan']


# In[219]:

print countMap['comment']['bone'],countMap['name']['bone']


# In[297]:





test_input_col=data['input']
test_input_col=[str(nm).lower() for nm in test_input_col]
test_input_col=[nm.split(' ') for nm in test_input_col]
test_input_col=[[stem(word.strip(",')(")) for word in ls if word not in stopwords  ] for ls in test_input_col]



# In[302]:

for i in range(0,len(test_input_col[0:10])):
    viterbi_table,back_table,label=viterbi(test_input_col[i])
    print 'prediction: \n',label
    print 'Given: \n',test_input_col[i],'\n Name: ',name_col[i],'\n Unit:',unit_col[i],'\n Comment',comment_col[i]


# In[305]:

print countMap['name']['extra-virgin'], countMap['comment']['extra-virgin']
print unit_name, unit_comment

