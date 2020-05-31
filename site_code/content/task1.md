---
title: "Task 1: Analysis of topic models in Yelp dataset"
date: 2020-05-30T19:28:33+05:30
draft: false
---

In this document we are going to look at the reviews given to restaurants on the Yelp platform and extract/analyse the topics discussed in the those reviews. We are going to compare topics by the following categories:
1. Topics by state
2. Topics by review sentiment. Positive or negative.
3. Topics discussed by the 50 most popular users (by fan count)
4. Topics by cuisine

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

  r = L * _log_(P(w | T)) + (1 - L) * _log_(P(w | T) / P(w))

  Here L is a regulating parameter that controls the importance given to lift vs probability. In all of my analysis I have taken the this value to be 0.6 as suggested by the following paper based on user study. [Link to original paper.](http://nlp.stanford.edu/events/illvi2014/papersievert-illvi2014.pdf)

#### Topics by states

We extracted reviews for all the restaurants by state to see if there were specific things that popped out in each state, e.g geography specific culinary preferences. We extracted 3 topics from the reviews for each state. For topic counts greater than that the word probabilities became too low to be meaningful. Also, some of the states had very few reviews which resulted in the topics overlapping massively. Hence we excluded all state with less than 50 reviews. For states that had more than 10000 rows we randomly sampled 10000 rows using the pandas DataFrame sample method. We created one model per state and the results are as below:

[![merge-from-ofoct2.jpg](https://i.postimg.cc/J0jJbXVw/merge-from-ofoct2.jpg)](https://postimg.cc/2L8VYVST)

As you can see, the topics manage to capture the main food items and cuisines for each of the states. In Arizona and Ontario sushi seems to be extremely popular but Arizona also seems to like mexican food a lot whereas Ontario is more interested in burgers.   
Some of the major places also are captured. We can see Vegas occurring in two topics quite prominently for Nevada for obvious reasons, as does Madison for Wisconsin. Waterloo seems to be an important place for foodies in Ontario and so on.

Now lets look at the salient words of topics according to pyLDAvis. For the sake of brevity I will only discuss the visualization for Arizona. [Link to rest of the visualisations](https://bobopd.github.io/capstone/ldavis/)

{{< pyldavis AZ>}}

The topics are fairly far apart meaning that they discuss different things which is good. However, the most prominent word in the word cloud _Sushi_ does not appear as a top word in any of the topics, suggesting that the word was frequent throughout the topics. The top words of topic 1 are _breakfast, coffee, eggs, toast and pancakes_ which clearly indicate that this is about breakfast. Topic 2 contains words about food items and cuisines like _pizza, thai, chinese, pasta etc_. This topic looks like it is dealing with the prominent cuisines. Finally topic 3 contains words that mainly signify mood/environment like _happy, friendly, table, staff, wait etc_. From this it is clear that the 3 topics discuss separate concepts and are well isolated, unlike the first visualisation which seemed to mostly concentrate on food items/cuisine which are obviously frequent items in general. Thus, the pyLDAvis method of ranking salient words in topics fares better in my opinion.

#### Topics by review sentiment

We have considered reviews that have a rating of 4 or greater as positive review and everything else as a negative review. Also, since the number of reviews were very large we have sampled 20000 positive and negative samples each for the topic extraction task. Following are the topics generated:

##### Postive reviews:

Contrasting the word cloud and the pyLDAvis again we see that the most prominent words in the word cloud do not feature prominently in pyLDAvis. Words like burger, sushi and fries are the most important words according to the word cloud. Burger and sushi do feature as the top words in topic 1 and 2 respectively in pyLDAvis bu those topics themselves are nowhere near as important as topic 3 and the main words in topic 3 are _friendly, staff, people, happy, etc_. We also got the same words in the word cloud but they were not the most salient. Thus we can see that although a lot of the words are shared between the two methods pyLDAvis does seem to come out on top again in generating more interesting topics.

[![positive.jpg](https://i.postimg.cc/fLbmgjyY/positive.jpg)](https://postimg.cc/yJwDDRFN)

{{< pyldavis disp_pos >}}

##### Negative reviews:

We can see a similar story repeat again for the negative reviews. From the word clouds it is evident that sushi is a popular dish and hence is relevant in both positive and negative reviews. However, we see that some of the most important items in positive reviews (burger, fish and fries) are almost exclusive to the positive topic (They have very low importance in the negative reviews). Also, both the word cloud and pyLDAvis seem to agree about the negative perception of mexican food. The topics in the negative reviews seem to overlap more than the positive ones.

[![negative.jpg](https://i.postimg.cc/QMmcbn8X/negative.jpg)](https://postimg.cc/1gggRBVT)

{{< pyldavis disp_neg >}}

___Note: Since it is quite evident that pyLDAvis is better at finding interesting words in topics compared to raw probabilites depicted in the word cloud we will henceforth forgo the word clouds.___ 

#### Topics by popular users

Here we have generated 5 topics from the reviews given by the 50 most popular users. The topics are spread fairly well apart except topic 3 and 5. Most of the top words seem to be food items and cuisines. Nothing too interesting here. 

{{< pyldavis pop_users >}}


#### Topics by cuisine

The categories array contains many values that are not cuisine related and also there are too many distinct values so I have decided to manually create a list of cuisines from the categories that have the most reviews so that we capture the most popular cuisines. I calculated the number of reviews by category and chose the following six cuisines from the categories with the largest number of reviews: {"American (New)", "Mexican", "Italian", "Japanese", "Chinese", "Thai"}. Also, since the number of reviews was very large for each cuisine I have sampled 10000 reviews per cuisine and created a model to find 3 topics.

[Link to all the visualisations](https://bobopd.github.io/capstone/ldavis/)

##### Thai

Topic 1 is the most easy to interpret. It relates almost completely with the thai cuisine and related food. Topic 2 is also an easily interpretable topic but is more restaurant related does not have anything to do with thai cuisine. Topic 3 does not seem to be coherent. Evidently, 3 topics was too many for this dataset.

{{< pyldavis thai >}}

##### American (New)

None of the topics look as homgenous as Topic 1 for the Thai cuisine. The topics seem to have captured the concept of meals and related ideas instead of dishes directly associated with the cuisine like Topic 1 in the previous visualisation. In this case Topic 1 clearly corresponds to breakfast as the salient words (like coffee, breakfast, eggs, toast, etc) all relate with the idea of a breakfast. Probably relating to the american breakfast. Topic 3 is again related to restaurants generally and nothing seems to be specific to the cuisine. Topic 2 is not as coherent as the other two. This looks like a repeat of the Thai visualisation where one topic is related quite closely to the cuisine, the second captures the general idea of restaurants and the third seems to be a catch all topic. Maybe using 2 topics would have been better in this case too.

{{< pyldavis american >}}