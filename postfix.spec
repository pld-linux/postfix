#
# Conditiona build:
# no_sasl - build wihtout SMTP AUTH support
# no_ldap - build without LDAP support
# no_pcre - build without Perl Compatible Regular Expresion support
#
Summary:	Postfix Mail Transport Agent
Summary(pl):	Agent Pocztowy Postfix
Name:		postfix
Version:	20000924
Release:	1
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Copyright:	Distributable
Source0:	ftp://ftp.porcupine.org/mirrors/postfix-release/experimental/snapshot-%{version}.tar.gz
Source1:	%{name}.aliases
Source2:	%{name}.cron
Source3:	%{name}.init
Source5:	%{name}.sysconfig
Patch0:		%{name}-config.patch
Patch1:		http://www.misiek.eu.org/ipv6/%{name}-ver20000922-ipv6-20000922.patch.gz
Patch2:		%{name}-pl.patch
URL:		http://www.postfix.org/
Provides:	smtpdaemon
Requires:	rc-scripts
%{!?no_ldap:BuildRequires:	openldap-devel}
BuildRequires:	openssl-devel >= 0.9.4-2
%{!?no_pcre:BuildRequires:	pcre-devel}
%{!?no_sasl:BuildRequires:	cyrus-sasl-devel}
BuildRequires:	grep
Obsoletes:	smtpdaemon
Obsoletes:	exim
Obsoletes:	sendmail
Obsoletes:	sendmail-cf
Prereq:		/sbin/chkconfig
Prereq:		/usr/sbin/useradd
Prereq:		/usr/sbin/groupadd
Prereq:		/usr/sbin/userdel
Prereq:		/usr/sbin/groupdel
Prereq:		/usr/bin/getgid
Prereq:		/bin/id
Prereq:		/bin/hostname
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc

%description
Postfix is attempt to provide an alternative to the widely-used
Sendmail program. Postfix attempts to be fast, easy to administer, and
hopefully secure, while at the same time being sendmail compatible
enough to not upset your users. This version have IPv6 support and
%{!?no_ldap:no }LDAP support.

%description -l pl
Postfix jest prób± dostarczenia alternatywnego MTA w stosunku do
szeroko u¿ywanego sendmaila. Postfix w zamierzeniu ma byæ szybki,
³atwy w administrowaniu, bezpieczny oraz ma byæ na tyle kompatybilny z
sendmailem by nie denerwowaæ Twoich u¿ytkowników. Ta wersja wspiera
IPv6%{!?no_ldap: oraz LDAP} %{?no_ldap: i nie zawiera wsparcia LDAP}.

%prep
%setup -q -n snapshot-%{version}
%patch0 -p1
%patch1 -p1 
%patch2 -p1 

%build
%{__make} -f Makefile.init makefiles
%{__make} tidy
%{__make} DEBUG="" OPT="-g $RPM_OPT_FLAGS" \
     CCARGS="%{!?no_ldap:-DHAS_LDAP} %{!?no_pcre:-DHAS_PCRE} %{!?no_sasl:-DUSE_SASL_AUTH } " AUXLIBS="%{!?no_ldap:-llber -lldap} -lnsl -ldb -lresolv %{!?no_pcre:-lpcre} %{!?no_sasl:-lsasl}"

%install
rm -rf $RPM_BUILD_ROOT
rm -f {html,man}/Makefile.in conf/{LICENSE,main.cf.default}

install -d $RPM_BUILD_ROOT%{_sysconfdir}/{mail,cron.daily,rc.d/init.d,sysconfig} \
	   $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir}/postfix,%{_mandir}/man{1,5,8}} \
	   $RPM_BUILD_ROOT%{_var}/spool/postfix/{active,corrupt,deferred,maildrop,private,saved,bounce,defer,incoming,pid,public} \
	   pfixtls

install -d sample-conf; mv -f conf/sample* sample-conf/ || :

