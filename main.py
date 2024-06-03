from ldap3 import Server, Connection, ALL, SUBTREE
from  python_freeipa import ClientMeta
import tarantool

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
        return  [item for sublist in response.data for item in sublist]

    def upload_users_to_tarantool(self,space:str):
        """
        Upload uids into Tarantool
        """
        uids = self.get_uids_freeipa()
        for uid in uids:
            if not(self.check_user_exist_t(uid=uid)):
                self.add_user_t(space=space,uid=uid)
        
        print(f"existing users: {self.get_users_t(space="ald")}")

    def get_uids_freeipa(self,):
        freeipa = ClientMeta(host=self.ald_host,verify_ssl=False,dns_discovery=True)
        freeipa.login('admin','BibaBobaidi0ts')
        users = freeipa.user_find()
        freeipa.logout()
        uids = [user['uid'][0] for user in users['result'] if 'uid' in user]
        return uids
    
    def get_users_openldap(self, search_base=""):
        """
        Get users from OpenLDAP
        """
        if not search_base:
            search_base = self.base_dn
        attributes = ['uid','uidNumber','cn','sn', 'userPassword',"loginshell","homedirectory","mail"]
       
        openldap_connection = Connection(self.server, user=self.user, password=self.password, auto_bind=True)
        openldap_connection.search(
            search_base=search_base, 
            search_filter='(objectClass=inetOrgPerson)', #inetOrgPerson posixAccount
            search_scope=SUBTREE, 
            attributes=attributes)
        
        openldap_connection.closed
        return openldap_connection.entries
    
    def add_user(self, user: Connection.entries):
        """
        Add a new user to FreeIpa
        """
        freeipa = ClientMeta(host=self.ald_host,verify_ssl=False,dns_discovery=True)
        freeipa.login('admin','BibaBobaidi0ts')
 
        if self.check_user_exist_t(str(user.uid)):
            print(f"user with uid={str(user.uid)}exist")
            return False
        else:
            try:
                freeipa.user_add(
                    a_uid=str(user.uid),
                    o_givenname=str(user.cn),
                    o_sn=str(user.sn),
                    o_cn=str(user.cn),
                    o_uidnumber=str(user.uidNumber),
                    o_loginshell="/bin/bash",
                    o_homedirectory=f"/home/{str(user.uid)}",
                    o_mail=str(user.mail),
                    o_setattr=f"userPassword={str(user.userPassword)}"
                )
                print(f"user with uid={str(user.uid)} added")
                freeipa.logout()
                return True
            except Exception as Ex:
                print (Ex)
                freeipa.logout()
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
    users = migration.get_users_openldap() 
    uids = [str(user.uid) for user in users]
    print(f"users from OpenLDAP: {uids} " )
    print("start migration")
    for user in users:
        migration.add_user(user)