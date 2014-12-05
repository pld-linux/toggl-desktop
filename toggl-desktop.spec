# TODO
# - third party:
#pocodir=third_party/poco
#openssldir=third_party/openssl
#jsoncppdir=third_party/jsoncpp/dist

%define		qtver	5.2
Summary:	Desktop client for the Toggle time tracking service
Name:		toggl-desktop
Version:	7.1.146
Release:	0.4
License:	LGPL v2.1
Group:		X11/Applications
# https://www.toggl.com/tour/desktop
Source0:	https://github.com/toggl/toggldesktop/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	b83b3e97e8aefd6d9280357a541aa2d1
Source1:	TogglDesktop.desktop
URL:		https://github.com/toggl/toggldesktop
Patch0:		ca-cert-path.patch
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Network-devel >= %{qtver}
BuildRequires:	Qt5Network-devel >= %{qtver}
BuildRequires:	Qt5WebKit-devel >= %{qtver}
BuildRequires:	poco-devel
BuildRequires:	qt5-qmake >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.583
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libXScrnSaver-devel
BuildRequires:	xz
Requires(post,postun):	/sbin/ldconfig
Requires:	ca-certificates
Requires:	desktop-file-utils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# Unresolved symbols found in: sqlite3_threadsafe
%define		skip_post_check_so	libTogglDesktopLibrary.so.1.0.0

%description
Toggl Desktop allows you to run Toggl Timer on the desktop. The
application supports both the classic Timer and the new Nano.

%prep
%setup -q -n toggldesktop-%{version}
%patch0 -p1

%{__sed} -i -e 's,cxx=g++,cxx=$(CXX),' Makefile
%{__sed} -i -e 's,cflags=-g,cflags=-g $(CXXFLAGS),' Makefile

%build
# NOTE: do not redefine CXXFLAGS, as it would ovewrite DEFINES, however
# CXXFLAGS are from qt5 build time, so they are "optimized" already.

cd src/lib/linux/TogglDesktopLibrary
qmake-qt5
cd -
%{__make} -C src/lib/linux/TogglDesktopLibrary
	CXX="%{__cxx}" \
	QMAKE=qmake-qt5 \

%{__make} -j1 \
	CXX="%{__cxx}" \
	QMAKE=qmake-qt5 \
	ui

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_desktopdir}}

install -p src/ui/linux/TogglDesktop/build/release/TogglDesktop \
	$RPM_BUILD_ROOT%{_bindir}

cp -a src/lib/linux/TogglDesktopLibrary/build/release/* \
	$RPM_BUILD_ROOT%{_libdir}

cp -a third_party/bugsnag-qt/build/release/* \
	$RPM_BUILD_ROOT%{_libdir}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libTogglDesktopLibrary.so
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libTogglDesktopLibrary.so.1.0
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libbugsnag-qt.so
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libbugsnag-qt.so.1.0

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
for icon in src/ui/linux/TogglDesktop/icons/*/toggldesktop.png; do
	size=${icon#src/ui/linux/TogglDesktop/icons/}
	size=${size%/toggldesktop.png}
	install -d $RPM_BUILD_ROOT%{_iconsdir}/hicolor/$size
	cp -p $icon $RPM_BUILD_ROOT%{_iconsdir}/hicolor/$size
done

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database
%update_icon_cache hicolor

%postun
/sbin/ldconfig
%update_desktop_database
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/TogglDesktop
%attr(755,root,root) %{_libdir}/libTogglDesktopLibrary.so.*.*.*
%ghost %{_libdir}/libTogglDesktopLibrary.so.1
%{_desktopdir}/TogglDesktop.desktop
%{_iconsdir}/hicolor/*/toggldesktop.png

# third party
%ghost %{_libdir}/libbugsnag-qt.so.1
%attr(755,root,root) %{_libdir}/libbugsnag-qt.so.*.*.*
