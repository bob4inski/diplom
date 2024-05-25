from ldap3 import Server, Connection, ALL, SUBTREE

class OpenLDAPClient:
    def __init__(self, server_uri, bind_dn, bind_password):
        server = Server(server_uri, get_info=ALL)
        self.conn = Connection(server, user=bind_dn, password=bind_password, auto_bind=True)

    def whoami(self):
        self.conn.extend.standard.who_am_i()

    def get_users(self, search_base):
        self.conn.search(
            search_base=search_base, 
            search_filter='(objectClass=posixAccount)', 
            search_scope=SUBTREE, 
            attributes=['uid', 'userPassword'])
        return self.conn.entries

if __name__ == "__main__":
    server_uri = 'ldap://185.241.195.163'
    admin_dn = 'cn=admin,dc=sirius,dc=com'
    search_base = 'dc=sirius,dc=com'
    bind_password = 'openldap'

    ldap_client = OpenLDAPClient(server_uri, admin_dn, bind_password)

    print("\nUsers:")
    users = ldap_client.get_users(search_base)
    for user in users:
        print(user.enty_to_ldif())
    #     print(f"DN: {user['dn']}")
    #     print(f"  cn: {user['attributes']['cn'][0]}")
    #     print(f"  uid: {user['attributes']['uid'][0]}")
    #     print(f"  userPassword: {user['attributes']['userPassword'][0]}")
    #     print()
