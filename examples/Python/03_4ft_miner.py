import pandas as pd
import sys
import sklearn.impute
from matplotlib import pyplot as plt

from sklearn.impute import SimpleImputer

from cleverminer import cleverminer

df = pd.read_csv ('https://www.cleverminer.org/data/accidents.zip', encoding='cp1250', sep='\t')
df=df[['Driver_Age_Band','Driver_IMD','Sex','Area','Journey','Road_Type','Speed_limit','Light','Vehicle_Location','Vehicle_Type','Vehicle_Age','Hit_Objects_in','Hit_Objects_off','Casualties','Severity']]

imputer = SimpleImputer(strategy="most_frequent")
df = pd.DataFrame(imputer.fit_transform(df),columns = df.columns)

clm = cleverminer(df=df,proc='4ftMiner',
                           quantifiers= {'Base':2000, 'aad':1},
                           ante ={
                                        'attributes':[
                                                {'name': 'Driver_Age_Band', 'type': 'seq', 'minlen': 1, 'maxlen': 3},
                                                {'name': 'Speed_limit', 'type': 'seq', 'minlen': 1, 'maxlen': 2},
                                                {'name': 'Sex', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                                                {'name': 'Journey', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
                                        ], 'minlen':1, 'maxlen':4, 'type':'con'},
                           succ ={
                                        'attributes':[
                                                {'name': 'Severity', 'type': 'lcut', 'minlen': 1, 'maxlen': 2}
                                        ], 'minlen':1, 'maxlen':1 , 'type':'con'}
                           )

clm.print_rulelist()
clm.print_summary()
clm.print_rule(3)
clm.draw_rule(3)