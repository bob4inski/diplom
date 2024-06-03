ldap_add: Constraint violation (19)
        additional info: pre-hashed passwords are not valid

ipa config-mod --enable-migration=true
```json
{'result': 
        {'cn': ['test10'], 
        'displayname': ['test10 test10'], 
        'initials': ['tt'], 
        'gecos': ['test10 test10'], 
        'objectclass': ['top', 'person', 'organizationalperson', 'inetorgperson', 'inetuser', 'posixaccount', 'krbprincipalaux', 'krbticketpolicyaux', 'ipaobject', 'ipasshuser', 'x-ald-user', 'x-ald-user-parsec14', 'x-ald-audit-policy', 'rbta-unit', 'rbta-address', 'rbtaCustomUserAttrs', 'rbta-inetorgperson-ext', 'ruPostMailAccount', 'rbtaUserMeta', 'ipaSshGroupOfPubKeys', 'mepOriginEntry'], 
        'xaldusermacmax': ['0'], 
        'xaldusermacmin': ['0'], 
        'userpassword': [{'__base64__': 'e1NTSEF9SDJHOTVRVzRpUFJuUmF1QnV6TlNwYXdpMkg0cEtKQis='}], 'ipauniqueid': ['edaf8a16-2033-11ef-82ed-7412b3c05601'], 
        'mepmanagedentry': ['cn=test10,cn=groups,cn=accounts,dc=sirius,dc=com'], 
        'proxyaddresses': ['SMTP:TEST10@SIRIUS.COM'], 
        'x-ald-aud-mask': ['0x0:0x0'], 
        'x-ald-user-mac': ['0:0x0:0:0x0'], 
        'gidnumber': ['22022'], 
        'rbtaou': ['sirius.com'], 
        'sn': ['test10'], 
        'krbcanonicalname': ['test10@SIRIUS.COM'], 
        'loginshell': ['/bin/bash'], 
        'givenname': ['test10'], 
        'mail': ['test10@sirius.com'], 
        'uid': ['test10'], 
        'uidnumber': ['22022'], 
        'krbprincipalname': ['test10@SIRIUS.COM'], 
        'homedirectory': ['/home/test10'], 
        'rbtadp': ['ou=sirius.com,cn=orgunits,cn=accounts,dc=sirius,dc=com'], 
        'preserved': False, 
        'has_password': True, 
        'has_keytab': False, 
        'memberof_group': ['ipausers'], 
        'memberof_role': ['Organization units'], 
        'dn': 'uid=test10,cn=users,cn=accounts,dc=sirius,dc=com'
        }, 
'value': 'test10', 
'summary': 'Added user "test10"'
}

