Summary:	PgpoolAdmin - web-based pgpool administration
Name:		pgpoolAdmin
Version:	3.0.3
Release:	1
License:	BSD
Group:		Applications/WWW
URL:		http://pgpool.projects.postgresql.org

Source0:	http://pgfoundry.org/frs/download.php/2964/%{name}-%{version}.tar.gz
Source1:	apache.conf
Source2:	lighttpd.conf
#Source3:	%{name}.conf

BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	pgpool-II
Requires:	php-pgsql >= 4.4.2
Requires:	webapps
Requires:	webserver(access)
Requires:	webserver(alias)
Requires:	webserver(auth)
Requires:	webserver(indexfile)
Requires:	webserver(php)
Requires:	webserver(php) >= 4.4.2

BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Buildarch:	noarch
%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}


Patch1:		%{name}-conf.patch

%description
The pgpool Administration Tool is management tool of pgpool-II. It is
possible to monitor, start, stop pgpool and change settings of
pgpool-II.

%description -l pl.UTF-8
Narzędzie pgpoolAdmin służy do zarządzania programem pgpool-II. Ma
możliwości monitorowania, startowania, zatrzymywania oraz zmieniania
konfiguracji pgpool-II.

%package setup
Summary:	Installer script for pgpoolAdmin
Summary(pl.UTF-8):	Skrypt instalacyjny pgpoolAdmina
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}

%description setup
This package provides installer script for pgpoolAdmin.

%description setup -l pl.UTF-8
Ten pakiet zawiera skrypt instalacyjny pgpoolAdmina.


%prep
%setup -q
%patch1 -p1
cat > apache.conf <<'EOF'
Alias /%{name} %{_appdir}
<Directory %{_appdir}>
	Allow from all
</Directory>
EOF

cat > lighttpd.conf <<'EOF'
alias.url += (
    "/%{name}" => "%{_appdir}",
)
EOF

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}

cp -p apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -p lighttpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

#mv $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir}}/apache.conf
#mv $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir}}/lighttpd.conf
cp -p $RPM_BUILD_ROOT%{_sysconfdir}/{apache,httpd}.conf

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
#cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf
cp -p $RPM_BUILD_ROOT%{_sysconfdir}/{apache,httpd}.conf
# oryginalne
install -d $RPM_BUILD_ROOT%{_appdir}/conf
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install *.php $RPM_BUILD_ROOT%{_appdir}
cp -a  doc/ images/ install/ lang/ libs/ templates/ templates_c/ screen.css $RPM_BUILD_ROOT%{_appdir}
install conf/* $RPM_BUILD_ROOT%{_sysconfdir}/
ln -s %{_sysconfdir}/pgmgt.conf.php $RPM_BUILD_ROOT/%{_appdir}/conf/pgmgt.conf.php

#if [ -d %{_sysconfdir}/httpd/conf.d/ ]
#then
#	install -d $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/
#	install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/%{name}.conf
#fi

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%post
	/bin/chgrp http  /etc/pgpool.conf
	/bin/chgrp http /etc/pcp.conf
	/bin/chmod g+w /etc/pgpool.conf /etc/pcp.conf

%postun
	chgrp root /etc/pgpool.conf /etc/pcp.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(660,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php
%dir %{_appdir}
# orignalne
#%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
#%config(noreplace) %{_sysconfdir}/%{name}/*
%{_appdir}/*.php
%{_appdir}/conf
%{_appdir}/doc
%{_appdir}/images
%{_appdir}/lang
%{_appdir}/libs
%{_appdir}/templates
%{_appdir}/templates_c
%attr(775,root,http) %{_appdir}/templates_c
%{_appdir}/screen.css
%doc README README.euc_jp

%files setup
%defattr(644,root,root,755)
%dir %{_appdir}/install
%{_appdir}/install/*.php
%{_appdir}/install/images
%{_appdir}/install/lang
