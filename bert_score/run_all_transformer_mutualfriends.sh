#!/usr/bin/env bash
bash bert-score/display_examples.sh mutualfriends ./mutualfriends/drop_words_1/ ./mutualfriends-data/drop_words_1
bash bert-score/display_examples.sh mutualfriends ./mutualfriends/drop_words_0.75/ ./mutualfriends-data/drop_words_0.75
bash bert-score/display_examples.sh mutualfriends ./mutualfriends/drop_words_0.5/ ./mutualfriends-data/drop_words_0.5
bash bert-score/display_examples.sh mutualfriends ./mutualfriends/drop_words_0.25/ ./mutualfriends-data/drop_words_0.25
bash bert-score/display_examples.sh mutualfriends ./mutualfriends/context_change_2/ ./mutualfriends-data/context_change_2
bash bert-score/display_examples.sh mutualfriends ./mutualfriends/context_change_4/ ./mutualfriends-data/context_change_4
bash bert-score/display_examples.sh mutualfriends ./mutualfriends/context_change_6/ ./mutualfriends-data/context_change_6
bash bert-score/display_examples.sh mutualfriends ./mutualfriends/context_change_8/ ./mutualfriends-data/context_change_8
bash bert-score/display_examples.sh mutualfriends ./mutualfriends/context_change_10/ ./mutualfriends-data/context_change_10
bash bert-score/display_examples.sh mutualfriends ./mutualfriends/zipf_drop_0_1/ ./mutualfriends-data/zipf_drop_0_1
bash bert-score/display_examples.sh mutualfriends ./mutualfriends/zipf_drop_1_3/ ./mutualfriends-data/zipf_drop_1_3
bash bert-score/display_examples.sh mutualfriends ./mutualfriends/zipf_drop_300_600/ ./mutualfriends-data/zipf_drop_300_600
bash bert-score/display_examples.sh mutualfriends ./mutualfriends/zipf_drop_600_1000/ ./mutualfriends-data/zipf_drop_600_1000
bash bert-score/display_examples.sh mutualfriends ./mutualfriends/zipf_drop_300_1000/ ./mutualfriends-data/zipf_drop_300_1000
echo "Done with MutualFriends"
