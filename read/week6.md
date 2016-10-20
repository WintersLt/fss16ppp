# Reading-Week 6

## DRONE: Predicting Priority of Reported Bugs by Multi-Factor Analysis

### Keywords

#### ii1) Temporal factor
The bug reporting factor that includes other bug reports that are reported at the same time.

#### ii2) DRONE 
A framework for PreDicting PRiority via Multi-Faceted FactOrANalysEs.


#### ii3) GRAY
A classification engine named (ThresholdinG and Linear Regression to ClAssifY Imbalanced Data) which
enhances linear regression with our thresholding approach to handle imbalanced bug report data.

#### ii4) Tokenization
Tokenization is a process to extract these tokens
from a textual document by splitting the document into tokens
according to the delimiters

### iii1) Motivational statements:
As resources are limited,
bug reports would be investigated based on their priority levels.
This priority assignment process however is a manual one.
Could we do better? In this paper, we propose an automated
approach based on machine learning that would recommend
a priority level based on information available in bug reports.

### iii2) Related work: 
Closest to author's work, is the series of work on bug report
severity prediction by Menzies and Marcus.These
studies predict the severity field of a bug report based on
the textual content of the report.

### iii3) Future Work:
In the future, the authors plan to include more bug reports from
more open source projects to experiment with. They also plan
to further improve the accuracy of their approach. For instance,
we can try to construct a linear regression model using only
the most discriminative features and evaluate the resulting
solution. We also plan to analyze the impact of inaccuracies
in the thresholding process on the final result of DRONE

### iii4) Baseline results:
Experiments on more than a hundred thousands bug reports from Eclipse
show that we can outperform baseline approaches in terms of
average F-measure by a relative improvement of 58.61%.

### Improvements

#### iv1)
It could be great to compare the effectiveness of various classification algorithms in comparison with GRAY in predicting the priority levels of bug reports
#### iv2)
Another improvement could be to find out the 	features are the most effective in
discriminating the priority levels
#### iv3) 
The expermient could be performed over more open source projects to verify the stated accuracy.

