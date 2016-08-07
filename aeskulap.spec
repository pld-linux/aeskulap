Summary:	Full open source replacement for commercially available DICOM viewers
Name:		aeskulap
Version:	0.2.2
Release:	0.1
Group:		X11/Applications/Science
# The sources of the (internal) libraries are LGPLv2+, the rest of the sources are GPLv2+,
# except binreloc.{c,h} and the documentation, which are in the public domain
License:	GPLv2+ and LGPLv2+ and Public Domain
Source0:	https://github.com/jenslody/aeskulap/archive/e3ef378/%{name}-%{version}.tar.gz
# Source0-md5:	184d2c2c7b2826723686b98cc6833a12
URL:		https://github.com/jenslody/aeskulap
BuildRequires:	GConf2
BuildRequires:	appstream-glib
BuildRequires:	dcmtk-devel >= 3.6.1
BuildRequires:	desktop-file-utils
BuildRequires:	gconfmm-devel
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel
BuildRequires:	gtkmm-devel
BuildRequires:	intltool
BuildRequires:	libglademm-devel
BuildRequires:	libjpeg-turbo-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	libtool
BuildRequires:	libwrap-devel
BuildRequires:	openssl-devel
BuildRequires:	rpmbuild(macros) >= 1.596
Requires(pre):	GConf2
Requires(post):	GConf2
Requires(preun):	GConf2
Requires:	desktop-file-utils
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
Requires:	shared-mime-info
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
%setup -qc
mv aeskulap-*/* .

%build
autoreconf --force --install
intltoolize --force --copy --automake
# point to the correct lib version depending on the arch
sed -i 's/lib -ldcmjpeg/%{_lib} -ldcmjpeg/' configure configure.ac

export CPPFLAGS='-std=c++11'
%configure \
	--disable-static \
	--disable-schemas-install

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop
appstream-util validate-relax --nonet $RPM_BUILD_ROOT%{_datadir}/appdata/%{name}.appdata.xml

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%gconf_schema_prepare %{name}

%post
%gconf_schema_upgrade %{name}
%update_icon_cache hicolor
%update_desktop_database

%preun
%gconf_schema_remove %{name}

%postun
%update_icon_cache hicolor
%update_desktop_database

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
