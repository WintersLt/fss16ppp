# Reading-Week 1

## Anh Tuan Nguyen, Tung Thanh Nguyen, Tien N. Nguyen, David Lo, Chengnian Sun. 2012. Duplicate Bug Report Detection with a Combination of Information Retrieval and Topic Modeling. Proceedings of the 27th IEEE/ACM International Conference on Automated Software Engineering (ASE 2012)

### Keywords
#### ii1) DBTM:
Duplicate Bug report Topic Model(DBTM) is the novel model proposed by this paper to identify and group together duplicate bug reports and it takes advantage of both term-based and topic-based features.
#### ii2) Topic modelling: 
This is a machine learning method for textual data mining. It identifies the "topics" or the abstract subject matter from a set of documents. In this case the set of documents is the collection of bug reports.
#### ii3) Information retieval: 
This is a data mining techinique to determine tectual similarity between documents. This paper uses a technique called BM25F, an advanced document similarity function based on weighted word vectors of documents.
#### ii4) Training: 
This is the process of estimating the parameters of a machine learning model using historical data. The authors has trained the proposed model bug reports from three different sources - Ecliplse, Mozilla and OpenOffice.

### iii1) Motivational statements: 
Identifying duplicate bugs automatically saves a lot of developer time. The authors further argue that the traditional attempts at this problem have involved mostly information retrieval(IR) based methods and perform poorly when the same bug is worded differently by bug reporters. So they propose an approach using ensemble method to combine topic modelling and traditional IR based approaches. Topic modelling helps identify duplicates even when bug reports on the same technical issue are worded differently.
### iii2) Related work: 
Traditionally IR methods like Vector Space Model(VSM) have been used for duplicate bug report detection. To improve the performace of IR models, they have been augmented with tools from NLP and adding extra features like failure traces attached to bug reports have been used. Another set of solutions to this problem have used machine learning techniques like binary classification and Support Vector Machines(SVM) have been used. Machine learning(ML) techniqies take more time and are less efficient on their own. Modern IR based approaches using a techniques called BM25F outperform ML based approaches. This paper combines topic based ML and BM25F IR techniques to produce even better results.
### 1113) Negative results:
The authors demonstrate, in their experiments, that they need a project with large number of topics for their model to  work. When K, the number of topics/features in the project is small (K<60), accuracy is low. Number of features for bug reports become too few to
distinguish, and so they are mis-classified by the model. The paper has a graph showing the effect of K on the accuracy of the results.
### iii4) Baseline results:
The paper considers the state of the art IR and topic based approaches as the baseline and obtains a 20% imporovement over them. The best existing model is called REP, which uses an IR only approach. 

### Improvements
#### iv1)
The authors test their model on just three projects. Testing on more projects will help to verify the claims made by the paper.
#### iv2)
Using alternatives to LDA for topic modelling like Explicit Semantic Analysis, to look for improvements in cases when the bug descriptions are very different for the same issue.
#### iv3) 
When less training data is available, the model does not perform well. In such case other features can be used like code commit history, identifying buggy components etc. 
