# Reading-Week 3

##A Discriminative Model Approach for Accurate Duplicate Bug Report Retrieval##

### Keywords

#### ii1) Support Vector Machine: (SVM) 
Support Vector Machine(SVM) is an approach to build-
ing a discriminative model or classifier based on a set of
labeled vectors.

#### ii2) Term Frequency:
TF is a local importance measure. Given
a term and a document, in general, TF corresponds to the
number of times the term appears within the document.

#### ii3) Inverse Term Frequency:
IDF is a global importance measure most
commonly calculated by the formula within the corpus,
idf (term) = log 2 (Dall / Dterm ) where Dall is the number of the documents in the corpus while Dterm is the number of documents containing the term.

#### ii4) Triaging
If other users have reported the bug before
then the bug would be classified as being a duplicate and
attached to the original first-reported “master” bug report.

### iii1) Motivational statements:
Automating triaging has been proved challenging as two reports
of the same bug could be written in various ways. There is
still much room for improvement in terms of accuracy of du-
plicate detection process. In this paper, we leverage recent
advances on using discriminative models for information re-
trieval to detect duplicate bug reports more accurately.

### iii2) Related work: 
One of the pioneer studies on duplicate bug report detection is by Runeson et al.Their approach first cleaned
the textual bug reports via natural language processing tech-
niques – tokenization, stemming and stop word removal.

### iii3) Future Work:
As a future work, the author plan to investigate the utility of paraphrases in discriminative models for potential improvement in accuracy. 
The other interesting direction is adopting pattern-based classification to extract richer feature
set that enables better discrimination and detection of duplicate bug reports

### iii4) Baseline results:
We have validated our approach on three large software bug
repositories from Firefox, Eclipse, and OpenOffice. We show
that our technique could result in 17–31%, 22–26%, and 35–
43% relative improvement over state-of-the-art techniques in
OpenOffice, Firefox, and Eclipse datasets respectively using
commonly available natural language information only.

### Improvements

#### iv1)
The authors have not focused much on the automatic filtering of duplicates to prevent multiple duplicate reports from 
reaching triagers instead the author choose to provide a list of similar bug reports to each incoming report under investigation. 

#### iv2)
The authors did get good results on the three open source bug repositories that they tested, however to solidfy their findings they should
test their approach on even larger repositories. If the results are consistent for larger repositories then we

#### iv3) 
The runtime overhead of our algorithm is higher than past approaches, for larger repositories it can be a bit of problem.

