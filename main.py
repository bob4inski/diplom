from ldap3 import Server, Connection, ALL, SUBTREE
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures as kfc
from  python_freeipa import ClientMeta
import time
import logging


class Migration:
    def __init__(self, server_uri, bind_dn, bind_password, base_dn: str, 
                 ald_host: str, ald_user: str, ald_password: str):
        
        self.openldap_user = bind_dn
        self.openldap_password = bind_password
        self.base_dn = base_dn

        self.ald_host = ald_host
        self.ald_user = ald_user
        self.ald_password = ald_password
        
        self.openserver  = Server(server_uri, get_info=ALL)
        self.openldap_connection = Connection(self.openserver, user=self.openldap_user, password=self.openldap_password, auto_bind=True)
        
        self.freeipa_client = ClientMeta(host=self.ald_host,verify_ssl=False,dns_discovery=True)
        self.freeipa_client.login(ald_user,ald_password)

    def check_uid_ipa(self,uid):
        user = self.freeipa_client.user_find(o_uid=uid)  
        if user['result']:
            return True
        else:
            return False 
      
    def get_uids_freeipa(self,):
        users = self.freeipa_client.user_find()
        self.uids_dict = {user['uid'][0]: True for user in users['result'] if 'uid' in user}

    
    def get_users_openldap(self, search_base=""):

        if not search_base:
            search_base = self.base_dn
        attributes = ['uid','uidNumber','cn','sn', 'userPassword',"loginshell","homedirectory","mail"]
       
        users = self.openldap_connection.search(
            search_base=search_base, 
            search_filter='(objectClass=inetOrgPerson)', #inetOrgPerson posixAccount
            search_scope=SUBTREE, 
            attributes=attributes).entries
  
        return users
    
    def add_user(self, user: Connection.entries):

        start_time = time.time()
        
        # if self.check_user_exist_t(str(user.uid)):
        #     logging.info(f"user with uid={str(user.uid)} exist; execution time: {(time.time() - start_time)}")
        #     return False
        # else:
        if str(user.uid) in self.uids_dict:
            logging.info(f"user with uid={str(user.uid)} exist; execution time: {(time.time() - start_time)}")
            
        else:
            try:
                self.freeipa_client.user_add(
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
                
            except Exception as Ex:
                logging.error(f"error {Ex}")
               
 

if __name__ == "__main__":
    openLDAP_uri = 'ldap://127.0.0.1'
    admin_dn = 'cn=admin,dc=sirius,dc=com'
    base_dn = 'dc=sirius,dc=com'
    admin_password = 'admin'

    ald_host = "ald.sirius.com"
    ald_user = "admin"
    ald_password = "admin"

    logging.basicConfig(filename="reverse-migration.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

    logging.info("Start migration")
    migration = Migration(openLDAP_uri, admin_dn, admin_password,base_dn=base_dn,
                          ald_host=ald_host,ald_user=ald_user, ald_password=ald_password)

    migration.get_uids_freeipa()
    users = migration.get_users_openldap()
    logging.info(f"got users from OpenLDAP, starting migrate")

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(migration.add_user, user) for user in users]
    for future in kfc.as_completed(futures):
        try:
            result = future.result()
        except Exception as e:
            logging.error(f"Migration error: {e}")