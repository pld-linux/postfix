# TODO:
# - check/fix 'polish' bcond
# - add http://www.aurore.net/projects/postfix_memcached/
#
# Conditional build:
%bcond_without	ldap	# without LDAP map module
%bcond_without	mysql	# without MySQL map module
%bcond_without	pgsql	# without PostgreSQL map module
%bcond_without	sasl	# without SMTP AUTH support
%bcond_without	ssl	# without SSL/TLS support
%bcond_without	cdb	# without cdb map support
%bcond_without	vda	# with VDA patch
%bcond_with	hir	# with Beeth's header_if_reject patch
%bcond_with	tcp	# with unofficial tcp: lookup table
#%bcond_with	polish	# with double English+Polish messages
#
Summary:	Postfix Mail Transport Agent
Summary(cs.UTF-8):	Postfix - program pro přepravu pošty (MTA)
Summary(es.UTF-8):	Postfix - Un MTA (Mail Transport Agent) de alto desempeño
Summary(fr.UTF-8):	Agent de transport de courrier Postfix
Summary(pl.UTF-8):	Serwer SMTP Postfix
Summary(pt_BR.UTF-8):	Postfix - Um MTA (Mail Transport Agent) de alto desempenho
Summary(sk.UTF-8):	Agent prenosu pošty Postfix
Name:		postfix
Version:	2.3.12
%define		vda_ver 2.3.3
Release:	3.1
Epoch:		2
License:	distributable
Group:		Networking/Daemons
Source0:	ftp://ftp.porcupine.org/mirrors/postfix-release/official/%{name}-%{version}.tar.gz
# Source0-md5:	54aa9e61cc640d2515d965b30cf73e37
Source1:	%{name}.aliases
Source2:	%{name}.cron
Source3:	%{name}.init
Source4:	%{name}.sysconfig
Source5:	%{name}.sasl
Source6:	%{name}.pamd
Source7:	http://web.onda.com.br/nadal/postfix/VDA/%{name}-%{vda_ver}-vda.patch.gz
# Source7-md5:	3506ab432360766b6a2708042b29943a
Patch0:		%{name}-config.patch
Patch1:		%{name}-conf_msg.patch
Patch2:		%{name}-dynamicmaps.patch
Patch3:		%{name}-master.cf_cyrus.patch
# from http://akson.sgh.waw.pl/~chopin/unix/postfix-2.1.5-header_if_reject.diff
Patch4:		%{name}-header_if_reject.patch
#Patch5:	%{name}-pl.patch
#Patch6:	%{name}-size-check-before-proxy.patch
#Patch7:	%{name}-log-proxy-rejects.patch
Patch8:		%{name}-ident.patch
Patch9:		%{name}-lib64.patch
Patch10:	%{name}-conf.patch
Patch11:	%{name}-dictname.patch
URL:		http://www.postfix.org/
%{?with_sasl:BuildRequires:	cyrus-sasl-devel}
BuildRequires:	db-devel
# getifaddrs() with IPv6 support
BuildRequires:	glibc-devel >= 6:2.3.4
%{?with_mysql:BuildRequires:	mysql-devel}
%{?with_ldap:BuildRequires:	openldap-devel >= 2.3.0}
%{?with_ssl:BuildRequires:	openssl-devel >= 0.9.7l}
BuildRequires:	pcre-devel
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
%{?with_cdb:BuildRequires:	tinycdb-devel}
%{?with_mysql:BuildRequires:	zlib-devel}
Requires(post):	/bin/hostname
Requires(post,postun):	/sbin/ldconfig
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	/sbin/chkconfig
Requires:	diffutils
Requires:	findutils
Requires:	rc-scripts
Requires:	sed
%{?with_cdb:Requires:tinycdb}
Suggests:	cyrus-sasl-saslauthd
Provides:	group(postfix)
Provides:	smtpdaemon
Provides:	user(postfix)
Obsoletes:	smtpdaemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Postfix is attempt to provide an alternative to the widely-used
Sendmail program. Postfix attempts to be fast, easy to administer, and
hopefully secure, while at the same time being sendmail compatible
enough to not upset your users. This version has IPv6 support.

%description -l es.UTF-8
Postfix es una alternativa para el mundialmente utilizado sendmail. Si
desea tener un servidor SMTP *rápido*, debe instalar este paquete.

