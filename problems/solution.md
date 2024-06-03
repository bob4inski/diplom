```bash
root@ald:~# ldapadd -f rbert.kdif -W -D "uid=admin,cn=users,cn=accounts,dc=sirius,dc=com"
Enter LDAP Password: 
adding new entry "uid=robert.sa,cn=users,cn=accounts,dc=sirius,dc=com"
ldap_add: Constraint violation (19)
        additional info: pre-hashed passwords are not valid


root@ald:~# ipa config-mod --enable-migration=true
  Максимальная длина имени пользователя: 32
  Максимальная длина имени хоста: 64
  Основа домашних каталогов: /home
  Оболочка по умолчанию: /bin/bash
  Группа пользователей по умолчанию: ipausers
  Почтовый домен по умолчанию: sirius.com
  Ограничение времени поиска: 2
  Ограничение размера поиска: 100
  Поля поиска пользователей: uid,givenname,sn,telephonenumber,ou,title
  Поля поиска групп: cn,description
  Включить режим миграции: TRUE
  Основа субъекта сертификата: O=SIRIUS.COM
  Уведомление об окончании действия пароля (в днях): 4
  Возможности подключаемого модуля паролей: AllowNThash, KDC:Disable Last Success
  Порядок применения списка пользователей SELinux: guest_u:s0$xguest_u:s0$user_u:s0$staff_u:s0-s0:c0.c1023$sysadm_u:s0-s0:c0.c1023$unconfined_u:s0-s0:c0.c1023
  Пользователь SELinux по умолчанию: unconfined_u:s0-s0:c0.c1023
  Типы PAC по умолчанию: MS-PAC, nfs:NONE
  Главные IPA-серверы: ald.sirius.com
  Главный IPA-сервер с поддержкой PKINIT: ald.sirius.com
  DNS-серверы IPA: ald.sirius.com
root@ald:~# ldapadd -f user.ldif -W -D "uid=admin,cn=users,cn=accounts,dc=sirius,dc=com"
Enter LDAP Password: 
adding new entry "uid=robert.sa,cn=users,cn=accounts,dc=sirius,dc=com"
```
```bash
ipa user-add testmigrate --first=testmigrate --last=testmigrate --uid=11003 --gid=5013 --home=/home/testmigrate --shell=/bin/bash --email=testmigrate@example.com --setattr=uidnumber=11003 --setattr=gidnumber=5013 --setattr=userPassword={SSHA}H2G95QW4iPRnRauBuzNSpawi2H4pKJB+

-----------------------------------
Добавлен пользователь "testmigrate"
-----------------------------------
  Имя учётной записи пользователя: testmigrate
  Имя: testmigrate
  Фамилия: testmigrate
  Полное имя: testmigrate testmigrate
  Отображаемое имя: testmigrate testmigrate
  Инициалы: tt
  Домашний каталог: /home/testmigrate
  GECOS: testmigrate testmigrate
  Оболочка входа: /bin/bash
  Имя учётной записи: testmigrate@SIRIUS.COM
  Псевдоним учётной записи: testmigrate@SIRIUS.COM
  Адрес электронной почты: testmigrate@example.com
  Пароль: e1NTSEF9SDJHOTVRVzRpUFJuUmF1QnV6TlNwYXdpMkg0cEtKQis=
  UID: 11003
  ID группы: 5013
  Минимальный уровень конфиденциальности: 0
  Максимальный уровень конфиденциальности: 0
  proxy addresses: SMTP:TESTMIGRATE@EXAMPLE.COM
  Link to department: ou=sirius.com,cn=orgunits,cn=accounts,dc=sirius,dc=com
  Link to head department: sirius.com
  Пароль: True
  Участник групп: ipausers
  Роли: Organization units
  Доступные ключи Kerberos: False
root@ald:~# ldapwhoami -W -D "uid=testmigrate,cn=users,cn=accounts,dc=sirius,dc=com"                                                 Enter LDAP Password: 
dn: uid=testmigrate,cn=users,cn=accounts,dc=sirius,dc=com
root@ald:~# ipa user-find
----------------------
найдено 2 пользователя
----------------------
  Имя учётной записи пользователя: admin
  Фамилия: Administrator
  Домашний каталог: /home/admin
  Оболочка входа: /bin/bash
  Псевдоним учётной записи: admin@SIRIUS.COM, root@SIRIUS.COM
  UID: 426000000
  ID группы: 426000000
  Учётная запись отключена: False

  Имя учётной записи пользователя: testmigrate
  Имя: testmigrate
  Фамилия: testmigrate
  Домашний каталог: /home/testmigrate
  Оболочка входа: /bin/bash
  Имя учётной записи: testmigrate@SIRIUS.COM
  Псевдоним учётной записи: testmigrate@SIRIUS.COM
  Адрес электронной почты: testmigrate@example.com
  UID: 11003
  ID группы: 5013
  Учётная запись отключена: False
---------------------------------
Количество возвращённых записей 2
---------------------------------
root@ald:~# ipa user-find -a
Usage: ipa [global-options] user-find [CRITERIA] [options]

ipa: error: no such option: -a
root@ald:~# ipa user-find -all
Usage: ipa [global-options] user-find [CRITERIA] [options]

ipa: error: no such option: -a
root@ald:~# ipa user-find --all
----------------------
найдено 2 пользователя
----------------------
  dn: uid=admin,cn=users,cn=accounts,dc=sirius,dc=com
  Имя учётной записи пользователя: admin
  Фамилия: Administrator
  Полное имя: Administrator
  Домашний каталог: /home/admin
  GECOS: Administrator
  Оболочка входа: /bin/bash
  Псевдоним учётной записи: admin@SIRIUS.COM, root@SIRIUS.COM
  Окончание действия пароля пользователя: 20240829203231Z
  Пароль: e1BCS0RGMl9TSEEyNTZ9QUFBSUFHUnFxVXZ1ZHlPV284NTJ4UHFvdnY3UTF6R3BtaXdQNzhmMlNZR2podDZ5b3dMRGQ1NnV5VFdRVG93REIyczdsOG9KYThGbWVYNnRuallyazkyNVhnN0o4WjVxWnlaMkd4SUZPNUZ2eFJpd0hWdm42MDdRQ2t1ZVNjZXoxRjRrelNhWXhvU2UzQ2tFQmNnRThiNlg1Und6NU1oczRKczlzR3FKNFBGWmpvUjAvc0ExeTVHT3N1Rkcyb25MRUtCeVJxaTEyTUEwWENPQmZuL081QzR4dFd1R1A2RHhlVU1uc0d2L1FuZ05NZGtJT2ZLdW1SZkIwVUgxNTNObUh2TWpZMEZ5Y2lCc3crcGVNYzZvbDlzSkgzNHA5NnRHMHU3T1h0Z1gvVmdzaGpEZmp2SDArdVhIRWwxdUxZRC80ckh3bTMwblBWaVJjSEJlZDBkK2NpTE50dE5HV0dPQ0xoeGxCR3JibENySEY4VnFPVFZhNXpIZ0VvWDVTSFVPU3hNZDRXeWpzTmx0RVE3VU9BQnFlQ2JNcVNId29XN0xmcWdvVmpCZTFVS2hJSU5y
  UID: 426000000
  ID группы: 426000000
  Маска уровней целостности: 63
  Учётная запись отключена: False
  Хранимый пользователь: False
  Link to department: ou=sirius.com,cn=orgunits,cn=accounts,dc=sirius,dc=com
  Link to head department: sirius.com
  Участник групп: admins, ald trust admin, trust admins, lpadmin
  Роли: ALDPRO - Main Administrator
  ipantsecurityidentifier: S-1-5-21-2173274814-2267897061-2596758960-500
  ipauniqueid: a6568f4a-1f8c-11ef-8cf1-7412b3c05601
  krbextradata: AALfM1pmcm9vdC9hZG1pbkBTSVJJVVMuQ09NAA==
  krblastpwdchange: 20240531203231Z
  krbprincipalkey: MIHeoAMCAQGhAwIBAaIDAgEBowMCAQGkgccwgcQwaKAbMBmgAwIBBKESBBA0XyV3X2Y7I1YxPlImYnU4oUkwR6ADAgESoUAEPiAAasUbkDRgONJ+jZWnsv2l2cqEiDDmf6MUFds1PEEvfLcK/kedEoQNUhRdU3huQi7+h+itOrB7tYuJAISGMFigGzAZoAMCAQShEgQQJl5FICE1Py4mIGdENEBrUqE5MDegAwIBEaEwBC4QAL9MpucBpBS3x9w4mU9NLCJVE0MDp6fS7LQe4u3fuxJDQKn2o2uPY5UXHzDr
  objectclass: top, person, posixaccount, krbprincipalaux, krbticketpolicyaux, inetuser, ipaobject, ipasshuser, x-ald-audit-policy,
               ipaSshGroupOfPubKeys, x-ald-user-parsec14, x-ald-user, ipaNTUserAttrs, rbta-unit, rbta-address, rbtaCustomUserAttrs,
               rbta-inetorgperson-ext, ruPostMailAccount
  x-ald-aud-mask: 0x0:0x0

  dn: uid=testmigrate,cn=users,cn=accounts,dc=sirius,dc=com
  Имя учётной записи пользователя: testmigrate
  Имя: testmigrate
  Фамилия: testmigrate
  Полное имя: testmigrate testmigrate
  Отображаемое имя: testmigrate testmigrate
  Инициалы: tt
  Домашний каталог: /home/testmigrate
  GECOS: testmigrate testmigrate
  Оболочка входа: /bin/bash
  Имя учётной записи: testmigrate@SIRIUS.COM
  Псевдоним учётной записи: testmigrate@SIRIUS.COM
  Окончание действия пароля пользователя: 20240829213812Z
  Адрес электронной почты: testmigrate@example.com
  Пароль: e1BCS0RGMl9TSEEyNTZ9QUFBSUFKNW1pb1ViaDJYcFloL1R4am9zbTkycUFjZlREaHhXQitNdFA5SnV2TUpvOWRIMXpjS1lldUR5VmY5SGRLMUo4VUR4Z3JUZ3dwNWlxbXJWV2ZuKy84ZmIwbkYwS1JkSjRhZmI2TTI0bXB5ZU9jQVlmelpCMWROS01VVkRLUEEza21uZWlJM0RpM2hjdUNzS0lkYW5pTEJseEw1WlcrOWQ0UzBVS3VMOE1ZbzlsRTRkQTNGNEgyM2x3cDdhWERqMFNqNDcvcXhYdzlNN0x4UExteURyVnVUYU9kZHBSbDJkL2lxRWJ1V05BYVlkdS9DOVZuNGpCei9QTTBJb3VCRWRWVUVNdEZJREJhMkdYRmEwM2F4V1ZUZFJmYTRFdzBoQWJjd1phQTZuS1haamVPK09LSWczcHN2d1pscE5TVDZPRTdGNSswTnlIUnIrYVNQYUxUQjY4MWRXa1NBak9ZUm9MU1hsWWxkSENBYUh3aTBaK2hhem1YYUhCczFiZjcrNEEyVDhVZWNDVUpmUW1vdWYwSFZLK0VYb1BVWmM1OWFIOTJpRkgzdmg2Z3gy
  UID: 11003
  ID группы: 5013
  Минимальный уровень конфиденциальности: 0
  Максимальный уровень конфиденциальности: 0
  Учётная запись отключена: False
  Хранимый пользователь: False
  proxy addresses: SMTP:TESTMIGRATE@EXAMPLE.COM
  Link to department: ou=sirius.com,cn=orgunits,cn=accounts,dc=sirius,dc=com
  Link to head department: sirius.com
  Участник групп: ipausers
  Роли: Organization units
  ipauniqueid: f6fa14ae-1f95-11ef-bc09-7412b3c05601
  krbextradata: AAJEQ1pmdGVzdG1pZ3JhdGVAU0lSSVVTLkNPTQA=
  krblastpwdchange: 20240531213812Z
  krbprincipalkey: MIHeoAMCAQGhAwIBAaIDAgEBowMCAQGkgccwgcQwaKAbMBmgAwIBBKESBBApQG1pUy0xZDNjfU02TGlnoUkwR6ADAgESoUAEPiAAlKfUW5BCofBYFEFGhHa63/8nJVrSuf94Hlc1Pn62EScYod6G59nzkxmhWP3FB7a29IKbB/Q9srRhOtPQMFigGzAZoAMCAQShEgQQTVImUzQzcG9RamJIR3JzIKE5MDegAwIBEaEwBC4QAMCVanv8FyZl4NPURFmH4xPcllS6+Gf1xYZmAy/BKaGmkYLRBcjmqzbSng6D
  mepmanagedentry: cn=testmigrate,cn=groups,cn=accounts,dc=sirius,dc=com
  objectclass: top, person, organizationalperson, inetorgperson, inetuser, posixaccount, krbprincipalaux, krbticketpolicyaux,
               ipaobject, ipasshuser, x-ald-user, x-ald-user-parsec14, x-ald-audit-policy, rbta-unit, rbta-address,
               rbtaCustomUserAttrs, rbta-inetorgperson-ext, ruPostMailAccount, rbtaUserMeta, ipaSshGroupOfPubKeys, mepOriginEntry
  x-ald-aud-mask: 0x0:0x0
  x-ald-user-mac: 0:0x0:0:0x0
---------------------------------
Количество возвращённых записей 2
---------------------------------
root@ald:~# ^C
root@ald:~# ldapwhoami -W -D "uid=testmigrate,cn=users,cn=accounts,dc=sirius,dc=com"
Enter LDAP Password: 
dn: uid=testmigrate,cn=users,cn=accounts,dc=sirius,dc=com
root@ald:~# cp /etc/sssd/sssd.conf  
sssd.conf         sssd.conf.backup  
root@ald:~# cp /etc/sssd/sssd.conf
sssd.conf         sssd.conf.backup  
root@ald:~# cp /etc/sssd/sssd.conf.backup /etc/sssd/sssd.conf
root@ald:~# sudo systemctl restart sssd
root@ald:~# ls /home
admin  ald-admin
root@ald:~# kinit testmigrate
Password for testmigrate@SIRIUS.COM: 
root@ald:~# klist
Ticket cache: KEYRING:persistent:426000000:krb_ccache_9w82UpK
Default principal: testmigrate@SIRIUS.COM

Valid starting       Expires              Service principal
01.06.2024 00:41:00  02.06.2024 00:40:54  krbtgt/SIRIUS.COM@SIRIUS.COM
root@ald:~# ipa user-add testmigrate --first=testmigrate --last=testmigrate --uid=11003 --gid=5013 --home=/home/testmigrate --shell=/bin/bash --email=testmigrate@example.com --setattr=uidnumber=110^C --setattr=gidnumber=5013 --setattr=userPassword={SSHA}H2G95QW4iPRnRauBuzNSpawi2H4pKJB+
root@ald:~# ipa user-add robert --first=robert --last=stryzhak --uid=11010 --gid=6013 --home=/home/robert --shell=/bin/bash --email=robert@example.com --setattr=uidnumber=110010 --setattr=gidnumber=6013 --setattr=userPassword={SSHA}H2G95QW4iPRnRauBuzNSpawi2H4pKJB+
ipa: ERROR: Недостаточно прав для доступа: Не удалось прочитать фильтр происхождения (originfilter) определения личной группы пользователя (UPG Definition). Проверьте ваши разрешения.
root@ald:~# kinit admin
Password for admin@SIRIUS.COM: 
kinit: Password incorrect while getting initial credentials
root@ald:~# kinit admin
Password for admin@SIRIUS.COM: 
kinit: Password read interrupted while getting initial credentials
root@ald:~# kinit admin
Password for admin@SIRIUS.COM: 
root@ald:~# ipa user-add robert --first=robert --last=stryzhak --uid=11010 --gid=6013 --home=/home/robert --shell=/bin/bash --email=robert@example.com --setattr=uidnumber=110010 --setattr=gidnumber=6013 --setattr=userPassword={SSHA}H2G95QW4iPRnRauBuzNSpawi2H4pKJB+
------------------------------
Добавлен пользователь "robert"
------------------------------
  Имя учётной записи пользователя: robert
  Имя: robert
  Фамилия: stryzhak
  Полное имя: robert stryzhak
  Отображаемое имя: robert stryzhak
  Инициалы: rs
  Домашний каталог: /home/robert
  GECOS: robert stryzhak
  Оболочка входа: /bin/bash
  Имя учётной записи: robert@SIRIUS.COM
  Псевдоним учётной записи: robert@SIRIUS.COM
  Адрес электронной почты: robert@example.com
  Пароль: e1NTSEF9SDJHOTVRVzRpUFJuUmF1QnV6TlNwYXdpMkg0cEtKQis=
  UID: 110010
  ID группы: 6013
  Минимальный уровень конфиденциальности: 0
  Максимальный уровень конфиденциальности: 0
  proxy addresses: SMTP:ROBERT@EXAMPLE.COM
  Link to department: ou=sirius.com,cn=orgunits,cn=accounts,dc=sirius,dc=com
  Link to head department: sirius.com
  Пароль: True
  Участник групп: ipausers
  Роли: Organization units
  Доступные ключи Kerberos: False
root@ald:~# ldapwhoami -W -D "uid=robert,cn=users,cn=accounts,dc=sirius,dc=com"
Enter LDAP Password: 
dn: uid=robert,cn=users,cn=accounts,dc=sirius,dc=com
root@ald:~#
