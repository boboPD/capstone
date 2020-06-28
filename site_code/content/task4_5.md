---
title: "Task 4 and 5: Sentiment Analysis of dish reviews"
date: 2020-06-28T15:40:34+05:30
draft: false
---

In this task I shall attempt to use the restaurant reviews to mine perceptions of various dishes served in the restaurants. Using this data we want to:

1. __Find the most popular dishes in a given cuisine.__ These would be the dishes that were most favourably reviewed for that cuisine.
2. __Recommend restaurants given a dish name.__ 

So basically, I need a way to analyse the sentiment of each dish in every review. For this task I will be using the list of dish names that we had extracted in the previous task. The analysis has been done for the [chinese cuisine](https://raw.githubusercontent.com/boboPD/capstone/master/code/Task4_5/chinese_phrases.csv) but the steps are general and can be replicated with any other cuisine given we have the candidate list of dish names for that cuisine. _Since the number of dishes in the file is too large and most of them are of very low quality I have decided to restrict my analysis to the top 50 dishes._

[The jupyter notebook for this task can be found here](https://github.com/boboPD/capstone/blob/master/code/Task4_5/Task%204%20and%205.ipynb)

## Methodology

Like I mentioned before, the main task is to create a single metric that encapsulates the users opinion of a dish in the review. Also, it is possible that the user talks about multiple dishes in the same review. They could like one dish and dislike another. It is also possible that multiple sentences express differing opinions about different aspects of the same dish. We need to keep those instances separate. In order to achieve these 2 objectives I did the following:

#### Tokenisation

Every review was split into its contituent sentences. Then we went through each of the sentences and kept only the ones that contained the names of the dishes that we were interested in. Then we grouped the sentences by the dish name they reference. That way I can extract opinions of different dishes from the same review. As an example, the following review:

| business_id | review_id | text |
| --- | --- | --- |
| b1 | r1 | The hamburger was great but fries were quite soggy. The fries also seemed to be old |

would get split into the following

| business_id | review_id | dish | sentences |
| --- | --- | --- | --- |
| b1 | r1 | hamburger | ["The hamburger was great but fries were quite soggy"] |
| b1 | r1 | fries | ["The hamburger was great but fries were quite soggy", "The fries also seemed to be old"] |

#### Sentiment score

For analysing the sentiment of each sentence I used the [AWS Comprehend Service](https://aws.amazon.com/comprehend/features/). It offers a sentiment analysis API that returns the overall sentiment of a text (Positive, Negative, Neutral, or Mixed). The response also contains the confidence scores for all the sentiments:

```json
{
    "Sentiment": "POSITIVE",
    "SentimentScore": {
        "Mixed": 1.8855966118280776e-05,
        "Negative": 0.0019940186757594347,
        "Neutral": 0.05054771527647972,
        "Positive": 0.947439432144165
    }
}
```
We need to convert this number into a single score and for that I decided to use the following heuristic based on the salient sentiment:

* POSITIVE: The score is added to the overall sentiment score
* NEGATIVE: The score is subtracted from the overall sentiment score
* NEUTRAL: The score is scaled down by a factor of 0.3 and then added. This is to support the understanding that neutral opinions should not affect the sentiment too positively
* MIXED: Mixed reviews were ignored since they don't contribute to the sentiment clearly

Using this method we generated a sentiment score for each (review, dish) pair.

Now, we all know that not all reviews are created equal on the internet. A review by a food critic would carry much more weightage than something that I write. In order to account for this in our sentiment score we decided to include two more parameters:

* Number of followers of the reviewer. Popular reviewers are given greater importance
* Number of votes received by the review

I wanted a review written by an extremely popular reviewer or one with many upvotes to positively affect the score but I also didn't want it to outshine all other reviews. Thus I decided to use a sublinear transformation on the sum of the upvotes and followers (log) to scale the existing sentiment score. So the formula for my final score for each (review, dish) pair is:

_score = log(upvotes + followers) * sentiment_score_

For the overall score of a dish I simply took an average of all the reviews scores for that dish.

## Preprocessing steps

I extracted all the reviews of restaurants serving Chinese cuisine (filtered on the tags Chinese & Restaurants). The reviews also contain counts of user votes:

```json
"votes": {
    "funny": 5,
    "useful": 20,
    "cool": 11
}
```

Since this is an indication of how popular/useful a review is I decided to keep a total count of the votes for every review. After that the reviews were split into sentences as mentioned above and passed to the AWS Comprehend API for scoring.

## Results

_Note: [Both the visualisations and the raw data is available in this excel.](https://uillinoisedu-my.sharepoint.com/:x:/g/personal/pd10_illinois_edu/Edsfz8yf29lPqr05OrjnwmQBRVhBEqoEb7L8yR2bLvIxoQ?e=8VpfRo) I have included screenshots in my ananlysis below but you can interact with the pivot tables on the excel. There are two sheets: Visuals and Raw data. The raw data sheet contains the final table created after calculation of the sentiment scores. Its used as the basis for the tables. You can take a look at that also to understand the schema of my data._


#### Popular dishes

To find the most popular dishes I simply took an average of all the sentiment scores per dish. The higher the score the more better the dish.

![Popular Dishes](/capstone/top_dishes_chinese.png)

#### Best restaururants for specific dishes

I took an average of all the sentiment scores grouped by Retaurant and dish to find the scores of each (restaurant, dish) pair. This way I can find out how good a restaurant is for a given dish based on the sentiment scores of the reviews. Another factor that impacts this is the overall rating of the restaurant on Yelp. This isn't included in my sentiment score. I considered simple multpying the sentiment score by the restaurant rating to create a single metric but that seemed to be too simplistic in my opinion. Hence I decided to create a chart where I can show both the sentiment score and the rating side by side so that users can make that judgement themselves. I pivot chart seemed perfect for that task. The height of the bar shows the sentiment score and the color indicates the yelp rating.

![Pivot chart showing sentiment scores by restaurant and dish](/capstone/vis_annot.png)

As I have indicated in the screenshot, you can use the filters on the excel to find different combinations of dish, restaurant and rating. You can also see the values in the pivot table just below the pivot chart.

![Pivot table showing raw sentiment scores by restaurant and dish](/capstone/sentiment_pivot.png)