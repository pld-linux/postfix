#
# Conditional build:
# --without sasl - build without SMTP AUTH support
# --without ssl  - build without SSL/TLS support
# --without ipv6 - build without IPv6 support
# --with polish  - build with polish messages support
# _without_psql  - no Postgres support
# _without_mysql - no MySQL support
# _without_ldap  - no LDAP support
#
%define	tls_ver 0.8.11a-1.1.11-0.9.6d
Summary:	Postfix Mail Transport Agent
Summary(cs):	Postfix - program pro p�epravu po�ty (MTA)
Summary(es):	Postfix - Un MTA (Mail Transport Agent) de alto desempe�o
Summary(fr):	Agent de transport de courrier Postfix
Summary(pl):	Serwer SMTP Postfix
Summary(pt_BR):	Postfix - Um MTA (Mail Transport Agent) de alto desempenho
Summary(sk):	Agent prenosu po�ty Postfix
Name:		postfix
Version:	1.1.11
Release:	9
Epoch:		2
Group:		Networking/Daemons
License:	distributable
Source0:	ftp://ftp.porcupine.org/mirrors/postfix-release/official/%{name}-%{version}.tar.gz
Source1:	%{name}.aliases
Source2:	%{name}.cron
Source3:	%{name}.init
Source5:	%{name}.sysconfig
Source6:	ftp://ftp.aet.tu-cottbus.de/pub/pfixtls/pfixtls-%{tls_ver}.tar.gz
Source7:	%{name}.sasl
Patch0:		%{name}-config.patch
Patch1:		%{name}-conf_msg.patch
Patch2:		%{name}-dynamicmaps.patch
Patch3:		%{name}-pgsql.patch
Patch4:		%{name}-master.cf_cyrus.patch
Patch5:		%{name}-ipv6.patch
Patch6:		%{name}-pl.patch
Patch7:		%{name}-db.patch
URL:		http://www.postfix.org/
BuildRequires:	awk
%{!?_without_sasl:BuildRequires:	cyrus-sasl-devel}
BuildRequires:	db-devel
BuildRequires:	grep
%{!?_without_ipv6:BuildRequires:	libinet6 >= 0.20010420-3}
%{!?_without_mysql:BuildRequires:	mysql-devel}
%{!?_without_ldap:BuildRequires:	openldap-devel >= 2.0.0}
%{!?_without_ssl:BuildRequires:	openssl-devel >= 0.9.6a}
BuildRequires:	pcre-devel
%{!?_without_psql:BuildRequires:	postgresql-devel}
PreReq:		rc-scripts
PreReq:		sed
Requires(pre):	/usr/sbin/useradd
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/bin/getgid
Requires(pre):	/bin/id
Requires(post):	/bin/hostname
Requires(post,postun):/sbin/ldconfig
Requires(post,preun):/sbin/chkconfig
Requires(postun):	/usr/sbin/userdel
Requires(postun):	/usr/sbin/groupdel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Provides:	smtpdaemon
Obsoletes:	smtpdaemon
Obsoletes:	exim
Obsoletes:	masqmail
Obsoletes:	omta
Obsoletes:	qmail
Obsoletes:	sendmail
Obsoletes:	sendmail-cf
Obsoletes:	sendmail-doc
Obsoletes:	smail
Obsoletes:	zmailer
Requires:	diffutils
Requires:	findutils

%description
Postfix is attempt to provide an alternative to the widely-used
Sendmail program. Postfix attempts to be fast, easy to administer, and
hopefully secure, while at the same time being sendmail compatible
enough to not upset your users. This version has IPv6 support.

%description -l pt_BR
O Postfix � uma alternativa para o mundialmente utilizado sendmail. Se
voc� deseja um servidor SMTP *r�pido*, instale este pacote.

%description -l es
Postfix es una alternativa para el mundialmente utilizado sendmail. Si
desea tener un servidor SMTP *r�pido*, debe instalar este paquete.

