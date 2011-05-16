#
# Do not edit this file. This file shows the default delivery status
# notification (DSN) messages that are built into Postfix.
#
# To change Postfix DSN messages, perhaps to add non-English text,
# follow instructions in the bounce(5) manual page.
#

#
# The failure template is used when mail is returned to the sender;
# either the destination rejected the message, or the destination
# could not be reached before the message expired in the queue.
#

failure_template = <<EOF
Charset: iso-8859-2
From: MAILER-DAEMON (Mail Delivery System)
Subject: Niedostarczona Korespondencja Zwrocona Nadawcy / Undelivered Mail Returned to Sender
Postmaster-Subject: Postmaster Copy: Undelivered Mail

Wiadomo�� wygenerowana przez system pocztowy $myhostname.

Z przykro�ci� informuj�, �e twoja wiadomo�� nie mog�a by�
dostarczona do jednego z odbiorc�w. Jest za��czona poni�ej.

W celu uzyskania dalszej pomocy, skontaktuj si� z <postmaster>
Koniecznie przeka� niniejszy raport; mo�esz usun�� w�asn�
tre�� z za��czonego listu, kt�ry zosta� zwr�cony.

                   System pocztowy

==============================================================

This is the mail system at host $myhostname.

I'm sorry to have to inform you that your message could not
be delivered to one or more recipients. It's attached below.

For further assistance, please send mail to <postmaster>

If you do so, please include this problem report. You can
delete your own text from the attached returned message.

                   The mail system
EOF


#
# The delay template is used when mail is delayed. Note a neat trick:
# the default template displays the delay_warning_time value as hours
# by appending the _hours suffix to the parameter name; it displays
# the maximal_queue_lifetime value as days by appending the _days
# suffix.
#
# Other suffixes are: _seconds, _minutes, _weeks. There are no other
# main.cf parameters that have this special behavior.
#
# You need to adjust these suffixes (and the surrounding text) if
# you have very different settings for these time parameters.
#

delay_template = <<EOF
Charset: iso-8859-2
From: MAILER-DAEMON (Mail Delivery System)
Subject: Opozniona Korespondencja (proby wciaz ponawiane) / Delayed Mail (still being retried)
Postmaster-Subject: Postmaster Warning: Delayed Mail

Wiadomo�� wygenerowana przez system pocztowy $myhostname.

########################################################################
# TO JEST TYLKO OSTRZE�ENIE. NIE MUSISZ WYSY�A� PONOWNIE SWOJEGO LISTU #
########################################################################

Twoja wiadomo�� nie mog�a by� dostarczona ponad $delay_warning_time_hours godzin.
Pr�by b�d� ponawiane przez $maximal_queue_lifetime_days dni.

W celu uzyskania dalszej pomocy, skontaktuj si� z <postmaster>
Koniecznie przeka� niniejszy raport; mo�esz usun�� w�asn�
tre�� z za��czonego listu, kt�ry zosta� zwr�cony.

                   System pocztowy

==============================================================

This is the mail system at host $myhostname.

####################################################################
# THIS IS A WARNING ONLY.  YOU DO NOT NEED TO RESEND YOUR MESSAGE. #
####################################################################

Your message could not be delivered for more than $delay_warning_time_hours hour(s).
It will be retried until it is $maximal_queue_lifetime_days day(s) old.

For further assistance, please send mail to <postmaster>

If you do so, please include this problem report. You can
delete your own text from the attached returned message.

                   The mail system
EOF


#
# The success template is used when mail is delivered to mailbox,
# when an alias or list is expanded, or when mail is delivered to a
# system that does not announce DSN support. It is an error to specify
# a Postmaster-Subject: here.
#

success_template = <<EOF
Charset: iso-8859-2
From: MAILER-DAEMON (Mail Delivery System)
Subject: Raport Udanego Dostarczenia Korespondencji / Successful Mail Delivery Report

Wiadomo�� wygenerowana przez system pocztowy $myhostname.

Twoja wiadomo�� zosta�a dostarczona wymienionym poni�ej adresatom.
Je�li poczta dotar�a do skrzynki nie otrzymasz wi�cej powiadomie�.
W przeciwnym wypadku mo�esz jeszcze dosta� powiadomienia o b��dach
z innych system�w.

                   System pocztowy

==============================================================

This is the mail system at host $myhostname.

Your message was successfully delivered to the destination(s)
listed below. If the message was delivered to mailbox you will
receive no further notifications. Otherwise you may still receive
notifications of mail delivery errors from other systems.

                   The mail system
EOF


#
# The verify template is used for address verification (sendmail -bv
# address...). or for verbose mail delivery (sendmail -v address...).
# It is an error to specify a Postmaster-Subject: here.
#

verify_template = <<EOF
Charset: iso-8859-2
From: MAILER-DAEMON (Mail Delivery System)
Subject: Raport Stanu Dostarczania Korespondencji / Mail Delivery Status Report

Wiadomo�� wygenerowana przez system pocztowy $myhostname.

Za��czony raport o dor�czeniu korespondencji, o kt�ry prosi�e�.

                   System pocztowy

==============================================================

This is the mail system at host $myhostname.

Enclosed is the mail delivery report that you requested.

                   The mail system
EOF
