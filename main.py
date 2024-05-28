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
            attributes=['uid','cn', 'userPassword'])
        return self.conn.entries
    
    def get_groups(self, search_base):
        self.conn.search(
            search_base=search_base, 
            search_filter='(objectClass=posixGroup)', 
            search_scope=SUBTREE,
            attributes=['cn', 'memberUid'])
        return self.conn.entries
    
    def get_users_in_group(self, group_dn):
        self.conn.search(
            search_base=group_dn,
            search_filter='(objectClass=posixGroup)',
            search_scope=SUBTREE,
            attributes=['memberUid'])
        members = self.conn.entries[0].memberUid if self.conn.entries else []
        return [member for member in members]

if __name__ == "__main__":
    server_uri = 'ldap://185.241.195.163'
    admin_dn = 'cn=admin,dc=sirius,dc=com'
    search_base = 'dc=sirius,dc=com'
    bind_password = 'openldap'

    ldap_client = OpenLDAPClient(server_uri, admin_dn, bind_password)

    # print("\nUsers:")
    # users = ldap_client.get_users(search_base)
    # for user in users:
    #     print(user)

    groups = ldap_client.get_groups(search_base)
    for group in groups:
        print(group.cn)

    print("\nGroups:")
    groups = ldap_client.get_groups(search_base)
    for group in groups:
        print(f"Group: {group.cn}")
        member_users = ldap_client.get_users_in_group(group.entry_dn)
        print(f"Members: {', '.join(member_users)}\n")

