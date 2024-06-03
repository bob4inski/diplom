ldif_template = """
dn: uid=user_{uid},ou=users,dc=sirius,dc=com
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
cn: user_{uid}
sn: lastname_{uid}
uid: user_{uid}
uidNumber: {uid_number}
gidNumber: {gid_number}
homeDirectory: /home/user_{uid}
loginShell: /bin/bash
userPassword: {user_password}
mail: user_{uid}@example.com
"""

# Example user password
user_password = "{SSHA}H2G95QW4iPRnRauBuzNSpawi2H4pKJB+"
f = open("users.ldif", "a")

# Generate 10 users starting from UID 30000
starting_uid_number = 41000
starting_gid_number = 41000
for i in range(10000):
    # Compute the current user's numeric UID.
    current_uid_number = starting_uid_number + i
    current_gid_number = starting_gid_number + i
    # Substitute into the LDIF template
    user_ldif_entry = ldif_template.format(uid=100+i, uid_number=current_uid_number, user_password=user_password,gid_number=current_gid_number)
    f.write(user_ldif_entry)