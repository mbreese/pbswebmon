# Makefile for MPI_START
VERSION=$(shell cat VERSION)
DESTDIR=
PREFIX=/var/www
WEBROOT=/var/www/html
SVNURL=https://pbswebmon.svn.sourceforge.net/svnroot/pbswebmon

all:
	$(MAKE) -C src all 
	$(MAKE) -C modules all
	$(MAKE) -C templates all
	$(MAKE) -C docs all

clean:
	$(MAKE) -C src clean
	$(MAKE) -C modules clean
	$(MAKE) -C templates clean
	$(MAKE) -C docs clean

install:
	mkdir -p $(DESTDIR)/$(WEBROOT)/pbswebmon
	mkdir -p $(DESTDIR)/$(PREFIX)/cgi-bin
	mkdir -p $(DESTDIR)/etc
	mkdir -p $(DESTDIR)/usr/share/doc/pbswebmon
	install -m 755 cgi-bin/pbswebmon.py $(DESTDIR)/$(PREFIX)/cgi-bin/pbswebmon.py
	install -m 644 *.js $(DESTDIR)/$(WEBROOT)/pbswebmon
	install -m 644 *.css $(DESTDIR)/$(WEBROOT)/pbswebmon
	install -m 644 pbswebmon.conf $(DESTDIR)/etc/pbswebmon.conf
	install -m 644 README $(DESTDIR)/usr/share/doc/pbswebmon/README
	

dist:	
	rm -rf pbswebmon-$(VERSION)
	svn export https://pbswebmon.svn.sourceforge.net/svnroot/pbswebmon/tags/pbswebmon-$(VERSION) pbswebmon-$(VERSION)
	sed -e "s/@VERSION@/$(VERSION)/" pbswebmon.spec.in > pbswebmon-$(VERSION)/pbswebmon-$(VERSION).spec
	tar cvzf pbswebmon-$(VERSION).tar.gz pbswebmon-$(VERSION)
	rm -rf pbswebmon-$(VERSION)

tag:
	svn cp $(SVNURL)/trunk $(SVNURL)/tags/pbswebmon-$(VERSION)/


rpm: dist
	rpmbuild -ta pbswebmon-$(VERSION).tar.gz

export VERSION
export PREFIX
export DESTDIR
