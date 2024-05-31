root@ald:~# ldapsearch -x -D "uid=admin,cn=users,cn=accounts,dc=sirius,dc=com" -W -LLL uid=* uid  | grep robert.sa
Enter LDAP Password: 
dn: uid=robert.sa,cn=users,cn=compat,dc=sirius,dc=com
uid: robert.sa
dn: uid=robert.sa,cn=users,cn=accounts,dc=sirius,dc=com
uid: robert.sa
root@ald:~# ipa user-find robert.sa
-----------------------
найдено 0 пользователей
-----------------------
---------------------------------
Количество возвращённых записей 0
---------------------------------
