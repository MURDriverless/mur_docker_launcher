ifeq ($(PREFIX),)
    PREFIX := /usr/local
endif

install:
	sudo install -m 755 mdock $(DESTDIR)$(PREFIX)/sbin