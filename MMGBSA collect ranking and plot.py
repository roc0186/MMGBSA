import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

dirs=sorted([i for i in os.listdir('./') if 'rep' in i])
cplxs=sorted(list(set(['mab0'+i.split('_')[0] for i in dirs])))
# print(dirs)
# print(cplxs)

def getmmpbsa(mmpbsa):
    f=open(mmpbsa)
    for i in f.readlines():
        if 'DELTA TOTAL' in i:
            # print(i)
            sc=i.split()[2]
            # print(sc)
    return sc
# print(getmmpbsa('/data/corp/peng.zhang02/13_FGFR2b_mabs_mmgbsa_chunqiu_20231023/04_rep0/5_run/process/MM-PBSA-5ns/mmpbsa.out'))
wdir=os.popen('pwd').read().strip()
# print(wdir)
out_file='5_run/process/MM-PBSA-5ns/mmpbsa.out'
mmpbsa_s=[os.path.join(wdir,i,out_file) for i in dirs]
# print(mmpbsa_s)
kv = {}
for i in range(len(dirs)):
    kv[dirs[i]]=getmmpbsa(mmpbsa_s[i])
kv

df= pd.DataFrame(np.fromiter(kv.values(),dtype=float).reshape([len(cplxs),int(len(dirs)/len(cplxs))]).T)
df.columns=cplxs
df=df.reindex(df.mean().sort_values().index, axis=1)

## plot and savefig
sns.stripplot(df)
plt.ylabel('MMGBSA (kcal/mole)')
plt.tight_layout()
plt.savefig('mmpbsa.png')
print('Binding affinity evaluated by MMGBSA of the last 5ns MD trajectory,go from strength to weakness:\n'+' > '.join(df.columns))
