%define		ver	19990906
%define		patchl	07
%define		pfixtls	0.4.2-19990906-pl05-0.9.4
Summary:	Postfix Mail Transport Agent
Summary(pl):	Agent Pocztowy Postfix
Name:		postfix
Version:	%{ver}_pl%{patchl}
Release:	1
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Copyright:	Distributable
Source0:	ftp://postfix.cloud9.net/%{name}-%{ver}-pl%{patchl}.tar.gz
Source1:	postfix.aliases
Source2:	postfix.cron
Source3:	postfix.init
Source4:	ftp://ftp.aet.tu-cottbus.de/pub/pfixtls/pfixtls-%{pfixtls}.tar.gz
Source5:	postfix.sysconfig
Patch0:		postfix-config.patch
Patch1:		http://www.xaa.iae.nl/~xaa/postfix6/patch.19990727.txt
Patch2:		postfix-tls.patch
Patch3:		postfix-glibc.patch
URL:		http://www.postfix.org/
Provides:	smtpdaemon
Requires:	rc-scripts
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel
BuildRequires:	grep
Obsoletes:	smtpdaemon
Prereq:		/sbin/chkconfig
Prereq:		%{_sbindir}/useradd
Prereq:		%{_sbindir}/groupadd
Prereq:		%{_sbindir}/userdel
Prereq:		%{_sbindir}/groupdel
BuildRoot:	/tmp/%{name}-%{version}-root

%define		_sysconfdir	/etc

%description
Postfix is attempt to provide an alternative to the widely-used Sendmail
program. Postfix attempts to be fast, easy to administer, and hopefully
secure, while at the same time being sendmail compatible enough to not upset
your users. This version have IPv6 support and LDAP support.
	 
%description -l pl
Postfix jest prób± dostarczenia alternatywnego MTA w stosunku do szeroko
u¿ywanego sendmaila. Postfix w zamierzeniu ma byæ szybki, ³atwy w
administrowaniu, bezpieczny oraz ma byæ na tyle kompatybilny z sendmailem by
nie denerwowaæ Twoich u¿ytkowników. Ta wersja wspiera IPv6 oraz LDAP.

%prep
%setup -q -n postfix-%{ver}-pl%{patchl} -a 4
%patch0 -p1 -b .wiget
%patch1 -p1
%patch2 -p1
%patch3 -p1
#patch -p1 <pfixtls-%{pfixtls}/pfixtls.diff

%build
make -f Makefile.init makefiles
make tidy
make DEBUG="" OPT="$RPM_OPT_FLAGS" CCARGS="-DHAS_LDAP -DHAS_SSL" \
     AUXLIBS="-llber -lldap -lssl -lsslcrypto"

%install
rm -rf $RPM_BUILD_ROOT
rm -f {html,man}/Makefile.in conf/{LICENSE,main.cf.default}

install -d $RPM_BUILD_ROOT%{_sysconfdir}/{mail,cron.daily,rc.d/init.d,sysconfig} \
	   $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir}/postfix,%{_mandir}/man{1,5,8}} \
	   $RPM_BUILD_ROOT%{_var}/spool/postfix/{active,corrupt,deferred,maildrop,private,saved,bounce,defer,incoming,pid,public} \
	   pfixtls

install -d sample-conf; mv -f conf/sample* sample-conf/ || :
mv -f pfixtls-%{pfixtls}/{doc,README,TODO,CHANGES} pfixtls

install -s bin/* $RPM_BUILD_ROOT%{_sbindir}
install -s libexec/* $RPM_BUILD_ROOT%{_libdir}/postfix
install conf/* $RPM_BUILD_ROOT%{_sysconfdir}/mail

(cd man; tar cf - .) | (cd $RPM_BUILD_ROOT%{_mandir}; tar xf -)

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/mail/aliases
install %{SOURCE2} $RPM_BUILD_ROOT/etc/cron.daily/postfix
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/postfix
install %{SOURCE5} $RPM_BUILD_ROOT/etc/sysconfig/postfix

ln -sf ../sbin/sendmail $RPM_BUILD_ROOT%{_bindir}/mailq
ln -sf ../sbin/sendmail $RPM_BUILD_ROOT%{_bindir}/newaliases
ln -sf ../sbin/sendmail $RPM_BUILD_ROOT%{_libdir}/sendmail

mv -f	$RPM_BUILD_ROOT%{_sysconfdir}/mail/postfix-script-sgid \
	$RPM_BUILD_ROOT%{_sysconfdir}/mail/postfix-script

rm -f	$RPM_BUILD_ROOT%{_sysconfdir}/mail/postfix-script-{diff,nosgid}

touch $RPM_BUILD_ROOT%{_sysconfdir}/mail/\
{aliases,access,canonical,relocated,transport,virtual}{,.db}

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* \
	LDAP_README HISTORY MYSQL_README UUCP_README \
	pfixtls/{README,TODO,CHANGES}
		
touch $RPM_BUILD_ROOT/var/spool/postfix/.nofinger

%pre
if [ -f /var/lock/subsys/postfix ]; then
	/etc/rc.d/init.d/postfix stop 2> /dev/null
fi
%{_sbindir}/groupadd -f -g 62 postfix
%{_sbindir}/useradd -M -g postfix -d /var/spool/postfix -u 62 -s /bin/false postfix 2> /dev/null
%{_sbindir}/groupadd -f -g 63 maildrop

%post
if ! grep -q "^hostmaster:" /etc/mail/aliases; then
        echo "Adding Entry for hostmaster in /etc/mail/aliases"
        echo "hostmaster:       root" >>/etc/mail/aliases
fi
newaliases
/sbin/chkconfig --add postfix
if [ -r /var/lock/subsys/postfix]; then
	/etc/rc.d/init.d/postfix restart >&2
else
	echo "Run \"/etc/rc.d/init.d/postfix start\" to start postfix daemon."
fi

%preun
if [ $1 = 0 ]; then
	if [ -f /var/lock/subsys/postfix ]; then
		/etc/rc.d/init.d/postfix stop 2> /dev/null
	fi
	/sbin/chkconfig --del postfix
fi

%postun
%{_sbindir}/groupdel maildrop 2> /dev/null
%{_sbindir}/userdel postfix 2> /dev/null
%{_sbindir}/groupdel postfix 2> /dev/null

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc html {LDAP_README,HISTORY,MYSQL_README,UUCP_README}.gz pfixtls
%doc sample-conf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mail/access
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mail/aliases
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mail/canonical
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mail/relocated
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mail/transport
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mail/virtual
%ghost %{_sysconfdir}/mail/*.db
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
