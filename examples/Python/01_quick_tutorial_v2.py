import pandas as pd
import sys

from sklearn.impute import SimpleImputer
from cleverminer import cleverminer

#read the data
df = pd.read_csv ('https://www.cleverminer.org/data/accidents.zip', encoding='cp1250', sep='\t')
df=df[['Driver_Age_Band','Sex','Speed_limit','Severity']]

#handle missing values
imputer = SimpleImputer(strategy="most_frequent")
df = pd.DataFrame(imputer.fit_transform(df),columns = df.columns)

clm = cleverminer(df=df,proc='4ftMiner',
       quantifiers= {'Base':2000, 'aad':0.5},
       ante ={
            'attributes':[
                {'name': 'Driver_Age_Band', 'type': 'seq', 'minlen': 1, 'maxlen': 3},
                {'name': 'Speed_limit', 'type': 'seq', 'minlen': 1, 'maxlen': 2},
                {'name': 'Sex', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
            ], 'minlen':1, 'maxlen':3, 'type':'con'},
       succ ={
            'attributes':[
                {'name': 'Severity', 'type': 'lcut', 'minlen': 1, 'maxlen': 2}
            ], 'minlen':1, 'maxlen':1 , 'type':'con'}
       )

clm.print_summary()
clm.print_rulelist()
clm.print_rule(13)
clm.draw_rule(13)