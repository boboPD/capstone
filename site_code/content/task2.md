---
title: "Task 2: Similarity of cuisines"
date: 2020-06-07T21:17:14+05:30
draft: false
---

In this task I shall attempt to extract a way to represent cuisines from the review text. I will be using the same preprocessed set of reviews that we used for the previous task. I had saved the proprocessed reviews as a csv file so it could be easily loaded for future tasks without having to redo the processing every time. Here is the jupyter notebook that contains the code for this task.

Two variantions of representing cuisines have been explored:

1. Representing cuisines as word ditributions over reviews for that cuisine
2. Using category tags most commonly occuring alongside the cuisine tag. E.g Japanese and Sushi bar tags commonly occur together

Also, since a large number of category tags in the data are not cuisines I have manually chosen 15 cuisines from the ones that have the highest number of reviews.

cuisines = {"American (New)", "Mexican", "Italian", "Steakhouses", "Japanese", "Chinese", "Sushi Bars", "Seafood", "Fast Food", "Thai" ,"Asian Fusion", "Mediterranean", "Barbeque", "French", "Cafes"}

## Cuisines as word distributions

In the first task I had extracted topics by cuisine and had noticed that one topic, in each case, was representative of the cuisine. I have included one visualisation here for clarity:

{{< pyldavis thai >}}

Set the  value of lambda to 0.3 and one can see that Topic 1 is obviously related to the thai cuisine. This means that cuisines can be represented as word probabilities. Doing this also makes it easy to apply common similarity measures like cosine similarity to the cuisines.

Since in the last task every cuisine seemed to have 1 topic that was cuisine out of 3 and the other two always seemed to be restaurant related I was wondering if it was possible to extract each cuisine into a topic of its own. So I filtered the dataset to include all the reviews for the 15 cuisines mentioned above and then trained an LDA model to extract 15 topics. However, the topics that were generated were not cuisine centric at all. So this method would not work.

[![temp.png](https://i.postimg.cc/pd5fd7D9/temp.png)](https://postimg.cc/wtHyfw4H)

Next, I decided to use a simple word probability distribution over the reviews in a cuisine. Basically,

```
P(w | T) = count of the word in the reviews for that cuisine/total count of words for the cuisine
```
I also removed words that occurred in over 50% of the reviews and words that were present in less than 5% of the reviews.

When I did this for the _Thai_ cuisine I got the following words:

|word    |   P(w \| T)|
|---|---|
|curry    |       0.012350|
|rice     |       0.009387|
|spicy    |       0.008782|
|lunch    |       0.008225|
|dish     |       0.007159|

This is very similar to the top words that we get in the LDA model. So this direction looked promising. In order to further improve the the representative words I divided each probability by the marginal probability of the word (this is basically the ____lift___ measure).

```
Importance of word for cuisine(I) = P(w | T) / P(w)
```

Once I calculated this for every word and re-sorted the list based on I the following list of top words emerged:

|word    |   `I`|
|---|---|
|panang   |      34.287433|
|curry    |      18.192718|
|yellow   |      10.891345|
|basil    |       9.708976|
|coconut  |       8.796578|
|spice    |       8.217093|
|level    |       7.380260|
|tofu     |       7.232515|
|noodles  |       6.889217|

This list is obviously a must better representation of the Thai cuisine than the previous one and so I settled on using this as my cuisine representation.

I repeated this task for each cuisine and was able to generate a matrix of cuisine x words. Reproducing a small version of that below for clarity. The cells that contain zero baiscally mean that the word was not present in that cuisine.

|	|appetizer	|asada|	asian|	atmosphere|	authentic|	ayce|	bacon|	basil|
|---|---|---|---|---|---|---|---|---|
|Asian Fusion|	0|	0|	6.352898|	0|	0|	0|	0|	0|
|Japanese|	0|	0|	0|	0|	0|	9.221005|	0|	0|
|Cafes	|0	|0	|0	|0|	0|	0|	2.073344|	0|
|Seafood	|1.749961	|0|	0|	0|	0|	0|	0|	0|
|Chinese	|0	|0	5.643795|	0|	2.860458|	0|	0|	0|

__To calculate the similarity I used a simple dot product of the two cuisines. Higher the value of the dot product, greater is the similarity.__ I basically calculated the dot product of the matrix above with a transpose of the same matrix to give me the similarity scores between each pair of cuisines. Below is the heat map I got:

[![sim-matrix.png](https://i.postimg.cc/L4gLmz65/sim-matrix.png)](https://postimg.cc/HjHV28M1)

The following observations can be made from the heat map:

* The Asian cuisines like Asian Fusion, Japanese, Chinese and Thai are all quite similar to each each other. Since sushi is essentially a Japanese dish, sushi bars have a very strong correlation with Japanese cuisine. All of these results are obvious and lends credence to the method used to create the heat map.

* Another correlation that we can see is French cuisine with Cafes, Seafood and Barbeque. French having a correlation with Cafes sounds plausible to me because of baked items like croissants that are commonly served in Cafes. However, the association of Seafood and Barbeque with French cuisine is interesting to me. Maybe its just a facet of French cuisine that I am not aware of.

* Another strong correlation is that of Steakhouses with Seafood, and Barbeque.

* Mexican food also seems to be correlated to Barbeques.

* Fast Food does not seem to be similar to any of the other cuisines. Maybe if I had included Burgers in my list of cuisines it would have shown a strong correlation with that.

Looking at the observations above we can conclude that the heat map does highlight similar cuisines and thus the above methodology can be used to extract a cuisine representation for food reviews.

## Cuisines represented by tags most commonly associated with them

The categories array contains many tags other than the cuisine like "Nightlife", "Bars", "Do-it-Yourself Food", etc. I want to create a graph of what tags most commonly occur with the cuisines. That way we can measure similarity by looking at what tags are common among 2 cuisines. To do this I removed "Restaurants" tag from the categories since all the rows contain that. Next I created a matrix with cuisines as rows and counts of tags as columns:

[![tag-cnt.png](https://i.postimg.cc/qRN2XNYq/tag-cnt.png)](https://postimg.cc/0Mq69y91)

Then I calculated the euclidean distance between each pair of cuisines using the tag counts as features.

[![sim-categ-matrix.png](https://i.postimg.cc/3rVs7fD6/sim-categ-matrix.png)](https://postimg.cc/jC6g4XcQ)

Some of the observations that can be made from this heat map:

* As we can see Sushi bars and Japanese seem to be present mostly alone.

* Barbeque, Thai and Mexican seem to share tags. Looking at the common tags I can see that Bars and Nightlife are in the top 10 for all 3. This means that this cuisine is common in nightclubs probably. This is interesting information and could be useful in my opinion

We can use this method to find cuisines that share properties other than food. It could lead to interesting observations about the cuisines.