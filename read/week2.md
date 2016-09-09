# Reading-Week 2

## J. Chang and D. Blei. Relational topic models for document networks. In AIStats, 2009.

### Keywords
#### ii1) RTM: 
	  Relational Topic Model(RTM) is the novel approach for modelling 
	  document networks presented in this paper. Document is modelled using 
	  LDA(Latent Dirichlet allocation) topic modelling technique. The link 
	  between documents is then modelled as a binary variable, one for each
	  pair of documents.

#### ii2) LDA: 
	  LDA is a generative probabilistic model popular for topic modelling
	  to describe a corpus of documents. In its generative process, each 
	  document is allocated a Dirichlet distributed vector of topic proportions, 
	  and each word of the document is assumed drawn by first drawing a topic
	  assignment from the overall topic distribution for document and then drawing 
	  the word from the corresponding topic distribution pertaining to that topic.

#### ii3) Document networks: 
	  A collection of textual documents that are related to 
	  each other in some way, so that they form links between each other that can 
	  be modelled as a network. e.g. Scientific papers and their citations, web pages
	  and hyperlinks.

#### ii4) Variational inference: 
It is a technique used in Bayesian inference to estimate intractable quantities, usually probabilities and expectations.
The authors use it estimate posterior inference, exact value of which is intractable. A family of distribution functions 
for latent variables are fit by varying the parameters.

### iii1) Motivational statements:
The ability to predict the content of a document from its links and links from the documents has widespread applications in fields like social networks, scientific papers citations and links among web pages. Most approaches before this paper treat the content and the connections between documents separately. This paper uses a combined approach which gives it the uniqie ability to predict content when connection is given and vice versa. Also the proposed model can make accurate predictions for hitherto unseen data. eg. friends for a new profile on a social network.
### iii2) Related work: 
Earlier approaches at modelling network of documents treated link structure as independent problem. Recent models incorporate the node attributes as well. While older approaches were not based on latent space modelling (i.e. incorporating a hidden variable like "topics"), some approaches that did use latent variables used it to account for links in data and not data itself. The work closest to this paper is by Nallapati et al. that proposed a model which includes words from documents in predicting links. But word attributes for links are different from those used for content prediction. This handicaps the model in predicting one of the two, given the other. This paper tries to overcome these shortcomings by using a unified approach to model both links and content.
### iii3) Patterns/Anti patterns:
The paper advises to use only the document links that are observed and ignore the unobserved ones while developing inference models. This helps model the idea that absense of a link does not necesserily mean that the two documents are not realated. And secondly, this reduces the amount of caclulations.

On the other hand while optimizing the document link probability function without any negative observations is not possible. The paper advises to use a regularization parameter(in case of logistic function) or an equivalent term to account for negative observations.
### iii4) Baseline results:
The baseline model used models words and links independently. The
words are modeled with a multinomial; the links are modeled with a Bernoulli. The proposed model outperforms the baseline by 6% in terms of log likelihood  of observed distribution. The model significantly outperforms in predicting links given words and vice versa.

### Improvements
#### iv1)
The claim for the application of RTM in social network modelling should be verified by using some social network dataset.
#### iv2)
Using other models than bag of words for document similarity can be tested. Since bag of words might not be applicable in situations like social networks.
#### iv3) 
The model can be tested on more datasets than the three mentioned to justify the results and see if improvements in prediction accuracy are universal.
