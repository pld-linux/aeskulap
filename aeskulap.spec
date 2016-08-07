Summary:	Full open source replacement for commercially available DICOM viewers
Name:		aeskulap
Version:	0.2.2
Release:	0.1
# The sources of the (internal) libraries are LGPLv2+, the rest of the sources are GPLv2+,
# except binreloc.{c,h} and the documentation, which are in the public domain
License:	GPLv2+ and LGPLv2+ and Public Domain
URL:		https://github.com/jenslody/aeskulap
Source0:	https://github.com/jenslody/aeskulap/archive/master.zip#/%{name}-%{version}-%{release}.zip
# Source0-md5:	62ce5c0da69e3edecb9d7c58effc43fd
Group:		X11/Applications/Science
BuildRequires:	GConf2
BuildRequires:	appstream-glib
BuildRequires:	dcmtk-devel >= 3.6.1
BuildRequires:	desktop-file-utils
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel
BuildRequires:	gtkmm-devel
BuildRequires:	intltool
BuildRequires:	libjpeg-turbo-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	libtool
BuildRequires:	libwrap-devel
BuildRequires:	openssl-devel
BuildRequires:	gconfmm-devel
BuildRequires:	libglademm-deve
Requires(pre):	GConf2
Requires(post):	GConf2
Requires(preun):	GConf2

%description
Aeskulap is able to load a series of special images stored in the
DICOM format for review. Additionally Aeskulap is able to query and
fetch DICOM images from archive nodes (also called PACS) over the
network.

The goal of this project is to create a full open source replacement
for commercially available DICOM viewers.

Aeskulap is based on gtkmm, glademm and gconfmm and designed to run
under Linux. Ports of these packages are available for different
platforms. It should be quite easy to port Aeskulap to any platform
were these packages are available.

%prep
%setup -q -n aeskulap-master
autoreconf --force --install
intltoolize --force --copy --automake

%build
# point to the correct lib version depending on the arch
sed -i 's/lib -ldcmjpeg/%{_lib} -ldcmjpeg/' configure configure.ac

export CPPFLAGS='-std=c++11'
%configure \
	--disable-static \
	--disable-schemas-install \

%{__make} %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

desktop-file-validate $RPM_BUILD_ROOT/%{_desktopdir}/%{name}.desktop
appstream-util validate-relax --nonet $RPM_BUILD_ROOT/%{_datadir}/appdata/%{name}.appdata.xml

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%gconf_schema_prepare %{name}

%post
%gconf_schema_upgrade %{name}
%update_icon_cache_post hicolor &>/dev/null || :
%{_bindir}/%update_desktop_database

%preun
%gconf_schema_remove %{name}

%postun
if [ $1 -eq 0 ] ; then
    %update_icon_cache_post hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
%{_bindir}/%update_desktop_database

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README doc/%{name}-tutorials.pdf
%attr(755,root,root) %{_bindir}/%{name}
%{_libdir}/%{name}/
%{_datadir}/%{name}/
%{_iconsdir}/hicolor/64x64/apps/%{name}.png
%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
%{_desktopdir}/%{name}.desktop
%{_datadir}/appdata/%{name}.appdata.xml
%{_sysconfdir}/gconf/schemas/%{name}.schemas
