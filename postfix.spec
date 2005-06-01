#
# Conditional build:
%bcond_without	ldap	# without LDAP map module
%bcond_without	mysql	# without MySQL map module
%bcond_without	pgsql	# without PostgreSQL map module
%bcond_without	sasl	# without SMTP AUTH support
%bcond_without	ssl	# without SSL/TLS support
%bcond_without	cdb	# without cdb map support
%bcond_with	vda	# with VDA patch
%bcond_with	hir	# with Beeth's header_if_reject patch
#%bcond_with	polish	# with double English+Polish messages
#
# TODO:
#	- check/fix 'polish' bcond
#
Summary:	Postfix Mail Transport Agent
Summary(cs):	Postfix - program pro pøepravu po¹ty (MTA)
Summary(es):	Postfix - Un MTA (Mail Transport Agent) de alto desempeño
Summary(fr):	Agent de transport de courrier Postfix
Summary(pl):	Serwer SMTP Postfix
Summary(pt_BR):	Postfix - Um MTA (Mail Transport Agent) de alto desempenho
Summary(sk):	Agent prenosu po¹ty Postfix
Name:		postfix
Version:	2.2.3
Release:	1.1
Epoch:		2
Group:		Networking/Daemons
License:	distributable
Source0:	ftp://ftp.porcupine.org/mirrors/postfix-release/official/%{name}-%{version}.tar.gz
# Source0-md5:	f164b701c3e97b950d4cc64aff4de3c0
Source1:	%{name}.aliases
Source2:	%{name}.cron
Source3:	%{name}.init
Source4:	%{name}.sysconfig
Source5:	%{name}.sasl
Source6:	%{name}.pamd
Source7:	http://web.onda.com.br/nadal/postfix/VDA/%{name}-%{version}-vda.patch.gz
# Source7-md5:	fcc8b7e7d94a9ce2d97453da0e6cd7c9
Patch0:		%{name}-config.patch
Patch1:		%{name}-conf_msg.patch
Patch2:		%{name}-dynamicmaps.patch
Patch3:		%{name}-master.cf_cyrus.patch
# from http://akson.sgh.waw.pl/~chopin/unix/postfix-2.1.5-header_if_reject.diff
Patch4:		%{name}-header_if_reject.patch
#Patch5:	%{name}-pl.patch
Patch6:		%{name}-foreground.patch
URL:		http://www.postfix.org/
BuildRequires:	awk
%{?with_sasl:BuildRequires:	cyrus-sasl-devel}
BuildRequires:	db-devel
# getifaddrs() with IPv6 support
BuildRequires:	glibc-devel >= 6:2.3.4
BuildRequires:	grep
%{?with_mysql:BuildRequires:	mysql-devel}
%{?with_ldap:BuildRequires:	openldap-devel >= 2.2.0}
%{?with_ssl:BuildRequires:	openssl-devel >= 0.9.7d}
BuildRequires:	pcre-devel
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	rpmbuild(macros) >= 1.202
%{?with_cdb:BuildRequires:	tinycdb-devel}
PreReq:		rc-scripts
PreReq:		sed
Requires(post):	/bin/hostname
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(post,preun):	/sbin/chkconfig
Requires(post,postun):	/sbin/ldconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires:	diffutils
Requires:	findutils
%{?with_cdb:Requires:tinycdb}
Provides:	group(postfix)
Provides:	smtpdaemon
Provides:	user(postfix)
Obsoletes:	courier
Obsoletes:	exim
Obsoletes:	masqmail
Obsoletes:	nullmailer
Obsoletes:	omta
Obsoletes:	qmail
Obsoletes:	sendmail
Obsoletes:	sendmail-cf
Obsoletes:	sendmail-doc
Obsoletes:	smail
Obsoletes:	smtpdaemon
Obsoletes:	ssmtp
Obsoletes:	zmailer
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Postfix is attempt to provide an alternative to the widely-used
Sendmail program. Postfix attempts to be fast, easy to administer, and
hopefully secure, while at the same time being sendmail compatible
enough to not upset your users. This version has IPv6 support.

%description -l pt_BR
O Postfix é uma alternativa para o mundialmente utilizado sendmail. Se
você deseja um servidor SMTP *rápido*, instale este pacote.

%description -l es
Postfix es una alternativa para el mundialmente utilizado sendmail. Si
desea tener un servidor SMTP *rápido*, debe instalar este paquete.

