DOCSET := R5RS
PYTHON := python3.5

help:
	@$(MAKE) --print-data-base --question no-such-target | \
	grep -v -e '^no-such-target' -e '^Makefile'	     | \
	awk '/^[^.%][-A-Za-z0-9_]*:/ \
	     { print substr($$1, 1, length($$1)-1) }'        | \
	sort					             | \
	pr -2 -t

docset: test clean
	./index.py
	tar \
          --exclude '*.py'		\
          --exclude '*.tgz'		\
          --exclude '.DS_Store'	        \
          --exclude '.git'		\
          --exclude '.gitignore'	\
          --exclude 'Makefile'		\
          -C ..                         \
          -cvzf                         \
          $(DOCSET).tgz                 \
          $(DOCSET).docset

test:
	./test_index.py

clean:
	rm -rf *~ __pycache__ *.tgz

.PHONY: help docset test clean
