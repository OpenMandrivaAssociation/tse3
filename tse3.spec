%define version 0.3.1
%define release %mkrel 4

%define major 0
%define libname %mklibname %{name}_ %major

Summary:	Trax Sequencer Engine
Name:		tse3
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Sound
URL:		https://download.sourceforge.net/tse3/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

Source0:	http://download.sourceforge.net/tse3/%{name}-%{version}.tar.bz2
Patch0:		tse3_alsa1.x_and_sustain.patch
Patch1:		tse3-0.3.1-gcc4.patch
Patch2:         tse3-fix-compile-amd64.patch
Patch3:		tse3-0.3.1-libtool.patch
BuildRequires:	alsa-lib-devel >= 1.0
BuildRequires:	automake1.8
BuildRequires:	kdemultimedia-arts-devel

%description
TSE3 is a powerful open source sequencer engine written in C++. It is
a 'sequencer engine' because it provides the actual driving force
elements of a sequencer but provides no form of fancy interface.
Sequencer applications or multimedia presentation packages will
incorporate the TSE3 libraries to provide a user with MIDI sequencing
facilities.

%package -n %{libname}
Summary:	Trax Sequencer Engine Library
Group:		Sound
Requires:	%{name} = %{version}

%description -n %{libname}
TSE3 is a powerful open source sequencer engine written in C++.
This is the main tse3 library.

%package -n %{libname}-devel
Summary:	Tse3 header files
Group:		Development/C++
Requires:	%libname = %version
Provides:	libtse3-devel = %{version}-%{release}
Obsoletes:	libtse3-devel
Provides:	%{name}-devel = %{version}-%{release}

%description  -n %{libname}-devel
Tse3 header files.

%prep
%setup -q
%patch1 -p0 -b .fix_compile_gcc4
%patch2 -p0 -b .fix_compile_amd64
%patch3 -p0

%build
#AUTOMAKE=automake-1.9 ACLOCAL=aclocal-1.9 autoreconf --force --install
autoreconf --force --install
#CXXFLAGS="%optflags -fno-rtti"
%configure2_5x --with-alsa \
	--without-aRts --without-oss
# doesn't support SMP build
%make -j1

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

# use percent-doc to handle documentation instead
rm -rf package-doc
mv $RPM_BUILD_ROOT/usr/doc package-doc

## fix wrong-script-end-of-line-encoding
perl -pi -e 's/\015$//' %buildroot/usr/include/tse3/plt/Win32.cpp
perl -pi -e 's/\015$//' %buildroot/usr/include/tse3/plt/Win32.h


%if %mdkversion < 200900
%post   -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,755)
%doc AUTHORS README package-doc/*
%{_bindir}/*
%{_mandir}/man1/*

%files -n %{libname}
%defattr(-,root,root,755)
%{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr(-,root,root,755)
%{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/tse3
%{_mandir}/man3/*
