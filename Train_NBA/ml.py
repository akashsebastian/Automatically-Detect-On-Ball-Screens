import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import svm
import pylab as pl
from sklearn.metrics import roc_curve, auc, accuracy_score



df = pd.read_csv('train_fin.csv')
df = df.dropna(axis=0)
target = df['Screen']
df_f = df.drop(['Game_ID','Event_Number','Frame_Number','Screen'],axis=1)
X_train, X_test, y_train, y_test = train_test_split(df_f,target,test_size=0.3,random_state=109)
clf = svm.SVC(C= 32, kernel='linear',probability=True)
probas_ = clf.fit(X_train,y_train).predict_proba(X_test)
fpr, tpr, thresholds = roc_curve(y_test, probas_[:, 1])
roc_auc = auc(fpr, tpr)
print ("Area under the ROC curve : {}".format(roc_auc))
y_pred = clf.predict(X_test)
print("Accuracy",accuracy_score(y_test,y_pred))
pl.clf()
pl.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
pl.plot([0, 1], [0, 1], 'k--')
pl.xlim([0.0, 1.0])
pl.ylim([0.0, 1.0])
pl.xlabel('False Positive Rate')
pl.ylabel('True Positive Rate')
pl.title('Receiver operating characteristic graph')
pl.legend(loc="lower right")
pl.savefig('roc.png')
# pl.show()
