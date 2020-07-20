---
title: "Task 6: Predicting hygiene from restaurant reviews"
date: 2020-07-20T23:04:28+05:30
draft: false
---

In this task we will attempt to predict which restaurants will pass or fail a public health inspection based on the reviews and some additional info like pincode, categories, review count and overall rating. We are given a total of 13299 rows of restaurant data out of which 546 rows contain the true labels. Moreover the training data is evenly split between the 2 classes while the rest of the rows are apparently not. So this is essentially a classification problem where the _amount of labelled data is much lower than the test data_ and there is also the problem of data skewness.

[You can find the code for this task here](https://github.com/boboPD/capstone/blob/master/code/Task6/Task6.ipynb)

I have tried the following approaches to solve the problem:

## Text Representation

I have tried the following ways of representing the text reviews:

* __Each review represented as a hygiene sentiment score__: I obtained this score by pulling out the sentences in the reviews that contain words that are semantically related to hygiene, like synonyms and antonyms, and then running them through a sentiment analyser. I got the list from https://www.powerthesaurus.org/. This is the list of words that I used as seed words: `{"sanitation", "salubrity", "sanitary", "hygienic", "tidiness", "sterility", "disinfection", "filth", "uncleanliness", "dirt", "garbage", "muck", "clean", "sterile", "dirty", "hygiene"}`.  
In this manner I was able to get a fairly accurate representation of reviews that dicussed hygiene. A negative score meant a bad review and a positive score meant hygiene was good. I verified a couple of the scores manually and felt that they were quite descriptive. _The major drawback of this approach was that less than 1/3 of the reviews contained the words in the list and even for the ones that did, quite a large number were very close to zero. Only 63 rows in the training set had this value._ Yet, I decided to keep this column since in some of the cases it could single handedly predict the outcome and I hoped that it would be a useful indicator nonetheless.

* __Reviews as unigrams:__ This is fairly self explanatory. I used the sklearn `CountVectorizer` to get my counts after removing stopwords and some basic data cleaning. Also, the vocabulary size was north of 90k which was causing the model training to take in impossibly long time on my machine and so I limited it to under 5000. I actually tried 3 values to see its effect on the models (1000, 2500 and 5000).

## Classification approaches

The tried using the following models for the classification problem:

* Basic Decision Tree
* AdaBoost
* Random Forest
* Decision Tree classifier trained by bagging approach
* Self training using the unlabelled data

I also tried the Naive Bayes and Logistic Regression to see how they performed by then were always well below the the others so I did not spend too much time on them.

## Results

_All the model training in this section is done using the first 546 rows as training data. Scikit-learn library was used for modelling._

### Training without the review text data

My first attempt consisted of training models only on the addtional info dataset augemented with my __hygiene score__. The cartegories were converted into an n-hot encoded vector after removing the "Restaurant" category since that was present in every record. So this is what my dataset looked like: 

![initial dataset with additional info and hygiene score](/capstone/hygiene1.png)

I modelled a Decision Tree with no cap on the depth, using AdaBoost that used a DecisionTree with depth 1 as the classifier and a random forest. Below are the results:

| Classifier | Precision | Recall |
| --- | --- | --- |
| Decision Tree | 0.5256 | 0.5272 |
| Random Forest | 0.5377 | 0.5418 |
| AdaBoost | 0.5544 | 0.5573 |

As expected the Decision Tree performed the worst and AdaBoost performed the best with the Random Forest classifier slotting in the middle. _Boosting performs better than Random forest because every subsequent classifier is trying to fix their predecessors mistakes._ This is also why boosting tends to overfit easily but by using only 50 trees with a depth of 1 each, I did not consider that to be a problem in this case.

### Added review text unigrams capped at 1000 words

However, the scores are pretty bad and its apparent to me that without the review text added to the training there would be no chance of any improvement. So I added the unigram representation of the reviews to my dataset. Initially I used a maximum of 1000 words. I tweaked the parameters of the models since the number of features had increased from 102 -> 1102. I have included the best performing ones in the table below. I'll discuss the tuning runs shortly.

| Classifier | Precision | Recall |
| --- | --- | --- |
| Decision Tree | 0.5724 | 0.5732 |
| AdaBoost | 0.6132 | 0.6147 |
| Random Forest | 0.6611 | 0.6619 |
| Bagging | 0.6733 | 0.6735 |

I was happy with the immediate improvement in my results. Some interesting things to notice about this run:

* AdaBoost didn't perform as well as random forest this time and that probably points to a certain amount of overfitting since the number of features was 1102 this time as opposed to 102 before. Ample opportunity for boosting to overfit the data.

* Bagging performed the best of the lot. Bagging is a known method to guard against imbalanced datasets and I was pleased to see that happening. _This method was also the slowest of the lot. It took about 20 mins for training and prediction. This is probably because I had not set a max-depth for the decision trees that were being trained by bagging. I did try setting it to 3 later but that caused a drop in the F1 score._ 

##### Model parameter tuning

Now, I realised that by default the random forest and boosted classifiers use only 10 classifiers internally. Since each of them trains a very shallow decision tree it was obviously not optimal since I now had over a 1100 features. There was no way 10 trees could approximate that function. So I increased the number of estimators to a few hundred. Results are below:

In both cases we can clearly see that the F1 score increases intially and falls after a point, signalling that we have overfit the training data. The sweet spot for Adaboost was 350 while that for random forest was 700. These numbers make sense because boosting tends to overfit faster than random forests.

__AdaBoost__

| Estimators | Precision | Recall |
| --- | --- | --- |
| 200 | 0.6116 | 0.6132 |
| 350 | 0.6132 | 0.6147 |
| 500 | 0.6058 | 0.6074 |

__Random Forest__

| Estimators | Precision | Recall |
| --- | --- | --- |
| 400 | 0.6481 | 0.6491 |
| 600 | 0.6603 | 0.6610 |
| 700 | 0.6611 | 0.6619 |
| 1000 | 0.6581 | 0.6589 |


### Review text unigrams with 2500 and 5000 words

Bouyed by the improvements resulting from the addition of the unigram features I decided to add more words this time to see how the models would behave. I tried with 2500 and 5000 words but the results were dissapointing. The models took significantly longer to train. The 2500 word feature set reported marginally higher F1 scores while adding 5000 words caused performance to degrade in all cases except that of the basic Decision Tree. Even in that the improvement was marginal. Precision increased from 0.5724 to 0.587 and Recall from 0.5732 to 0.5886. So I gave up at this point.

### Self Training

I decided to use 50% of the unlabelled data to help train my models and hopefully increase my F1 score.  I also felt that my `hygiene_sentiment` score would be a powerfull indicator and so I decided to include all of the ones with a value less than 0 to the unlabelled training set. The rest I sampled from the unlabelled dataset. Then I essentially trained a model on the labelled dataset and used it to predict the labels of the unlabelled rows. I selected the rows where the prediction confidence was high and added them back to my training dataset and retrained my model on this new larger dataset. Once a stopping condition is reached I use the final model for predicitons. Here is my code

```python
  training_data = features[:546]
  unlabelled_data = features[546:]
  unlabelled_data_for_training = unlabelled_data[unlabelled_data["hygiene_sentiment"] < 0]
  unlabelled_data_for_training = unlabelled_data_for_training.append(unlabelled_data[unlabelled_data["hygiene_sentiment"] >= 0].sample(2500))
  curr_training_set = training_data
  curr_labels = pd.Series(given_labels)
  
  print(f"Initial training data: {training_data.shape}, Type: {type(training_data)}")
  
  iterations = 0
  
  self_train_clf = ske.RandomForestClassifier(n_estimators=700)
  #self_train_clf = ske.BaggingClassifier(base_estimator=DecisionTreeClassifier(), n_estimators=150)
  
  while unlabelled_data_for_training.shape[0] > 0:
      self_train_clf.fit(curr_training_set, curr_labels)
      probs = self_train_clf.predict_proba(unlabelled_data_for_training)
      results = self_train_clf.predict(unlabelled_data_for_training)
      high_conf = (probs[:,0] >= 0.8) | (probs[:,1] >= 0.8)
  
      if len(results[high_conf]) < 10:
          print("Terminating")
          break
      curr_training_set = curr_training_set.append(unlabelled_data_for_training[high_conf])
      curr_labels = curr_labels.append(pd.Series(results[high_conf]))
  
      unlabelled_data_for_training = unlabelled_data_for_training[np.invert(high_conf)]
      iterations = iterations + 1
      print(f"iter: {iterations} Remaining unlabelled data: {unlabelled_data_for_training.shape[0]}")
```

I tried using the BaggingClassifier since it was my best performing classifier up to this point but the training simply took too long and I had to abandon it. RandomForest was much faster and so I used that. As you can see, I stopped when the number of high confidence rows was less than 10. It typically took about 50 iterations to get to that point.

I must say that I had really high hopes from this but the results were quite dissapointing. No matter what classifier I tried, self training resulted in a worse classifier than if I had trained it on the labelled data alone. In hindsight, __this does make sense because the classfier was not well performing to begin with and so retraining on data it had clasified itself was simply reinforcing its own mistakes.__

## Conclusion

The best performance I achieved was with the bagging approach with a Precision of 0.6733 and a Recall of 0.6735. I am aware that folks have achieved much better results than this. Looking forward to reading their reports to see what I overlooked.