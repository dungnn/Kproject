find . -name "aclocal.m4" | xargs rm -rv
find . -name "autom4te.cache" | xargs rm -rv
find . -name "config.log" | xargs rm -rv
find . -name "config.status" | xargs rm -rv
find . -name "configure" | xargs rm -rv
find . -name ".deps" | xargs rm -rv
find . -name ".dirname" | xargs rm -rv
find . -name "Makefile" | xargs rm -rv
find . -name "Makefile.in" | xargs rm -rv

aclocal
autoconf
automake -a --copy
