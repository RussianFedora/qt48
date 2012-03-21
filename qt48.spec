# Fedora Review: http://bugzilla.redhat.com/188180

# configure options
# -no-pch disables precompiled headers, make ccache-friendly
%define no_pch -no-pch

# See http://bugzilla.redhat.com/223663
%define multilib_archs x86_64 %{ix86} ppc64 ppc s390x s390 sparc64 sparcv9

Summary: Qt toolkit
Name:    qt48
Epoch:   1
Version: 4.8.0
Release: 10.1%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License: (LGPLv2 with exceptions or GPLv3 with exceptions) and ASL 2.0 and BSD and FTL and MIT
Group: System Environment/Libraries
Url: http://qt.nokia.com/
Source0: qt-everywhere-opensource-src-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#Obsoletes: qt4 < %{version}-%{release}
#Provides: qt4 = %{version}-%{release}
%{?_isa:Provides: qt4%{?_isa} = %{version}-%{release}}

# default Qt config file
Source4: Trolltech.conf

# header file to workaround multilib issue
Source5: qconfig-multilib.h

# set default QMAKE_CFLAGS_RELEASE
Patch2: qt-everywhere-opensource-src-4.8.0-tp-multilib-optflags.patch

# get rid of timestamp which causes multilib problem
Patch4: qt-everywhere-opensource-src-4.8.0-timestamp.patch

# enable ft lcdfilter
Patch15: qt-x11-opensource-src-4.5.1-enable_ft_lcdfilter.patch

# may be upstreamable, not sure yet
# workaround for gdal/grass crashers wrt glib_eventloop null deref's
Patch23: qt-everywhere-opensource-src-4.6.3-glib_eventloop_nullcheck.patch

# workaround for a MOC issue with Boost 1.48 headers (#756395)
Patch24: qt-everywhere-opensource-src-4.8.0-rc1-moc-boost148.patch

## upstreamable bits
# fix invalid inline assembly in qatomic_{i386,x86_64}.h (de)ref implementations
Patch53: qt-x11-opensource-src-4.5.0-fix-qatomic-inline-asm.patch

# fix invalid assumptions about mysql_config --libs
# http://bugzilla.redhat.com/440673
Patch54: qt-everywhere-opensource-src-4.7.0-beta2-mysql_config.patch

# http://bugs.kde.org/show_bug.cgi?id=180051#c22
Patch55: qt-everywhere-opensource-src-4.6.2-cups.patch

# Fails to create debug build of Qt projects on mingw (rhbz#653674)
Patch64: qt-everywhere-opensource-src-4.7.1-QTBUG-14467.patch

# fix QTreeView crash triggered by KPackageKit (patch by David Faure)
Patch65: qt-everywhere-opensource-src-4.8.0-tp-qtreeview-kpackagekit-crash.patch

# fix the outdated standalone copy of JavaScriptCore
Patch67: qt-everywhere-opensource-src-4.8.0-beta1-s390.patch

# https://bugs.webkit.org/show_bug.cgi?id=63941
# -Wall + -Werror = fail
Patch68: webkit-qtwebkit-2.2-no_Werror.patch

# revert qlist.h commit that seems to induce crashes in qDeleteAll<QList (QTBUG-22037)
Patch69: qt-everywhere-opensource-src-4.8.0-QTBUG-22037.patch

# Qt doesn't close orphaned file descriptors after printing (#746601, QTBUG-14724)
Patch70: qt-everywhere-opensource-src-4.8.0-QTBUG-14724.patch 

# Buttons in Qt applications not clickable when run under gnome-shell (#742658, QTBUG-21900)
Patch71:  qt-everywhere-opensource-src-4.8.0-QTBUG-21900.patch

# restore Qt-4.7 behavior (which kde needs) to QUrl.toLocalfile
# https://bugzilla.redhat.com/show_bug.cgi?id=749213
Patch72: qt-everywhere-opensource-src-4.8.0-QUrl_toLocalFile.patch

# QtWebKit wtf library: GMutex is a union rather than a struct in GLib >= 2.31
# fixes FTBFS: https://bugs.webkit.org/show_bug.cgi?id=69840
Patch73: qt-everywhere-opensource-src-4.8.0-qtwebkit-glib231.patch

# workaround
# sql/drivers/tds/qsql_tds.cpp:341:49: warning: dereferencing type-punned pointer will break strict-aliasing rules [-Wstrict-aliasing]
Patch74: qt-everywhere-opensource-src-4.7.4-tds_no_strict_aliasing.patch

# workaround crash on ppc64
Patch75: qt-ppc64-crash.patch

# add missing method for QBasicAtomicPointer on s390(x)
Patch76: qt-everywhere-opensource-src-4.8.0-s390-atomic.patch

# don't spam if libicu is not present at runtime
Patch77:  qt-everywhere-opensource-src-4.8.0-icu_no_spam.patch

# avoid dropping events, which lead to "ghost entries in kde task manager" problem
# https://bugs.kde.org/show_bug.cgi?id=275469
Patch78: qt-everywhere-opensource-src-4.8.0-filter_event.patch

# fix qvfb build
Patch79: qt-everywhere-opensource-src-4.8.0-qvfb.patch

# gcc doesn't support flag -fuse-ld=gold
Patch80: qt-everywhere-opensource-src-4.8.0-ld-gold.patch

# gcc-4.7 build issue
Patch81: qt-everywhere-opensource-src-4.8.0-gcc-4.7.patch

# upstream patches

# security patches
# CVE-2011-3922 qt: Stack-based buffer overflow in embedded harfbuzz code
Patch200: qt-4.8.0-CVE-2011-3922-bz#772125.patch

# desktop files
Source20: assistant.desktop
Source21: designer.desktop
Source22: linguist.desktop
Source23: qtdemo.desktop
Source24: qtconfig.desktop

# upstream qt4-logo, http://trolltech.com/images/products/qt/qt4-logo
Source30: hi128-app-qt4-logo.png
Source31: hi48-app-qt4-logo.png

## BOOTSTRAPPING, undef docs, demos, examples, phonon, webkit

## optional plugin bits
# set to -no-sql-<driver> to disable
# set to -qt-sql-<driver> to enable *in* qt library
%define ibase -plugin-sql-ibase
%define mysql -plugin-sql-mysql
%define odbc -plugin-sql-odbc
%define psql -plugin-sql-psql
%define sqlite -plugin-sql-sqlite
%define tds -plugin-sql-tds

%define phonon -phonon
%define phonon_backend -phonon-backend
%define dbus -dbus-linked
%define graphicssystem -graphicssystem raster
%define gtkstyle -gtkstyle
# FIXME/TODO: use system webkit for assistant, examples/webkit, demos/browser
%define webkit -webkit

# See http://bugzilla.redhat.com/196901
%define _qt4 %{name}
%define _qt4_prefix %{_libdir}/%{name}
%define _qt4_bindir %{_qt4_prefix}/bin
# _qt4_datadir is not multilib clean, and hacks to workaround that breaks stuff.
#define _qt4_datadir %{_datadir}/qt4
%define _qt4_datadir %{_qt4_prefix}
%define _qt4_demosdir %{_qt4_prefix}/demos
%define _qt4_docdir %{_docdir}/%{name}
%define _qt4_examplesdir %{_qt4_prefix}/examples
%define _qt4_headerdir %{_includedir} 
%define _qt4_importdir %{_qt4_prefix}/imports 
%define _qt4_libdir %{_libdir}/%{name}
%define _qt4_plugindir %{_qt4_prefix}/plugins
%define _qt4_sysconfdir %{_qt4_prefix}/etc
%define _qt4_translationdir %{_datadir}/%{name}/translations

BuildRequires: cups-devel
BuildRequires: desktop-file-utils
BuildRequires: findutils
BuildRequires: libjpeg-devel
BuildRequires: libmng-devel
BuildRequires: libtiff-devel
BuildRequires: pkgconfig
BuildRequires: pkgconfig(alsa) 
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: libicu-devel
BuildRequires: pkgconfig(NetworkManager)
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(libpulse)
BuildRequires: pkgconfig(xtst) 
BuildRequires: pkgconfig(zlib)
BuildRequires: rsync

## In theory, should be as simple as:
#define x_deps libGL-devel libGLU-devel
## but, "xorg-x11-devel: missing dep on libGL/libGLU" - http://bugzilla.redhat.com/211898 
%define x_deps pkgconfig(ice) pkgconfig(sm) pkgconfig(xcursor) pkgconfig(xext) pkgconfig(xfixes) pkgconfig(xft) pkgconfig(xi) pkgconfig(xinerama) pkgconfig(xrandr) pkgconfig(xrender) pkgconfig(xt) pkgconfig(xv) pkgconfig(x11) pkgconfig(xproto) pkgconfig(gl) pkgconfig(glu) 
BuildRequires: %{x_deps}

%if "%{?ibase}" != "-no-sql-ibase"
BuildRequires: firebird-devel
%endif

%if "%{?mysql}" != "-no-sql-mysql"
BuildRequires: mysql-devel >= 4.0
%endif

%if "%{?phonon_backend}" == "-phonon-backend"
BuildRequires: pkgconfig(gstreamer-0.10) 
BuildRequires: pkgconfig(gstreamer-plugins-base-0.10) 
%endif

%if "%{?gtkstyle}" == "-gtkstyle"
BuildRequires: pkgconfig(gtk+-2.0) 
%endif

%if "%{?psql}" != "-no-sql-psql"
BuildRequires: postgresql-devel
%endif

%if "%{?odbc}" != "-no-sql-odbc"
BuildRequires: unixODBC-devel
%endif

%if "%{?sqlite}" != "-no-sql-sqlite"
%define _system_sqlite -system-sqlite
BuildRequires: pkgconfig(sqlite3) 
%endif

Obsoletes: %{name}-sqlite < 1:4.7.1-16
Provides:  %{name}-sqlite = %{?epoch:%{epoch}:}%{version}-%{release} 
%{?_isa:Provides: %{name}-sqlite%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}}

%if "%{?tds}" != "-no-sql-tds"
BuildRequires: freetds-devel
%endif

Obsoletes: qgtkstyle < 0.1
Provides:  qgtkstyle = 0.1-1
Requires: ca-certificates

%description 
Qt is a software toolkit for developing applications.

This package contains base tools, like string, xml, and network
handling.

%package assistant
Summary: Documentation browser for Qt 4
Group: Documentation
Requires: %{name}-sqlite%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: qt4-assistant = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-x11%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%description assistant
%{summary}.

%package config
Summary: Graphical configuration tool for programs using Qt 4 
Group: User Interface/Desktops
# -config introduced in 4.7.1-10 , for upgrade path
# seems to tickle a pk bug, https://bugzilla.redhat.com/674326
#Obsoletes: %{name}-x11 < 1:4.7.1-10
#Obsoletes: qt4-config < 4.5.0
#Provides:  qt4-config = %{version}-%{release}
Requires: %{name}-x11%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%description config 
%{summary}.

%define demos 1
%package demos
Summary: Demonstration applications for %{name}
Group:   Documentation
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
%description demos
%{summary}.

%define docs 1
%package doc
Summary: API documentation for %{name}
Group: Documentation
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-assistant
Provides:  qt4-doc = %{?epoch:%{epoch}:}%{version}-%{release}
# help workaround yum bug http://bugzilla.redhat.com/502401
Obsoletes: qt-doc < 1:4.5.1-4
BuildArch: noarch
%description doc
%{summary}.  Includes:
Qt Assistant

