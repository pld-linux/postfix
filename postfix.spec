Summary:	Postfix Mail Transport Agent
Summary(pl):	Agent Pocztowy Postfix
Name:		postfix
Version:	19990122-pl01
Release:	3
URL:		http://www.postfix.org/
Source0:	ftp://postfix.cloud9.net/%{name}-beta-%{version}.tar.gz
Source1:	postfix.aliases
Source2:	postfix.cron
Source3:	postfix.init
Source4:	postfix-contrib-beta.tar.gz
Source5:	postfix-beta-19990122-pl01.tar.gz.sig
Source6:	postfix-contrib-beta.tar.gz.sig
Source7:	mail.sh
Patch0:		postfix-config.patch
Patch1:		postfix-postconf.diff
Copyright:	Distributable
Group:		Networking/Daemons
Provides:	smtpdaemon
Conflicts:	sendmail
Conflicts:	smail
Conflicts:	zmailer
Conflicts:	zmail
Conflicts:	exim
Conflicts:	qmail
Prereq:		/sbin/chkconfig
BuildRoot:	/tmp/%{name}-%{version}-root

%description
Postfix is attempt to provide an alternative to the widely-used
Sendmail program. Postfix attempts to be fast, easy to administer,
and hopefully secure, while at the same time being sendmail
compatible enough to not upset your users.
	 
%description -l pl
Postfix jest prób± dostarczenia alternatywnego MTA w stosunku
do szeroko u¿ywanego sendmaila. Postfix w zamierzeniu ma byæ szybki,
³atwy w administrowaniu, bezpieczny oraz ma byæ na tyle kompatybilny
z sendmailem by nie denerwowaæ Twoich u¿ytkowników.

%prep
%setup -q -n %{name}-beta-%{version}
%patch0 -p1
%patch1 -p1

%build
make -f Makefile.init makefiles
make tidy
make DEBUG="" OPT="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
rm -f html/Makefile.in

install -d $RPM_BUILD_ROOT/etc/{cron.daily,profile.d,mail,rc.d/init.d} \
	$RPM_BUILD_ROOT{%{_bindir},%{_libdir}/postfix,%{_mandir}/man{1,5,8},%{_sbindir}} \
	$RPM_BUILD_ROOT/var/spool/postfix/{active,corrupt,deferred,maildrop,private,saved,bounce,defer,incoming,pid,public}

install bin/sendmail bin/post* $RPM_BUILD_ROOT/usr/sbin
install `ls bin/*|egrep -v 'post|fsstone|smtp-|sendmail'` $RPM_BUILD_ROOT/usr/lib/postfix
install conf/access $RPM_BUILD_ROOT/etc/mail
install conf/canonical $RPM_BUILD_ROOT/etc/mail
install conf/main.cf $RPM_BUILD_ROOT/etc/mail
install conf/master.cf $RPM_BUILD_ROOT/etc/mail
install conf/postfix-script-nosgid $RPM_BUILD_ROOT/etc/mail/postfix-script
install conf/relocated $RPM_BUILD_ROOT/etc/mail
install conf/transport $RPM_BUILD_ROOT/etc/mail
install conf/virtual $RPM_BUILD_ROOT/etc/mail
install man/man1/* $RPM_BUILD_ROOT%{_mandir}/man1
install man/man5/* $RPM_BUILD_ROOT%{_mandir}man5
install man/man8/* $RPM_BUILD_ROOT%{_mandir}man8

install -d sample; install conf/sample* sample

install %{SOURCE1} $RPM_BUILD_ROOT/etc/mail/aliases
install %{SOURCE2} $RPM_BUILD_ROOT/etc/cron.daily/postfix
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/postfix

install %{SOURCE7} $RPM_BUILD_ROOT/etc/profile.d

ln -sf ../sbin/sendmail $RPM_BUILD_ROOT/usr/bin/mailq
ln -sf ../sbin/sendmail $RPM_BUILD_ROOT/usr/bin/newaliases
ln -sf ../sbin/sendmail $RPM_BUILD_ROOT/usr/lib/sendmail

touch $RPM_BUILD_ROOT/etc/mail/{aliases,access,canonical,relocated,transport,virtual}{,.db}

strip $RPM_BUILD_ROOT/usr/lib/postfix/* || :
gzip -9nf $RPM_BUILD_ROOT/usr/man/man*/*
touch $RPM_BUILD_ROOT/var/spool/postfix/.nofinger

