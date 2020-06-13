---
title: "Task 3: Extracting dishes from reviews"
date: 2020-06-13T16:22:08+05:30
draft: false
---

In this excercise I will attempt to extract dishes that belong to a cuisine from the user reviews. For example, from the Chinese restaurant reviews I will try to extract the names of chinese dishes like hakka noodles, kung pao chicken etc. The primary method I used for this task is phrase extraction from the reviews and then trying to rank the phrases based on the probability that they are dishes for the cuisine in question.

For this task we chose to analyse 3 cuisines: Chinese, French and Italian.

## Preprocessing steps

In order to do phrase extraction I decided to tokenise all the reviews for a cuisine into an array of sentences. Since I am just trying to detect dish names, the individual reviews themselves are not important. Also, dish names will never be spread across sentence boundaries so if I split by sentences its guaranteed to not lose any dishes. This also helps us deal with arbitrary artifacts in user reviews like multiple line breaks, bullet points, etc.

To tokenise the reviews into sentences I used the *sent_tokenise()* method in nltk. I tried both the Punkt tokeniser and the regular expression tokeniser. The Punkt sentence tokeniser performed suprisingly poorly. It would only separate two sentences if there was a space after the period. Consider the two sentences below:

* This is sentence 1. This is sentence 2.
* This is sentence 2.This is sentence 2.

The only difference between these two sentences is the space after the first period in the first example. Yet the Punkt tokeniser was only was to separate the 2 sentences in the first case. Since most of the reviews were not formatted well it performed really poorly. A lot of the reviews did not have a space after the periods and that resulted in some of the reviews being returned as is with no evidence of any tokenisation at all. Hence I used a simple regular expression tokeniser that would separate the sentences based on simple english punctuation symbols. I know that this has obvious limitations like Dr. John Doe would get broken up into two sentences but food reviews typically don't contain too many such cases and the regular expression tokeniser did work much better at separating the sentences when I looked at them myself.

So at the end of the preprocessing stage we have a set of 3 files, one for each cuisine, that contains the list of sentences from the reviews for that cuisine. [You can see the output for chinese here](/capstone/chinese.txt).

## Phrase extraction

For phrase extraction I have used SegPhrase. Since that required the presence of a relatively small number of labelled examples I have labelled the chinese phrases for the first task. I intend to use these labels with SegPhrase. The max number of tokens/phrase was set to the default of 6. I ran SegPhrase for all 3 cuisines on the review sentences generated in the previous step using the chinese labels as the training set for the classfier. Below is the the top 25 phrases for each cuisine for analysis:

| Chinese | Italian | French |
| --- | --- | --- |
|	dim sum	|	zuppa toscana	|	foie gras	|
|	sweet and sour sauce	|	yukon gold	|	croque monsieur	|
|	fried rice	|	wedding reception	|	short ribs	|
|	sesame oil	|	vino bambino	|	sea bass	|
|	el topo	|	vin santo	|	pinot noir	|
|	kung pao chicken	|	villa dolce	|	los angeles	|
|	stir fried	|	video poker	|	coq au vin	|
|	soy sauce	|	united states	|	prix fixe	|
|	pork belly	|	tutti santi	|	iced tea	|
|	peking duck	|	treasure island	|	hash browns	|
|	noodle soup	|	timely manner	|	guy savoy	|
|	mongolian beef	|	sun prairie	|	sin city	|
|	iced tea	|	spring training	|	sea urchin	|
|	hot pot	|	slot machines	|	salted caramel	|
|	green onion	|	sierra nevada	|	quiche lorraine	|
|	egg rolls	|	sheeps milk	|	passion fruit	|
|	deep fried	|	scott conant	|	orange juice	|
|	crab puffs	|	saving grace	|	olive oil	|
|	crab puff	|	sauvignon blanc	|	marche bacchus	|
|	crab legs	|	san marzano	|	maple syrup	|
|	chow mein	|	san marco	|	john dory	|
|	brown sauce	|	san diego	|	heat lamps	|
|	black bean	|	salted caramel sundae	|	grand marnier	|
|	shangri la	|	salted caramel	|	eiffel tower	|
|	pea pods	|	queen creek	|	dress code	|  
 ----
As you can immediately notice, the phrases for chinese are almost all dishes. The accuracy is is excellent. However, the italian and french phrases don't do so well. The phrases themselves are of really good quality but they are mostly not dish names. __This points to overfitting__, since we used the chinese labels to train the classfier it did really well on the chinese dishes but not so much for the other cuisines. In fact, a lot of the dishes in this list appeared in the labels and so the classifier had already seen them. In order to make sure that it was overfit I also created labels for the italian data and then re-ran SegPhrase on the Italian reviews with the italian labels. This is what I got:

| Italian | Italian improved |
| --- | --- |
|	zuppa toscana	|	white wine	|
|	yukon gold	|	wolfgang puck	|
|	wedding reception	|	whipped cream	|
|	vino bambino	|	strip mall	|
|	vin santo	|	sea bass	|
|	villa dolce	|	san francisco	|
|	video poker	|	pinot noir	|
|	united states	|	pine nuts	|
|	tutti santi	|	parmigiano reggiano	|
|	treasure island	|	panna cotta	|
|	timely manner	|	osso bucco	|
|	sun prairie	|	olive oil	|
|	spring training	|	olive garden	|
|	slot machines	|	naked city	|
|	sierra nevada	|	mashed potatoes	|
|	sheeps milk	|	mario batali	|
|	scott conant	|	mamma mia	|
|	saving grace	|	iced tea	|
|	sauvignon blanc	|	humble pie	|
|	san marzano	|	hash browns	|
|	san marco	|	goat cheese	|
|	san diego	|	gluten free	|
|	salted caramel sundae	|	fra diavolo	|
|	salted caramel	|	foie gras	|
|	queen creek	|	filet mignon	|

_Note: The first column is the same as the first run while the second column contains the phrases obtained using the italian labels_

As you can see, there is a marked improvement in the quality of the phrases. A lot of them now are actually dishes unlike the first time. This conclusively proves that the models are indeed overfitting the labels and the only way to extract dish names of cuisines from reviews through SegPhrase is to actually have good labels for dish names for each cuisines we are interested in.