
# coding: utf-8

# In[20]:

import pandas as pd
from stemming.porter2 import stem


# In[188]:

data= pd.read_csv('../nyt-ingredients-snapshot-2015.csv')
with open('../stopwords.txt','r') as f:
    stopwords=f.readlines()
    stopwords=[word.strip('\n') for word in stopwords]


# In[189]:

input_col=data['input']
split_sents=[]
for sent in input_col:
    split_sents.append(str(sent).split(' '))


# In[190]:

name_col=data['name']
nameCountMap={}
name_col=[str(nm).lower() for nm in name_col]
name_col=[nm.split(' ') for nm in name_col]
name_col=[[stem(word.strip(",'")) for word in ls if word not in stopwords  ] for ls in name_col]
for word in word_list:
    if not nameCountMap.has_key(word):
        nameCountMap[word]=word_list.count(word)


# In[191]:

unit_col=data['unit']
unit_col=[str(nm).lower() for nm in unit_col]
unit_col=[nm.split(' ') for nm in unit_col]
unit_col=[[stem(word.strip(",'")) for word in ls if word not in stopwords  ] for ls in unit_col]
# unit_col


# In[192]:

input_col=data['input']
input_col=[str(nm).lower() for nm in input_col]
input_col=[nm.split(' ') for nm in input_col]
input_col=[[stem(word.strip(",'")) for word in ls if word not in stopwords  ] for ls in input_col]
# input_col


# In[193]:

comment_col=data['comment']
comment_col=[str(nm).lower() for nm in comment_col]
comment_col=[nm.split(' ') for nm in comment_col]
comment_col=[[stem(word.strip(",'")) for word in ls if word not in stopwords  ] for ls in comment_col]


# In[194]:

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
    print inp
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





# In[195]:

for i in range(0,len(input_col)):
    transitionProb(input_col[i],i)


# In[196]:

print start_name
print start_qtys
print start_qtye
print start_unit
print start_comment


print name_qtys 
print name_qtye 
print name_name 
print name_unit 
print name_comment 

print qtys_name 
print qtys_qtys 
print qtys_qtye 
print qtys_unit 
print qtys_comment 

print qtye_name 
print qtye_qtys 
print qtye_qtye 
print qtye_unit 
print qtye_comment 

print unit_name 
print unit_qtys 
print unit_qtye 
print unit_unit 
print unit_comment 

print comment_name 
print comment_qtys 
print comment_qtye 
print comment_unit 
print comment_comment 


