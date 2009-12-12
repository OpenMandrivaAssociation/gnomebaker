%define name	gnomebaker
%define version 0.6.4
%define release %mkrel 3

Name: 	 	%{name}
Summary: 	Simple CD burning frontend for GNOME
Version: 	%{version}
Release: 	%{release}

Source:		http://prdownloads.sourceforge.net/gnomebaker/%{name}-%{version}.tar.gz
Patch0:		gnomebaker-0.6.4-mdv-fix-str-fmt.patch
URL:		http://biddell.co.uk/gnomebaker.php
License:	GPL
Group:		Archiving/Cd burning
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	imagemagick libgnomeui2-devel libglade2.0-devel bison
BuildRequires:	scrollkeeper
BuildRequires:	gstreamer0.10-devel
BuildRequires:  libnotify-devel
BuildRequires:	perl-XML-Parser
BuildRequires:	desktop-file-utils
BuildRequires:	intltool automake1.9
Requires:	cdrkit cdrkit-genisoimage cdrkit-icedax
Requires:	gstreamer0.10-plugins-base gstreamer0.10-flac

%description
GnomeBaker is a GTK2/Gnome cd burning application.

As of 0.4 GnomeBaker can:
* Create data cds
* Blank rewritable disks
* Copy data cds
* Copy audio cds
* Burn existing cd iso images
* Can burn via scsi and atapi
* Drag and drop to create data cds (including DnD to and from nautilus)
* Create audio cds from existing wavs, mp3, flac and oggs
* Integrate with gconf for storage of application settings
* Burn DVDs
* Supports multisession burning
* Blank/Format DVDs
* Burn Cue/Bin files
* Burn data cds on the fly

In the future it will also do the following and hopefully much more:
* Create video cds from existing video and stills
* Create mixed mode cds

%prep
%setup -q
%patch0 -p1 -b .strfmt
chmod 644 AUTHORS ChangeLog NEWS TODO README
#./autogen.sh

%build
export CFLAGS="%optflags -rdynamic"
%configure2_5x --enable-libnotify
%make
										
%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
rm -fr $RPM_BUILD_ROOT/%_prefix/doc

#menu
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-System-Archiving-CDBurning" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

#icons
mkdir -p $RPM_BUILD_ROOT/%_liconsdir
convert -size 48x48 pixmaps/%name-48.png $RPM_BUILD_ROOT/%_liconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_iconsdir
convert -size 32x32 pixmaps/%name-48.png $RPM_BUILD_ROOT/%_iconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_miconsdir
convert -size 16x16 pixmaps/%name-48.png $RPM_BUILD_ROOT/%_miconsdir/%name.png

%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post
%update_menus
%update_icon_cache hicolor		
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%clean_icon_cache hicolor
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS TODO README
%{_bindir}/%name
%{_datadir}/gnome/help/%name
%{_datadir}/applications/%name.desktop
%{_datadir}/%name
%_datadir/icons/hicolor/*/apps/*
%dir %{_datadir}/omf/%name
%{_datadir}/omf/%name/*-C.omf
%{_liconsdir}/%name.png
%{_iconsdir}/%name.png
%{_miconsdir}/%name.png


