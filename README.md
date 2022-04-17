# An Empirical study to understand the Compositional Prowess of Neural Dialog Models
Authors: Vinayshekhar Bannihatti Kumar, Vaibhav Kumar, Mukul Bhutani and Alexander Rudnicky
Paper Link: To appear soon
This reposity contains the code to reproduce our results from the ACL Neagtive Insights Workshop.

## Abstract
In this work, we examine the problems associated with neural dialog models under the common theme of compositionality. Specifically, we investigate three manifestations of compositionality: (1) Productivity, (2) Substitutivity, and (3) Systematicity. These manifestations shed light on the generalization, syntactic robustness, and semantic capabilities of neural dialog models. We design probing experiments by perturbing the training data to study the above phenomenon. We make informative observations based on automated metrics and hope that this work increases research interest in understanding the capacity of these models.

## Training Models
bash run_multiple_ids.sh train <transformer/s2s/s2s_att_general> <dailydialog/personachat/dialog_babi:Task:5> EXPERIMENT_NAME EXPERIMENT_DATA_FOLDER
1. The first argument specifies the type of model to train - transformers, seq2seq with lstms or seq2seq with lstms and attention.
2. The second argument specifies the dataset to train on
3. The third argument specifies the name of the experiment that is being run.
4. The fourth argument specifies the data pertubation which has been done at training for that experiment

## Evaluating Models
bash run.sh eval <transformer/s2s/s2s_att_general> <dailydialog/personachat/dialog_babi:Task:5> EXPERIMENT_NAME EXPERIMENT_DATA_FOLDER
This runs all evaluations indicated in run_multiple_ids.sh using a saved model. The result of running this should give metrics like indicated in our paper.

## Citation
```
```

## Questions?
For any questions, please contact any of the authors.