%pre
if [ -f /var/lock/subsys/postfix ]; then
	/etc/rc.d/init.d/postfix stop 2> /dev/null
fi

%post
/sbin/chkconfig --add postfix

if ! grep -q "^hostmaster:" /etc/mail/aliases; then
        echo "Adding Entry for hostmaster in /etc/mail/aliases"
        echo "hostmaster:       root" >>/etc/mail/aliases
fi

for i in postmaster postoffice MAILER-DAEMON postmast nobody webmaster administrator \
ftpmaster newsmaster w3cache squid news proxy abuse ircd postfix; do
        if ! grep -q "^$i:" /etc/mail/aliases; then
                echo "Adding Entry for $i in /etc/mail/aliases"
                echo "$i:       hostmaster" >>/etc/mail/aliases
        fi
done
newaliases

echo "
UWAGA ! Postfix standardowo jest skonfigurowany do dostarczania
poczty do prywatnych katalogów u¿ytkowników (\$HOME/Mailbox).
By u¿ytkownicy mogli czytaæ nadchodz±c± pocztê musisz
w pliku konfiguracyjnym /etc/sysconfig/system umie¶ciæ liniê:
HOME_MAIL=yes
Mo¿esz tak¿e uaktywniæ dostarczanie poczty w standardowe miejsce
(/var/spool/mail/\$USER). By to uczyniæ wyedytuj plik
/etc/mail/main.cf i zakomentuj liniê:
home_mailbox = Mailbox

				PLD Team
"

%preun
if [ $1 = 0 ]; then
	if [ -f /var/lock/subsys/postfix ]; then
		/etc/rc.d/init.d/postfix stop 2> /dev/null
	fi
	/sbin/chkconfig --del postfix
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc html sample 0README COMPATIBILITY HISTORY LICENSE RELEASE_NOTES TODO
%config(noreplace) %verify(not size mtime md5) /etc/mail/aliases
%ghost /etc/mail/aliases.db
%attr(740,root,root) /etc/cron.daily/postfix
%dir /etc/mail
%config(noreplace) %verify(not size mtime md5) /etc/mail/access
%ghost /etc/mail/access.db
%config(noreplace) %verify(not size mtime md5) /etc/mail/canonical
%ghost /etc/mail/canonical.db
%config(noreplace) %verify(not size mtime md5) /etc/mail/main.cf
%config(noreplace) %verify(not size mtime md5) /etc/mail/master.cf
%attr(755,root,root) %config(noreplace) %verify(not size mtime md5) /etc/mail/postfix-script
%config(noreplace) %verify(not size mtime md5) /etc/mail/relocated
%ghost /etc/mail/relocated.db
%config(noreplace) %verify(not size mtime md5) /etc/mail/transport
%ghost /etc/mail/transport.db
%config(noreplace) %verify(not size mtime md5) /etc/mail/virtual
%ghost /etc/mail/virtual.db
%attr(740,root,root) /etc/rc.d/init.d/postfix
%attr(755,root,root) /etc/profile.d/mail.sh
%attr(755,root,root) /usr/bin/*
%attr(755,root,root) /usr/sbin/*
%attr(755,root,root) /usr/lib/sendmail
/usr/man/*/*
%attr(755,root,root) /usr/lib/postfix
%attr(755,root,root) %dir /var/spool/postfix
%dir %attr(700, postfix,root, 700) %dir /var/spool/postfix/active
%attr(700, postfix,root, 700) %dir /var/spool/postfix/bounce
%attr(700, postfix,root, 700) %dir /var/spool/postfix/corrupt
%attr(700, postfix,root, 700) %dir /var/spool/postfix/defer
%attr(700, postfix,root, 700) %dir /var/spool/postfix/deferred
%attr(700, postfix,root, 700) %dir /var/spool/postfix/incoming
%attr(1733,postfix,root,1733) %dir /var/spool/postfix/maildrop
%attr(755, postfix,root,755) %dir /var/spool/postfix/pid
%attr(700, postfix,root, 700) %dir /var/spool/postfix/private
%attr(755, postfix,root,755) %dir /var/spool/postfix/public
%attr(700, postfix,root, 700) %dir /var/spool/postfix/saved
%attr(644, postfix,root) /var/spool/postfix/.nofinger
