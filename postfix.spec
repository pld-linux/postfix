#
# Conditional build:	
# --without sasl - build wihtout SMTP AUTH support
# --without ldap - build without LDAP support
# --without pcre - build without Perl Compatible Regular Expresion support
# --without ssl  - build without SSL/TLS support
# --with mysql - build with MySQL support
# --without ipv6  - build without IPv6 support
#
%define	tls_ver 0.8.1-1.1.1-0.9.6c
Summary:	Postfix Mail Transport Agent
Summary(pl):	Serwer SMTP Postfix
Name:		postfix
Version:	1.1.2
Release:	0.1
Epoch:		1
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
License:	distributable
Source0:	ftp://ftp.porcupine.org/mirrors/postfix-release/official/%{name}-%{version}.tar.gz
Source1:	%{name}.aliases
Source2:	%{name}.cron
Source3:	%{name}.init
Source5:	%{name}.sysconfig
Source6:	ftp://ftp.aet.tu-cottbus.de/pub/pfixtls/pfixtls-%{tls_ver}.tar.gz
Source7:	%{name}.sasl
Patch0:		%{name}-config.patch
Patch1:		%{name}-pl.patch
Patch2:		%{name}-conf_msg.patch
Patch3:		%{name}-ipv6.patch
URL:		http://www.postfix.org/
Provides:	smtpdaemon
Prereq:		rc-scripts
%{!?_without_ldap:BuildRequires:	openldap-devel >= 2.0.0}
%{!?_without_ssl:BuildRequires:	openssl-devel >= 0.9.6a}
%{!?_without_pcre:BuildRequires:	pcre-devel}
%{!?_without_sasl:BuildRequires:	cyrus-sasl-devel}
%{!?_without_ipv6:BuildRequires:	libinet6 >= 0.20010420-3}
BuildRequires:	db3-devel
BuildRequires:	grep
BuildRequires:	awk
Prereq:		/sbin/chkconfig
Prereq:		/usr/sbin/useradd
Prereq:		/usr/sbin/groupadd
Prereq:		/usr/sbin/userdel
Prereq:		/usr/sbin/groupdel
Prereq:		/usr/bin/getgid
Prereq:		/bin/id
Prereq:		/bin/hostname
%{!?_without_ldap:Prereq:	openldap >= 2.0.0}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
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
Requires:	procmail

%description
Postfix is attempt to provide an alternative to the widely-used
Sendmail program. Postfix attempts to be fast, easy to administer, and
hopefully secure, while at the same time being sendmail compatible
enough to not upset your users. This version have IPv6 support and
%{!?_without_ldap:no }LDAP support.

%description -l pl
Postfix jest prób± dostarczenia alternatywnego MTA w stosunku do
szeroko u¿ywanego sendmaila. Postfix w zamierzeniu ma byæ szybki,
³atwy w administrowaniu, bezpieczny oraz ma byæ na tyle kompatybilny z
sendmailem by nie denerwowaæ Twoich u¿ytkowników. Ta wersja wspiera
IPv6%{!?_without_ldap: oraz LDAP}.

%prep
%setup -q -a6 
%patch0 -p1
%patch1 -p1
patch -p1 -s <pfixtls-%{tls_ver}/pfixtls.diff 
%patch2 -p1
%{!?_without_ipv6:%patch3 -p1 }

%build
%{__make} -f Makefile.init makefiles
%{__make} tidy
%{__make} DEBUG="" OPT="%{rpmcflags}" \
	CCARGS="%{!?_without_ldap:-DHAS_LDAP} %{!?_without_pcre:-DHAS_PCRE} %{!?_without_sasl:-DUSE_SASL_AUTH} %{?_with_mysql:-DHAS_MYSQL -I%{_includedir}/mysql} %{!?_without_ssl:-DHAS_SSL -I%{_includedir}/openssl}" \
	AUXLIBS="%{!?_without_ldap:-llber -lldap} -lnsl -ldb -lresolv %{!?_without_pcre:-lpcre} %{!?_without_sasl:-lsasl} %{?_with_mysql:-lmysqlclient} %{!?_without_ssl:-lssl -lcrypto}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{mail,cron.daily,rc.d/init.d,sasl,sysconfig} \
	   $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir}/postfix,%{_mandir}/man{1,5,8}} \
	   $RPM_BUILD_ROOT%{_var}/spool/postfix/{active,corrupt,deferred,maildrop,private,saved,bounce,defer,incoming,pid,public} \
	   pfixtls

