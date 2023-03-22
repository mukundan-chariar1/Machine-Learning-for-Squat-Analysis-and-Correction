from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv('D:\MLSAC\CMG\ctual.csv')

y_test = df['actual']
y_pred = df['pred']


labels = ["quarter", "half", "full"]

cm = confusion_matrix(y_test, y_pred)

cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

disp = ConfusionMatrixDisplay(confusion_matrix=cm_norm, display_labels=labels)

disp.plot(cmap=plt.cm.Blues)
plt.show()