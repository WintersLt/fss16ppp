# Reading-Week 7

## Automated Library Recommendation by Ferdian Thung, David Lo, and Julia Lawall

### Keywords
#### ii1) Frequent Itemset Mining
Frequent itemset mining takes as input a transaction
database (i.e., a multi-set of transactions), where each transaction
is a set of items, and outputs sets of items (aka. itemsets)
that appear frequently (i.e., each frequent itemset is a subset of
many transactions) in the database.

#### ii2) Association Rule Mining
An association rule is an “if/then” rule that captures a
relationship between two itemsets X and Y in the database. It
can be written as:
X → Y
#### ii3) Collaborative Filtering
Collaborative filtering is an automatic technique to make
predictions about an entity based on information collected
about other similar entities.
#### ii4) TrainingProjects 
TrainingProjects is a set
of projects, along with the names of third-party libraries used
by each of them. Models are extracted by the following subcomponents:
. RuleExtractor
. FeatureVectorExtractor

### iii1) Motivational statements:
Many third party libraries are available to be downloaded
and used. Using such libraries can reduce development
time and make the developed software more reliable. However,
developers are often unaware of suitable libraries to be used
for their projects and thus they miss out on these benefits. To
help developers better take advantage of the available libraries,
we propose a new technique that automatically recommends
libraries to developers. Our technique takes as input the set of
libraries that an application currently uses, and recommends
other libraries that are likely to be relevant

### iii2) Related work: 
Mandelin et al. propose the problem of jungloid mining. Given a query that describes the input and output
types, jungloid mining returns code fragments that satisfy the
query. Thummalapenta and Xie propose the tool ParseWeb that recommends code examples from the web.

### iii3) Future Work:
The author explains their future plans as: We would also like to extend our approach to be able to
recommend libraries to projects that only use a small number
of libraries or do not use any libraries at all.
In terms of our experimental method, we plan to experiment
with various experimental settings, e.g., considering different
numbers of projects being dropped, considering different
number of libraries used, etc. We also plan to integrate our
proposed approach in an IDE (e.g., Eclipse) and perform a
user study.

### iii4) Baseline results:
We investigate the effectiveness of our hybrid approach on
500 software projects that use many third-party libraries. Our
experiments show that our approach can recommend libraries
with recall rate@5 of 0.852 and recall rate@10 of 0.894.

### Improvements

#### iv1)
 Author can imporve the efficiency of their proposed method by considering the fact that sometimes libraries are known to users but maybe they are unaware of the methods in it. 
#### iv2)
The authors could include more projects to furthur validate their results.
#### iv3) 
The authors could also consider not only the libraries but also their domain, to furthur enhance the accuracy.
