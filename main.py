from ldap3 import Server, Connection, ALL, SUBTREE, MODIFY_ADD
import tarantool

class LDAPClient:
    def __init__(self, server_uri, bind_dn, bind_password, base_dn: str, 
                 tarantool_host: str,tarantool_port: int):
        
        self.tarantool_host = tarantool_host
        self.tarantool_port = tarantool_port

        server = Server(server_uri, get_info=ALL)
        self.base_dn = base_dn

        Connection(server, user=bind_dn, password=bind_password, auto_bind=True).closed
       # self.conn.closed

    def whoami(self):
        self.conn.extend.standard.who_am_i()

    def check_if_exist_t(self, uid: str):
        response = self.t_connection.select(space_name='ald', key=uid)
        if len(response.data) == 0:
            return False
        elif len(response.data) == 1:
            return True
        
    def add_user_t(self,space: str, uid: str): 
        self.t_connection = tarantool.Connection(host=self.tarantool_host,
                            port=self.tarantool_port
                            )

        if self.check_if_exist_t(uid):
            self.t_connection.close()
            return "user exist"
        else:
            user = (uid,)
            self.t_connection.space(space).insert(user)
            self.t_connection.close()
            return "user added"
        

    def get_users_t(self,space: str):
        self.t_connection = tarantool.Connection(host=self.tarantool_host,
                            port=self.tarantool_port
                            )
        response = self.t_connection.select(space_name=space)
        return response.data

    def upload_users_to_tarantool(self,space:str):
        users = self.get_users(get_all="uid")
        for user in users:
            self.add_user_t(space=space,uid=str(user.uid))
        
    def get_users(self, search_base="",get_all="all"):
        if not search_base:
            search_base = self.base_dn
        attributes = {
            "all":['uid','uidNumber','cn', 'userPassword'],
            "uid":['uid']
        }

        self.conn.search(
            search_base=search_base, 
            search_filter='(objectClass=inetOrgPerson)', #inetOrgPerson posixAccount
            search_scope=SUBTREE, 
            attributes=attributes[get_all])

        return self.conn.entries
    
    def get_groups(self, search_base=""):
        if not search_base:
            search_base = self.base_dn

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

    def add_user(self, user_dn, attributes):
        """
        Add a new user to LDAP.
        user_dn: The distinguished name of the new user.
        attributes: A dictionary of attributes for the user.
        """
        # todo
        # name = "amogus"
        # new_user_dn = f"uid={name},ou=users,dc=sirius,dc=com"
        # new_user_attributes = {
        #     'objectClass': ['inetOrgPerson', 'top'],
        #     'uid': name,
        #     'cn': name,
        #     'sn': name,
        #    # 'uidNumber': 11000,
        #     'userPassword': '{SSHA}PIIGPPpA4gtmxIchvfemwrBgQANEB+Yu'
        # }

        # add check_if_exist
        if self.conn.add(user_dn, attributes=attributes):
            print(f"User {user_dn} added successfully.")
        else:
            print(f"Failed to add user {user_dn}.", self.conn.result)
            
    # New method to add a group
    def add_group(self, group_dn, attributes):
        """
        Add a new group to LDAP.
        group_dn: The distinguished name of the new group.
        attributes: A dictionary of attributes for the group.
        """
        if self.conn.add(group_dn, attributes=attributes):
            print(f"Group {group_dn} added successfully.")
        else:
            print(f"Failed to add group {group_dn}.", self.conn.result)

    # New method to add a user to a group
    def add_user_to_group(self, group_dn, user_dn):
        """
        Add a user to a group.
        group_dn: The distinguished name of the group.
        user_dn: The distinguished name of the user to be added.
        """
        if self.conn.modify(group_dn, {'memberUid': [MODIFY_ADD, [user_dn]]}):
            print(f"User {user_dn} added to group {group_dn} successfully.")
        else:
            print(f"Failed to add user {user_dn} to group {group_dn}.", self.conn.result)
    
    #todo def check_if_in_group
    
    def check_if_exist(self, cn):
        """
        Check if an LDAP entry with the specified CN exists.
        search_base: The base DN under which to search for the entry.
        cn: The common name of the entry to check.
        """
        search_filter = f'(cn={cn})'
        self.conn.search(search_base=self.base_dn, search_filter=search_filter, search_scope=SUBTREE, attributes=['cn'])
        return bool(self.conn.entries)

if __name__ == "__main__":
    server_uri = 'ldap://185.241.195.163'
    admin_dn = 'cn=admin,dc=sirius,dc=com'
    base_dn = 'dc=sirius,dc=com'
    bind_password = 'openldap'
    t_host = '185.241.195.163'
    t_port = 3301
    OpenLDAP = LDAPClient(server_uri, admin_dn, bind_password,base_dn=base_dn,
                          tarantool_host=t_host,tarantool_port=t_port)

   # OpenLDAP.upload_users_to_tarantool(space="ald")
    print("get_users")
    #a = OpenLDAP.get_users_t(space="ald")
    a = OpenLDAP.get_users()
    print(a)
    # server_uri = 'ldap://192.168.232.80'
    # admin_dn = 'uid=admin,cn=users,cn=accounts,dc=sirius,dc=com'
    # base_dn = 'dc=sirius,dc=com'
    # bind_password = 'openldap'

    # AldPro = LDAPClient(server_uri, admin_dn, bind_password,base_dn=base_dn)
    

    # user_dn = "uid=new_user,ou=users,dc=sirius,dc=com"
    # user_attributes = {
    #     'objectClass': ['inetOrgPerson', 'posixAccount', 'top'],
    #     'uid': 'new_user',
    #     'cn': 'New User',
    #     'sn': 'User',
    #     'uidNumber': '11011',
    #     'gidNumber': '11011',
    #     'homeDirectory': '/home/new_user',
    #     'userPassword': '{SSHA}PIIGPPpA4gtmxIchvfemwrBgQANEB+Yu',
    #     'mail': 'new_user@example.com',
    #     'loginShell': '/bin/bash'
    # }
    # OpenLDAP.add_user(user_dn, user_attributes)
    # # OpenLDAP.add_user(new_user_dn, new_user_attributes)
    # users = OpenLDAP.get_users(get_all="uid") 
   
    # #get_all all|uid
    # for user in users:
        # print(user.uid)

    # groups = migrate_from.get_groups()
    # for group in groups:
    #     print(group.cn)

    # print(ldap_client.check_if_exist("Jane Doe"))

    # group_dn = "cn=developers,ou=groups,dc=sirius,dc=com"
    # ldap_client.add_user_to_group(group_dn, "janedoe")   

    # print("\nGroups:")
    # groups = ldap_client.get_groups(base_dn)
    # for group in groups:
    #     print(f"Group: {group.cn}")
    #     member_users = ldap_client.get_users_in_group(group.entry_dn)
    #     print(f"Members: {', '.join(member_users)}\n")

