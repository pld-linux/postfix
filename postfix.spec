Summary:     Postfix Mail Transport Agent
Name:        postfix
Version:     19990122-pl01
Release:     3
URL:         http://www.postfix.org/
Source0:     ftp://postfix.cloud9.net/%{name}-beta-%{version}.tar.gz
Source1:     postfix.aliases
Source2:     postfix.cron
Source3:     postfix.init
Source4:     postfix-contrib-beta.tar.gz
Source5:     postfix-beta-19990122-pl01.tar.gz.sig
Source6:     postfix-contrib-beta.tar.gz.sig
Source7:     mail.sh
Patch0:      postfix-config.patch
Patch1:	     postfix-postconf.diff
Copyright:   Distributable
Group:       Networking/Daemons
Provides:    smtpdaemon
Conflicts:   sendmail
Conflicts:   smail
Conflicts:   zmailer
Conflicts:   zmail
Conflicts:   exim
Conflicts:   qmail
Prereq:      /sbin/chkconfig
BuildRoot:   /tmp/buildroot-%{name}-%{version}
Summary(pl): Agent Pocztowy Postfix

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

install -d $RPM_BUILD_ROOT/etc/{cron.daily,profile.d,mail,rc.d/init.d}
install -d $RPM_BUILD_ROOT/usr/{bin,lib/postfix,man/man{1,5,8},sbin}
install -d $RPM_BUILD_ROOT/var/spool/postfix/{active,corrupt,deferred,maildrop,private,saved,bounce,defer,incoming,pid,public}

install -m755 bin/sendmail bin/post* $RPM_BUILD_ROOT/usr/sbin
install -m755 `ls bin/*|egrep -v 'post|fsstone|smtp-|sendmail'` $RPM_BUILD_ROOT/usr/lib/postfix
install -m644 conf/access $RPM_BUILD_ROOT/etc/mail
install -m644 conf/canonical $RPM_BUILD_ROOT/etc/mail
install -m644 conf/main.cf $RPM_BUILD_ROOT/etc/mail
install -m644 conf/master.cf $RPM_BUILD_ROOT/etc/mail
install -m755 conf/postfix-script-nosgid $RPM_BUILD_ROOT/etc/mail/postfix-script
install -m644 conf/relocated $RPM_BUILD_ROOT/etc/mail
install -m644 conf/transport $RPM_BUILD_ROOT/etc/mail
install -m644 conf/virtual $RPM_BUILD_ROOT/etc/mail
install -m644 man/man1/* $RPM_BUILD_ROOT/usr/man/man1
install -m644 man/man5/* $RPM_BUILD_ROOT/usr/man/man5
install -m644 man/man8/* $RPM_BUILD_ROOT/usr/man/man8

install -d sample; install -m644 conf/sample* sample

install -m644 %{SOURCE1} $RPM_BUILD_ROOT/etc/mail/aliases
install -m755 %{SOURCE2} $RPM_BUILD_ROOT/etc/cron.daily/postfix
install -m755 %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/postfix

install -m755 %{SOURCE7} $RPM_BUILD_ROOT/etc/profile.d

ln -sf ../sbin/sendmail $RPM_BUILD_ROOT/usr/bin/mailq
ln -sf ../sbin/sendmail $RPM_BUILD_ROOT/usr/bin/newaliases
ln -sf ../sbin/sendmail $RPM_BUILD_ROOT/usr/lib/sendmail

for I in etc/mail/{aliases,access,canonical,relocated,transport,virtual}
do
   touch $RPM_BUILD_ROOT/$I{,.db}
done

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
%attr(740, root, root) /etc/cron.daily/postfix
%dir /etc/mail
%config(noreplace) %verify(not size mtime md5) /etc/mail/access
%ghost /etc/mail/access.db
%config(noreplace) %verify(not size mtime md5) /etc/mail/canonical
%ghost /etc/mail/canonical.db
%config(noreplace) %verify(not size mtime md5) /etc/mail/main.cf
%config(noreplace) %verify(not size mtime md5) /etc/mail/master.cf
%attr(755, root, root) %config(noreplace) %verify(not size mtime md5) /etc/mail/postfix-script
%config(noreplace) %verify(not size mtime md5) /etc/mail/relocated
%ghost /etc/mail/relocated.db
%config(noreplace) %verify(not size mtime md5) /etc/mail/transport
%ghost /etc/mail/transport.db
%config(noreplace) %verify(not size mtime md5) /etc/mail/virtual
%ghost /etc/mail/virtual.db
%attr(740, root, root) /etc/rc.d/init.d/postfix
%attr(755, root, root) /etc/profile.d/mail.sh
%attr(755, root, root) /usr/bin/*
%attr(755, root, root) /usr/sbin/*
%attr(755, root, root) /usr/lib/sendmail
%attr(644, root, man) /usr/man/*/*
%attr(755, root, root, 755) /usr/lib/postfix
%attr(755, root, root, 755) %dir /var/spool/postfix
%dir %attr(700, postfix, root, 700) %dir /var/spool/postfix/active
%dir %attr(700, postfix, root, 700) %dir /var/spool/postfix/bounce
%dir %attr(700, postfix, root, 700) %dir /var/spool/postfix/corrupt
%dir %attr(700, postfix, root, 700) %dir /var/spool/postfix/defer
%dir %attr(700, postfix, root, 700) %dir /var/spool/postfix/deferred
%dir %attr(700, postfix, root, 700) %dir /var/spool/postfix/incoming
%dir %attr(1733,postfix, root,1733) %dir /var/spool/postfix/maildrop
%dir %attr(755, postfix, root, 755) %dir /var/spool/postfix/pid
%dir %attr(700, postfix, root, 700) %dir /var/spool/postfix/private
%dir %attr(755, postfix, root, 755) %dir /var/spool/postfix/public
%dir %attr(700, postfix, root, 700) %dir /var/spool/postfix/saved
%attr(644, postfix, root) /var/spool/postfix/.nofinger

%changelog
* Thu Feb 25 1999 Arkadiusz Mi¶kiewicz <misiek@pld.org.pl>
- PLDized

* Tue Feb 16 1999 Edgard Castro <castro@usmatrix.net>
  [19990122-pl01-1]

* Sun Jan 24 1999 Arne Coucheron <arneco@online.no>
  [19990122-1]
- shell for postfix user changed to /bin/true to avoid logins to the account
- files in /usr/libexec/postfix moved to /usr/lib/postfix since this complies
  more with the Red Hat standard

* Wed Jan 06 1999 Arne Coucheron <arneco@online.no>
  [19981230-2]
- added URL for the source
- added a cron job for daily check of errors
- sample config files moved from /etc/postfix/sample to the docdir 
- dropped making of symlinks in /usr/sbin and instead installing the real
  files there
- because of the previous they're not needed anymore in /usr/libexec/postfix,
  so they are removed from that place

* Fri Jan 01 1999 Arne Coucheron <arneco@online.no>
  [19981230-1]

* Tue Dec 29 1998 Arne Coucheron <arneco@online.no>
  [19981222-1]
- first build of rpm version
