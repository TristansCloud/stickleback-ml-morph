# lists every 5th files
ls | awk 'NR % 5 == 0'