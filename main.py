from ldap3 import Server, Connection, ALL, SUBTREE
from  python_freeipa import ClientMeta
import subprocess
import tarantool
import json

class Migration:
    def __init__(self, server_uri, bind_dn, bind_password, base_dn: str, 
                 tarantool_host: str,tarantool_port: int,
                 ald_host: str, ald_user: str, ald_password: str):
        
        self.tarantool_host = tarantool_host
        self.tarantool_port = tarantool_port
        self.user = bind_dn
        self.password = bind_password
        self.base_dn = base_dn
        self.ald_host = ald_host
        self.ald_user = ald_user
        self.ald_password = ald_password

        self.server  = Server(server_uri, get_info=ALL)
    
    def check_user_exist_t(self, uid: str):
        check_connection = tarantool.Connection(host=self.tarantool_host,
                            port=self.tarantool_port
                            )
        response = check_connection.select(space_name='ald', key=uid)
        check_connection.close

        if len(response.data) == 0:
            return False
        elif len(response.data) == 1:
            return True
        
    def add_user_t(self,space: str, uid: str): 
        t_connection = tarantool.Connection(host=self.tarantool_host,
                            port=self.tarantool_port
                            )

        user = (uid,)
        t_connection.space(space).insert(user)
        t_connection.close
        
        
    def get_users_t(self,space: str):
        t_connection = tarantool.Connection(host=self.tarantool_host,
                            port=self.tarantool_port
                            )
        response = t_connection.select(space_name=space)
        return response.data

    def upload_users_to_tarantool(self,space:str):
        users = self.get_users(get_all="uid")
        for user in users:
            if not(self.check_user_exist_t(uid=str(user.uid))):
                self.add_user_t(space=space,uid=str(user.uid))
        
    def get_users(self, search_base="",get_all="all"):
        if not search_base:
            search_base = self.base_dn
        attributes = {
            "all":['uid','uidNumber','cn','sn', 'userPassword',"loginshell","homedirectory","mail"],
            "uid":['uid']
        }
        connection = Connection(self.server, user=self.user, password=self.password, auto_bind=True)
        connection.search(
            search_base=search_base, 
            search_filter='(objectClass=inetOrgPerson)', #inetOrgPerson posixAccount
            search_scope=SUBTREE, 
            attributes=attributes[get_all])
        
        connection.closed
        return connection.entries
    
    def add_user(self, user: Connection.user):
        """
        Add a new user to FreeIpa
        attributes: A dictionary of attributes for the user.
        """
        connection = ClientMeta(host=self.ald_host,verify_ssl=False,dns_discovery=True)
        connection.login('admin','BibaBobaidi0ts')
 
        if self.check_if_exist_t(str(user.uid)):
            print("user exist")
            return False
        else:
            try:
                connection.user_add(
                    a_uid=attributes['uid'],
                    o_givenname=attributes['cn'],
                    o_sn=attributes['sn'],
                    o_cn=attributes['cn'],
                    o_uidnumber=attributes['uidNumber'],
                    o_loginshell="/bin/bash",
                    o_homedirectory=f"/home/{attributes['uid']}",
                    o_mail=attributes['mail'],
                    o_setattr=attributes['userPassword']
                )

            except Exception as Ex:
                print (Ex)
                return False
 

if __name__ == "__main__":
    server_uri = 'ldap://185.241.195.163'
    admin_dn = 'cn=admin,dc=sirius,dc=com'
    base_dn = 'dc=sirius,dc=com'
    bind_password = 'openldap'

    t_host = '185.241.195.163'
    t_port = 3301

    ald_host = "ald.sirius.com"
    ald_user = "admin"
    ald_password = "BibaBobaidi0ts"
    
    migration = Migration(server_uri, admin_dn, bind_password,base_dn=base_dn,
                          tarantool_host=t_host,tarantool_port=t_port,
                          ald_host=ald_host,ald_user=ald_user, ald_password=ald_password)

    migration.upload_users_to_tarantool(space="ald")
    users = migration.get_users(get_all="all") 
    for user in users:
        migration.add_user(user)