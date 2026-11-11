clm = cleverminer(df=df)

clm.mine(target='Severity',proc='CFMiner',
                           quantifiers= {'S_Down':1, 'Base':100},
                           cond ={
                                        'attributes':[
                                                {'name': 'Driver_Age_Band', 'type': 'seq', 'minlen': 1, 'maxlen': 3},
                                                {'name': 'Driver_IMD', 'type': 'seq', 'minlen': 1, 'maxlen': 3},
                                                {'name': 'Sex', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                                                {'name': 'Journey', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                                                {'name': 'Speed_limit', 'type': 'seq', 'minlen': 1, 'maxlen': 3},
                                                {'name': 'Light', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                                                {'name': 'Vehicle_Type', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
                                        ], 'minlen':1, 'maxlen':2, 'type':'con'}
                                  )

clm.print_summary()
clm.print_rulelist()
clm.print_rule(1)

clm.mine(target='Severity',proc='CFMiner',
                           quantifiers= {'S_Down':1, 'Base':100, 'relmax_leq' : 0.183},
                           cond ={
                                        'attributes':[
                                                {'name': 'Driver_Age_Band', 'type': 'seq', 'minlen': 1, 'maxlen': 3},
                                                {'name': 'Driver_IMD', 'type': 'seq', 'minlen': 1, 'maxlen': 3},
                                                {'name': 'Sex', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                                                {'name': 'Journey', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                                                {'name': 'Speed_limit', 'type': 'seq', 'minlen': 1, 'maxlen': 3},
                                                {'name': 'Light', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                                                {'name': 'Vehicle_Type', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
                                        ], 'minlen':1, 'maxlen':2, 'type':'con'}
                                  )


clm.print_summary()
clm.print_rulelist()
clm.print_rule(1)