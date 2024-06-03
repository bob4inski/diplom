from ldap3 import Server, Connection, ALL, SUBTREE
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures as kfc
from  python_freeipa import ClientMeta
import time
import logging


class Migration:
    def __init__(self, server_uri, bind_dn, bind_password, base_dn: str, 
                 ald_host: str, ald_user: str, ald_password: str):
        
        self.user = bind_dn
        self.password = bind_password
        self.base_dn = base_dn
        self.ald_host = ald_host
        self.ald_user = ald_user
        self.ald_password = ald_password

        self.server  = Server(server_uri, get_info=ALL)
    
    def get_uids_freeipa(self,):
        freeipa = ClientMeta(host=self.ald_host,verify_ssl=False,dns_discovery=True)
        freeipa.login('admin','BibaBobaidi0ts')
        users = freeipa.user_find()
        freeipa.logout()
        uids = [user['uid'][0] for user in users['result'] if 'uid' in user]
        self.uids_dict = {user['uid'][0]: True for user in users['result'] if 'uid' in user}
        #return uids
    
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
        start_time = time.time()
        
        # if self.check_user_exist_t(str(user.uid)):
        #     logging.info(f"user with uid={str(user.uid)} exist; execution time: {(time.time() - start_time)}")
        #     return False
        # else:
        if str(user.uid) in self.uids_dict:
            logging.info(f"user with uid={str(user.uid)} exist; execution time: {(time.time() - start_time)}")
            return False
        else:
            try:
                freeipa = ClientMeta(host=self.ald_host,verify_ssl=False,dns_discovery=True)
                freeipa.login('admin','BibaBobaidi0ts')

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
                logging.info(f"user with uid={str(user.uid)} added; execution time: {(time.time() - start_time)} ")
                self.uids_dict[str(user.uid)] = True
                freeipa.logout()
                return True
            except Exception as Ex:
                logging.error(f"error {Ex}")
                return False
 

if __name__ == "__main__":
    server_uri = 'ldap://185.241.195.163'
    admin_dn = 'cn=admin,dc=sirius,dc=com'
    base_dn = 'dc=sirius,dc=com'
    bind_password = 'openldap'

    ald_host = "ald.sirius.com"
    ald_user = "admin"
    ald_password = "BibaBobaidi0ts"

    logging.basicConfig(filename="migration.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

    logging.info("Start migration")
    migration = Migration(server_uri, admin_dn, bind_password,base_dn=base_dn,
                          ald_host=ald_host,ald_user=ald_user, ald_password=ald_password)

    users = migration.get_users_openldap()
    migration.get_uids_freeipa()
    logging.info(f"got users from OpenLDAP, starting migrate")
    for user in users:
        migration.add_user(user)

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(migration.add_user, user) for user in users]
    # If you need to process the results or catch exceptions, you can iterate over futures
    for future in kfc.as_completed(futures):
        try:
            result = future.result()
            # Handle the result (maybe logging or something else)
        except Exception as e:
            # Handle the exception, e.g., logging
            logging.error(f"Migration error: {e}")