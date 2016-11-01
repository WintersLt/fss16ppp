# Reading-Week 8

## Automatic Recommendation of API Methods from Feature Requests by Ferdian Thung, Shaowei Wang, David Lo, and Julia Lawall

### Keywords
#### ii1) Feature Requests and JIRA
JIRA is an issue management system developed by Altassian.
It is used in many software projects to capture
and store issues that are reported by users and developers.

#### ii2) Text Pre-processing
Text pre-processing is an important task in text mining [21].
Its purpose is to convert a piece of text into a common
representation easily processed by a text mining algorithm
and to remove certain noise. Widely used text pre-processing
strategies include tokenization and stemming.

#### ii3) Tokenization
Tokenization refers to the process that breaks a document
into word tokens. Delimiters are used to demarcate one token
from another. Typically, space and punctuation are used as
delimiters.

#### ii4) Stemming 
Stemming is the process of converting a word to its base
form. This base form is usually called the stem word. For
example, word “argue”, “argues”, “argued”, and “arguing”
have a common stem word “argu”. Even though word “argu”
is not a dictionary word, the conversion assures that we can
identify a word in its different forms and link these word
forms together

### iii1) Motivational statements:
Many software systems rely on a variety of external libraries
for various functionalities. Accordingly, developers often use
external libraries to implement required changes. However,
using these libraries effectively, requires knowledge of the
relevant methods and classes that they provide. Given the large
number of libraries, and the large number of methods and
classes that they provide, it can be a challenge for developers
to identify the methods and classes of interest, given a target
requirement document expressed as a feature request.
Considering the above issues and opportunities, there is a
need for an automated approach that could help developers to
better harness the power of libraries. The automated approach
should be able to recommend library methods given a feature
request. We refer to our problem as method recommendation
from feature requests.

### iii2) Related work: 
Mandelin et al. propose the tool Prospector, which recommends
objects and method calls, referred to as jungloids, to
convert an object of a particular type, to an object of another
type. Prospector takes as input a query consisting of a
pair of the input type and the output type. It then analyzes
signatures of API methods and constructs a signature graph
to recommend jungloids based on the query. A jungloid is
ranked based on the number of methods it contains and the
output type. Thummalapenta and Xie investigate the same
problem. 

### iii3) Future Work:
The author explains their future plans as: In the future, we plan to improve our solution further
to achieve even higher recall-rate@k scores. Some possible
directions include using state-of-the-art natural language processing, taking the information stored in the code
base into account, and specification mining.

### iii4) Baseline results:
We have evaluated our approach on more than 500
feature requests of Axis2/Java, CXF, Hadoop Common, HBase,
and Struts 2. Our experiments show that our approach is able to
recommend the right methods from 10 libraries with an average
recall-rate@5 of 0.690 and recall-rate@10 of 0.779 respectively.

### Improvements

#### iv1)
 Author should validate their results by evaluating on projects with limited number of feature requests.
#### iv2)
 Authors could also have included the results of their proposed approach for bug reports in addition to feature requests. This could have widen the scope of usage for their approach.
#### iv3) 
The authors could also have included teh performance results of their proposed approach when applied in an IDE.
