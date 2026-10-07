clm = cleverminer(df=df,proc='SD4ftMiner',
                           quantifiers= {'Base1':4000,'Base2':4000, 'Ratiopim':1.4},
                           ante ={
                                        'attributes':[
                                                {'name': 'Vehicle_Type', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                                                {'name': 'Speed_limit', 'type': 'seq', 'minlen': 1, 'maxlen': 2},
                                        ], 'minlen':1, 'maxlen':4, 'type':'con'},
                           succ ={
                                        'attributes':[
                                                {'name': 'Severity', 'type': 'lcut', 'minlen': 1, 'maxlen': 2}
                                        ], 'minlen':1, 'maxlen':1 , 'type':'con'},
                           frst ={
                                        'attributes':[
                                                {'name': 'Driver_Age_Band', 'type': 'seq', 'minlen': 1, 'maxlen': 3}
                                        ], 'minlen':1, 'maxlen':1, 'type':'con'},
                           scnd ={
                                        'attributes':[
                                                {'name': 'Driver_Age_Band', 'type': 'seq', 'minlen': 1, 'maxlen': 3}
                                        ], 'minlen':1, 'maxlen':1, 'type':'con'}
#               ,opts = {'no_optimizations':True,'max_categories':20}
                                   )

clm.print_summary()
clm.print_rulelist()
clm.print_rule(1)