%package devel
Summary: Development files for the Qt toolkit
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-x11%{?_isa}
Requires: %{name}-sqlite%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{x_deps}
Requires: pkgconfig
#%if 0%{?phonon:1}
#Provides: qt4-phonon-devel = %{version}-%{release}
#%endif
#Obsoletes: qt4-designer < %{version}-%{release}
#Provides:  qt4-designer = %{version}-%{release}
# as long as libQtUiTools.a is included
Provides:  %{name}-static = %{version}-%{release}
#Obsoletes: qt4-devel < %{version}-%{release}
#Provides:  qt4-devel = %{version}-%{release}
#%{?_isa:Provides: qt4-devel%{?_isa} = %{version}-%{release}}
Provides:  %{name}-static = %{version}-%{release}

%description devel
This package contains the files necessary to develop
applications using the Qt toolkit.  Includes:
Qt Linguist

# make a devel private subpkg or not?
%define private 1
%package devel-private
Summary: Private headers for Qt toolkit 
Group: Development/Libraries
Provides: qt4-devel-private = %{version}-%{release}
Requires: %{name}-devel = %{?epoch:%{epoch}:}%{version}-%{release}
BuildArch: noarch
%description devel-private
%{summary}.

%define examples 1
%package examples
Summary: Programming examples for %{name}
Group: Documentation
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%description examples
%{summary}.

%define qvfb 1
%package qvfb
Summary: Virtual frame buffer for Qt for Embedded Linux
Group: Applications/Emulators
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%description qvfb
%{summary}.

%package ibase
Summary: IBase driver for Qt's SQL classes
Group:  System Environment/Libraries
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:  qt4-ibase = %{version}-%{release}
%{?_isa:Provides: qt4-ibase%{?_isa} = %{version}-%{release}}
%description ibase
%{summary}.

%package mysql
Summary: MySQL driver for Qt's SQL classes
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
#Obsoletes: qt4-MySQL < %{version}-%{release}
#Provides:  qt4-MySQL = %{version}-%{release}
#Obsoletes: qt4-mysql < %{version}-%{release}
#Provides:  qt4-mysql = %{version}-%{release}
#%{?_isa:Provides: qt4-mysql%{?_isa} = %{version}-%{release}}
%description mysql 
%{summary}.

%package odbc 
Summary: ODBC driver for Qt's SQL classes
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
#Obsoletes: qt4-ODBC < %{version}-%{release}
#Provides:  qt4-ODBC = %{version}-%{release}
#Obsoletes: qt4-odbc < %{version}-%{release}
#Provides:  qt4-odbc = %{version}-%{release}
%{?_isa:Provides: qt4-odbc%{?_isa} = %{version}-%{release}}
%description odbc 
%{summary}.

%package postgresql 
Summary: PostgreSQL driver for Qt's SQL classes
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
#Obsoletes: qt4-PostgreSQL < %{version}-%{release}
#Provides:  qt4-PostgreSQL = %{version}-%{release}
#Obsoletes: qt4-postgresql < %{version}-%{release}
#Provides:  qt4-postgresql = %{version}-%{release}
#%{?_isa:Provides: qt4-postgresql%{?_isa} = %{version}-%{release}}
%description postgresql 
%{summary}.

%package tds
Summary: TDS driver for Qt's SQL classes
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: qt4-tds = %{version}-%{release}
%{?_isa:Provides: qt4-tds%{?_isa} = %{version}-%{release}}
%description tds
%{summary}.

%package x11
Summary: Qt GUI-related libraries
Group: System Environment/Libraries
# include Obsoletes here to be safe(r) bootstrap-wise with phonon-4.5.0
# that will Provides: it -- Rex
Obsoletes: qt-designer-plugin-phonon < 1:4.7.2-6
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
#Obsoletes: qt4-x11 < %{version}-%{release}
#Provides:  qt4-x11 = %{version}-%{release}
#%{?_isa:Provides: qt4-x11%{?_isa} = %{version}-%{release}}
%description x11
Qt libraries used for drawing widgets and OpenGL items.


%prep
%setup -q -n qt-everywhere-opensource-src-%{version} 

%patch2 -p1 -b .multilib-optflags
# drop backup file(s), else they get installed too, http://bugzilla.redhat.com/639463
rm -fv mkspecs/linux-g++*/qmake.conf.multilib-optflags
%patch4 -p1 -b .uic_multilib
%patch15 -p1 -b .enable_ft_lcdfilter
%patch23 -p1 -b .glib_eventloop_nullcheck
%patch24 -p1 -b .moc-boost148
## TODO: still worth carrying?  if so, upstream it.
%patch53 -p1 -b .qatomic-inline-asm
## TODO: upstream me
%patch54 -p1 -b .mysql_config
%patch55 -p1 -b .cups-1
%patch64 -p1 -b .QTBUG-14467
%patch65 -p1 -b .qtreeview-kpackagekit-crash
%patch67 -p1 -b .s390
pushd src/3rdparty/webkit
%patch68 -p1 -b .no_Werror
popd
%patch69 -p1 -b .QTBUG-22037
%patch70 -p1 -b .QTBUG-14724
%patch71 -p1 -b .QTBUG-21900
%patch72 -p1 -b .QUrl_toLocalFile
%if 0%{?fedora} > 16
# This quick fix works ONLY with GLib >= 2.31. It's harder to fix this portably.
# See https://bugs.webkit.org/show_bug.cgi?id=69840 for the gory details.
%patch73 -p1 -b .qtwebkit-glib231
%endif
%patch74 -p1 -b .tds_no_strict_aliasing
%patch75 -p1 -b .ppc64-crash
%patch76 -p1 -b .s390-atomic
%patch77 -p1 -b .icu_no_spam
%patch78 -p1 -b .filter_events
%patch79 -p1 -b .qvfb
%patch80 -p1 -b .ld.gold
%patch81 -p1 -b .gcc-4.7

# upstream patches

# security fixes
%patch200 -p1 -b .CVE-2011-3922

