from ldap3 import Server, Connection, ALL

# LDAP server and admin credentials
ldap_server = 'ldap://185.241.195.163'  # Replace with your LDAP server
ldap_admin_dn = 'cn=admin,dc=sirius,dc=com'  # Replace with your admin DN
ldap_admin_password = 'openldap'  # Replace with your admin password

# Connect to the LDAP server
server = Server(ldap_server, get_info=ALL)
conn = Connection(server, ldap_admin_dn, ldap_admin_password, auto_bind=True)

# Perform the LDAP search
search_base = 'dc=sirius,dc=com'
search_filter = '(objectClass=posixAccount)'
search_attributes = ['cn','uid', 'userPassword']

conn.search(search_base, search_filter, attributes=search_attributes)

# Print the results
for entry in conn.entries:
    print(entry)

# Disconnect from the LDAP server
conn.unbind()