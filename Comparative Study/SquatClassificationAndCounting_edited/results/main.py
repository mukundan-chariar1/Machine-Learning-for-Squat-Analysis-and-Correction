import matplotlib.pyplot as plt
import numpy
import sklearn
import pandas as pd
from sklearn import metrics

# insert values produced by the codes we have ran under actual and predicted
# test the values by adding them using numpy or pandas, have used numpy for now

#path1= "D:\MLSAC\Confusion Matrix generation\actual.csv"
#path2= "D:\MLSAC\Confusion Matrix generation\predicted.csv"

df = pd.read_csv('D:\MLSAC\CMG\ctual.csv')

# dummy values to check
#actual = numpy.random.binomial(1,.9,size = 1000)
#predicted = numpy.random.binomial(1,.9,size = 1000)

confusion_matrix1 = metrics.confusion_matrix(df['a_quarter'],df['quarter'])
confusion_matrix2 = metrics.confusion_matrix(df['a_half'],df['half'])
confusion_matrix3 = metrics.confusion_matrix(df['a_full'],df['full'])


cm_display1 = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix1, display_labels = [False, True])
cm_display2 = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix2, display_labels = [False, True])
cm_display3 = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix3, display_labels = [False, True])


cm_display1.plot()
plt.title("qaurter")
cm_display2.plot()
plt.title("half")
cm_display3.plot()
plt.title("full")
plt.show()