import os
import pandas as pd
import gc
path='.'
files=[]
for r,d,f in os.walk(path):
    for file in f:
        if '.json' in file:
            files.append(file)
print(files)
for num,file_name in enumerate(files):
    print("File name: {} File number: {}/{}".format(file_name, num, len(files)))
    df = pd.read_json('Extract/' + file_name)
    length = len(df)
    del df
    gc.collect()
    for i in range(length):
        cmd = 'python3 main.py --path=Extract/' + file_name + ' --event=' + str(i)
        print(cmd)
        os.system(cmd)
