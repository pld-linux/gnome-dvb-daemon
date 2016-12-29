#
# Conditional build:
%bcond_without	totem	# Totem plugin
#
Summary:	Daemon to setup DVB devices, record and watch TV shows and browse EPG
Summary(pl.UTF-8):	Demon do ustawiania urządzeń DVB, nagrywania i oglądania programów TV oraz przeglądania EPG
Name:		gnome-dvb-daemon
Version:	0.2.90
Release:	2
License:	GPL v3+
Group:		X11/Applications/Multimedia
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-dvb-daemon/0.2/%{name}-%{version}.tar.xz
# Source0-md5:	06409269886d174ac54883b07f71faac
URL:		https://wiki.gnome.org/Projects/DVBDaemon
BuildRequires:	autoconf >= 2.63.2
BuildRequires:	automake >= 1:1.11
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.32.0
BuildRequires:	gstreamer-devel >= 1.4.0
# pkgconfig(gstreamer-mpegts-1.0), plugins: tsparse dvbbasebin dvbsrc
BuildRequires:	gstreamer-plugins-bad-devel >= 1.4.0
# pkgconfig(gstreamer-rtsp-1.0)
BuildRequires:	gstreamer-plugins-base-devel >= 1.4.0
# rtpmp2tpay plugin
BuildRequires:	gstreamer-plugins-good >= 1.4.0
BuildRequires:	gstreamer-rtsp-server-devel >= 1.4.0
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libgee-devel >= 0.8.0
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	pkgconfig >= 1:0.9
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-pygobject3-devel >= 3.2.1
BuildRequires:	sqlite3-devel >= 3.4
BuildRequires:	udev-devel
BuildRequires:	vala >= 2:0.25.1
Requires(post,postun):	gtk-update-icon-cache
Requires:	glib2 >= 1:2.32.0
Requires:	hicolor-icon-theme
Requires:	gstreamer >= 1.4.0
Requires:	gstreamer-plugins-bad >= 1.4.0
Requires:	gstreamer-plugins-base >= 1.4.0
Requires:	gstreamer-plugins-good >= 1.4.0
Requires:	gstreamer-rtsp-server >= 1.4.0
Requires:	libgee >= 0.8.0
Requires:	python3-pygobject3 >= 3.2.1
Requires:	sqlite3 >= 3.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME DVB Daemon is a daemon written in Vala to setup your DVB
devices, record and watch TV shows and browse EPG. It can be
controlled directly via its D-Bus interface or with UI applications
that come with it.

%description -l pl.UTF-8
GNOME DVB Daemon to napisany w języku Vala demon do ustawiania
urządzeń DVB, nagrywania i oglądania programów telewizyjnych oraz
przeglądania elektronicznych przewodników po programach (EPG). Może
być sterowany bezpośrednio poprzez interfejs D-Bus albo przy użyciu
dołączonych aplikacji z interfejsem użytkownika.

%package -n totem-dvb-daemon
Summary:	GNOME DVB Daemon plugin for Totem
Summary(pl.UTF-8):	Wtyczka GNOME DVB Daemon dla Totema
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}-%{release}
Requires:	totem

%description -n totem-dvb-daemon
Totem plugin to watch live TV and recorded shows using GNOME DVB
Daemon.

%description -n totem-dvb-daemon -l pl.UTF-8
Wtyczka Totema do oglądania telewizji na żywo oraz nagranych programów
przy użyciu GNOME DVB Daemona.

%prep
%setup -q

%{__sed} -i -e '1s,/usr/bin/env python,/usr/bin/python3,' client/{gnome-dvb-control,gnome-dvb-setup}

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{?with_totem:--enable-totem-plugin} \
	--with-totem-plugin-dir=%{_libdir}/totem/plugins
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/gnome-dvb-control
%attr(755,root,root) %{_bindir}/gnome-dvb-daemon
%attr(755,root,root) %{_bindir}/gnome-dvb-setup
%{py3_sitescriptdir}/gnomedvb
%{_datadir}/dbus-1/services/org.gnome.DVB.service
%{_datadir}/dbus-1/services/org.gnome.UPnP.MediaServer2.DVBDaemon.service
%{_desktopdir}/gnome-dvb-control.desktop
%{_desktopdir}/gnome-dvb-setup.desktop
%{_iconsdir}/hicolor/*x*/apps/gnome-dvb-daemon.png
%{_iconsdir}/hicolor/*x*/apps/gnome-dvb-setup.png
%{_iconsdir}/hicolor/scalable/apps/gnome-dvb-daemon.svg
%{_iconsdir}/hicolor/scalable/apps/gnome-dvb-setup.svg

%files -n totem-dvb-daemon
%defattr(644,root,root,755)
%dir %{_libdir}/totem/plugins/dvb-daemon
%{_libdir}/totem/plugins/dvb-daemon/dvb-daemon.plugin
%{_libdir}/totem/plugins/dvb-daemon/dvb-daemon.py
