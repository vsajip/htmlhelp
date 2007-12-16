RM_R = $(RM) -r

EPYDOC = epydoc
EPYDOC_FLAGS = \
	--no-private --css blue \
	--name 'HTML Help Python API' \
	--navlink 'HTML Help Python API homepage' \
	--url http://htmlhelp.berlios.de/api/python/ \

MODULE = ../htmlhelp

default: html

all: html pdf

html pdf:
	@$(RM_R) $@
	$(EPYDOC) --$@ $(EPYDOC_FLAGS) $(MODULE)

clean:
	rm -rf html pdf


.PHONY: default all html pdf clean
