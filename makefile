ifeq ($(PREFIX),)
    PREFIX := /usr/local
endif

install:
	install -m 755 mdock $(DESTDIR)$(PREFIX)/bin