rm -f {html,man}/Makefile.in conf/{LICENSE,main.cf.default}

install -d sample-conf; mv -f conf/sample* sample-conf/ || :

install bin/* $RPM_BUILD_ROOT%{_sbindir}
install libexec/* $RPM_BUILD_ROOT%{_libdir}/postfix
install conf/* $RPM_BUILD_ROOT%{_sysconfdir}/mail

(cd man; tar cf - .) | (cd $RPM_BUILD_ROOT%{_mandir}; tar xf -)

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/mail/aliases
install %{SOURCE2} $RPM_BUILD_ROOT/etc/cron.daily/postfix
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/postfix
install %{SOURCE5} $RPM_BUILD_ROOT/etc/sysconfig/postfix
install %{SOURCE7} $RPM_BUILD_ROOT/etc/sasl/smtpd.conf
install auxiliary/rmail/rmail $RPM_BUILD_ROOT%{_bindir}/rmail

ln -sf ../sbin/sendmail $RPM_BUILD_ROOT%{_bindir}/mailq
ln -sf ../sbin/sendmail $RPM_BUILD_ROOT%{_bindir}/newaliases
ln -sf ../sbin/sendmail $RPM_BUILD_ROOT%{_libdir}/sendmail

touch $RPM_BUILD_ROOT%{_sysconfdir}/mail/\
	{aliases,access,canonical,relocated,transport,virtual}{,.db}

gzip -9nf *README COMPATIBILITY HISTORY LICENSE RELEASE_NOTES \
	README_FILES/*README

touch $RPM_BUILD_ROOT/var/spool/postfix/.nofinger

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`/usr/bin/getgid postfix`" ]; then
	if [ "`getgid postfix`" != "62" ]; then
		echo "Warning: group postfix haven't gid=62. Correct this before installing postfix" 1>&2
		exit 1
	fi
else
	/usr/sbin/groupadd -g 62 -r -f postfix
fi
if [ -n "`/usr/bin/getgid maildrop`" ]; then
	if [ "`/usr/bin/getgid maildrop`" != "63" ]; then
		echo "Warning: group maildrop haven't gid=63. Correct this before installing postfix" 1>&2
		exit 1
	fi
else
	/usr/sbin/groupadd -g 63 -r -f maildrop
fi
if [ -n "`/bin/id -u postfix 2>/dev/null`" ]; then
	if [ "`/bin/id -u postfix`" != "62" ]; then
		echo "Warning: user postfix haven't uid=62. Correct this before installing postfix" 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -u 62 -r -d /var/spool/postfix -s /bin/false -c "Postfix User" -g postfix postfix 1>&2
fi

%post
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
if [ "$1" = "0" ]; then
	/usr/sbin/groupdel maildrop 2> /dev/null
	/usr/sbin/userdel postfix 2> /dev/null
	/usr/sbin/groupdel postfix 2> /dev/null
fi

%files
%defattr(644,root,root,755)
%doc html *.gz README_FILES/*.gz
%doc sample-conf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mail/access
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mail/aliases
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mail/canonical
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mail/relocated
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mail/transport
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mail/virtual
#%ghost %{_sysconfdir}/mail/*.db
%dir %{_sysconfdir}/mail
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mail/main.cf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mail/master.cf
%attr(755,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mail/postfix-script
%attr(740,root,root) /etc/cron.daily/postfix
%attr(754,root,root) /etc/rc.d/init.d/postfix
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/postfix
%{!?_without_sasl:%config(noreplace) %verify(not size mtime md5) /etc/sasl/smtpd.conf}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/s*
%attr(2755,root,mail) %{_sbindir}/postfix
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
%attr(755,root,root) %{_libdir}/postfix
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
