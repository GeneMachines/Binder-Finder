awk '{split(, pfam, .); split(, id, :); print id[2] , pfam[1] }' <$FILE | sort --unique > foobar.txt