%description -l fr
Postfix (voir http://www.postfix.org/) se veut une alternative à
sendmail, responsable de l'acheminement de 70% des courriers
électroniques sur Internet. IBM en a suppotré le développement, mais
ne contrôle pas son évolution. Le but est d'installer Postfix sur le
plus grand nombre de systèmes possible. Dans cette optique, il a été
écrit pour être totalement sous le contrôle de l'utilisateur.

%description -l it
Postfix (http://www.postfix.org/) e' un'alternativa al programma
sendmail utilizzato per la gestione del 70 per cento della posta
Internet.

Seppur IBM supporti lo sviluppo di Postfix, non controlla la sua
evoluzione.

Consultate la pagine web http://www.moongroup.com/how-to.phtml nella
quale troverete le indicazioni per una corretta installazione e
configurazione di questo programma.

%description -l pl
Postfix jest prób± dostarczenia alternatywnego MTA w stosunku do
szeroko u¿ywanego sendmaila. Postfix w zamierzeniu ma byæ szybki,
³atwy w administrowaniu, bezpieczny oraz ma byæ na tyle kompatybilny z
sendmailem by nie denerwowaæ u¿ytkowników. Ta wersja obs³uguje IPv6.

%description -l pt_BR
O Postfix é uma alternativa para o mundialmente utilizado sendmail. Se
você deseja um servidor SMTP *rápido*, instale este pacote.

%description -l sk
Postfix (pozri http://www.postfix.org/) má za cieµ by» alternatívou k
¹iroko roz¹írenému programu sendmail, zodpovednému za 70% v¹etkej
elektronickej po¹ty doruèenej na Internete.

Aj keï IBM podporovala vývoj Postfixu, zdr¾iava sa vplyvu na jeho
vývoj. Cieµom je in¹talácia Postfixu na èo najväè¹om poète systémov.
Do tohoto momentu je softvér poskytovaný bez ovplyvòovania, tak¾e sa
mô¾e vyvíja» podµa jeho pou¾ívateµov.

Urèite si preèítajte http://www.moongroup.com/how-to.phtml, kde sú
popísané kroky potrebné pred a po in¹talácii Postfixu.

%package devel
Summary:	Postfix loadable modules development package
Summary(pl):	Pakiet dla programistów ³adowanych modu³ów do postfiksa
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Header files to build additional map types for Postfix.

%description devel -l pl
Pliki nag³ówkowe do tworzenia dodatkowych typów map dla Postfiksa.

%package dict-ldap
Summary:	LDAP map support for Postfix
Summary(pl):	Obs³uga map LDAP dla Postfiksa
Group:		Networking/Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	openldap >= 2.2.0

%description dict-ldap
This package provides support for LDAP maps in Postfix.

%description dict-ldap -l pl
Ten pakiet dodaje obs³ugê map LDAP do Postfiksa.

%package dict-mysql
Summary:	MySQL map support for Postfix
Summary(pl):	Obs³uga map MySQL dla Postfiksa
Group:		Networking/Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description dict-mysql
This package provides support for MySQL maps in Postfix.

%description dict-mysql -l pl
Ten pakiet dodaje obs³ugê map MySQL do Postfiksa.

%package dict-pcre
Summary:	PCRE map support for Postfix
Summary(pl):	Obs³uga map PCRE dla Postfiksa
Group:		Networking/Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description dict-pcre
This package provides support for PCRE maps in Postfix.

%description dict-pcre -l pl
Ten pakiet dodaje obs³ugê map PCRE do Postfiksa.

%package dict-pgsql
Summary:	PostgreSQL map support for Postfix
Summary(pl):	Obs³uga map PostgreSQL dla Postfiksa
Group:		Networking/Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description dict-pgsql
This package provides support for PostgreSQL maps in Postfix.

%description dict-pgsql -l pl
Ten pakiet dodaje obs³ugê map PostgreSQL do Postfiksa.

%prep
%setup -q
%{?with_vda:zcat %{SOURCE7} | patch -p1 -s}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%{?with_hir:%patch4 -p0}
#%{?with_polish:%patch5 -p1}
%patch6 -p1

%build
%{__make} -f Makefile.init makefiles
%{__make} tidy
%{__make} \
	DEBUG="" \
	OPT="%{rpmcflags}" \
	%{!?with_ldap:LDAPSO=""} \
	%{!?with_mysql:MYSQLSO=""} \
	%{!?with_pgsql:PGSQLSO=""} \
	CCARGS="%{?with_ldap:-DHAS_LDAP} -DHAS_PCRE %{?with_sasl:-DUSE_SASL_AUTH -I/usr/include/sasl} %{?with_mysql:-DHAS_MYSQL -I/usr/include/mysql} %{?with_pgsql:-DHAS_PGSQL -I/usr/include/postgresql} %{?with_ssl:-DUSE_TLS -I/usr/include/openssl} -DMAX_DYNAMIC_MAPS %{?with_cdb:-DHAS_CDB} -DHAVE_GETIFADDRS" \
	AUXLIBS="-ldb -lresolv %{?with_sasl:-lsasl} %{?with_ssl:-lssl -lcrypto} %{?with_cdb:-lcdb}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{cron.daily,rc.d/init.d,sysconfig,pam.d} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{mail,sasl} \
	$RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir}/postfix,/usr/lib}\
	$RPM_BUILD_ROOT{%{_includedir}/postfix,%{_mandir}/man{1,5,8}} \
	$RPM_BUILD_ROOT%{_var}/spool/postfix/{active,corrupt,deferred,maildrop,private,saved,bounce,defer,incoming,pid,public}

rm -f {html,man}/Makefile.in conf/{LICENSE,main.cf.default}

install bin/* $RPM_BUILD_ROOT%{_sbindir}
install libexec/* $RPM_BUILD_ROOT%{_libdir}/postfix
install conf/* $RPM_BUILD_ROOT%{_sysconfdir}/mail
sed -e's,^daemon_directory = .*,daemon_directory = %{_libdir}/postfix,' \
	conf/main.cf > $RPM_BUILD_ROOT%{_sysconfdir}/mail/main.cf

for f in dns global master util ; do
	install lib/lib${f}.a $RPM_BUILD_ROOT%{_libdir}/libpostfix-${f}.so.1
	ln -sf lib${f}.so.1 $RPM_BUILD_ROOT%{_libdir}/libpostfix-${f}.so
done
install lib/dict*.so $RPM_BUILD_ROOT%{_libdir}/postfix
install include/*.h $RPM_BUILD_ROOT%{_includedir}/postfix

(cd man; tar cf - .) | (cd $RPM_BUILD_ROOT%{_mandir}; tar xf -)

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/mail/aliases
install %{SOURCE2} $RPM_BUILD_ROOT/etc/cron.daily/postfix
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/postfix
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/postfix
install %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/sasl/smtpd.conf
install %{SOURCE6} $RPM_BUILD_ROOT/etc/pam.d/smtp
install auxiliary/rmail/rmail $RPM_BUILD_ROOT%{_bindir}/rmail

ln -sf /usr/sbin/sendmail $RPM_BUILD_ROOT%{_bindir}/mailq
ln -sf /usr/sbin/sendmail $RPM_BUILD_ROOT%{_bindir}/newaliases
ln -sf /usr/sbin/sendmail $RPM_BUILD_ROOT/usr/lib/sendmail

touch $RPM_BUILD_ROOT%{_sysconfdir}/mail/\
	{aliases,access,canonical,relocated,transport,virtual}{,.db}

> $RPM_BUILD_ROOT/var/spool/postfix/.nofinger

rm -rf $RPM_BUILD_ROOT/etc/mail/makedefs.out $RPM_BUILD_ROOT/usr/share/man/cat*

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 62 postfix
%groupadd -g 63 maildrop
%useradd -u 62 -d /var/spool/postfix -s /bin/false -c "Postfix User" -g postfix postfix

%post
/sbin/ldconfig
if ! grep -q "^postmaster:" /etc/mail/aliases; then
	echo "Adding Entry for postmaster in /etc/mail/aliases" >&2
	echo "postmaster:	root" >>/etc/mail/aliases
fi
if [ "$1" = "1" ]; then
	# only on installation, not upgrade
	if ! grep -q "^myhostname" /etc/mail/main.cf; then
		postconf -e myhostname=`/bin/hostname -f`
	fi
else
	postfix upgrade-configuration
fi

newaliases
/sbin/chkconfig --add postfix
if [ -f /var/lock/subsys/postfix ]; then
	/etc/rc.d/init.d/postfix restart >&2
else
	echo "Run \"/etc/rc.d/init.d/postfix start\" to start postfix daemon." >&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/postfix ]; then
		/etc/rc.d/init.d/postfix stop >&2
	fi
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
%config(noreplace) %verify(not md5 size mtime) /etc/pam.d/smtp
%{?with_sasl:%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sasl/smtpd.conf}
%attr(755,root,root) %{_libdir}/libpostfix-*.so.*
%attr(755,root,root) %{_bindir}/*
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
