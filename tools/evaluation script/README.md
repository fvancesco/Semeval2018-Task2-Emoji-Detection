Official evaluation script
=====

The official evaluation script for this task can be run from the terminal as follows:

```bash
python scorer-semeval2018-task2.py [gold_key] [output_key]
```

Example of usage:

```bash
python scorer-semeval2018-task2.py trial/english.trial.gold.txt trial/english.output.txt
```

*Note: Gold and output files should have the same number of lines. If for some occurrence the system is not confident enough to output any answer, just leave that line empty.*
