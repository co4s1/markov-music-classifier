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


## Conclusion
Based on the results of this exploration, the extent to which a first-order Markov chain transition
matrix encapsulate particular composer's style is to an extent that a particular composer can be
associated and identified by their note transition matrix to a high degree of accuracy. The note-
only transition matrix classified all 16 test pieces correctly, yielding 100% accuracy. The
combined note-and-duration matrix achieved 93.75% accuracy, and the duration-only metric
achieved 87.5%. This suggests that while music is a form of art with infinite possibilities of artistic
expression, composers “DNA” is embedded in their work and is quantifiable. 

## Appendix
Table of the results of classification:
| File              | Metric    | Mozart LL | Bach LL   | Winner   |
| ----------------- | --------- | --------- | --------- | -------- |
| BWV788.musicxml   | Notes     | −6422.71  | −5079.36  | Bach ✓   |
| Durs              | −5366.16  | −2129.70  | Bach ✓    |
| Comb              | −12876.49 | −11830.39 | Bach ✓    |
| BWV789.musicxml   | Notes     | −7092.34  | −3680.86  | Bach ✓   |
| Durs              | −2986.31  | −1659.19  | Bach ✓    |
| Comb              | −13626.12 | −10519.84 | Bach ✓    |
| BWV790.musicxml   | Notes     | −6011.21  | −4051.63  | Bach ✓   |
| Durs              | −6667.06  | −2901.89  | Bach ✓    |
| Comb              | −13134.63 | −11141.07 | Bach ✓    |
| BWV812.musicxml   | Notes     | −25994.85 | −18431.64 | Bach ✓   |
| Durs              | −16601.98 | −9442.10  | Bach ✓    |
| Comb              | −52497.00 | −48394.88 | Bach ✓    |
| BWV813.musicxml   | Notes     | −25416.56 | −18020.12 | Bach ✓   |
| Durs              | −16841.40 | −7772.90  | Bach ✓    |
| Comb              | −45251.68 | −44328.94 | Bach ✓    |
| BWV849.musicxml   | Notes     | −28242.19 | −18702.73 | Bach ✓   |
| Durs              | −23314.02 | −10545.60 | Bach ✓    |
| Comb              | −47428.20 | −43863.81 | Bach ✓    |
| BWV853.musicxml   | Notes     | −7148.41  | −5589.32  | Bach ✓   |
| Durs              | −13121.60 | −3273.64  | Bach ✓    |
| Comb              | −28158.38 | −6327.01  | Bach ✓    |
| BWV_0851.musicxml | Notes     | −2984.72  | −2984.62  | Bach ✓   |
| Durs              | −422.23   | −455.79   | Mozart \* |
| Comb              | −9537.97  | −8017.21  | Bach ✓    |
| k574.musicxml     | Notes     | −3739.84  | −4497.65  | Mozart ✓ |
| Durs              | −1133.19  | −1077.62  | Bach \*   |
| Comb              | −9477.06  | −10924.09 | Mozart ✓  |
| Sonata K576       | Notes     | −5891.13  | −7194.68  | Mozart ✓ |
| Durs              | −1511.43  | −1541.26  | Mozart ✓  |
| Comb              | −12364.23 | −14141.03 | Mozart ✓  |
| Sonata K333 mvt 1 | Notes     | −3874.27  | −6202.82  | Mozart ✓ |
| Durs              | −542.39   | −730.60   | Mozart ✓  |
| Comb              | −7950.00  | −13899.21 | Mozart ✓  |
| Sonata K333 mvt 2 | Notes     | −4856.84  | −5152.93  | Mozart ✓ |
| Durs              | −1393.41  | −1477.50  | Mozart ✓  |
| Comb              | −11050.96 | −10976.00 | Bach \*   |
| Sonata K333 mvt 3 | Notes     | −10950.82 | −14274.67 | Mozart ✓ |
| Durs              | −2515.99  | −3119.91  | Mozart ✓  |
| Comb              | −22947.50 | −33116.08 | Mozart ✓  |
| Sonata K310 mvt 1 | Notes     | −4711.18  | −5641.17  | Mozart ✓ |
| Durs              | −750.99   | −912.40   | Mozart ✓  |
| Comb              | −9091.22  | −12639.45 | Mozart ✓  |
| Sonata K310 mvt 2 | Notes     | −3011.68  | −5497.03  | Mozart ✓ |
| Durs              | −698.30   | −765.72   | Mozart ✓  |
| Comb              | −7505.45  | −12500.87 | Mozart ✓  |
| Sonata K310 mvt 3 | Notes     | −2686.38  | −3727.36  | Mozart ✓ |
| Durs              | −707.33   | −837.43   | Mozart ✓  |
| Comb              | −6349.42  | −9477.78  | Mozart ✓  |
* Misclassification


