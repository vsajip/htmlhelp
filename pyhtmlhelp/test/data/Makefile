HHC = "C:/Program Files/HTML Help Workshop/hhc.exe"

ifeq ($(WINDIR),)
HHC := wine $(HHC)
endif

all: \
	sample_archive \
	sample_archive.zip \
	sample_archive.tar \
	sample_archive.tgz \
	sample_archive.chm \
	sample_book.py \
	sample_book \
	sample_book.devhelp \
	sample_book.hhp \
	sample_book.htb \
	sample_book.tgz \
	sample_book.chm

SAMPLE_ARCHIVE_FILES = \
	empty \
	file \
	dir/file \
	dir/subdir/file

empty:
	touch $@

file dir/file dir/subdir/file:
	mkdir -p $(@D)
	echo "Sample..." > $@

#.INTERMEDIATE: $(SAMPLE_ARCHIVE_FILES)

sample_archive: $(SAMPLE_ARCHIVE_FILES)
	@rm -rf $@
	mkdir $@
	cp --parent $^ $@

sample_archive.zip: $(SAMPLE_ARCHIVE_FILES)
	zip $@ $^

sample_archive.tgz: $(SAMPLE_ARCHIVE_FILES)
	tar -czf $@ $^

sample_archive.tar: $(SAMPLE_ARCHIVE_FILES)
	tar -cf $@ $^

sample_archive.chm: sample_archive.hhp $(SAMPLE_ARCHIVE_FILES)
	$(HHC) $<

sample_archive.hhp: $(SAMPLE_ARCHIVE_FILES)
	echo "[OPTIONS]" > $@
	echo "" >> $@
	echo "[FILES]" >> $@
	find $^ -type f -not -name .svn >> $@

SAMPLE_BOOK_FILES = $(shell xsltproc files.xsl sample_book.xml)

page%.html:
	mkdir -p $(@D)
	echo '<html><head><title>Title</title></head><body><p>Paragraph.</p></body></html>' > $@

#.INTERMEDIATE: $(SAMPLE_BOOK_FILES) page%.html

sample_book: $(SAMPLE_BOOK_FILES)
	@rm -rf $@
	mkdir $@
	cp --parent $^ $@

%.py: %.xml
	xsltproc python.xsl $< > $@

%.devhelp: %.xml
	xsltproc devhelp.xsl $< > $@

%.hhp: %.xml %.hhc %.hhk
	xsltproc chm_hhp.xsl $< > $@

%.hhc: %.xml
	xsltproc chm_hhc.xsl $< > $@

%.hhk: %.xml
	xsltproc chm_hhk.xsl $< > $@

%.tgz: %.devhelp
	@rm -f book.devhelp
	@rm -rf book
	cp $*.devhelp book.devhelp
	mkdir book
	cp --parents $(filter-out %.devhelp,$^) book
	tar -czf $@ book.devhelp book
	@rm -f book.devhelp
	@rm -rf book

%.htb: %.hhp %.hhc %.hhk 
	zip -r $@ $^

%.chm: %.hhp %.hhc %.hhk
	-$(HHC) $<

.PRECIOUS: %.hhp %.hhc %.hhk

sample_book.tgz: $(SAMPLE_BOOK_FILES)
sample_book.htb: $(SAMPLE_BOOK_FILES)
sample_book.chm: $(SAMPLE_BOOK_FILES)

clean:
	rm -f \
		sample_archive.hhp

purge:
	rm -f \
		sample_archive \
		sample_archive.zip \
		sample_archive.tar \
		sample_archive.tgz \
		sample_archive.chm

.PHONY: all clean purge
