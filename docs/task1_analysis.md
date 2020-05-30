# Analysis of topic models in Yelp dataset

In this document we are going to look at the reviews given to restaurants on the Yelp platform and extract/analyse the topics discussed in the those reviews. We are going to compare topics by the following categories:
1. Topics by state
2. Topics by review sentiment. Positive or negative.
3. Topics discussed by the 50 most popular users (by fan count)

## Preprocessing steps

After reading the restaurant and review data from the flat files the review data was preprocessed in order to generate better topics.

#### Tokenising

In this step we are converting the plain text reviews in our data into an array of words. This is needed for the next step where we create a bag of words representation of our reviews. Additionally, we have also converted all of the words into lowercase in order to avoid the same word being treated as a different token in our bag of words model due to different casing.

#### Stop Word Removal

Since all of the reviews in this corpus are for restaurants there will be certain words that are common in this domain. For example, words like food and restaurant is expected to appear very frequently in the reviews and although they are not standard stop words for english they don't add any semantic meaning to the task at hand. Hence, we'll have to build a custom list of stop words tailored for restaurant reviews. Our custom stop word list was built in the following manner:

  * Get a list of common stop words for the English language from https://www.ranks.nl/stopwords.
  * This the above list we added the 30 most commonly occurring words in our reviews that are functional in nature like _food, good, place, restaurant, etc_.

Now the reviews are ready to be processed.

## Topic Modelling

We are using the __Gensim__ library to create topic models. We have used word clouds to visualise topics and also used pyLDAvis to create interactive visualisations. We will now go through each of the topics.

* __Word Clouds__: The word clouds that you will see below essentially try to model the importance of each word in a topic and the importance of the topics too. The size of the words are proportional to the probability of the word given the topic i.e P(w \| T). Also, all the words belonging to the same topic are represented in the same colour.

* __pyLDAvis__: The pyLDAvis library has a unique take to extracting representative words from a topic. They use a concept called relevance to rank the most important words in the topic. Relevance in nothing but the weighted average of the logarithms of P(w \| T) and the list of P(w \| T). So essentially it tries to capture how popular the word is in that topic and also how exclusive it is to the topic. ___The idea is that the representative words in a topic are those that are both frequent and exclusive to that topic___:

  ```
  r = L * _log_(P(w | T)) + (1 - L) * _log_(P(w | T) / P(w))
  ```
  Here L is a regulating parameter that controls the importance given to lift vs probability. [Link to original paper.](http://nlp.stanford.edu/events/illvi2014/papersievert-illvi2014.pdf)

#### Topics by states

We extracted reviews for all the restaurants by state to see if there were specific things that popped out in each state, e.g geography specific culinary preferences. We extracted 3 topics from the reviews for each state. For topic counts greater than that the word probabilities became too low to be meaningful. Also, some of the states had very few reviews which resulted in the topics overlapping massively. Hence we excluded all state with less than 50 reviews. For states that had more than 10000 rows we randomly sampled 10000 rows using the pandas DataFrame sample method. We created one model per state and the results are as below:

[![merge-from-ofoct2.jpg](https://i.postimg.cc/J0jJbXVw/merge-from-ofoct2.jpg)](https://postimg.cc/2L8VYVST)

As you can see, the topics manage to capture the main food items and cuisines for each of the states. In Arizona and Ontario sushi seems to be extremely popular but Arizona also seems to like mexican food a lot whereas Ontario is more interested in burgers.   
Some of the major places also are captured. We can see Vegas occurring in two topics quite prominently for Nevada for obvious reasons, as does Madison for Wisconsin. Waterloo seems to be an important place for foodies in Ontario and so on.

#### Topics by review sentiment

We have considered reviews that have a rating of 4 or greater as positive review and everything else as a negative review. Also, since the number of reviews were very large we have sampled 20000 positive and negative samples each for the topic extraction task. Following are the topics generated:

##### Postive reviews:

[![positive.jpg](https://i.postimg.cc/fLbmgjyY/positive.jpg)](https://postimg.cc/yJwDDRFN)

##### Negative reviews:

[![negative.jpg](https://i.postimg.cc/QMmcbn8X/negative.jpg)](https://postimg.cc/1gggRBVT)

From the word clouds it is evident that sushi is a popular dish and hence is relevant in both positive and negative reviews. However, we see that some of the most important items in positive reviews (burger, fish and fries) are almost exclusive to the positive topic (They have very low importance in the negative reviews).  
We can also see that positive reviews have words that have positive connotations like _friendly, happy and delicious_ whereas the negative reviews have words like _wait, server_, which is consistent with the expectation of negative reviews. From the lower relative importance of the words for ambience and experience in both the categories we can also say that ambience plays a smaller role in the overall experience that the quality of the food; again, an expected outcome.

