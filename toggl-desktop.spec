%define		qtver	4.6
Summary:	Desktop client for the Toggle time tracking service
Name:		toggl-desktop
Version:	2.5.2.0
Release:	0.1
License:	LGPL
Group:		X11/Applications
# bzr branch lp:toggl-desktop # version from version.cpp
Source0:	%{name}-%{version}.tar.xz
# Source0-md5:	94f53c166d109037d0bf753fd7021c48
URL:		https://launchpad.net/toggl-desktop
BuildRequires:	QtCore-devel >= %{qtver}
BuildRequires:	QtCore-devel >= %{qtver}
BuildRequires:	QtGui-devel >= %{qtver}
BuildRequires:	QtNetwork-devel >= %{qtver}
BuildRequires:	QtNetwork-devel >= %{qtver}
BuildRequires:	QtWebKit-devel >= %{qtver}
BuildRequires:	qt4-qmake >= %{qtver}
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libXScrnSaver-devel
BuildRequires:	xz
Requires:	QtCore >= %{qtver}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Toggl Desktop allows you to run Toggl Timer on the desktop. The
application supports both the classic Timer and the new Nano.

%prep
%setup -q -n %{name}

%build
qmake-qt4
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/TogglDesktop
%{_desktopdir}/TogglDesktop.desktop
%{_pixmapsdir}/TogglDesktop.png