install -s bin/* $RPM_BUILD_ROOT%{_sbindir}
install -s libexec/* $RPM_BUILD_ROOT%{_libdir}/postfix
#install bin/* $RPM_BUILD_ROOT%{_sbindir}
#install libexec/* $RPM_BUILD_ROOT%{_libdir}/postfix
install conf/* $RPM_BUILD_ROOT%{_sysconfdir}/mail

(cd man; tar cf - .) | (cd $RPM_BUILD_ROOT%{_mandir}; tar xf -)

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/mail/aliases
install %{SOURCE2} $RPM_BUILD_ROOT/etc/cron.daily/postfix
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/postfix
install %{SOURCE5} $RPM_BUILD_ROOT/etc/sysconfig/postfix

ln -sf ../sbin/sendmail $RPM_BUILD_ROOT%{_bindir}/mailq
ln -sf ../sbin/sendmail $RPM_BUILD_ROOT%{_bindir}/newaliases
ln -sf ../sbin/sendmail $RPM_BUILD_ROOT%{_libdir}/sendmail

mv -f  $RPM_BUILD_ROOT%{_sysconfdir}/mail/postfix-script-sgid \
	$RPM_BUILD_ROOT%{_sysconfdir}/mail/postfix-script

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/mail/postfix-script-{diff,nosgid}

touch $RPM_BUILD_ROOT%{_sysconfdir}/mail/\
	{aliases,access,canonical,relocated,transport,virtual}{,.db}

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* \
	LDAP_README HISTORY MYSQL_README UUCP_README \
	0README BEWARE COMPATIBILITY DEBUG_README LICENSE LMTP_README \
	PCRE_README  \
	RELEASE_NOTES RESTRICTION_CLASS SASL_README TODO FILTER_README
		
touch $RPM_BUILD_ROOT/var/spool/postfix/.nofinger

%pre
if [ -n "`/usr/bin/getgid postfix`" ]; then
	if [ "`getgid postfix`" != "62" ]; then
		echo "Warning: group postfix haven't gid=62. Corect this before install postfix" 1>&2
		exit 1
	fi
else
	/usr/sbin/groupadd -g 62 -r -f postfix
	if [ -f /var/db/group.db ]; then
		/usr/bin/update-db 1>&2
	fi
fi
if [ -n "`/usr/bin/getgid maildrop`" ]; then
	if [ "`/usr/bin/getgid maildrop`" != "63" ]; then
		echo "Warning: group maildrop haven't gid=63. Corect this before install postfix" 1>&2
		exit 1
	fi
else
	/usr/sbin/groupadd -g 63 -r -f maildrop
	if [ -f /var/db/group.db ]; then
		/usr/bin/update-db 1>&2
	fi
fi
if [ -n "`/bin/id -u postfix 2>/dev/null`" ]; then
	if [ "`/bin/id -u postfix`" != "62" ]; then
		echo "Warning: user postfix haven't uid=62. Corect this before install postfix" 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -u 62 -r -d /var/spool/postfix -s /bin/false -c "Postfix User" -g postfix postfix 1>&2
	if [ -f /var/db/passwd.db ]; then
		/usr/bin/update-db 1>&2
	fi
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
if [ $1 = 0 ]; then
	/usr/sbin/groupdel maildrop 2> /dev/null
	/usr/sbin/userdel postfix 2> /dev/null
	/usr/sbin/groupdel postfix 2> /dev/null
	if [ -f /var/db/passwd.db ] || [ -f /var/db/group.db ]; then
		/usr/bin/update-db 1>&2
	fi
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc html {LDAP_README,HISTORY,MYSQL_README,UUCP_README}.gz 
%doc {0README,BEWARE,COMPATIBILITY,DEBUG_README,LICENSE,LMTP_README,PCRE_README}.gz
%doc {RELEASE_NOTES,RESTRICTION_CLASS,SASL_README,TODO,FILTER_README}.gz
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
%attr(740,root,root) /etc//cron.daily/postfix
%attr(754,root,root) /etc/rc.d/init.d/postfix
%attr(640,root,root) %config(noreplace) /etc/sysconfig/postfix
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/s*
%attr(755,root,root) %{_sbindir}/post*i*
%attr(755,root,root) %{_sbindir}/postl*
%attr(755,root,root) %{_sbindir}/postc*
%attr(755,root,root) %{_sbindir}/postmap
%attr(755,root,root) %{_sbindir}/postsuper
%attr(2755,root,maildrop) %{_sbindir}/postdrop
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
%attr(755, postfix,root) %dir %{_var}/spool/postfix/public
%attr(700, postfix,root) %dir %{_var}/spool/postfix/saved
%attr(644, postfix,root) %{_var}/spool/postfix/.nofinger
%{_mandir}/man*/*
