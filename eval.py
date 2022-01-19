import sys
import shutil
import os
import fnmatch
import pandas as pd
import numpy as np
import tensorflow as tf
import logging
import matplotlib.pyplot as plt

cwdPath = str(os.path.abspath(os.getcwd()) + '/')
dumpPath, postPath, pot = cwdPath + str(sys.argv[1]), cwdPath + str(sys.argv[2]), str(sys.argv[3])
nAtoms = ''

def checkInputs(srcDir, destDir, pot):
    if dumpPath == '':
        print('Path to Lammps dump files was not passed correctly from Lammps to Python.')
        print('Exiting Python script.')
        sys.exit()
    elif pot == '':
        print('Potential type was not passed correctly from Lammps to Python.')
        print('Exiting Python script.')
        sys.exit()
    elif postPath == '':
        print('Save path for python files was not passed correctly from Lammps to Python.')
        print('Exiting Python script.')
        sys.exit()
    else:
        print('Using Lammps dump files in: ' + srcDir)
        print('Potential type: ' + pot)
        print('Python output files will be saved to: ' + destDir)
    return   

def cpDump(srcDir, destDir): #Copy dump files to postPath to preserve originals
    for file in os.listdir(srcDir):
        if 'dump' in file or 'Dump' in file:
            if os.path.getsize(srcDir + file) != 0:
                shutil.copy(srcDir + file, destDir + file)
                print(file + ' copied to ' + destDir + ' to be edited.')
            else:
                print(file + " is empty and won't be converted to a .csv file.")
        else:
            print(file + " not recognized as a Lammps dump file, and won't be converted to a .csv file.")
            print(" Dump files must contain 'dump' or 'Dump' in the filename.")
    return

def editTxt(dirPath): #Edit copied dump files for use with pandas
    nAtoms  =''
    atomSet = False
    #skip = 0
    #lines = []
    for file in os.listdir(dirPath):
        #count = 0  #check is dataframe length = # file lines
        setF = False
        skip = 0
        lines = []
        if file.endswith('.csv'):
            pass
        else:
            fName = str(file)
            prefix = ''
            with open(dirPath + fName, 'r') as f:
                lines = f.readlines()
            with open(dirPath + fName, 'w') as f:
                for line in lines:
                    if skip > 0:
                        skip = skip - 1
                        continue
                    if 'ITEM' not in line:
                        if nAtoms == '' and atomSet == True:
                            nAtoms = line.strip('\n')
                            continue
                        f.write(line)
                    elif "TIMESTEP" in line:
                        skip = 1
                        continue
                    elif "ATOMS " in line:
                        if setF == True:
                            continue
                        elif setF == False:
                            line = line.split("ATOMS ")[1]
                            f.write(line)
                            setF = True
                    elif 'BOX BOUNDS' in line:
                        skip = 3
                        continue
                    elif 'NUMBER OF ATOMS' in line:    
                        if nAtoms == '':
                            atomSet = True
                            continue
                        else:
                            skip = 1
                            continue
            #print('lines couted: ' + str(count))
    nAtoms = nAtoms.strip('\n')
    return nAtoms

def dump2CSV(srcDir, destDir, pType): #Convert all dump files in specified path to individual CSVs
    refDF=potDF=refData=potData=refName=potName=''
    
    cpDump(srcDir, destDir)
    nAtoms = editTxt(destDir)

    for file in os.listdir(destDir):
        if file.endswith('.csv'):
            pass
        else:#change this back to else 
            #df = pd.read_csv(destDir + file, header=None, sep='\n')
            #df = df[0].str.split('\s+', expand=True)
            df = pd.read_csv(destDir + file, header=0, sep=' ')
            df = df.drop(df.columns[df.shape[1]-1], axis=1) #Drop 11 col of nan values
            df = df.apply(pd.to_numeric, errors='coerce')
            print(df)
            print(df)
            #dfNum.iloc[:][0] = dfNum.iloc[:][0].astype(str).astype(int, errors='ignore')
            #varRange = dfNum.shape[0]
            #print(varRange)
            #for i in range(0, varRange):
                #if i < 10:
                    #print('i value: ' + str(i))
                    #value = str(dfNum.iloc[i,0]) #.lower()
                    #print(dfNum.index)
                    #value = str(dfNum.iloc[i][0]) #.lower() maybe try astype int
                    #print(value)
                    #print('value: ' + str(value))
                    #if 'nan' in value.lower() or value.startswith('0') or value.startswith('-'):
                    #    print('found val: ' + str(value))
                    #    print(dfNum.iloc[i])
                    #    dfNum.drop(df[df[i] == i], inplace=True)
                    #dfNum = dfNum.drop(dfNum[].index)
                    #value=''
                #print('i is: ' + str(i) + ' and val: ' + value)
                #if value =='nan' or value == '0.0':
                #    print('dfnum before:')
                #    dfnum = dfnum.drop(i)
                #    dfnum = dfnum.drop([i])
                #    print('dfnum after:')
                #    print(dfnum)
            file = os.path.splitext(file)[0] #remove file extension ex. '.txt', '.dump'

            if 'ref' in file:
                refName = str(file)
                refDF = df.loc[df['id']==1]
                refData = (refDF.iloc[:,10]).to_numpy()
                print('refDF: ')
                print(refDF.head(10))
                print('refData: ')
                print(refData)
            elif pType in file:
                potName = str(file)
                potDF = df.loc[df['id']==1]
                potData = (potDF.iloc[:,10]).to_numpy()
                print('potDF: ')
                print(potDF.head(10))
                print('potData: ')
                print(potData)
            df.to_csv(destDir + file + '.csv', index=False)
    #for i in range(len(refDF.columns) - 1):
    #    col = str(i)
    #    condition = str(refDF.iloc[:,i].equals(potDF.iloc[:,i]))
    #    if condition == 'True':
    #        print(refName + ' and ' + potName + ' columns: ' + col + ' match.')
    #    else:
    #        print(refName + ' and ' + potName + ' columns: ' + col + ' do not match.')
    #Uncomment this block after fix loop above

    tFlow(refData,potData)
    return nAtoms

def tFlow(refData, potData):
    logger = tf.get_logger()
    logger.setLevel(logging.ERROR)

    ref_val = np.array(refData, dtype = float)
    pot_val = np.array(potData, dtype = float)
    
    for i,c in enumerate(pot_val):
        print("{} adp potential energy.\t {} reference potential energy".format(c, ref_val[i]))
    
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(units=1, input_shape=[1])
    ])
    
    model.compile(loss='mean_squared_error', optimizer=tf.keras.optimizers.Adam(0.1))

    history = model.fit(pot_val, ref_val, epochs = 500, verbose=False)
    print('Model training complete')
    
    #plt.xlabel('Epoch Number')
    #plt.ylabel("Loss Magnitude")
    #plt.plot(history.history['loss'])

    print(model.predict([-5.025]))

    return

checkInputs(dumpPath, postPath, pot)
nAtoms = dump2CSV(dumpPath, postPath, pot)
#verData(postPath, pot)
