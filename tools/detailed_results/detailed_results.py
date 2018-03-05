# -*- coding: utf-8 -*-
import sys, os
import numpy as np
reload(sys)  
sys.setdefaultencoding('utf8')
import emojilib
from shutil import copyfile
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['xtick.labelsize'] = 10
matplotlib.rcParams['ytick.labelsize'] = 10
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import warnings
warnings.filterwarnings("ignore")

mapping_us = { '❤':'0' , '😍':'1' , '😂':'2' , '💕':'3' , '🔥':'4' , '😊':'5' , '😎':'6' , '✨':'7' , '💙':'8' , '😘':'9' , '📷':'10' , '🇺🇸':'11' , '☀':'12' , '💜':'13' , '😉':'14' , '💯':'15' , '😁':'16' , '🎄':'17' , '📸':'18' , '😜':'19'}
mapping_es = { '❤':'0' , '😍':'1' , '😂':'2' , '💕':'3' , '😊':'4' , '😘':'5' , '💪':'6' , '😉':'7' , '👌':'8' , '🇪🇸':'9' , '😎':'10' , '💙':'11' , '💜':'12' , '😜':'13' , '💞':'14' , '✨':'15' , '🎶':'16' , '💘':'17' , '😁':'18' , '   ':'19'}

start= '''
\\documentclass{article}
\\usepackage{graphicx}
\\begin{document}

\\begin{table}
\\centering
\\begin{tabular}{|c|ccc|c|} \\hline
\\textbf{Emo} & \\textbf{P} & \\textbf{R} & \\textbf{F1} & \\textbf{\\%} \\\\ \\hline
'''
end = '''
\hline
\end{tabular}
\caption{\label{table:emoji_detailed} Precision, Recall, F-measure and percentage of occurrences in the test set of each emoji.}
\end{table}
\end{document}
'''

def plot_confusion_matrix(cm, cmap=plt.cm.Blues, n_labels = 20, file_path="confusion.png"):
    fig, ax = plt.subplots(1,1)
    plt.xlabel('Predicted label', **csfont)
    plt.ylabel('True label', **csfont)
    xl, yl, xh, yh = np.array(ax.get_position()).ravel()
    w=xh-xl
    h=yh-yl
    xp=xl+w/n_labels 
    size=0.03

    ax.matshow(cm, cmap=cmap)
    ax.xaxis.tick_bottom()
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    #add y labels
    eps = 0.0045
    m=w/n_labels+eps
    magic_x = 0.145
    for i in range(n_labels):
        k = n_labels-1-i
        emoji_cldr = emojilib.demojize(mapping[str(k)].decode('utf-8'))[1:-1]
        img=mpimg.imread('./img/'+emoji_cldr+'.png')
        ax1=fig.add_axes([magic_x, yl+size/2+m*i, size, size])
        ax1.axison = False
        imgplot = ax1.imshow(img)

    #add x labels
    eps = -0.0065
    if n_labels == 19:
        eps = -0.0070
    m=w/n_labels+eps
    magic_y = 0.075
    for k in range(n_labels):
        emoji_cldr = emojilib.demojize(mapping[str(k)].decode('utf-8'))[1:-1]
        img=mpimg.imread('./img/'+emoji_cldr+'.png')
        ax1=fig.add_axes([xp+size/2+m*k, magic_y, size, size])
        ax1.axison = False
        imgplot = ax1.imshow(img)

    plt.savefig(file_path,dpi=500, bbox_inches='tight', pad_inches=0.2)


#-------------------------------------------------------------------------
lang = sys.argv[1] # english | spanish
pred_path = lang = sys.argv[2]

if "english" in lang:
    gold_path = "us_test.labels"
    total_test = 50000
    n_labels = 20
    mapping = {v: k for k, v in mapping_us.iteritems()}
elif "spanish" in lang:
    gold_path = "es_test.labels"
    n_labels = 19
    total_test = 10000
    mapping = {v: k for k, v in mapping_es.iteritems()}
else:
    raise ValueError(lang+": not supported. Type 'english' or 'spanish'")

G = open(gold_path, 'r').read().replace("\r","").replace(" ","").split("\n")
P = open(pred_path, 'r').read().replace("\r","").replace(" ","").split("\n")
G = G[:total_test]
P = P[:total_test]
labels = [str(x) for x in range(n_labels)]

#-------------------------------------------------------------------------
#measure p,r,f1 (also for each class)
acc = accuracy_score(G, P)
p_macro, r_macro, f1_macro, _ = precision_recall_fscore_support(G, P, labels=labels, average="macro")
p_list, r_list, f1_list, freq_list = precision_recall_fscore_support(G, P, labels=labels, average=None)


#csv results as in https://goo.gl/P515KW
csv_results = [f1_macro,p_macro,r_macro,acc]+list(f1_list)
csv_results_str = [str(x) for x in csv_results]
with open("results.csv",'w') as out:
    out.write(",".join(csv_results_str) + "\n")

#Latex table
l = ""
for i in range(n_labels):
    p = str(np.round(p_list[i]*100,2))
    r = str(np.round(r_list[i]*100,2))
    f1= str(np.round(f1_list[i]*100,2))
    freq = str(np.round(freq_list[i]*100.0/total_test,2))
    emoji_cldr = emojilib.demojize(mapping[str(i)].decode('utf-8'))[1:-1]
    l += "\\includegraphics[height=0.37cm,width=0.37cm]{img/"+emoji_cldr+".png} & "+p+" & " + r + " & " + f1 + " & " + freq + "\\\\ \n"

with open("table.tex",'w') as out:
    out.write(start)
    out.write(l)
    out.write(end)

#Confusion matrix
cm = confusion_matrix(G, P, labels)
csfont = {'fontname':'Times', 'fontsize':'17'}
np.set_printoptions(precision=2)
M = cm.sum(axis=1)
# Normalize the confusion matrix by row (i.e by the number of samples in each predicted class)
cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
plot_confusion_matrix(cm, n_labels=n_labels, file_path="confusion.png")