%description -l fr.UTF-8
Postfix (voir http://www.postfix.org/) se veut une alternative à
sendmail, responsable de l'acheminement de 70% des courriers
électroniques sur Internet. IBM en a suppotré le développement, mais
ne contrôle pas son évolution. Le but est d'installer Postfix sur le
plus grand nombre de systèmes possible. Dans cette optique, il a été
écrit pour être totalement sous le contrôle de l'utilisateur.

%description -l it.UTF-8
Postfix (http://www.postfix.org/) e' un'alternativa al programma
sendmail utilizzato per la gestione del 70 per cento della posta
Internet.

Seppur IBM supporti lo sviluppo di Postfix, non controlla la sua
evoluzione.

Consultate la pagine web http://www.moongroup.com/how-to.phtml nella
quale troverete le indicazioni per una corretta installazione e
configurazione di questo programma.

%description -l pl.UTF-8
Postfix jest próbą dostarczenia alternatywnego MTA w stosunku do
szeroko używanego sendmaila. Postfix w zamierzeniu ma być szybki,
łatwy w administrowaniu, bezpieczny oraz ma być na tyle kompatybilny z
sendmailem by nie denerwować użytkowników. Ta wersja obsługuje IPv6.

%description -l pt_BR.UTF-8
O Postfix é uma alternativa para o mundialmente utilizado sendmail. Se
você deseja um servidor SMTP *rápido*, instale este pacote.

%description -l sk.UTF-8
Postfix (pozri http://www.postfix.org/) má za cieľ byť alternatívou k
široko rozšírenému programu sendmail, zodpovednému za 70% všetkej
elektronickej pošty doručenej na Internete.

Aj keď IBM podporovala vývoj Postfixu, zdržiava sa vplyvu na jeho
vývoj. Cieľom je inštalácia Postfixu na čo najväčšom počte systémov.
Do tohoto momentu je softvér poskytovaný bez ovplyvňovania, takže sa
môže vyvíjať podľa jeho používateľov.

Určite si prečítajte http://www.moongroup.com/how-to.phtml, kde sú
popísané kroky potrebné pred a po inštalácii Postfixu.

%package devel
Summary:	Postfix loadable modules development package
Summary(pl.UTF-8):	Pakiet dla programistów ładowanych modułów do postfiksa
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Header files to build additional map types for Postfix.

%description devel -l pl.UTF-8
Pliki nagłówkowe do tworzenia dodatkowych typów map dla Postfiksa.

%package dict-ldap
Summary:	LDAP map support for Postfix
Summary(pl.UTF-8):	Obsługa map LDAP dla Postfiksa
Group:		Networking/Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	openldap >= 2.3.0

%description dict-ldap
This package provides support for LDAP maps in Postfix.

%description dict-ldap -l pl.UTF-8
Ten pakiet dodaje obsługę map LDAP do Postfiksa.

%package dict-mysql
Summary:	MySQL map support for Postfix
Summary(pl.UTF-8):	Obsługa map MySQL dla Postfiksa
Group:		Networking/Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description dict-mysql
This package provides support for MySQL maps in Postfix.

%description dict-mysql -l pl.UTF-8
Ten pakiet dodaje obsługę map MySQL do Postfiksa.

%package dict-pcre
Summary:	PCRE map support for Postfix
Summary(pl.UTF-8):	Obsługa map PCRE dla Postfiksa
Group:		Networking/Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description dict-pcre
This package provides support for PCRE maps in Postfix.

%description dict-pcre -l pl.UTF-8
Ten pakiet dodaje obsługę map PCRE do Postfiksa.

%package dict-pgsql
Summary:	PostgreSQL map support for Postfix
Summary(pl.UTF-8):	Obsługa map PostgreSQL dla Postfiksa
Group:		Networking/Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description dict-pgsql
This package provides support for PostgreSQL maps in Postfix.

%description dict-pgsql -l pl.UTF-8
Ten pakiet dodaje obsługę map PostgreSQL do Postfiksa.

%package qshape
Summary:	qshape - Print Postfix queue domain and age distribution
Group:		Networking/Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description qshape
The qshape program helps the administrator understand the Postfix
queue message distribution in time and by sender domain or recipient
domain. The program needs read access to the queue directories and
queue files, so it must run as the superuser or the mail_owner
specified in main.cf (typically postfix).

%prep
%setup -q
%{?with_vda:zcat %{SOURCE7} | patch -p1 -s}
%patch0 -p1
%patch1 -p0
%patch2 -p1
%patch3 -p1
%{?with_hir:%patch4 -p0}
#%{?with_polish:%patch5 -p1}
#%patch6 -p1
#%patch7 -p1 --obsolete ?
%patch8 -p1
sed -i '/scache_clnt_create/s/server/var_scache_service/' src/global/scache_clnt.c
%if "%{_lib}" == "lib64"
%patch9 -p1
%endif
%patch10 -p1
%patch11 -p1

%if %{with tcp}
sed -i 's/ifdef SNAPSHOT/if 1/' src/util/dict_open.c
%endif

%build
%{__make} -f Makefile.init makefiles
%{__make} tidy
%{__make} \
	CC="%{__cc}" \
	DEBUG="" \
	OPT="%{rpmcflags} -D_FILE_OFFSET_BITS=64" \
	%{!?with_ldap:LDAPSO=""} \
	%{!?with_mysql:MYSQLSO=""} \
	%{!?with_pgsql:PGSQLSO=""} \
	CCARGS="" \
	AUXLIBS="-ldb -lresolv %{?with_sasl:-lsasl} %{?with_ssl:-lssl -lcrypto} %{?with_cdb:-lcdb} -lpcre %{?with_ldap:-lldap -llber} %{?with_pgsql:-lpq} %{?with_mysql:-lmysqlclient -lz}"


#	CCARGS="%{?with_ldap:-DHAS_LDAP} -DHAS_PCRE %{?with_sasl:-DUSE_SASL_AUTH -DUSE_CYRUS_SASL -I/usr/include/sasl} %{?with_mysql:-DHAS_MYSQL -I/usr/include/mysql} %{?with_pgsql:-DHAS_PGSQL -I/usr/include/postgresql} %{?with_ssl:-DUSE_TLS -I/usr/include/openssl} -DMAX_DYNAMIC_MAPS %{?with_cdb:-DHAS_CDB} -DHAVE_GETIFADDRS" \

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{cron.daily,rc.d/init.d,sysconfig,pam.d,security} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{mail,sasl} \
	$RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir}/postfix,%{_prefix}/lib}\
	$RPM_BUILD_ROOT{%{_includedir}/postfix,%{_mandir}/man{1,5,8}} \
	$RPM_BUILD_ROOT%{_var}/spool/postfix/{active,corrupt,deferred,maildrop,private,saved,bounce,defer,incoming,pid,public}

rm -f {html,man}/Makefile.in conf/{LICENSE,main.cf.default}

install bin/* $RPM_BUILD_ROOT%{_sbindir}
install libexec/* $RPM_BUILD_ROOT%{_libdir}/postfix
ln $RPM_BUILD_ROOT%{_libdir}/postfix/smtp $RPM_BUILD_ROOT%{_libdir}/postfix/lmtp
ln $RPM_BUILD_ROOT%{_libdir}/postfix/qmgr $RPM_BUILD_ROOT%{_libdir}/postfix/nqmgr
install conf/* $RPM_BUILD_ROOT%{_sysconfdir}/mail
sed -e's,^daemon_directory = .*,daemon_directory = %{_libdir}/postfix,' \
	conf/main.cf > $RPM_BUILD_ROOT%{_sysconfdir}/mail/main.cf

for f in dns global master util ; do
	install lib/lib${f}.a $RPM_BUILD_ROOT%{_libdir}/libpostfix-${f}.so.1
	ln -sf lib${f}.so.1 $RPM_BUILD_ROOT%{_libdir}/libpostfix-${f}.so
done
install lib/dict*.so $RPM_BUILD_ROOT%{_libdir}/postfix
install include/*.h $RPM_BUILD_ROOT%{_includedir}/postfix

tar cf - -C man . | tar xf - -C $RPM_BUILD_ROOT%{_mandir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/mail/aliases
install %{SOURCE2} $RPM_BUILD_ROOT/etc/cron.daily/postfix
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/postfix
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/postfix
install %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/sasl/smtpd.conf
install %{SOURCE6} $RPM_BUILD_ROOT/etc/pam.d/smtp
install auxiliary/rmail/rmail $RPM_BUILD_ROOT%{_bindir}/rmail
install auxiliary/qshape/qshape.pl $RPM_BUILD_ROOT%{_bindir}/qshape

ln -sf %{_sbindir}/sendmail $RPM_BUILD_ROOT%{_bindir}/mailq
ln -sf %{_sbindir}/sendmail $RPM_BUILD_ROOT%{_bindir}/newaliases
ln -sf %{_sbindir}/sendmail $RPM_BUILD_ROOT/usr/lib/sendmail

touch $RPM_BUILD_ROOT%{_sysconfdir}/mail/\
	{aliases,access,canonical,relocated,transport,virtual}{,.db}

touch $RPM_BUILD_ROOT/etc/security/blacklist.smtp

> $RPM_BUILD_ROOT/var/spool/postfix/.nofinger

rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/mail/makedefs.out $RPM_BUILD_ROOT%{_mandir}/cat*

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 62 postfix
%groupadd -g 63 maildrop
%useradd -u 62 -d /var/spool/postfix -s /bin/false -c "Postfix User" -g postfix postfix

%post
/sbin/ldconfig
if ! grep -q "^postmaster:" %{_sysconfdir}/mail/aliases; then
echo "Adding Entry for postmaster in %{_sysconfdir}/mail/aliases" >&2
echo "postmaster: root" >>%{_sysconfdir}/mail/aliases
fi
if [ "$1" = "1" ]; then
	# only on installation, not upgrade
	if ! grep -q "^myhostname" %{_sysconfdir}/mail/main.cf; then
		postconf -e myhostname=`/bin/hostname -f`
	fi
else
	postfix upgrade-configuration
fi

newaliases
/sbin/chkconfig --add postfix
%service postfix restart "postfix daemon"

%preun
if [ "$1" = "0" ]; then
	%service postfix stop
	/sbin/chkconfig --del postfix
fi

%postun
/sbin/ldconfig
if [ "$1" = "0" ]; then
	%groupremove maildrop
	%userremove postfix
	%groupremove postfix
fi

%files
%defattr(644,root,root,755)
%doc html *README COMPATIBILITY HISTORY LICENSE RELEASE_NOTES TLS_*
%doc README_FILES/*README
%doc examples/smtpd-policy
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mail/access
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mail/aliases
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mail/canonical
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mail/generic
#%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mail/pcre_table
#%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mail/regexp_table
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mail/relocated
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mail/transport
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mail/virtual
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mail/header_checks
#%ghost %{_sysconfdir}/mail/*.db
%dir %{_sysconfdir}/mail
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mail/dynamicmaps.cf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mail/main.cf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mail/master.cf
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mail/postfix-script
%attr(755,root,root) %{_sysconfdir}/mail/post-install
%{_sysconfdir}/mail/postfix-files
%attr(740,root,root) /etc/cron.daily/postfix
%attr(754,root,root) /etc/rc.d/init.d/postfix
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/postfix
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/smtp
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/security/blacklist.smtp
%{?with_sasl:%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sasl/smtpd.conf}
%attr(755,root,root) %{_libdir}/libpostfix-*.so.*
%attr(755,root,root) %{_bindir}/mailq
%attr(755,root,root) %{_bindir}/newaliases
%attr(755,root,root) %{_bindir}/rmail
%attr(755,root,root) %{_sbindir}/s*
%attr(755,root,root) %{_sbindir}/postfix
%attr(755,root,root) %{_sbindir}/postalias
%attr(755,root,root) %{_sbindir}/postkick
%attr(755,root,root) %{_sbindir}/postl*
%attr(755,root,root) %{_sbindir}/postc*
%attr(755,root,root) %{_sbindir}/postmap
%attr(2755,root,maildrop) %{_sbindir}/postqueue
%attr(755,root,root) %{_sbindir}/postsuper
%attr(2755,root,maildrop) %{_sbindir}/postdrop
%attr(755,root,root) %{_sbindir}/qmqp-sink
%attr(755,root,root) %{_sbindir}/qmqp-source
%attr(755,root,root) /usr/lib/sendmail
%dir %{_libdir}/postfix
%attr(755,root,root) %{_libdir}/postfix/[!d]*
%attr(755,root,root) %{_libdir}/postfix/discard
%attr(755,root,root) %dir %{_var}/spool/postfix
%attr(700,postfix,root) %dir %{_var}/spool/postfix/active
%attr(700,postfix,root) %dir %{_var}/spool/postfix/bounce
%attr(700,postfix,root) %dir %{_var}/spool/postfix/corrupt
%attr(700,postfix,root) %dir %{_var}/spool/postfix/defer
%attr(700,postfix,root) %dir %{_var}/spool/postfix/deferred
%attr(700,postfix,root) %dir %{_var}/spool/postfix/incoming
%attr(1730,postfix,maildrop) %dir %{_var}/spool/postfix/maildrop
%attr(755,postfix,root) %dir %{_var}/spool/postfix/pid
%attr(700,postfix,root) %dir %{_var}/spool/postfix/private
%attr(710,postfix,maildrop) %dir %{_var}/spool/postfix/public
%attr(700,postfix,root) %dir %{_var}/spool/postfix/saved
%attr(644,postfix,root) %{_var}/spool/postfix/.nofinger
%{_mandir}/man*/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpostfix-*.so
%{_includedir}/postfix

%if %{with ldap}
%files dict-ldap
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/postfix/dict_ldap.so
%endif

%if %{with mysql}
%files dict-mysql
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/postfix/dict_mysql.so
%endif

%files dict-pcre
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/postfix/dict_pcre.so

%if %{with pgsql}
%files dict-pgsql
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/postfix/dict_pgsql.so
%endif

%files qshape
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qshape
