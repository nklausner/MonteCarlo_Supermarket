#!/usr/bin/env python3
# coding: utf-8


import pandas as pd


def extract_transition_probabilities():

    print('extracting transition probabilities')
    dfl = []
    fnl = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
    states = ['entrance', 'fruit', 'spices', 'dairy', 'drinks', 'checkout']
    transitions = [[0 for i in range(6)] for i in range(6)]
    n_total = 0

    # read data from files to dataframes
    for filename in fnl:
        df = pd.read_csv(f'../data/{filename}.csv', delimiter=';')
        dfl.append(df)
        print(f'read ../data/{filename}.csv')
    
    # modify columns a bit
    for df in dfl:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.rename(columns = {'customer_no':'customer'}, inplace = True)
    
    # add customer checkout if missing
    for df in dfl:
        fccl = []
        #opening_time = df.timestamp.min()
        closing_time = df.timestamp.max() + pd.DateOffset(minutes=1)
        
        for i in df.customer.unique():
            if df[(df.customer == i) & (df.location == 'checkout')].empty:
                df.loc[len(df)] = [closing_time, i, 'checkout']
                fccl.append(i)
        
        assert df.customer.max() == df[df.location == 'checkout'].location.count()
        print('force checkout for customers: ', fccl)
    
    # get total data point count
    for df in dfl:
        n_total += df.shape[0]
    
    # extract transitions for every customer in data
    for df in dfl:
        for cid in df.customer.unique():
            mydf = df[df.customer == cid]
            # entrance transition
            s0 = states.index(mydf.iloc[0].location)
            transitions[0][s0] += 1
            # following transitions
            for i in range(mydf.shape[0] - 1):
                s1 = states.index(mydf.iloc[i].location)
                s2 = states.index(mydf.iloc[i+1].location)
                t1 = mydf.iloc[i]['timestamp']
                t2 = mydf.iloc[i+1]['timestamp']
                dt = int((t2 - t1) / pd.Timedelta(minutes=1))
                transitions[s1][s2] += 1
                if dt > 1:
                    transitions[s1][s1] += (dt - 1)
        print(f'extracted transitions for {df.shape[0]} data points')
    
    # normalize the transition matrix
    transitions[5][5] = 1.0
    for i in range(len(transitions)):
        mysum = sum(transitions[i])
        if mysum > 0:
            for j in range(len(transitions[i])):
                transitions[i][j] = float(transitions[i][j]) / mysum

    # display the transition matrix
    print(f'{n_total} data points')
    print('transition_matrix:')
    print(states)
    checklist = []
    for line in transitions:
        print(line)
        checklist.append(sum(line))
    print('check sums:', checklist)
    
    return(transitions)


if __name__ == '__main__':
    extract_transition_probabilities()