%description -l fr
Postfix (voir http://www.postfix.org/) se veut une alternative �
sendmail, responsable de l'acheminement de 70% des courriers
�lectroniques sur Internet. IBM en a suppotr� le d�veloppement, mais
ne contr�le pas son �volution. Le but est d'installer Postfix sur le
plus grand nombre de syst�mes possible. Dans cette optique, il a �t�
�crit pour �tre totalement sous le contr�le de l'utilisateur.

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
Postfix jest pr�b� dostarczenia alternatywnego MTA w stosunku do
szeroko u�ywanego sendmaila. Postfix w zamierzeniu ma by� szybki,
�atwy w administrowaniu, bezpieczny oraz ma by� na tyle kompatybilny z
sendmailem by nie denerwowa� Twoich u�ytkownik�w. Ta wersja wspiera
IPv6.

%description -l pt_BR
O Postfix � uma alternativa para o mundialmente utilizado sendmail. Se
voc� deseja um servidor SMTP *r�pido*, instale este pacote.

%description -l sk
Postfix (pozri http://www.postfix.org/) m� za cie� by� alternat�vou k
�iroko roz��ren�mu programu sendmail, zodpovedn�mu za 70% v�etkej
elektronickej po�ty doru�enej na Internete.

Aj ke� IBM podporovala v�voj Postfixu, zdr�iava sa vplyvu na jeho
v�voj. Cie�om je in�tal�cia Postfixu na �o najv��om po�te syst�mov.
Do tohoto momentu je softv�r poskytovan� bez ovplyv�ovania, tak�e sa
m��e vyv�ja� pod�a jeho pou��vate�ov.

Ur�ite si pre��tajte http://www.moongroup.com/how-to.phtml, kde s�
pop�san� kroky potrebn� pred a po in�tal�cii Postfixu.

%package devel
Summary:	Postfix loadable modules development package
Summary(pl):	Pakiet dla programist�w �adowanych modu��w do postfiksa
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Header files to build additional map types for Postfix.

%description devel -l pl
Pliki nag��wkowe do tworzenia dodatkowych typ�w map dla Postfiksa.

%package dict-ldap
Summary:	LDAP map support for Postfix
Summary(pl):	Obs�uga map LDAP dla Postfiksa
Group:		Networking/Daemons
Requires:	%{name} = %{version}
Requires:	openldap >= 2.0.0

%description dict-ldap
This package provides support for LDAP maps in Postfix.

%description dict-ldap -l pl
Ten pakiet dodaje obs�ug� map LDAP do Postfiksa.

%package dict-mysql
Summary:	MySQL map support for Postfix
Summary(pl):	Obs�uga map MySQL dla Postfiksa
Group:		Networking/Daemons
Requires:	%{name} = %{version}

%description dict-mysql
This package provides support for MySQL maps in Postfix.

%description dict-mysql -l pl
Ten pakiet dodaje obs�ug� map MySQL do Postfiksa.

%package dict-pcre
Summary:	PCRE map support for Postfix
Summary(pl):	Obs�uga map PCRE dla Postfiksa
Group:		Networking/Daemons
Requires:	%{name} = %{version}

%description dict-pcre
This package provides support for PCRE maps in Postfix.

%description dict-pcre -l pl
Ten pakiet dodaje obs�ug� map PCRE do Postfiksa.

%package dict-pgsql
Summary:	PostgreSQL map support for Postfix
Summary(pl):	Obs�uga map PostgreSQL dla Postfiksa
Group:		Networking/Daemons
Requires:	%{name} = %{version}

%description dict-pgsql
This package provides support for PostgreSQL maps in Postfix.

%description dict-pgsql -l pl
Ten pakiet dodaje obs�ug� map PostgreSQL do Postfiksa.

%prep
%setup -q -a6
%patch0 -p1
patch -p1 -s <pfixtls-%{tls_ver}/pfixtls.diff
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%{!?_without_ipv6:%patch5 -p1}
%{?_with_polish:%patch6 -p1}
%patch7 -p1

%build
%{__make} -f Makefile.init makefiles
%{__make} tidy
%{__make} DEBUG="" OPT="%{rpmcflags}" \
	CCARGS="%{!?_without_ldap:-DHAS_LDAP} -DHAS_PCRE %{!?_without_sasl:-DUSE_SASL_AUTH} %{!?_without_mysql:-DHAS_MYSQL} %{!?_without_psql:-DHAS_PGSQL} %{!?_without_mysql:-I%{_includedir}/mysql} %{!?_without_psql:-I%{_includedir}/postgresql} %{!?_without_ssl:-DHAS_SSL -I%{_includedir}/openssl} -DMAX_DYNAMIC_MAPS" \
	AUXLIBS="-ldb -lresolv %{!?_without_sasl:-lsasl} %{!?_without_ssl:-lssl -lcrypto}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{mail,cron.daily,rc.d/init.d,sasl,sysconfig} \
	$RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir}/postfix,%{_includedir}/postfix,%{_mandir}/man{1,5,8}} \
	$RPM_BUILD_ROOT%{_var}/spool/postfix/{active,corrupt,deferred,maildrop,private,saved,bounce,defer,incoming,pid,public} \
	pfixtls

rm -f {html,man}/Makefile.in conf/{LICENSE,main.cf.default}

install -d sample-conf; mv -f conf/sample* sample-conf/ || :

install bin/* $RPM_BUILD_ROOT%{_sbindir}
install libexec/* $RPM_BUILD_ROOT%{_libdir}/postfix
install conf/* $RPM_BUILD_ROOT%{_sysconfdir}/mail

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
install %{SOURCE5} $RPM_BUILD_ROOT/etc/sysconfig/postfix
install %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/sasl/smtpd.conf
install auxiliary/rmail/rmail $RPM_BUILD_ROOT%{_bindir}/rmail

ln -sf /usr/sbin/sendmail $RPM_BUILD_ROOT%{_bindir}/mailq
ln -sf /usr/sbin/sendmail $RPM_BUILD_ROOT%{_bindir}/newaliases
ln -sf /usr/sbin/sendmail $RPM_BUILD_ROOT%{_libdir}/sendmail

touch $RPM_BUILD_ROOT%{_sysconfdir}/mail/\
	{aliases,access,canonical,relocated,transport,virtual}{,.db}

> $RPM_BUILD_ROOT/var/spool/postfix/.nofinger

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`/usr/bin/getgid postfix`" ]; then
	if [ "`getgid postfix`" != "62" ]; then
		echo "Error: group postfix doesn't have gid=62. Correct this before installing postfix." 1>&2
		exit 1
	fi
else
	/usr/sbin/groupadd -g 62 -r -f postfix
fi
if [ -n "`/usr/bin/getgid maildrop`" ]; then
	if [ "`/usr/bin/getgid maildrop`" != "63" ]; then
		echo "Error: group maildrop doesn't have gid=63. Correct this before installing postfix." 1>&2
		exit 1
	fi
else
	/usr/sbin/groupadd -g 63 -r -f maildrop
fi
if [ -n "`/bin/id -u postfix 2>/dev/null`" ]; then
	if [ "`/bin/id -u postfix`" != "62" ]; then
		echo "Error: user postfix doesn't have uid=62. Correct this before installing postfix." 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -u 62 -r -d /var/spool/postfix -s /bin/false -c "Postfix User" -g postfix postfix 1>&2
fi

%post
/sbin/ldconfig
if ! grep -q "^postmaster:" /etc/mail/aliases; then
	echo "Adding Entry for postmaster in /etc/mail/aliases" >&2
	echo "postmaster:	root" >>/etc/mail/aliases
fi
if ! grep -q "^myhostname" /etc/mail/main.cf; then
	postconf -e myhostname=`/bin/hostname -f`
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
	/usr/sbin/groupdel maildrop 2> /dev/null
	/usr/sbin/userdel postfix 2> /dev/null
	/usr/sbin/groupdel postfix 2> /dev/null
fi

%triggerpostun -- postfix < 1:1.1.2
sed -e 's/^\(pickup[ 	]\+fifo[ 	]\+[^ 	]\+[ 	]\+\)[^ 	]\+\([ 	]\)/\1-\2/;
s/^\(cleanup[ 	]\+unix[ 	]\+\)[^ 	]\+\([ 	]\)/\1n\2/' /etc/mail/master.cf \
	> /etc/mail/master.cf.rpmtmp
mv -f /etc/mail/master.cf.rpmtmp /etc/mail/master.cf

%files
%defattr(644,root,root,755)
%doc html *README COMPATIBILITY HISTORY LICENSE RELEASE_NOTES
%doc README_FILES/*README
%doc sample-conf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mail/access
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mail/aliases
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mail/canonical
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mail/relocated
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mail/transport
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mail/virtual
#%ghost %{_sysconfdir}/mail/*.db
%dir %{_sysconfdir}/mail
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mail/dynamicmaps.cf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mail/main.cf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mail/master.cf
%attr(755,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mail/postfix-script
%attr(755,root,root) %{_sysconfdir}/mail/post-install
%{_sysconfdir}/mail/postfix-files
%attr(740,root,root) /etc/cron.daily/postfix
%attr(754,root,root) /etc/rc.d/init.d/postfix
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/postfix
%{!?_without_sasl:%config(noreplace) %verify(not size mtime md5) /etc/sasl/smtpd.conf}
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
%attr(755,root,root) %{_sbindir}/qmqp-source
%attr(755,root,root) %{_libdir}/sendmail
%dir %{_libdir}/postfix
%attr(755,root,root) %{_libdir}/postfix/[^d]*
%attr(755,root,root) %dir %{_var}/spool/postfix
%attr(700, postfix,root) %dir %{_var}/spool/postfix/active
%attr(700, postfix,root) %dir %{_var}/spool/postfix/bounce
%attr(700, postfix,root) %dir %{_var}/spool/postfix/corrupt
%attr(700, postfix,root) %dir %{_var}/spool/postfix/defer
%attr(700, postfix,root) %dir %{_var}/spool/postfix/deferred
%attr(700, postfix,root) %dir %{_var}/spool/postfix/incoming
%attr(1730,postfix,maildrop) %dir %{_var}/spool/postfix/maildrop
%attr(755, postfix,root) %dir %{_var}/spool/postfix/pid
%attr(700, postfix,root) %dir %{_var}/spool/postfix/private
%attr(710, postfix,maildrop) %dir %{_var}/spool/postfix/public
%attr(700, postfix,root) %dir %{_var}/spool/postfix/saved
%attr(644, postfix,root) %{_var}/spool/postfix/.nofinger
%{_mandir}/man*/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpostfix-*.so
%{_includedir}/postfix

%if %{!?_without_ldap:1}%{?_without_ldap:0}
%files dict-ldap
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/postfix/dict_ldap.so
%endif

%if %{!?_without_mysql:1}%{?_without_mysql:0}
%files dict-mysql
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/postfix/dict_mysql.so
%endif

%files dict-pcre
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/postfix/dict_pcre.so

%if %{!?_without_psql:1}%{?_without_psql:0}
%files dict-pgsql
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/postfix/dict_pgsql.so
%endif
