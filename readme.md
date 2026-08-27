# Markov chain classical music classifier
## Abstract 
The training process involved counting every occurrence of a transition between two states across the entire training library used to create the probability distribution. 
If there is an underlying style for a particular composer, the composer can be thought of as the probability distribution function. By recording transitions experimentally over a large number of iterations, the experimental probability distribution should converge to the “theoretical” probability distribution "function" of that composer. 
For the purpose of this investigation, 26 movements (Sonatas, Fantasias, Rondos) of Wolfgang Amadeus Mozart, representing 30004 transitions, were analysed, and 15 movements (Inventions, Sinfonias, Preludes) of Johann Sebastian Bach, representing 34015 transitions, were analysed.


## Results

The model was tested on 16 pieces not used in the training data. Moreover, the test pieces were
picked to not contain any association with the training model, by ensuring that not only same works
but also that different movements from different works are do not overlap between training and test.
8 Bach works and 8 Mozart works were picked, none of which were included in the training set to construct the initial transition matrices. 
Each piece was evaluated by comparing it through Log-Likelihood with three different state spaces
constructed from the gathered training data: Notes only, Durations only, and a Combined (note +
duration) state space, yielding 48 individual tests. The results are summarised in the table below,
where a correct classification is one where the higher Log-Likelihood corresponds to the true
composer

### Classifier table
| Metric  | Bach (8 pieces) | Mozart (8 pieces) | Overall Accuracy |
| ------- |:---------------:|------------------:|------------------:|
| Notes Only  | 8/8 (100%) | 8/8 (100%) | 16/16 (100%) |
| Durations Only  | 7/8 (87.5%) | 7/8 (87.5%) | 14/16 (87.5%) |
| Combined  | 8/8 (100%) | 7/8 (87.5%) | 15/16 (93.75%) |



### Heatmaps
In these maps,the y-axis represents the current note (Xn) and the x-axis represents the subsequent note (Xn+1).
Warmer colors indicate a high probability that a particular transition, and cooler colors represent
a lower probability.

**Mozart notes heatmap**

<img src="https://github.com/co4s1/markov-music-classifier/blob/master/maps/mozart_notes_dna.png" width="450">

**Mozart notes and durations heatmap**

<img src="https://github.com/co4s1/markov-music-classifier/blob/master/maps/mozart_notes_and_durations_dna.png" width="450">


**Bach notes heatmap**

<img src="https://github.com/co4s1/markov-music-classifier/blob/master/maps/bach_notes_dna.png" width="450">

**Bach notes and durations heatmap**

<img src="https://github.com/co4s1/markov-music-classifier/blob/master/maps/bach_notes_and_durations_dna.png" width="450">
