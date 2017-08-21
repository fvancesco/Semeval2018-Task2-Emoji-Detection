Labels Mapping
=====

We use the 20 most frequent emojis in English and 20 most frequent in Spanish. To simplify the task (and avoid unicode decoding problems) we map the emojis to numbers from 0 to 19. The mapping can be found in the two txt files, where each line is in the format:

label number [0:19] \<TAB\> emoji unicode \<TAB\> emoji CLDR short name

You can also check these two pages, were we link the images of the emojis to visualize them (some OS do not support emojis):

* [English mapping](https://fvancesco.github.io/tmp/labels_us.html)
* [Spanish mapping](https://fvancesco.github.io/tmp/labels_es.html)

