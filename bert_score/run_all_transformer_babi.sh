#!/usr/bin/env bash
bash bert-score/display_examples.sh dialog_babi:Task:5 ./dialog_babi:Task:5/baseline/ ./babi-data/baseline
bash bert-score/display_examples.sh dialog_babi:Task:5 ./dialog_babi:Task:5/drop_words_1/ ./babi-data/drop_words_1
bash bert-score/display_examples.sh dialog_babi:Task:5 ./dialog_babi:Task:5/drop_words_0.75/ ./babi-data/drop_words_0.75
bash bert-score/display_examples.sh dialog_babi:Task:5 ./dialog_babi:Task:5/drop_words_0.5/ ./babi-data/drop_words_0.5
bash bert-score/display_examples.sh dialog_babi:Task:5 ./dialog_babi:Task:5/drop_words_0.25/ ./babi-data/drop_words_0.25
bash bert-score/display_examples.sh dialog_babi:Task:5 ./dialog_babi:Task:5/context_change_2/ ./babi-data/context_change_2
bash bert-score/display_examples.sh dialog_babi:Task:5 ./dialog_babi:Task:5/context_change_4/ ./babi-data/context_change_4
bash bert-score/display_examples.sh dialog_babi:Task:5 ./dialog_babi:Task:5/context_change_6/ ./babi-data/context_change_6
bash bert-score/display_examples.sh dialog_babi:Task:5 ./dialog_babi:Task:5/context_change_8/ ./babi-data/context_change_8
bash bert-score/display_examples.sh dialog_babi:Task:5 ./dialog_babi:Task:5/context_change_10/ ./babi-data/context_change_10
bash bert-score/display_examples.sh dialog_babi:Task:5 ./dialog_babi:Task:5/zipf_drop_0_1/ ./babi-data/zipf_drop_0_1
bash bert-score/display_examples.sh dialog_babi:Task:5 ./dialog_babi:Task:5/zipf_drop_1_3/ ./babi-data/zipf_drop_1_3
bash bert-score/display_examples.sh dialog_babi:Task:5 ./dialog_babi:Task:5/zipf_drop_300_600/ ./babi-data/zipf_drop_300_600
bash bert-score/display_examples.sh dialog_babi:Task:5 ./dialog_babi:Task:5/zipf_drop_600_1000/ ./babi-data/zipf_drop_600_1000
bash bert-score/display_examples.sh dialog_babi:Task:5 ./dialog_babi:Task:5/zipf_drop_300_1000/ ./babi-data/zipf_drop_300_1000
echo "Babi done!"
