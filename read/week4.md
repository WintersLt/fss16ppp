# Reading-Week 4

##  C. Sun, D. Lo, S.-C. Khoo, and J. Jiang. Towards more accurate retrieval of duplicate bug reports.

### Keywords
#### ii1) BM25F:
M25F is an effective textual similarity function for structured document retrieval and is meant for facilitating the retrieval of documents relevant to a short query.

#### ii2) Textual Features:
The first feature defined in (7) is the textual similarity between two bug reports over the fields summary and description
computed by BM25F.

#### ii3) Mean average precision(MAP): 
MAP is a single-figure measure of ranked retrieval results independent of the size of the top list. It is designed for
general ranked retrieval problem, where a query can have multiple relevant documents.

#### ii4) Parameter Tuning:
To apply gradient descent, for each parameter x in REP, we manually derive the partial derivative of RNC with respect to x.
This process is called as parameter tuning.

### iii1) Motivational statements:
In a bug tracking system, different testers or users
may submit multiple reports on the same bugs, referred to as
duplicates, which may cost extra maintenance efforts in triaging
and fixing bugs. In order to identify such duplicates accurately,
in this paper we propose a retrieval function (REP) to measure
the similarity between two bug reports

### iii2) Related work: 
Wang et al. use another feature vector construction approach
where each feature is computed by considering both term
frequency (TF) and inverse document frequency (IDF) of the
words in the bug reports following the formula:
T F(word)∗IDF(word)

### iii3) Future Work:
In the future, the authors plan to build indexing structure of bug
report repository to speed up the retrieval process. They also plan to integrate their technique into Bugzilla tracking system.

### iii4) Baseline results:
The authors have investigated the utility of our technique on 4 sizable
bug datasets extracted from 3 large open-source projects,i.e., OpenOffice, Firefox and Eclipse; and find that both
BM25F ext and REP are indeed able to improve the retrieval performance. 
For retrieval performance of REP, compared to our previous work based on SVM, it increases
recall rate@k by 10–27%, and MAP by 17–23%.

### Improvements

#### iv1)
The authors could have also compared their results using other similarity techniques than Cosine Similarity. 

#### iv2)
The authors could also have taken execution trace information present in the bug reports into consideration.

#### iv3) 
The authors could also have considered filtering the duplicate bugs to reach triagers. It may be something useful to look into.

