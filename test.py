from  python_freeipa import ClientMeta

client = ClientMeta(host='ald.sirius.com',verify_ssl=False,dns_discovery=True)
client.login('admin','BibaBobaidi0ts')
users = client.user_add(
    a_uid="test2",
    o_uidnumber="22002",
    o_cn="test2",
    o_sn="test2",
    o_givenname="test2",
    # o_gidnumber="22001",
    o_loginshell="/bin/bash",
    o_homedirectory="/home/fromp",
    # o_mail="fromp@sirius.com",
    o_setattr="userPassword={SSHA}H2G95QW4iPRnRauBuzNSpawi2H4pKJB+"
)
# user = client.user_add('test3', 'John', 'Doe', 'John Doe', o_preferredlanguage='EN')

print(users)

