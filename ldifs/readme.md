ipa user-add testmigrate --first=testmigrate --last=testmigrate --uid=11003 --gid=5013 --home=/home/testmigrate --shell=/bin/bash --email=testmigrate@example.com --setattr=uidnumber=11003 --setattr=gidnumber=5013


```bash


dn: uid=robert.sa,cn=users,cn=accounts,dc=sirius,dc=com
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
cn: robert.sa
sn: stryzhak
uid: robert.sa
uidNumber: 11011
gidNumber: 51013
homeDirectory: /home/robert.sa
loginShell: /bin/bash
userPassword: {SSHA}H2G95QW4iPRnRauBuzNSpawi2H4pKJB+
mail: robert.sa@example.com
```