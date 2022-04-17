#!/usr/bin/env bash
bash bert-score/display_examples.sh dailydialog ./dailydialog/drop_words_1.0/ ./dailydialog-data/drop_words_1.0
bash bert-score/display_examples.sh dailydialog ./dailydialog/drop_words_0.75/ ./dailydialog-data/drop_words_0.75
bash bert-score/display_examples.sh dailydialog ./dailydialog/drop_words_0.5/ ./dailydialog-data/drop_words_0.5
bash bert-score/display_examples.sh dailydialog ./dailydialog/drop_words_0.25/ ./dailydialog-data/drop_words_0.25
bash bert-score/display_examples.sh dailydialog ./dailydialog/context_change_2/ ./dailydialog-data/context_change_2
bash bert-score/display_examples.sh dailydialog ./dailydialog/context_change_4/ ./dailydialog-data/context_change_4
bash bert-score/display_examples.sh dailydialog ./dailydialog/context_change_6/ ./dailydialog-data/context_change_6
bash bert-score/display_examples.sh dailydialog ./dailydialog/context_change_8/ ./dailydialog-data/context_change_8
bash bert-score/display_examples.sh dailydialog ./dailydialog/context_change_10/ ./dailydialog-data/context_change_10
bash bert-score/display_examples.sh dailydialog ./dailydialog/zipf_drop_0_1/ ./dailydialog-data/zipf_drop_0_1
bash bert-score/display_examples.sh dailydialog ./dailydialog/zipf_drop_1_3/ ./dailydialog-data/zipf_drop_1_3
bash bert-score/display_examples.sh dailydialog ./dailydialog/zipf_drop_500_1000/ ./dailydialog-data/zipf_drop_500_1000
bash bert-score/display_examples.sh dailydialog ./dailydialog/zipf_drop_500_1500/ ./dailydialog-data/zipf_drop_500_1500
bash bert-score/display_examples.sh dailydialog ./dailydialog/zipf_drop_1000_1500/ ./dailydialog-data/zipf_drop_1000_1500
echo "Done with Dailydialog"
