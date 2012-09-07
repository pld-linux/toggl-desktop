Summary:	Desktop client for the Toggle time tracking service
Name:		toggl-desktop
Version:	2.5.1
Release:	0.1
License:	LGPL
Group:		X11/Applications
URL:		http://www.toggl.com/
Source0:	TogglDesktop-%{version}.tar.gz
# Source0-md5:	94f53c166d109037d0bf753fd7021c48
BuildRequires:	QtCore-devel >= 4.6
BuildRequires:	xorg-lib-libXScrnSaver-devel
Requires:	QtCore >= 4.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Toggl Desktop allows you to run Toggl Timer on the desktop. The
application supports both the classic Timer and the new Nano.

%prep
%setup -q -n TogglDesktop-%{version}

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
