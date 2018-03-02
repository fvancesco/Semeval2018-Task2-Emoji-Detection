Semeval 2018 Task 2 - Detailed Results
===== 
 
Run the script as: 

```bash
python detailed_results.py LANGUAGE PREDICTION_FILE
```
where LANG = english | spanish

For example:
```bash
python detailed_results.py english english.output.txt
```

The script generates 3 files: 
* csv file containing one line as in [Google sheet](https://goo.gl/P515KW) (macro f1, macro p, macro r, and f1 of each class)
* table.tex
* confusion.png
