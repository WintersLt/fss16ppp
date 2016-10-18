# Reading-Week 5

## Anahita Alipour Abram Hindle Eleni Stroulia A Contextual Approach towards More Accurate Duplicate Bug Report Detection

### Keywords
#### ii1) atent semantic indexing (LSI) 
A generative probabilistic model for sets of discrete data which is a type of Information Retrieval.

#### ii2) Formal Concept Analysis (FCA)
A mathematical theory of data analysis using formal contexts and concept lattices.

#### ii3)Triager
he person who is in charge of processing the newly reported bugs and
passing them to appropriate developers to get fixed

#### ii4) Natural language processing
Is a field of computer science, artificial intelligence, and computational linguistics concerned with the interactions between computers and human (natural) languages.

### iii1) Motivational statements:
In our work, we extend the state of
the art by investigating how contextual information, relying on
our prior knowledge of software quality, software architecture,
and system-development (LDA) topics, can be exploited to im-
prove bug-deduplication. We demonstrate the effectiveness of our
contextual bug-deduplication method on the bug repository of the
Android ecosystem. Based on this experience, we conclude that
researchers should not ignore the context of software engineering
when using IR tools for deduplication.

### iii2) Related work: 
The authors address internal validity by replicating past work (Sun
et al.) but also by evaluating both on true negatives (non-
duplicates) and true positives (duplicates), where as Sun
et al.'s methodology only tested for recommendations on
true positives.

### iii3) Future Work:
In the future, the authors plan to build indexing structure of bug
report repository to speed up the retrieval process. They also plan to integrate their technique into Bugzilla tracking system.

### iii4) Baseline results:
By including the overlap of context as
features the authors found that their contextual approach improves the
accuracy of bug-report deduplication by 11.55% 

### Improvements

#### iv1)
The authors did get good results on the Android repository that they tested, however to solidfy their findings they should
test their approach on even larger repositories. If the results are consistent for larger repositories then it will really back their claims.
#### iv2)
Construct validity is threatened by the word-lists in the sense of how they are constructed and if the word-lists actually represent context or just important tokens. 
#### iv3) 
External validity of the experiment is limited by the sole use of the Android bug tracker.