# drop -fexceptions from $RPM_OPT_FLAGS
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's|-fexceptions||g'`

%define platform linux-g++

# some 64bit platforms assume -64 suffix, https://bugzilla.redhat.com/569542
%if "%{?__isa_bits}"  == "64"
%define platform linux-g++-64
%endif

# https://bugzilla.redhat.com/478481
%ifarch x86_64
%define platform linux-g++
%endif

sed -i \
  -e "s|-O2|$RPM_OPT_FLAGS|g" \
  -e "s|g++.conf|g++-multilib.conf|g" \
  mkspecs/%{platform}/qmake.conf

# undefine QMAKE_STRIP, so we get useful -debuginfo pkgs
sed -i -e "s|^QMAKE_STRIP.*=.*|QMAKE_STRIP             =|" mkspecs/common/linux.conf 

# set correct lib path
if [ "%{_lib}" == "lib64" ] ; then
  sed -i -e "s,/usr/lib /lib,/usr/%{_lib} /%{_lib},g" config.tests/{unix,x11}/*.test
  sed -i -e "s,/lib /usr/lib,/%{_lib} /usr/%{_lib},g" config.tests/{unix,x11}/*.test
fi

# let makefile create missing .qm files, the .qm files should be included in qt upstream
for f in translations/*.ts ; do
  touch ${f%.ts}.qm
done


%build

# build shared, threaded (default) libraries
./configure -v \
  -confirm-license \
  -opensource \
  -optimized-qmake \
  -prefix %{_qt4_prefix} \
  -bindir %{_qt4_bindir} \
  -datadir %{_qt4_datadir} \
  -demosdir %{_qt4_demosdir} \
  -docdir %{_qt4_docdir} \
  -examplesdir %{_qt4_examplesdir} \
  -headerdir %{_qt4_headerdir} \
  -importdir %{_qt4_importdir} \
  -libdir %{_qt4_libdir} \
  -plugindir %{_qt4_plugindir} \
  -sysconfdir %{_qt4_sysconfdir} \
  -translationdir %{_qt4_translationdir} \
  -platform %{platform} \
  -release \
  -shared \
  -cups \
  -fontconfig \
  -largefile \
  -gtkstyle \
  -no-rpath \
  -reduce-relocations \
  -no-separate-debug-info \
  %{?phonon} %{!?phonon:-no-phonon} \
  %{?phonon_backend} \
  %{?no_pch} \
  %{?no_javascript_jit} \
  -sm \
  -stl \
  -system-libmng \
  -system-libpng \
  -system-libjpeg \
  -system-libtiff \
  -system-zlib \
  -xinput \
  -xcursor \
  -xfixes \
  -xinerama \
  -xshape \
  -xrandr \
  -xrender \
  -xkb \
  -glib \
  -icu \
  -openssl-linked \
  -xmlpatterns \
  %{?dbus} %{!?dbus:-no-dbus} \
  %{?graphicssystem} \
  %{?webkit} %{!?webkit:-no-webkit } \
  %{?ibase} \
  %{?mysql} \
  %{?psql} \
  %{?odbc} \
  %{?sqlite} %{?_system_sqlite} \
  %{?tds} \
  %{!?docs:-nomake docs} \
  %{!?demos:-nomake demos} \
  %{!?examples:-nomake examples}

make %{?_smp_mflags}

# TODO: consider patching tools/tools.pro to enable building this by default
%{?qvfb:make %{?_smp_mflags} -C tools/qvfb}

# recreate .qm files
LD_LIBRARY_PATH=`pwd`/lib bin/lrelease translations/*.ts


%install
rm -rf %{buildroot}

make install INSTALL_ROOT=%{buildroot}

%if 0%{?qvfb}
make install INSTALL_ROOT=%{buildroot} -C tools/qvfb
%find_lang qvfb --with-qt --without-mo
%else
rm -f %{buildroot}%{_qt4_translationdir}/qvfb*.qm
%endif

%if 0%{?private}
# install private headers
# using rsync -R as easy way to preserve relative path names
# we're cheating and using %%_prefix (/usr) directly here
rsync -aR \
  include/Qt{Core,Declarative,Gui,Script}/private \
  src/{corelib,declarative,gui,script}/*/*_p.h \
  %{buildroot}%{_prefix}/
%endif

# Add desktop file(s)
desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  --vendor="qt4" \
  %{SOURCE20} %{SOURCE21} %{SOURCE22} %{?demos:%{SOURCE23}} %{SOURCE24}

## pkg-config
# strip extraneous dirs/libraries 
# safe ones
glib2_libs=$(pkg-config --libs glib-2.0 gobject-2.0 gthread-2.0)
ssl_libs=$(pkg-config --libs openssl)
for dep in \
  -laudio -ldbus-1 -lfreetype -lfontconfig ${glib2_libs} \
  -ljpeg -lm -lmng -lpng -lpulse -lpulse-mainloop-glib ${ssl_libs} -lsqlite3 -lz \
  -L/usr/X11R6/lib -L/usr/X11R6/%{_lib} -L%{_libdir} ; do
  sed -i -e "s|$dep ||g" %{buildroot}%{_qt4_libdir}/lib*.la 
#  sed -i -e "s|$dep ||g" %{buildroot}%{_qt4_libdir}/pkgconfig/*.pc
  sed -i -e "s|$dep ||g" %{buildroot}%{_qt4_libdir}/*.prl
done
# riskier
for dep in -ldl -lphonon -lpthread -lICE -lSM -lX11 -lXcursor -lXext -lXfixes -lXft -lXinerama -lXi -lXrandr -lXrender -lXt ; do
  sed -i -e "s|$dep ||g" %{buildroot}%{_qt4_libdir}/lib*.la 
#  sed -i -e "s|$dep ||g" %{buildroot}%{_qt4_libdir}/pkgconfig/*.pc 
  sed -i -e "s|$dep ||g" %{buildroot}%{_qt4_libdir}/*.prl
done

# nuke dangling reference(s) to %buildroot
sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" %{buildroot}%{_qt4_libdir}/*.prl
sed -i -e "s|-L%{_builddir}/qt-everywhere-opensource-src-%{version}%{?pre:-%{pre}}/lib||g" \
  %{buildroot}%{_qt4_libdir}/pkgconfig/*.pc \
  %{buildroot}%{_qt4_libdir}/*.prl

# nuke QMAKE_PRL_LIBS, seems similar to static linking and .la files (#520323)
# don't nuke, just drop -lphonon (above)
#sed -i -e "s|^QMAKE_PRL_LIBS|#QMAKE_PRL_LIBS|" %{buildroot}%{_qt4_libdir}/*.prl

# .la files, die, die, die.
rm -f %{buildroot}%{_qt4_libdir}/lib*.la

%if 0
#if "%{_qt4_docdir}" != "%{_qt4_prefix}/doc"
# -doc make symbolic link to _qt4_docdir
rm -rf %{buildroot}%{_qt4_prefix}/doc
ln -s  ../../share/doc/%{name} %{buildroot}%{_qt4_prefix}/doc
%endif

# let rpm handle binaries conflicts
mkdir %{buildroot}%{_bindir}
pushd %{buildroot}%{_qt4_bindir}
for i in * ; do
  case "${i}" in
    assistant|designer|linguist|lrelease|lupdate|moc|qmake|qtconfig|qtdemo|uic)
      mv $i ../../../bin/${i}-%{name}
      ln -s ../../../bin/${i}-%{name} .
      ln -s ../../../bin/${i}-%{name} $i
      ;;
    *)
      mv $i ../../../bin/
      ln -s ../../../bin/$i .
      ;;
  esac
done
popd

mv %{buildroot}%{_bindir}/qdbus %{buildroot}%{_bindir}/qdbus-%{name}

# _debug targets (see bug #196513)
pushd %{buildroot}%{_qt4_libdir}
for lib in libQt*.so ; do
   libbase=`basename $lib .so | sed -e 's/^lib//'`
#  ln -s $lib lib${libbase}_debug.so
   echo "INPUT(-l${libbase})" > lib${libbase}_debug.so 
done
for lib in libQt*.a ; do
   libbase=`basename $lib .a | sed -e 's/^lib//' `
#  ln -s $lib lib${libbase}_debug.a
   echo "INPUT(-l${libbase})" > lib${libbase}_debug.a
done
popd

%ifarch %{multilib_archs}
# multilib: qconfig.h
  mv %{buildroot}%{_qt4_headerdir}/Qt/qconfig.h %{buildroot}%{_qt4_headerdir}/QtCore/qconfig-%{_arch}.h
  install -p -m644 -D %{SOURCE5} %{buildroot}%{_qt4_headerdir}/QtCore/qconfig-multilib.h
  ln -sf qconfig-multilib.h %{buildroot}%{_qt4_headerdir}/QtCore/qconfig.h
  ln -sf ../QtCore/qconfig.h %{buildroot}%{_qt4_headerdir}/Qt/qconfig.h
%endif

%if "%{_qt4_libdir}" != "%{_libdir}"
  mkdir -p %{buildroot}/etc/ld.so.conf.d
  echo "%{_qt4_libdir}" > %{buildroot}/etc/ld.so.conf.d/0_%{name}-%{_arch}.conf
%endif

# Trolltech.conf
install -p -m644 -D %{SOURCE4} %{buildroot}%{_qt4_sysconfdir}/Trolltech.conf

# qt4-logo (generic) icons
install -p -m644 -D %{SOURCE30} %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}-logo.png
install -p -m644 -D %{SOURCE31} %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}-logo.png
# assistant icons
install -p -m644 -D tools/assistant/tools/assistant/images/assistant.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/assistant48.png
install -p -m644 -D tools/assistant/tools/assistant/images/assistant-128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/assistant48.png
# designer icons
install -p -m644 -D tools/designer/src/designer/images/designer.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/designer48.png
# linguist icons
for icon in tools/linguist/linguist/images/icons/linguist-*-32.png ; do
  size=$(echo $(basename ${icon}) | cut -d- -f2)
  install -p -m644 -D ${icon} %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/linguist48.png
done

# Qt.pc
cat >%{buildroot}%{_qt4_libdir}/pkgconfig/Qt.pc<<EOF
prefix=%{_qt4_prefix}
bindir=%{_qt4_bindir}
datadir=%{_qt4_datadir}
demosdir=%{_qt4_demosdir}
docdir=%{_qt4_docdir}
examplesdir=%{_qt4_examplesdir}
headerdir=%{_qt4_headerdir}
importdir=%{_qt4_importdir}
libdir=%{_qt4_libdir}
moc=%{_qt4_bindir}/moc
plugindir=%{_qt4_plugindir}
qmake=%{_qt4_bindir}/qmake
sysconfdir=%{_qt4_sysconfdir}
translationdir=%{_qt4_translationdir}

Name: Qt
Description: Qt Configuration
Version: %{version}
EOF

%if "%{_qt4_libdir}" != "%{_libdir}"
  mkdir -p %{buildroot}%{_libdir}
  mv %{buildroot}%{_qt4_libdir}/pkgconfig %{buildroot}%{_libdir}/
%endif

# rpm macros
mkdir -p %{buildroot}%{_sysconfdir}/rpm
cat >%{buildroot}%{_sysconfdir}/rpm/macros.qt48<<EOF
%%_qt4 %{name}
%%_qt48 %{version}
%%_qt4_epoch %{epoch}
%%_qt4_version %{version}
%%_qt4_evr %{epoch}:%{version}-%{release}
%%_qt4_prefix %%{_libdir}/qt48
%%_qt4_bindir %%{_qt4_prefix}/bin
%%_qt4_datadir %%{_qt4_prefix}
%%_qt4_demosdir %%{_qt4_prefix}/demos
%%_qt4_docdir %%{_docdir}/qt48
%%_qt4_examples %%{_qt4_prefix}/examples
%%_qt4_headerdir %%{_includedir}
%%_qt4_importdir %%{_qt4_prefix}/imports
%%_qt4_libdir %%{_libdir}/%{name}
%%_qt4_plugindir %%{_qt4_prefix}/plugins
%%_qt4_qmake %%{_qt4_bindir}/qmake
%%_qt4_sysconfdir %%{_sysconfdir}
%%_qt4_translationdir %%{_datadir}/qt48/translations 
EOF

# create/own stuff under %%_qt4_plugindir
mkdir %{buildroot}%{_qt4_plugindir}/crypto
mkdir %{buildroot}%{_qt4_plugindir}/gui_platform
mkdir %{buildroot}%{_qt4_plugindir}/styles

## nuke bundled phonon bits
rm -fv  %{buildroot}%{_qt4_libdir}/libphonon.so*
rm -rfv %{buildroot}%{_libdir}/pkgconfig/phonon.pc
# contents slightly different between phonon-4.3.1 and qt-4.5.0
rm -fv  %{buildroot}%{_includedir}/phonon/phononnamespace.h
# contents dup'd but should remove just in case
rm -fv  %{buildroot}%{_includedir}/phonon/*.h
rm -rfv %{buildroot}%{_qt4_headerdir}/phonon*
#rm -rfv %{buildroot}%{_qt4_headerdir}/Qt/phonon*
rm -fv %{buildroot}%{_datadir}/dbus-1/interfaces/org.kde.Phonon.AudioOutput.xml
rm -fv %{buildroot}%{_qt4_plugindir}/designer/libphononwidgets.so
# backend
rm -fv %{buildroot}%{_qt4_plugindir}/phonon_backend/*_gstreamer.so
rm -fv %{buildroot}%{_datadir}/kde4/services/phononbackends/gstreamer.desktop
# nuke bundled webkit bits 
rm -fv %{buildroot}%{_qt4_datadir}/mkspecs/modules/qt_webkit_version.pri
rm -fv %{buildroot}%{_qt4_headerdir}/Qt/qgraphicswebview.h
rm -fv %{buildroot}%{_qt4_headerdir}/Qt/qweb*.h
rm -frv %{buildroot}%{_qt4_headerdir}/QtWebKit/
rm -frv %{buildroot}%{_qt4_importdir}/QtWebKit/
rm -fv %{buildroot}%{_qt4_libdir}/libQtWebKit.*
rm -fv %{buildroot}%{_qt4_plugindir}/designer/libqwebview.so
rm -fv %{buildroot}%{_libdir}/pkgconfig/QtWebKit.pc
rm -frv %{buildroot}%{_qt4_prefix}/tests/

%find_lang qt --with-qt --without-mo

%find_lang assistant --with-qt --without-mo
%find_lang qt_help --with-qt --without-mo
%find_lang qtconfig --with-qt --without-mo
cat assistant.lang qt_help.lang qtconfig.lang >qt-x11.lang

%find_lang designer --with-qt --without-mo
%find_lang linguist --with-qt --without-mo
cat designer.lang linguist.lang >qt-devel.lang

mv %{buildroot}%{_datadir}/applications/qt4-qtconfig.desktop \
	%{buildroot}%{_datadir}/applications/qt48-qtconfig.desktop

mv %{buildroot}%{_bindir}/qdbusviewer \
	%{buildroot}%{_bindir}/qdbusviewer-qt48


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post assistant
touch --no-create %{_datadir}/icons/hicolor ||:

%posttrans assistant 
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:

%postun assistant 
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
fi

%post devel
touch --no-create %{_datadir}/icons/hicolor ||:

%posttrans devel
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:

%postun devel
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
fi

%post x11
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor ||:

%posttrans x11
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:

%postun x11
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
fi

%files -f qt.lang
%defattr(-,root,root,-)
%doc README LICENSE.GPL3 LICENSE.LGPL LGPL_EXCEPTION.txt
%if "%{_qt4_libdir}" != "%{_libdir}"
/etc/ld.so.conf.d/*
%dir %{_qt4_libdir}
%endif
%dir %{_qt4_prefix}
%if "%{_qt4_bindir}" == "%{_bindir}"
%{_qt4_prefix}/bin
%else
%dir %{_qt4_bindir}
%endif
%if "%{_qt4_datadir}" != "%{_datadir}/qt48"
%dir %{_datadir}/qt48
%else
%dir %{_qt4_datadir}
%endif
%dir %{_qt4_docdir}
%dir %{_qt4_docdir}/html/
%dir %{_qt4_docdir}/qch/
%dir %{_qt4_docdir}/src/

%if "%{_qt4_sysconfdir}" != "%{_sysconfdir}"
%dir %{_qt4_sysconfdir}
%endif
%config(noreplace) %{_qt4_sysconfdir}/Trolltech.conf
%{_qt4_datadir}/phrasebooks/
%{_qt4_libdir}/libQtCore.so.4*
%if 0%{?dbus:1}
%if "%{_qt4_bindir}" != "%{_bindir}"
%{_bindir}/qdbus-%{name}
%endif
%{_qt4_bindir}/qdbus
%{_qt4_libdir}/libQtDBus.so.4*
%endif
%{_qt4_libdir}/libQtNetwork.so.4*
%{_qt4_libdir}/libQtScript.so.4*
%{_qt4_libdir}/libQtSql.so.4*
%{_qt4_libdir}/libQtTest.so.4*
%{_qt4_libdir}/libQtXml.so.4*
%{_qt4_libdir}/libQtXmlPatterns.so.4*
%dir %{_qt4_plugindir}
%dir %{_qt4_plugindir}/crypto/
%dir %{_qt4_plugindir}/sqldrivers/
%dir %{_qt4_translationdir}/
%{_qt4_plugindir}/sqldrivers/libqsqlite*

%files assistant
%defattr(-,root,root,-)
%if "%{_qt4_bindir}" != "%{_bindir}"
%{_bindir}/assistant*
%endif
%{_qt4_bindir}/assistant*
%{_datadir}/applications/*assistant.desktop
%{_datadir}/icons/hicolor/*/apps/assistant*

%files config
%defattr(-,root,root,-)
%if "%{_qt4_bindir}" != "%{_bindir}"
%{_bindir}/qt*config*
%endif
%{_qt4_bindir}/qt*config*
%{_datadir}/applications/*qtconfig.desktop

%if 0%{?demos}
%files demos
%defattr(-,root,root,-)
%{_qt4_bindir}/qt*demo*
%if "%{_qt4_bindir}" != "%{_bindir}"
%{_bindir}/qt*demo*
%endif
%{_datadir}/applications/*qtdemo.desktop
%{_qt4_demosdir}/
%endif

%files devel -f qt-devel.lang
%defattr(-,root,root,-)
%{_sysconfdir}/rpm/macros.*
%{_qt4_bindir}/lconvert
%{_qt4_bindir}/lrelease*
%{_qt4_bindir}/lupdate*
%{_qt4_bindir}/moc*
%{_qt4_bindir}/pixeltool*
%{_qt4_bindir}/qdoc3*
%{_qt4_bindir}/qmake*
%{_qt4_bindir}/qmlplugindump
%{_qt4_bindir}/qt3to4
%{_qt4_bindir}/qttracereplay
%{_qt4_bindir}/rcc*
%{_qt4_bindir}/uic*
%{_qt4_bindir}/qcollectiongenerator
%if 0%{?dbus:1}
%{_qt4_bindir}/qdbuscpp2xml
%{_qt4_bindir}/qdbusxml2cpp
%endif
%{_qt4_bindir}/qhelpconverter
%{_qt4_bindir}/qhelpgenerator
%{_qt4_bindir}/xmlpatterns
%{_qt4_bindir}/xmlpatternsvalidator
%if "%{_qt4_bindir}" != "%{_bindir}"
%{_bindir}/lconvert
%{_bindir}/lrelease*
%{_bindir}/lupdate*
%{_bindir}/pixeltool*
%{_bindir}/moc*
%{_bindir}/qdoc3
%{_bindir}/qmake*
%{_bindir}/qt3to4
%{_bindir}/qttracereplay
%{_bindir}/rcc*
%{_bindir}/uic*
%{_bindir}/designer*
%{_bindir}/linguist*
%{_bindir}/qcollectiongenerator
%if 0%{?dbus:1}
%{_bindir}/qdbuscpp2xml
%{_bindir}/qdbusxml2cpp
%endif
%{_bindir}/qhelpconverter
%{_bindir}/qhelpgenerator
%{_bindir}/qmlplugindump
%{_bindir}/xmlpatterns
%{_bindir}/xmlpatternsvalidator
%endif
%if "%{_qt4_headerdir}" != "%{_includedir}"
%dir %{_qt4_headerdir}/
%endif
%{_qt4_headerdir}/*
%{_qt4_datadir}/mkspecs/
%if "%{_qt4_datadir}" != "%{_qt4_prefix}"
%{_qt4_prefix}/mkspecs/
%endif
%{_qt4_datadir}/q3porting.xml
%if 0%{?phonon:1}
## nuke this one too?  -- Rex
%{_qt4_libdir}/libphonon.prl
%endif
%{_qt4_libdir}/libQt*.so
%{_qt4_libdir}/libQtUiTools*.a
%{_qt4_libdir}/libQt*.prl
%{_libdir}/pkgconfig/*.pc
# Qt designer
%{_qt4_bindir}/designer*
%{_datadir}/applications/*designer.desktop
%{_datadir}/icons/hicolor/*/apps/designer*
%{?docs:%{_qt4_docdir}/qch/designer.qch}
# Qt Linguist
%{_qt4_bindir}/linguist*
%{_datadir}/applications/*linguist.desktop
%{_datadir}/icons/hicolor/*/apps/linguist*
%{?docs:%{_qt4_docdir}/qch/linguist.qch}
%if 0%{?private}
%exclude %{_qt4_headerdir}/*/private/

%files devel-private
%defattr(-,root,root,-)
%{_qt4_headerdir}/QtCore/private/
%{_qt4_headerdir}/QtDeclarative/private/
%{_qt4_headerdir}/QtGui/private/
%{_qt4_headerdir}/QtScript/private/
%{_qt4_headerdir}/../src/corelib/
%{_qt4_headerdir}/../src/declarative/
%{_qt4_headerdir}/../src/gui/
%{_qt4_headerdir}/../src/script/
%endif

%if 0%{?docs}
%files doc
%defattr(-,root,root,-)
%{_qt4_docdir}/html/*
%{_qt4_docdir}/qch/*.qch
%exclude %{_qt4_docdir}/qch/designer.qch
%exclude %{_qt4_docdir}/qch/linguist.qch
%{_qt4_docdir}/src/*
#{_qt4_prefix}/doc
%endif

%if 0%{?examples}
%files examples
%defattr(-,root,root,-)
%{_qt4_examplesdir}/
%endif

%if 0%{?qvfb}
%files qvfb -f qvfb.lang
%defattr(-,root,root,-)
%{_bindir}/qvfb
%{_qt4_bindir}/qvfb
%endif

%if "%{?ibase}" == "-plugin-sql-ibase"
%files ibase
%defattr(-,root,root,-)
%{_qt4_plugindir}/sqldrivers/libqsqlibase*
%endif

%if "%{?mysql}" == "-plugin-sql-mysql"
%files mysql
%defattr(-,root,root,-)
%{_qt4_plugindir}/sqldrivers/libqsqlmysql*
%endif

%if "%{?odbc}" == "-plugin-sql-odbc"
%files odbc 
%defattr(-,root,root,-)
%{_qt4_plugindir}/sqldrivers/libqsqlodbc*
%endif

%if "%{?psql}" == "-plugin-sql-psql"
%files postgresql 
%defattr(-,root,root,-)
%{_qt4_plugindir}/sqldrivers/libqsqlpsql*
%endif

%if "%{?tds}" == "-plugin-sql-tds"
%files tds
%defattr(-,root,root,-)
%{_qt4_plugindir}/sqldrivers/libqsqltds*
%endif

%files x11 -f qt-x11.lang
%defattr(-,root,root,-)
%dir %{_qt4_importdir}/
%{_qt4_importdir}/Qt/
%{_qt4_libdir}/libQt3Support.so.4*
%{_qt4_libdir}/libQtCLucene.so.4*
%{_qt4_libdir}/libQtDesigner.so.4*
%{_qt4_libdir}/libQtDeclarative.so.4*
%{_qt4_libdir}/libQtDesignerComponents.so.4*
%{_qt4_libdir}/libQtGui.so.4*
%{_qt4_libdir}/libQtHelp.so.4*
%{_qt4_libdir}/libQtMultimedia.so.4*
%{_qt4_libdir}/libQtOpenGL.so.4*
%{_qt4_libdir}/libQtScriptTools.so.4*
%{_qt4_libdir}/libQtSvg.so.4*
%{_qt4_plugindir}/*
%exclude %{_qt4_plugindir}/crypto
%exclude %{_qt4_plugindir}/sqldrivers
%if "%{_qt4_bindir}" != "%{_bindir}"
%{?dbus:%{_bindir}/qdbusviewer*}
%{_bindir}/qmlviewer
%endif
%{?dbus:%{_qt4_bindir}/qdbusviewer*}
%{_qt4_bindir}/qmlviewer
%{_datadir}/icons/hicolor/*/apps/%{name}-logo.*


%changelog
* Wed Mar 21 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 1:4.8.0-10.1.R
- drop some Provides and Obsoletes

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.8.0-10
- Rebuilt for c++ ABI breakage

* Mon Feb 20 2012 Than Ngo <than@redhat.com> - 4.8.0-9
- get rid of timestamp which causes multilib problem

* Tue Jan 24 2012 Than Ngo <than@redhat.com> - 4.8.0-8
- disable Using gold linker, g++ doesn't support flags gold linker
- fix gcc-4.7 issue

* Tue Jan 10 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-7
- improved filter_event patch (kde#275469)

* Mon Jan 09 2012 Than Ngo <than@redhat.com> - 4.8.0-6
- bz#772128, CVE-2011-3922, Stack-based buffer overflow in embedded harfbuzz code

* Tue Dec 27 2011 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-5
- fix qvfb 

* Tue Dec 27 2011 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-4
- filter event patch, avoid "ghost entries in kde taskbar" problem (kde#275469)

* Tue Dec 20 2011 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-3
- don't spam if libicu is not present at runtime (#759923)

* Mon Dec 19 2011 Dan Horák <dan[at]dannu.cz> 4.8.0-2
- add missing method for QBasicAtomicPointer on s390(x)

* Thu Dec 15 2011 Jaroslav Reznik <jreznik@redhat.com> 4.8.0-1
- 4.8.0

* Mon Dec 12 2011 Jaroslav Reznik <jreznik@redhat.com> 4.8.0-0.29.rc1
- Fixes the position of misplaced mouse input (QTBUG-22420)

* Sun Dec 04 2011 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-0.28.rc1
- Control whether icu support is built (#759923)

* Sat Dec 03 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.8.0-0.27.rc1
- work around a MOC issue with Boost 1.48 headers (#756395)

* Wed Nov 30 2011 Than Ngo <than@redhat.com> - 4.8.0-0.26.rc1
- workaround crash on ppc64

* Mon Nov 14 2011 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-0.25.rc1
- BuildRequires: pkgconfig(libpng)
- -devel: drop Requires: libpng-devel libjpeg-devel 
- qt4.macros: +%%_qt4_epoch, %%_qt4_evr

* Thu Nov 03 2011 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-0.24.rc1
- build tds sql driver with -fno-strict-aliasing 

* Fri Oct 28 2011 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-0.23.rc1
- crash when using a visual with 24 bits per pixel (#749647,QTBUG-21754)

* Fri Oct 28 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.8.0-0.22.rc1
- fix FTBFS in QtWebKit's wtf library with GLib 2.31

* Thu Oct 27 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.8.0-0.21.rc1
- fix missing NULL check in the toLocalFile patch (fixes Digikam segfault)

* Thu Oct 27 2011 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-0.20.rc1
- restore qt-4.7-compatible behavior to QUrl.toLocalFile (#749213)

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.8.0-0.19.rc1
- Rebuilt for glibc bug#747377

* Mon Oct 24 2011 Than Ngo <than@redhat.com> 4.8.0-0.18.rc1
- bz#748297, update the URL of qt packages

* Tue Oct 18 2011 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-0.17.rc1
- Buttons in Qt applications not clickable when run under gnome-shell (#742658, QTBUG-21900)

* Mon Oct 17 2011 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-0.16.rc1
- Qt doesn't close orphaned file descriptors after printing (#746601, QTBUG-14724)

* Sat Oct 15 2011 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-0.15.rc1
- revert qlist.h commit that seems to induce crashes in qDeleteAll<QList... (QTBUG-22037)

* Sat Oct 15 2011 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-0.14.rc1
- pkgconfig-style deps

* Thu Oct 13 2011 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-0.13.rc1
- 4.8.0-rc1

* Mon Oct 03 2011 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-0.12.20111002
- 20111002 4.8 branch snapshot

* Sat Sep 17 2011 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-0.11.beta1
- ./configure -webkit

* Wed Sep 14 2011 Lukas Tinkl <ltinkl@redhat.com> 1:4.8.0-0.10.beta1
- fix missing CSS styles and JS functions in the generated HTML
  documentation, omitted from the upstream tarball

* Wed Aug 17 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.0-0.9.beta1
- -graphicssystem raster (#712617)
- drop sqlite_pkg option

* Sun Jul 31 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.0-0.8.beta1
- macros.qt4: s|_qt47|_qt48|

* Thu Jul 28 2011 Dan Horák <dan[at]danny.cz> 1:4.8.0-0.7.beta1
- fix the outdated standalone copy of JavaScriptCore (s390)

* Sat Jul 23 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.0-0.6.beta1
- fix QMAKE_LIBDIR_QT, for missing QT_SHARED define (#725183)

* Wed Jul 20 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.0-0.5.beta1
- 4.8.0-beta1
- drop webkit_packaged conditional
- drop old patches
- drop qvfb (for now, ftbfs)

* Wed Jul 13 2011 Than Ngo <than@redhat.com> - 1:4.8.0-0.4.tp
- move macros.* to -devel

* Tue Jul 05 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.0-0.3.tp
- Adding qt-sql-ibase driver for qt (#719002) 
- qvfb subpackage (#718416)

* Tue Jun 21 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.0-0.2.tp
- fontconfig patch (#705348, QTBUG-19947)

* Wed May 25 2011 Jaroslav Reznik <jreznik@redhat.com> 1:4.8.0-0.1.tp
- 4.8.0-tp
- drop phonon_internal, phonon_backend_packaged build options

* Thu May 19 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.7.3-3
- omit %%{_qt4_plugindir}/designer/libqwebview.so too

* Thu May 19 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.7.3-2
- omit bundled webkit on f16+ (in favor of separately packaged qtwebkit)

* Thu May 05 2011 Jaroslav Reznik <jreznik@redhat.com> 1:4.7.3-1
- 4.7.3

* Thu Apr 21 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.7.2-9
- -webkit-devel: move qt_webkit_version.pri here

* Fri Apr 01 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.7.2-8
- -devel-private: qt-creator/QmlDesigner requires qt private headers (#657498)

* Fri Mar 25 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.7.2-7
- followup patch for QTBUG-18338, blacklist fraudulent SSL certifcates

* Fri Mar 25 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.7.2-6
- drop qt-designer-plugin-phonon

* Fri Mar 25 2011 Than Ngo <than@redhat.com> - 1:4.7.2-5
- apply patch to fix QTBUG-18338, blacklist fraudulent SSL certifcates

* Tue Mar 22 2011 Jaroslav Reznik <jreznik@redhat.com> 1:4.7.2-4
- rebuild (mysql)

* Fri Mar 11 2011 Dan Horák <dan[at]danny.cz> 1:4.7.2-3
- workaround memory exhaustion during linking of libQtWebKit on s390

* Mon Mar 07 2011 Jaroslav Reznik <jreznik@redhat.com> 1:4.7.2-2
- Fix QNetworkConfigurationManager crash due to null private pointer (#682656)

* Tue Mar 01 2011 Jaroslav Reznik <jreznik@redhat.com> 1:4.7.2-1
- 4.7.2

* Wed Feb 23 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.7.1-18
- libQtWebKit.so has no debug info (#667175)

* Wed Feb 16 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.7.1-17
- Obsoletes: qt-sqlite < 1:4.7.1-16

* Tue Feb 15 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.7.1-16
- drop -sqlite subpkg, move into main (#677418) 

* Wed Feb 09 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.7.1-15
- -assistant subpkg (#660287)
- -config drop Obsoletes: qt-x11 (avoid/workaround #674326)
- -config unconditionally drop NoDisplay (since we're dropping the Obsoletes too)
- -designer-plugin-phonon subpkg (#672088)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.7.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.1-13
- -config: fix Obsoletes for real this time

* Wed Jan 26 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.1-12
- fix qt-config related Obsoletes/Provides

* Wed Jan 26 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.1-11
- upstream fix for QTextCursor regression (QTBUG-15857, kde#249373)

* Tue Jan 25 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.1-10
- -config subpkg
- qt-x11 pulls in phonon (#672088)
- qtconfig.desktop: drop NoDisplay (f15+ only, for now)

* Thu Jan 20 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.1-9.1
- apply the Assistant QtWebKit dependency removal (#660287) everywhere

* Thu Jan 06 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.1-9
- qsortfilterproxymodel fix (merge_request/934)

* Tue Jan 04 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.1-8
- only do Requires: phonon-backend if using qt's phonon

* Fri Dec 24 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.7.1-7
- fix QTreeView crash triggered by KPackageKit (patch by David Faure)

* Fri Dec 24 2010 Rex Dieter <rdieter@fedoraproject.org> 4.7.1-6
- rebuild (mysql)

* Wed Dec 08 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.7.1-5
- make the Assistant QtWebKit dependency removal (#660287) F15+ only for now
- fix QTextCursor crash in Lokalize and Psi (QTBUG-15857, kde#249373, #660028)
- add some more NULL checks to the glib_eventloop_nullcheck patch (#622164)

* Mon Dec 06 2010 Than Ngo <than@redhat.com> 4.7.1-4
- bz#660287, using QTextBrowser in assistant to drop qtwebkit dependency

* Tue Nov 23 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.1-3
- Fails to create debug build of Qt projects on mingw (#653674, QTBUG-14467)

* Mon Nov 22 2010 Than Ngo <than@redhat.com> - 4.7.1-2
- bz#528303, Reordering of Malayalam Rakar not working properly

* Thu Nov 11 2010 Than Ngo <than@redhat.com> - 4.7.1-1
- 4.7.1

* Mon Oct 25 2010 Jaroslav Reznik <jreznik@redhat.com> - 4.7.0-8
- QtWebKit, CVE-2010-1822: crash by processing certain SVG images (#640290)

* Mon Oct 18 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-7
- qt-devel contains residues from patch run (#639463)

* Fri Oct 15 2010 Than Ngo <than@redhat.com> - 4.7.0-6
- apply patch to fix the color issue in 24bit mode (cirrus driver)

* Thu Sep 30 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-5
- Wrong Cursor when widget become native on X11 (QTBUG-6185)

* Mon Sep 27 2010 Than Ngo <than@redhat.com> - 4.7.0-4
- apply upstream patch to fix QTreeView-regression (QTBUG-13567)

* Thu Sep 23 2010 Than Ngo <than@redhat.com> - 4.7.0-3
- fix typo in license

* Thu Sep 23 2010 Than Ngo <than@redhat.com> - 4.7.0-2
- fix bz#562049, bn-IN Incorrect rendering
- fix bz#562058, bn_IN init feature is not applied properly
- fix bz#631732, indic invalid syllable's are not recognized properly
- fix bz#636399, oriya script open type features are not applied properly

* Tue Sep 21 2010 Than Ngo <than@redhat.com> - 4.7.0-1
- 4.7.0

* Thu Sep 09 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-0.31.rc1
- -webkit-devel: add missing %%defattr
- -webkit: move qml/webkit bits here

* Wed Sep 08 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-0.30.rc1
- Crash in drawPixmap in Qt 4.7rc1 (#631845, QTBUG-12826)

* Mon Aug 30 2010 Than Ngo <than@redhat.com> - 4.7.0-0.29.rc1
- drop the patch, it's already fixed in upstream

* Thu Aug 26 2010 Than Ngo <than@redhat.com> - 4.7.0-0.28.rc1
- 4.7.0 rc1

* Thu Jul 08 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-0.26.beta2
- rebase patches, avoiding use of patch fuzz
- omit old qt-copy/kde-qt patches, pending review
- omit kde4_plugin patch
- ftbfs:s/qml/qmlviewer, libQtMediaServices no longer included

* Thu Jul 08 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-0.25.beta2
- 4.7.0-beta2

* Tue Jul 01 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-0.24.beta1
- X11Embed broken (rh#609757, QTBUG-10809)

* Tue Jul 01 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.7.0-0.23.beta1
- use find_lang to package the qm files (#609749)
- put the qm files into the correct subpackages
- remove qvfb translations, we don't ship qvfb

* Tue Jun 29 2010 Rex Dieter <rdieter@fedoraproject.org. 4.7.0-0.22.beta1
- workaround glib_eventloop crasher induced by gdal/grass (bug #498111)

* Fri Jun 20 2010 Rex Dieter <rdieter@fedoraproject.org> 4.7.0-0.20.beta1
- avoid timestamps in uic-generated files to be multilib-friendly

* Fri Jun 18 2010 Rex Dieter <rdieter@fedoraproject.org> 4.7.0-0.19.beta1
- revert -no-javascript-jit change, false-alarm (#604003)
- QtWebKit does not search correct plugin path(s) (#568860)
- QtWebKit browsers crash with flash-plugin (rh#605677,webkit#40567)
- drop qt-x11-opensource-src-4.5.0-gcc_hack.patch

* Wed Jun 16 2010 Rex Dieter <rdieter@fedoraproject.org> 4.7.0-0.18.beta1
- -no-javascript-jit on i686 (#604003)

* Wed Jun 16 2010 Karsten Hopp <karsten@redhat.com> 4.7.0-0.17.beta1 
- add s390 and s390x to 3rdparty/webkit/JavaScriptCore/wtf/Platform.h and
  3rdparty/javascriptcore/JavaScriptCore/wtf/Platform.h

* Fri Jun 11 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-0.16.beta1
- scrub -lpulse-mainloop-glib from .prl files (#599844)
- scrub references to %%buildroot in .pc, .prl files

* Thu May 27 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-0.15.beta1
- Unsafe use of rand() in X11 (QTBUG-9793)

* Fri May 21 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-0.14.beta1
- drop -no-javascript-jit (webkit#35154)

* Mon May 17 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-0.13.beta1
- QT_GRAPHICSSYSTEM env support

* Sun May 16 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-0.12.beta1
- -webkit-devel: move Qt/qweb*.h here (#592680)

* Fri May 07 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-0.11.beta1
- -webkit-devel: Obsoletes: qt-devel ... (upgrade path)

* Thu May 06 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-0.10.beta1
- -webkit-devel: Provides: qt4-webkit-devel , Requires: %%name-devel

* Thu May 06 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-0.9.beta1
- 4.7.0-beta1
- -webkit-devel : it lives! brainz!

* Fri Apr 30 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-0.8.tp
- prepping for separate QtWebKit(-2.0)
- -webkit subpkg,  Provides: QtWebKit ...
- -devel: Provides: QtWebKit-devel ...
- TODO: -webkit-devel (and see what breaks)

* Wed Apr 28 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-0.7.tp
- own %%{_qt4_plugindir}/crypto

* Sat Apr 03 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.7.0-0.6.tp
- backport fix for QTBUG-9354 which breaks kdeutils build

* Fri Apr 02 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-0.5.tp
- Associate text/vnd.trolltech.linguist with linguist (#579082)

* Tue Mar 23 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 4.7.0-0.4.tp
- fix type cast issue on sparc64

* Sun Mar 21 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.7.0-0.3.tp
- also strip -lpulse from .prl files (fixes PyQt4 QtMultimedia binding build)

* Tue Mar 16 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.7.0-0.2.tp
- qt-4.7.0-tp
- macros.qt4 : +%%_qt4_importdir
- don't strip libs from pkgconfig files, Libs.private is now used properly
- add -lphonon to stripped libs instead of brutally hacking out
  QMAKE_PRL_LIBS altogether (#520323)
- qt-assistant-adp packaged separately now, not included here

* Sat Mar 13 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.6.2-7
- BR alsa-lib-devel (for QtMultimedia)

* Sat Mar 13 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.6.2-6
- Provides: qt-assistant-adp(-devel)

* Fri Mar 05 2010 Than Ngo <than@redhat.com> - 4.6.2-5
- Make tablet detection work with new wacom drivers (#569132)

* Mon Mar 01 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.6.2-4
- fix 64bit platform logic, use linux-g++-64 everywhere except x86_64 (#569542)

* Sun Feb 28 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.6.2-3
- fix CUPS patch not to crash if currentPPD is NULL (#566304)

* Tue Feb 16 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.6.2-2
- macros.qt4: s/qt45/qt46/

* Mon Feb 15 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.6.2-1
- 4.6.2

* Fri Feb 05 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.6.1-3
- improve cups support (#523846, kde#180051#c22)

* Tue Jan 19 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.6.1-2
- drop bitmap_font_speed patch, rejected upstream

* Tue Jan 19 2010 Than Ngo <than@redhat.com> - 4.6.1-1
- 4.6.1

* Mon Jan 11 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.6.0-5
- bitmap_font_speed patch (QTBUG-7255)

* Sat Jan 09 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.6.0-4
- Fix crash when QGraphicsItem destructor deletes other QGraphicsItem (kde-qt cec34b01)
- Fix a crash in KDE/Plasma with QGraphicsView. TopLevel list of items (kde-qt 63839f0c)

* Wed Dec 23 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.6.0-3
- disable QtWebKit JavaScript JIT again, incompatible with SELinux (#549994)

* Sat Dec 05 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.6.0-2
- own %%{_qt4_plugindir}/gui_platform

* Tue Dec 01 2009 Than Ngo <than@redhat.com> - 4.6.0-1
- 4.6.0

* Tue Nov 17 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.6.0-0.6.rc1
- qt-4.6.0-rc1

* Sat Nov 14 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.6.0-0.5.beta1 
- -tds: Add package with TDS sqldriver (#537586)
- add arch'd provides for sql drivers

* Sun Nov 08 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.6.0-0.4.beta1
- -x11: Requires: %%{name}-sqlite%{?_isa}

* Mon Oct 26 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.6.0-0.3.beta1
- kde-qt patches (as of 20091026)

* Fri Oct 16 2009 Than Ngo <than@redhat.com> - 4.6.0-0.2.beta1 
- subpackage sqlite plugin, add Require on qt-sqlite in qt-x11
  for assistant
- build/install qdoc3 again

* Wed Oct 14 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.6.0-0.1.beta1
- qt-4.6.0-beta1
- no kde-qt patches (yet)

* Sat Oct 10 2009 Than Ngo <than@redhat.com> - 4.5.3-4
- fix translation build issue
- rhel cleanup

* Tue Oct 06 2009 Jaroslav Reznik <jreznik@redhat.com> - 4.5.3-3
- disable JavaScriptCore JIT, SE Linux crashes (#527079)

* Fri Oct 02 2009 Than Ngo <than@redhat.com> - 4.5.3-2
- cleanup patches
- if ! phonon_internal, exclude more/all phonon headers
- qt-devel must Requires: phonon-devel (#520323)

* Thu Oct 01 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.3-1
- qt-4.5.3

* Tue Sep 29 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.2-21
- switch to external/kde phonon

* Mon Sep 28 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.2-20
- use internal Qt Assistant/Designer icons
- -devel: move designer.qch,linguist.qch here
- move ownership of %%_qt4_docdir, %%_qt4_docdir/qch to main pkg

* Sun Sep 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.2-19
- Missing Qt Designer icon (#476605)

* Fri Sep 11 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.2-18
- drop gcc -fno-var-tracking-assignments hack (#522576)

* Fri Sep 11 2009 Than Ngo <than@redhat.com> - 4.5.2-17
- drop useless check for ossl patch, the patch works fine with old ossl

* Wed Sep 09 2009 Than Ngo <than@redhat.com> - 4.5.2-16
- add a correct system_ca_certificates patch

* Tue Sep 08 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.2-15
- use system ca-certificates (#521911)

* Tue Sep 01 2009 Than Ngo <than@redhat.com> - 4.5.2-14
- drop fedora < 9 support
- only apply ossl patch for fedora > 11

* Mon Aug 31 2009 Than Ngo <than@redhat.com> - 4.5.2-13
- fix for CVE-2009-2700

* Thu Aug 27 2009 Rex Dieter <rdieter@fedoraproject.org> 4.5.2-12
- use platform linux-g++ everywhere (ie, drop linux-g++-64 on 64 bit),
  avoids plugin/linker weirdness (bug #478481)

* Wed Aug 26 2009 Tomas Mraz <tmraz@redhat.com> - 1:4.5.2-11
- rebuilt with new openssl

* Thu Aug 20 2009 Than Ngo <than@redhat.com> - 4.5.2-10
- switch to kde-qt branch

* Tue Aug 18 2009 Than Ngo <than@redhat.com> - 4.5.2-9
- security fix for CVE-2009-1725 (bz#513813)

* Sun Aug 16 2009 Than Ngo <than@redhat.com> - 4.5.2-8
- fix phonon-backend-gstreamer for using pulsaudio (#513421)

* Sat Aug 14 2009 Rex Dieter <rdieter@fedoraproject.org> 4.5.2-7
- kde-qt: 287-qmenu-respect-minwidth
- kde-qt: 0288-more-x-keycodes (#475247)

* Wed Aug 05 2009 Rex Dieter <rdieter@fedoraproject.org> 4.5.2-6
- use linker scripts for _debug targets (#510246)
- tighten deps using %%{?_isa}
- -x11: Requires(post,postun): /sbin/ldconfig

* Thu Jul 30 2009 Than Ngo <than@redhat.com> - 4.5.2-5
- apply upstream patch to fix issue in Copy and paste

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 02 2009 Than Ngo <than@redhat.com> - 4.5.2-3
- pregenerate PNG, drop BR on GraphicsMagick (bz#509244)

* Fri Jun 26 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.5.2-2
- take current qt-copy-patches snapshot (20090626)
- disable patches which are already in 4.5.2
- fix the qt-copy patch 0274-shm-native-image-fix.diff to apply against 4.5.2

* Thu Jun 25 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.5.2-1
- Qt 4.5.2

* Sun Jun 07 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-18
- phonon-backend-gstreamer pkg, with icons
- optimize (icon-mostly) scriptlets

* Sun Jun 07 2009 Than Ngo <than@redhat.com> - 4.5.1-17
- drop the hack, apply patch to install Global header, gstreamer.desktop
  and dbus services file

* Sat Jun 06 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-16
- install awol Phonon/Global header

* Fri Jun 05 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.5.1-15
- apply Phonon PulseAudio patch (needed for the xine-lib backend)

* Fri Jun 05 2009 Than Ngo <than@redhat.com> - 4.5.1-14
- enable phonon and gstreamer-backend

* Sat May 30 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-13
- -doc: Obsoletes: qt-doc < 1:4.5.1-4 (workaround bug #502401)

* Sat May 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-12
- +phonon_internal macro to toggle packaging of qt's phonon (default off)

* Fri May 22 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-11
- qt-copy-patches-20090522

* Wed May 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-10.2
- full (non-bootstrap) build

* Wed May 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-10.1
- allow for minimal bootstrap build (*cough* arm *cough*)

* Wed May 06 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-10
- improved kde4_plugins patch, skip expensive/unneeded canonicalPath

* Wed May 06 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-9
- include kde4 plugin path by default (#498809)

* Mon May 04 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-8
- fix invalid assumptions about mysql_config --libs (bug #440673)
- fix %%files breakage from 4.5.1-5

* Wed Apr 29 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-7
- -devel: Provides: qt4-devel%%{?_isa} ...

* Mon Apr 27 2009 Than Ngo <than@redhat.com> - 4.5.1-6
- drop useless hunk of qt-x11-opensource-src-4.5.1-enable_ft_lcdfilter.patch

* Mon Apr 27 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-5
- -devel: Provides: *-static for libQtUiTools.a

* Fri Apr 24 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-4
- qt-doc noarch
- qt-demos, qt-examples (split from -doc)
- (cosmetic) re-order subpkgs in alphabetical order
- drop unused profile.d bits

* Fri Apr 24 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-3
- enable FT_LCD_FILTER (uses freetype subpixel filters if available at runtime)

* Fri Apr 24 2009 Than Ngo <than@redhat.com> - 4.5.1-2
- apply upstream patch to fix the svg rendering regression

* Thu Apr 23 2009 Than Ngo <than@redhat.com> - 4.5.1-1
- 4.5.1

* Tue Apr 14 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.0-14
- fix vrgb/vgbr corruption, disable QT_USE_FREETYPE_LCDFILTER (#490377)

* Fri Apr 10 2009 Than Ngo <than@redhat.com> - 4.5.0-13
- unneeded executable permissions for profile.d scripts

* Wed Apr 01 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.5.0-12
- fix inline asm in qatomic (de)ref (i386/x86_64), should fix Kolourpaint crash

* Mon Mar 30 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.0-11
- qt fails to build on ia64 (#492174)

* Fri Mar 25 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.0-10
- qt-copy-patches-20090325

* Tue Mar 24 2009 Than Ngo <than@redhat.com> - 4.5.0-9
- lrelease only shows warning when duplicate messages found in *.ts( #491514)

* Fri Mar 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.0-8
- qt-copy-patches-20090319

* Thu Mar 19 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.0-7
- include more phonon bits, attempt to fix/provide phonon bindings
  for qtscriptgenerator, PyQt, ...

* Tue Mar 17 2009 Than Ngo <than@redhat.com> - 4.5.0-6
- fix lupdate segfault (#486866)

* Sat Mar 14 2009 Dennis Gilmore <dennis@ausil.us> - 4.5.0-5
- add patch for sparc64. 
- _Atomic_word is not always an int

* Tue Mar 10 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.0-4
- macros.qt4: %%_qt45
- cleanup more phonon-related left-overs 

* Wed Mar 04 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.0-3
- -no-phonon-backend
- include qdoc3
- move designer plugins to runtime (#487622)

* Tue Mar 03 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.0-2
- License: LGPLv2 with exceptions or GPLv3 with exceptions
- BR: gstreamer-devel
- drop qgtkstyle patch (no longer needed)
- -x11: move libQtScriptTools here (linked with libQtGui)

* Tue Mar 03 2009 Than Ngo <than@redhat.com> - 4.5.0-1
- 4.5.0

* Fri Feb 27 2009 Rex Dieter <rdieter@fedoraproject.org> - 1:4.5.0-0.8.20090224
- 20090224 snapshot
- adjust pkgconfig hackery

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.5.0-0.7.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 22 2009 Rex Dieter <rdieter@fedoraproject.org> 4.5.0-0.5.rc1
- revert license, change won't land until official 4.5.0 release
- workaround broken qhostaddress.h (#485677)
- Provides: qgtkstyle = 0.1

* Fri Feb 20 2009 Rex Dieter <rdieter@fedoraproject.org> 4.5.0-0.4.rc1
- saner versioned Obsoletes
- -gtkstyle, Obsoletes: qgtkstyle < 0.1
- enable phonon support and associated hackery

* Mon Feb 16 2009 Than Ngo <than@redhat.com> 4.5.0-0.3.rc1
- fix callgrindChildExitCode is uninitialzed

* Sun Feb 15 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.0-0.2.rc1
- qt-copy-patches-20090215
- License: +LGPLv2

* Wed Feb 11 2009 Than Ngo <than@redhat.com> - 4.5.0-0.rc1.0
- 4.5.0 rc1

* Thu Feb 05 2009 Rex Dieter <rdieter@fedoraproject.org> 4.4.3-16
- track branches/qt-copy/4.4, and backout previous trunk(qt45) ones

* Mon Feb 02 2009 Than Ngo <than@redhat.com> 4.4.3-15
- disable 0269,0270,0271 patches, it causes issue in systray

* Thu Jan 29 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.4.3-14
- qt-copy-patches-20090129

* Mon Jan 26 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.4.3-13
- Provides: qt4%%{?_isa} = %%version-%%release
- add %%_qt4 to macros.qt4

* Thu Jan 22 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.4.3-12 
- respin (mysql)

* Fri Jan 16 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.4.3-11
- rebuild for new OpenSSL

* Mon Jan 12 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.4.3-10
- drop qt-x11-opensource-src-4.3.4-no-hardcoded-font-aliases.patch (#447298),
  in favor of qt-copy's 0263-fix-fontconfig-handling.diff

* Mon Jan 12 2009 Than Ngo <than@redhat.com> - 4.4.3-9
- qt-copy-patches-20090112

* Tue Dec 30 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.3-8
- qt-copy-patches-20081225

* Fri Dec 12 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.3-7
- rebuild for pkgconfig deps

* Wed Nov 12 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.3-6
- qt-copy-patches-20081112

* Tue Nov 11 2008 Than Ngo <than@redhat.com> 4.4.3-5
- drop 0256-fix-recursive-backingstore-sync-crash.diff, it's
  included in qt-copy-pathes-20081110

* Mon Nov 10 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.3-4
- qt-copy-patches-20081110

* Mon Nov 10 2008 Than Ngo <than@redhat.com> 4.4.3-3
- apply 0256-fix-recursive-backingstore-sync-crash.diff

* Thu Nov 06 2008 Than Ngo <than@redhat.com> 4.4.3-2
- bz#468814, immodule selection behavior is unpredictable without QT_IM_MODULE,
  patch from Peng Wu
- backport fix from 4.5

* Sun Sep 28 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.3-1
- 4.4.3

* Wed Sep 24 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.2-2
- omit systray patch (for now)

* Sat Sep 20 2008 Than Ngo <than@redhat.com> 4.4.2-1
- 4.4.2

* Mon Sep 08 2008 Rex Dieter <rdieter@fedoraproject.org> - 4.4.1-3
- apply QMAKEPATH portion of multilib patch only if needed
- qt-copy-patches-20080908

* Wed Aug 06 2008 Than Ngo <than@redhat.com> -  4.4.1-2
- fix license tag
- fix Obsoletes: qt-sqlite (missing epoch)

* Tue Aug 05 2008 Than Ngo <than@redhat.com> -  4.4.1-1
- 4.4.1

* Tue Aug 05 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-17
- fold -sqlite subpkg into main (#454930)

* Wed Jul 23 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-16
- qt-copy-patches-20080723 (kde#162793)
- omit deprecated phonon bits

* Sat Jul 19 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-15
- fix/workaround spec syntax 

* Sat Jul 19 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-14
- macros.qt4: fix %%_qt4_datadir, %%_qt4_translationdir

* Thu Jul 17 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-13
- (re)fix qconfig-multilib.h for sparc64

* Fri Jul 11 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-12
- qt-copy-patches-20080711

* Mon Jun 23 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-11
- fix dbus conditional (#452487)

* Sat Jun 14 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-10
- strip -lsqlite3 from .pc files (#451490)

* Sat Jun 14 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.4.0-9
- restore -qt4 suffixes

* Fri Jun 13 2008 Than Ngo <than@redhat.com> 4.4.0-8
- drop qt wrapper, make symlinks to /usr/bin

* Tue Jun 10 2008 Than Ngo <than@redhat.com> 4.4.0-7
- fix #450310, multilib issue 

* Fri Jun 06 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-6
- qt-copy-patches-20080606
- drop BR: libungif-devel (not used)
- move libQtXmlPatters, -x11 -> main
- move qdbuscpp2xml, qdbusxml2cpp, xmlpatters, -x11 -> -devel

* Tue May 27 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.4.0-5
- under GNOME, default to QGtkStyle if available

* Mon May 19 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.4.0-4
- don't hardcode incorrect font substitutions (#447298)

* Fri May 16 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-3
- qt-copy-patches-20080516

* Tue May 13 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.4.0-2
- revert _qt4_bindir change for now, needs more work (#446167)

* Tue May 06 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-1
- qt-4.4.0

* Tue Apr 29 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-0.6.rc1
- -webkit (include in -x11 subpkg), drop separate -webkit-devel
- omit qt4-wrapper.sh deps (since it's not used atm)
- qt-copy-patches-20080429
- Obsoletes/Provides: WebKit-qt(-devel) <|= 1.0.0-1  (#442200)

* Thu Apr 24 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-0.5.rc1
- strip -lssl -lcrypto from *.pc files too

* Tue Apr 08 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.4.0-0.4.rc1
- updated patch for #437440 ([as-IN] Consonant combination issue) by Pravin Satpute
- port the patch to Qt 4.4 (the code moved to harfbuzz) and reenable it

* Fri Apr 04 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-0.3.rc1
- qt-4.4.0-rc1
- -xmlpatterns (and drop -no-exceptions)
- -reduce-relocations, -dbus-linked, -openssl-linked
- -no-nas
- -no-phonon (-no-gstreamer), -no-webkit (for now, at least until
  conflicts with WebKit-qt and kdelibs4 are sorted out)
- %%_qt4_bindir -> %%_bindir, avoid qt4-wrapper hackage (#277581, #422291)
- qtconfig.desktop: NoDisplay=true (#244879)

* Wed Apr 02 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.3.4-10
- look for OpenSSL using versioned sonames (#432271)

* Wed Mar 26 2008 Than Ngo <than@redhat.com> 4.3.4-9
- apply patch bz#437440 to fix [as-IN] Consonant combination issue, thanks to Pravin Satpute

* Sun Mar 23 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.3.4-8
- -x11: add missing Provides: qt4-assistant when building as qt

* Thu Mar 13 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.3.4-7
- fix Requires of main package to include Epoch (thanks to Christopher Aillon)

* Wed Mar 12 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.3.4-6
- rename to qt on Fedora >= 9

* Mon Mar 10 2008 Rex Dieter <rdieter@fedoraproject.org> 4.3.4-5
- -x11: move qdbusviewer here

* Wed Mar 05 2008 Than Ngo <than@redhat.com> 4.3.4-4
- upstream patch to fix 4.3 regression

* Fri Feb 29 2008 Than Ngo <than@redhat.com> 4.3.4-3
- respin aliasing.patch, it's safer

* Thu Feb 28 2008 Than Ngo <than@redhat.com> 4.3.4-2
- fix aliasing violations that caused qmake crash

* Fri Feb 22 2008 Rex Dieter <rdieter@fedoraproject.org> 4.3.4-1
- qt-4.3.4

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 4.3.3-9
- Autorebuild for GCC 4.3

* Tue Feb 19 2008 Rex Dieter <rdieter@fedoraproject.org> 4.3.3-8
- qt-copy patches 20080219
- drop -optimized-qmake, for now, to avoid qmake segfaults (gcc43 issue?) 

* Fri Feb 15 2008 Rex Dieter <rdieter@fedoraproject.org> 4.3.3-7
- %%qt_datadir: %%_datadir/qt4 -> %%_libdir/qt4

* Wed Jan 30 2008 Rex Dieter <rdieter@fedoraproject.org> 4.3.3-6
- qt-copy 20080130 patch set (helps address previous 0180-window-role BIC)
- Trolltech.conf: (default) fontsize=10
- License: GPLv2 with exceptions or QPL

* Thu Jan 24 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.3-5
- License: GPLv2 or QPL
- qt-copy patches

* Thu Jan 17 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.3-4
- Qt.pc: fix typo for demosdir (use %%_qt4_demosdir)

* Mon Jan 07 2008 Than Ngo <than@redhat.com> 4.3.3-3
- apply patch from Dirk Müller to fix strict aliasing violations in tool classes

* Fri Dec 21 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.3-2
- -doc: Requires: %%name-assistant, omit assistant bin, 
  -x11: Provides: %%name-assistant (#147948)

* Wed Dec 05 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.3-1
- qt-4.3.3

* Tue Dec 04 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.2-7
- move assistant to -x11, leave .desktop in -doc (#147948)

* Sun Dec 02 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.2-6
- move qdbus to main pkg (#407861)

* Mon Oct 22 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.2-5
- -optimized-qmake

* Fri Oct 19 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.2-4
- slowdown with 4.3.2 (#334281)

* Tue Oct 16 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.2-2
- create/own %%_qt4_plugindir/styles

* Thu Oct 04 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.2-1
- qt-4.3.2
- (re)fix ppc64 segfaults, ppc64 fix upstreamed (previous patch was 
  inadvertantly not applied) (#246324)

* Fri Sep 14 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.1-8
- -x11: Req: redhat-rpm-config rpm, app-wrapper/multilib fun (#277581)

* Thu Sep 13 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.1-7
- include qt4-logo icon, used by qtdemo/qtconfig (#241452)
- linguist.desktop: use new linguist4 icons
- -devel,-x11: %%post/%%postun scriptlets (icons, mimetypes)

* Thu Sep 13 2007 Than Ngo <than@redhat.com> -  4.3.1-4
- fixed bz241452, add qtdemo/qtconfig icons
- fixed bz249242, designer4 - segmentation fault on s390x

* Wed Aug 23 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.1-3
- ppc64 patch (#246324)

* Fri Aug 10 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.1-2
- License: GPLv2 (see also GPL_EXCEPTIONS*.txt)
- omit needless %%check
- (re)add package review comment/reference

* Thu Aug 09 2007 Than Ngo <than@redhat.com> -  4.3.1-1
- update to 4.3.1

* Wed Aug 08 2007 Than Ngo <than@redhat.com> 4.3.0-11
- add %%_qt4_version

* Tue Aug 07 2007 Than Ngo <than@redhat.com> 4.3.0-10
- cleanup

* Sun Jul 15 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.0-9
- multilib broken: qconfig.h (#248768)
- +%%_qt4_demosdir,%%_qt4_examplesdir
- + Qt.pc, provide pkgconfig access to qt4 macros/variables

* Thu Jul 05 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.0-8
- fix %%_qt4_prefix/doc symlink

* Thu Jun 28 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.0-7
- prepare for possible rename qt4 -> qt (+Provides: qt4)
- make _qt4_* macro usage consistent (with %%check's)

* Sat Jun 23 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.0-5
- fix rpm macros, (%%_qt_plugindir, %%_qt4_translationdir}

* Thu Jun 21 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.0-4
- .desktop Category cleanup

* Thu Jun 21 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.0-3
- cleanup qconfig.h/multilib bits, add s390x/s390

* Wed May 30 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.0-2
- ExclusiveArch: %%ix86 -> i386 (for koji)

* Wed May 30 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.0-1
- qt-4.3.0(final)

* Fri May 04 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.3.0-0.5.rc1
- update to 4.3.0 RC1
- drop LD_RUN_PATH hack

* Fri May 04 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.3.0-0.3.snapshot20070423
- update to qt-4.3.0-snapshot-20070423
- build with SSL support (BR openssl-devel)
- drop upstreamed mysql_config.patch

* Wed May 02 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.0-0.2.beta
- qt-4.3.0beta
- -system-libtiff, BR: libtiff-devel

* Wed May 02 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.2.3-8
- QFileDialog file wrapping patch (qt#153635, rh#236908)
- License: GPL, dropping LICENSE.QPL (#237702)

* Thu Mar 29 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.2.3-7
- CVE-2007-0242, utf8-bug-qt4-2.diff

* Thu Mar 22 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.2.3-6
- -system-sqlite, BR: sqlite-devel
- drop mysql_config hackery

* Wed Mar 21 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.2.3-5
- strip (all) glib2 libs from .pc files
- prepend _ to rpm macros
- drop Obsoletes: qt4-debug

* Thu Mar 15 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.2.3-3
- make /etc/rpm/macros.qt4 owned only by qt4-devel

* Thu Mar 15 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.2.3-2
- fix mkspecs/common availability (#232392)

* Tue Mar 13 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.2.3-1
- qt-4.2.3
- multilib: move all arch-specific mkspecs bits to %%qt4_prefix/mkspecs (#223663)
- +%%_sysconfdir/rpm/macros.qt4
- +%%config %%qt4_sysconfdir/Trolltech.conf

* Tue Mar 06 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.2.2-8
- multilib: qconfig.pri, /etc/profile.d/* (#223663)

* Mon Mar 05 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.2.2-7
- fixup qconfig-multilib.h for powerpc/powerpc64 (#223663)
- include qt-copy's 0154-qdbuscpp2xml-moc_path.diff (#230875)

* Wed Feb 28 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.2.2-5
- fixup qconfig-multilib.h (#223663)
- qt4.(sh|csh): define QMAKESPEC (#223663)
- null'ify QMAKE_LIBDIR_QT, leave QMAKE_INCDIR_QT alone for now. (#230224)

* Tue Feb 27 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.2.2-3
- drop ./configure -no-reduce-exports (ie, support visibility) 
- multilib issues (#223663)

* Wed Dec 06 2006 Rex Dieter <rexdieter[AT]users.sf.net. 4.2.2-2
- respin for postgresql

* Fri Dec 01 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.2-1
- qt-4.2.2 (#218575)

* Wed Nov 15 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.1-3
- move libQtDesigner to -x11

* Mon Oct 23 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.1-2
- use respun upstream 4.2.1 tarball
- fix pre-modular-X libGL/libGLU deps (#211898)

* Sun Oct 22 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.1-1
- qt-4.2.1

* Wed Oct 04 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.0-1
- qt-4.2.0(final)

* Thu Sep 28 2006 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.2.0-0.9.20060927
- update to qt-4.2.0-snapshot-20060927
- update QDBus executable names
- -x11: exclude plugins/designer (which belong to -devel)
- BuildConflicts: qt4-devel
- drop -fno-strict-aliasing hack (fc5+)

* Wed Sep 27 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.0-0.8.rc1
- qtconfig.desktop: Categories=+AdvancedSettings;Settings

* Fri Sep 08 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.0-0.7.rc1
- 4.2.0-rc1

* Fri Aug 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.0-0.6.20060821
- update to 4.2.0-snapshot-20060821 (same as today's qt-copy)
- -no-separate-debug-info
- - ./configure -xfixes, BR: libXfixes-devel

* Mon Aug 07 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.0-0.5.tp1
- fix empty -debuginfo
- use $RPM_OPT_FLAGS

* Thu Jul 20 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.0-0.4.tp1
- strip -laudio, -ldbus-1, -lglib-2.0 from .pc files

* Thu Jul 20 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.0-0.3.tp1
- -no-reduce-exports (for now)
- -fno-strict-aliasing (fc5+)

* Fri Jul 07 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.0-0.2.tp1
- -system-nas-sound, BR: nas-devel (bug # 197937)
- -qdbus (fc6+, BR: dbus-devel >= 0.62)
- -glib (BR: glib2-devel)

* Fri Jun 30 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.0-0.1.tp1
- 4.2.0-tp1 (technology preview 1)

* Thu Jun 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.4-5
- make FHS-friendly (bug #196901)
- cleanup %%_bindir symlinks, (consistently) use qt4 postfix

* Wed Jun 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.4-4
- x11: split-out gui(x11) from non-gui bits (bug #196899)

* Mon Jun 26 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.4-3
- -debug: drop, adds nothing over -debuginfo, make lib..._debug 
  symlinks instead (bug #196513)
- assistant.desktop: fix tooltip (bug #197039)

* Mon Jun 26 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.4-2
- -devel: include -debug libs (bug #196513)
- -devel: move libQtDesigner here
- -config: mash into main pkg, should be multilib friendly now

* Fri Jun 23 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.4-1
- 4.1.4

* Tue Jun 20 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.3-9
- make each sql plugin optional

* Fri Jun 09 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.3-8
- qmake.conf: undefine QMAKE_STRIP to get useful -debuginfo (bug #193602)
- move (not symlink) .pc files into %%_libdir/pkgconfig

* Thu Jun 08 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.3-7
- *really* fix qt4-wrapper.sh for good this time.

* Mon May 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.3-6
- make qt4-wrapper.sh use rpm when pkg-config/qt4-devel isn't
  installed (#193369)

* Fri May 26 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.3-5
- strip -lXi from .pc files (#193258)
- simplify sql plugin builds via %%buildSQL macro
- -libdir %%qt_libdir 

* Wed May 24 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.3-4
- move (most) %%dir ownership (back) to main pkg

* Sun May 21 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.3-3
- fix %%mysql_libs macro

* Sat May 20 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.3-2
- -mysql: use mysql_config for setting cflags/ldflags.
- -mysql: BR: mysql-devel > 4.0

* Sat May 20 2006 Laurent Rineau <laurent.rineau__fc_extra@normalesup.org>
- Fix the last reference to %{qtdir}/lib: use %{_lib} instead of "lib".
- Fix the ownership of subpackages: they need to own parents of directories they install files in.

* Fri May 19 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.3-1
- 4.1.3
- %%qtdir/lib/*.pc -> %%qtdir/%%_lib/*.pc 
  (hopefully, the last hardcoded reference to %%qtdir/lib)

* Fri May 19 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-20
- fix some unowned dirs
- try harder to purge %%builddir from .pc,.prl files
- -docdir %%_docdir/%%name-doc-%%version, since we use %%doc macro in main pkg
- -doc: own %%qt_docdir
- use qt4-wrapper.sh to ensure launch of qt4 versions of apps that
  (may) overlap with those from qt3 
- use %%qtdir/%%_lib in ld.so.conf.d/*.conf files too

* Tue May 16 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-19
- drop libQtAssistantClient,libQtUiTools shlib patches

* Tue May 16 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-18
- %%_bindir symlinks: qtconfig4 -> qt4config, qtdemo4 -> qt4demo
- -libdir %%qtdir/%%_lib, simplifies %%_lib != lib case
- -docdir %%_docdir/%%name-%%version
- build shared versions of libQtAssistantClient,libQtUiTools too
- strip extraneous -L paths, libs from *.prl files too

* Tue May 16 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-17
- .desktop: Qt -> Qt4, and Comment= (where missing)
- -devel: include -designer here, Obsoletes/Provides: %%name-designer.
   It's small, simplifies things... one less subpkg to worry about.
- -doc: include %%qtdir/doc symlink here
- -docdir %%_docdir/%%name-doc-%%version

* Mon May 15 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-16
- set/use RPM_OPT_FLAGS only for our platform
- (really) don't give %%_bindir symlink for qt3to4 another "4" suffix
- don't add 4 suffix to uic3, rcc (they don't conflict with qt(3)-devel)
- -devel: add  linguist.desktop
- -doc: move assistant here, Provides: %%{name}-assistant, add assistant.desktop
- -doc: add qtdemo.desktop
- -doc: Requires qt4 (instead of qt4-devel)
- assistant4.patch: search for assistant4 instead of (qt3's) assistant in $PATH 
- -qtconfig: add qtconfig.desktop
- updated %%sumaries to mention where (some) tools are, including assistant, linguist,
  qtdemo

* Mon May 15 2006 Laurent Rineau <laurent.rineau__fc_extra@normalesup.org> - 4.1.2-15
- Rename -docs to -doc.
- Files in the -doc subpackage are no longer in %%doc.
- Move qtdemo to the subpackage -doc.
- Fix symlinks in %%{_bindir}.
- Only modify mkspecs/linux-g++*/qmake.conf, instead of all mkspecs/*/qmake.conf.

* Sun May 14 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-14
- remove MapNotify from .desktop file(s).
- install -m644 LICENSE.*
- -docs: don't mark examples as %doc
- drop unused %%debug macro

* Sat May 13 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-13
- include unpackaged pkgconfig files

* Sat May 13 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-12
- fix typos so it actually builds.

* Sat May 13 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-11
- drop optional ld.so.conf.d usage, make mandatory
- make %%_bindir symlinks to all %%qtdir/bin stuff (even qt3to4)
- pkgconfig files: hardlinks -> relative symlinks, strip -L%{_libdir}/mysql
  and -L%%{_builddir}/qt-x11-opensource-src-%%version/lib
- cleanup/simplify Summary/%%description entries
- $RPM_BUILD_ROOT -> %%buildroot, $RPM_BUILD_DIR -> %%_builddir

* Sat May 13 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-10
- cleanup/simplify license bits, include LICENSE.QPL
- drop unused -styles/-Xt subpkg reference
- drop unused motif extention bits
- drop initialpreference from .desktop files

* Fri May 12 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-9
- drop reference to non-existent config.test/unix/checkavail

* Fri May 12 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-8
- simplify build* macros
- lower-case all subpkgs (ie, -MySQL -> -mysql )
- drop BR: perl, sed

* Thu May 11 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-7
- rework %%post/%%postun, mostly to placate rpmlint
- drop Prefix:
- drop use of qt4.(sh|csh), they're empty atm anyway
- use Source'd designer.desktop (instead of inline cat/echo)
- symlinks to %%_bindir: qmake4, designer4, qtconfig4
- drop qtrc, qt4 doesn't use it.
- -docs subpkg for API html docs, demos, examples.
- BR: libXcursor-devel libXi-devel (fc5+)

* Thu Apr 27 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-6
- devel: Requires: pkgconfig

* Sat Apr 15 2006 Simon Perreault <nomis80@nomis80.org> 4.1.2-5
- Disable C++ exceptions.

* Mon Apr 10 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-4
- qt4.(sh|csh): place-holders only, don't define QTDIR (and QTLIB)
  as that (potentially) conflicts with qt-3.x.

* Thu Apr 06 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-2
- -devel: Drop (artificial) Conflicts: qt-devel
- fix %%ld_so_conf_d usage
- %%qtdir/%%_lib symlink

* Wed Apr 05 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-1
- drop Epoch
- cleanup (a lot!)

* Tue Dec 20 2005 Than Ngo <than@redhat.com> 1:4.1.0-0.1
- update to 4.1.0

* Fri Sep 09 2005 Than Ngo <than@redhat.com> 1:4.0.1-0.1
- update to 4.0.1

