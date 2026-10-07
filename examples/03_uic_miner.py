clm = cleverminer(df=df,target='Severity',proc='UICMiner',
                           quantifiers= {'aad_score':20,'aad_weights':[5,1,0],'base':200},
                           ante ={
                                        'attributes':[
                                                {'name': 'Driver_Age_Band', 'type': 'seq', 'minlen': 1, 'maxlen': 3},
                                                {'name': 'Driver_IMD', 'type': 'seq', 'minlen': 1, 'maxlen': 3},
                                                {'name': 'Sex', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                                                {'name': 'Area', 'type': 'subset', 'minlen': 1, 'maxlen': 2},
                                                {'name': 'Journey', 'type': 'subset', 'minlen': 1, 'maxlen': 2},
                                                {'name': 'Road_Type', 'type': 'subset', 'minlen': 1, 'maxlen': 2},
                                                {'name': 'Speed_limit', 'type': 'seq', 'minlen': 1, 'maxlen': 2},
                                                {'name': 'Light', 'type': 'subset', 'minlen': 1, 'maxlen': 2},
                                                {'name': 'Vehicle_Location', 'type': 'subset', 'minlen': 1, 'maxlen': 2},
                                                {'name': 'Vehicle_Type', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                                                {'name': 'Vehicle_Age', 'type': 'seq', 'minlen': 1, 'maxlen': 11}
                                        ], 'minlen':1, 'maxlen':2, 'type':'con'}

                                  )
clm.print_summary()
clm.print_rule(1)
clm.print_rule(17)