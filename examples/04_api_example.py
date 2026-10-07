clm = cleverminer(df=df,proc='4ftMiner',
       quantifiers= {'Base':2000, 'aad':0.4},
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

print(clm.result)
clm.print_summary()
clm.print_rulelist()
clm.print_rule(8)