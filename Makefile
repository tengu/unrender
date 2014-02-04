
all:

t:
	cat test/paths \
	| python unrender.py path --threashold=3 \
	| tee x.out
	diff x.out test/paths.out
