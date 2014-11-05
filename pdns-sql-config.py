#!/usr/bin/python
import sys

# get this using the command:
# pdns_server --no-config --config --launch=gmysql,gpgsql 2>/dev/null | grep 'query='
DEFAULTCONFIG="""
# gmysql-activate-domain-key-query=update cryptokeys set active=1 where domain_id=(select id from domains where name='%s') and  cryptokeys.id=%d
# gmysql-add-domain-key-query=insert into cryptokeys (domain_id, flags, active, content) select id, %d, %d, '%s' from domains where name='%s'
# gmysql-any-id-query=SELECT content,ttl,prio,type,domain_id,disabled,name,auth FROM records WHERE disabled=0 and name='%s' and domain_id=%d
# gmysql-any-query=SELECT content,ttl,prio,type,domain_id,disabled,name,auth FROM records WHERE disabled=0 and name='%s'
# gmysql-basic-query=SELECT content,ttl,prio,type,domain_id,disabled,name,auth FROM records WHERE disabled=0 and type='%s' and name='%s'
# gmysql-clear-domain-all-keys-query=delete from cryptokeys where domain_id=(select id from domains where name='%s')
# gmysql-clear-domain-all-metadata-query=delete from domainmetadata where domain_id=(select id from domains where name='%s')
# gmysql-clear-domain-metadata-query=delete from domainmetadata where domain_id=(select id from domains where name='%s') and domainmetadata.kind='%s'
# gmysql-deactivate-domain-key-query=update cryptokeys set active=0 where domain_id=(select id from domains where name='%s') and  cryptokeys.id=%d
# gmysql-delete-comment-rrset-query=DELETE FROM comments WHERE domain_id=%d AND name='%s' AND type='%s'
# gmysql-delete-comments-query=DELETE FROM comments WHERE domain_id=%d
# gmysql-delete-domain-query=delete from domains where name='%s'
# gmysql-delete-empty-non-terminal-query=delete from records where domain_id='%d' and name='%s' and type is null
# gmysql-delete-names-query=delete from records where domain_id = %d and name='%s'
# gmysql-delete-rrset-query=delete from records where domain_id=%d and name='%s' and type='%s'
# gmysql-delete-tsig-key-query=delete from tsigkeys where name='%s'
# gmysql-delete-zone-query=delete from records where domain_id=%d
# gmysql-get-all-domain-metadata-query=select kind,content from domains, domainmetadata where domainmetadata.domain_id=domains.id and name='%s'
# gmysql-get-all-domains-query=select domains.id, domains.name, records.content, domains.type, domains.master, domains.notified_serial, domains.last_check from domains LEFT JOIN records ON records.domain_id=domains.id AND records.type='SOA' AND records.name=domains.name WHERE records.disabled=0 OR %d
# gmysql-get-domain-metadata-query=select content from domains, domainmetadata where domainmetadata.domain_id=domains.id and name='%s' and domainmetadata.kind='%s'
# gmysql-get-order-after-query=select min(ordername) from records where ordername > '%s' and domain_id=%d and disabled=0 and ordername is not null
# gmysql-get-order-before-query=select ordername, name from records where ordername <= '%s' and domain_id=%d and disabled=0 and ordername is not null order by 1 desc limit 1
# gmysql-get-order-first-query=select ordername, name from records where domain_id=%d and disabled=0 and ordername is not null order by 1 asc limit 1
# gmysql-get-order-last-query=select ordername, name from records where ordername != '' and domain_id=%d and disabled=0 and ordername is not null order by 1 desc limit 1
# gmysql-get-tsig-key-query=select algorithm, secret from tsigkeys where name='%s'
# gmysql-get-tsig-keys-query=select name,algorithm, secret from tsigkeys
# gmysql-id-query=SELECT content,ttl,prio,type,domain_id,disabled,name,auth FROM records WHERE disabled=0 and type='%s' and name='%s' and domain_id=%d
# gmysql-info-all-master-query=select id,name,master,last_check,notified_serial,type from domains where type='MASTER'
# gmysql-info-all-slaves-query=select id,name,master,last_check,type from domains where type='SLAVE'
# gmysql-info-zone-query=select id,name,master,last_check,notified_serial,type from domains where name='%s'
# gmysql-insert-comment-query=INSERT INTO comments (domain_id, name, type, modified_at, account, comment) VALUES (%d, '%s', '%s', %d, '%s', '%s')
# gmysql-insert-empty-non-terminal-query=insert into records (domain_id,name,type,disabled,auth) values ('%d','%s',null,0,'1')
# gmysql-insert-ent-order-query=insert into records (type,domain_id,disabled,name,ordername,auth) values (null,'%d',0,'%s','%s','%d')
# gmysql-insert-ent-query=insert into records (type,domain_id,disabled,name,auth) values (null,'%d',0,'%s','%d')
# gmysql-insert-record-order-query=insert into records (content,ttl,prio,type,domain_id,disabled,name,ordername,auth) values ('%s',%d,%d,'%s',%d,%d,'%s','%s','%d')
# gmysql-insert-record-query=insert into records (content,ttl,prio,type,domain_id,disabled,name,auth) values ('%s',%d,%d,'%s',%d,%d,'%s','%d')
# gmysql-insert-slave-query=insert into domains (type,name,master,account) values('SLAVE','%s','%s','%s')
# gmysql-insert-zone-query=insert into domains (type,name) values('NATIVE','%s')
# gmysql-list-comments-query=SELECT domain_id,name,type,modified_at,account,comment FROM comments WHERE domain_id=%d
# gmysql-list-domain-keys-query=select cryptokeys.id, flags, active, content from domains, cryptokeys where cryptokeys.domain_id=domains.id and name='%s'
# gmysql-list-query=SELECT content,ttl,prio,type,domain_id,disabled,name,auth FROM records WHERE (disabled=0 OR %d) and domain_id='%d' order by name, type
# gmysql-list-subzone-query=SELECT content,ttl,prio,type,domain_id,disabled,name,auth FROM records WHERE disabled=0 and (name='%s' OR name like '%s') and domain_id='%d'
# gmysql-master-zone-query=select master from domains where name='%s' and type='SLAVE'
# gmysql-nullify-ordername-and-auth-query=update records set ordername=NULL,auth=0 where name='%s' and type='%s' and domain_id='%d' and disabled=0
# gmysql-nullify-ordername-and-update-auth-query=update records set ordername=NULL,auth=%d where domain_id='%d' and name='%s' and disabled=0
# gmysql-remove-domain-key-query=delete from cryptokeys where domain_id=(select id from domains where name='%s') and cryptokeys.id=%d
# gmysql-remove-empty-non-terminals-from-zone-query=delete from records where domain_id='%d' and type is null
# gmysql-set-auth-on-ds-record-query=update records set auth=1 where domain_id='%d' and name='%s' and type='DS' and disabled=0
# gmysql-set-domain-metadata-query=insert into domainmetadata (domain_id, kind, content) select id, '%s', '%s' from domains where name='%s'
# gmysql-set-order-and-auth-query=update records set ordername='%s',auth=%d where name='%s' and domain_id='%d' and disabled=0
# gmysql-set-tsig-key-query=replace into tsigkeys (name,algorithm,secret) values('%s','%s','%s')
# gmysql-supermaster-query=select account from supermasters where ip='%s' and nameserver='%s'
# gmysql-update-kind-query=update domains set type='%s' where name='%s'
# gmysql-update-lastcheck-query=update domains set last_check=%d where id=%d
# gmysql-update-master-query=update domains set master='%s' where name='%s'
# gmysql-update-serial-query=update domains set notified_serial=%d where id=%d
# gmysql-zone-lastchange-query=select max(change_date) from records where domain_id=%d
# gpgsql-activate-domain-key-query=update cryptokeys set active=true where domain_id=(select id from domains where name=E'%s') and  cryptokeys.id=%d
# gpgsql-add-domain-key-query=insert into cryptokeys (domain_id, flags, active, content) select id, %d, (%d = 1), '%s' from domains where name=E'%s'
# gpgsql-any-id-query=SELECT content,ttl,prio,type,domain_id,disabled::int,name,auth::int FROM records WHERE disabled=false and name=E'%s' and domain_id=%d
# gpgsql-any-query=SELECT content,ttl,prio,type,domain_id,disabled::int,name,auth::int FROM records WHERE disabled=false and name=E'%s'
# gpgsql-basic-query=SELECT content,ttl,prio,type,domain_id,disabled::int,name,auth::int FROM records WHERE disabled=false and type='%s' and name=E'%s'
# gpgsql-clear-domain-all-keys-query=delete from cryptokeys where domain_id=(select id from domains where name=E'%s')
# gpgsql-clear-domain-all-metadata-query=delete from domainmetadata where domain_id=(select id from domains where name=E'%s')
# gpgsql-clear-domain-metadata-query=delete from domainmetadata where domain_id=(select id from domains where name=E'%s') and domainmetadata.kind=E'%s'
# gpgsql-deactivate-domain-key-query=update cryptokeys set active=false where domain_id=(select id from domains where name=E'%s') and  cryptokeys.id=%d
# gpgsql-delete-comment-rrset-query=DELETE FROM comments WHERE domain_id=%d AND name=E'%s' AND type=E'%s'
# gpgsql-delete-comments-query=DELETE FROM comments WHERE domain_id=%d
# gpgsql-delete-domain-query=delete from domains where name=E'%s'
# gpgsql-delete-empty-non-terminal-query=delete from records where domain_id='%d' and name='%s' and type is null
# gpgsql-delete-names-query=delete from records where domain_id=%d and name=E'%s'
# gpgsql-delete-rrset-query=delete from records where domain_id=%d and name=E'%s' and type=E'%s'
# gpgsql-delete-tsig-key-query=delete from tsigkeys where name='%s'
# gpgsql-delete-zone-query=delete from records where domain_id=%d
# gpgsql-get-all-domain-metadata-query=select kind,content from domains, domainmetadata where domainmetadata.domain_id=domains.id and name=E'%s'
# gpgsql-get-all-domains-query=select domains.id, domains.name, records.content, domains.type, domains.master, domains.notified_serial, domains.last_check from domains LEFT JOIN records ON records.domain_id=domains.id AND records.type='SOA' AND records.name=domains.name WHERE records.disabled=false OR %d::bool
# gpgsql-get-domain-metadata-query=select content from domains, domainmetadata where domainmetadata.domain_id=domains.id and name=E'%s' and domainmetadata.kind=E'%s'
# gpgsql-get-order-after-query=select ordername from records where disabled=false and ordername ~>~ E'%s' and domain_id=%d and ordername is not null order by 1 using ~<~ limit 1
# gpgsql-get-order-before-query=select ordername, name from records where disabled=false and ordername ~<=~ E'%s' and domain_id=%d and ordername is not null order by 1 using ~>~ limit 1
# gpgsql-get-order-first-query=select ordername, name from records where disabled=false and domain_id=%d and ordername is not null order by 1 using ~<~ limit 1
# gpgsql-get-order-last-query=select ordername, name from records where disabled=false and ordername != '' and domain_id=%d and ordername is not null order by 1 using ~>~ limit 1
# gpgsql-get-tsig-key-query=select algorithm, secret from tsigkeys where name=E'%s'
# gpgsql-get-tsig-keys-query=select name,algorithm, secret from tsigkeys
# gpgsql-id-query=SELECT content,ttl,prio,type,domain_id,disabled::int,name,auth::int FROM records WHERE disabled=false and type='%s' and name=E'%s' and domain_id=%d
# gpgsql-info-all-master-query=select id,name,master,last_check,notified_serial,type from domains where type='MASTER'
# gpgsql-info-all-slaves-query=select id,name,master,last_check,type from domains where type='SLAVE'
# gpgsql-info-zone-query=select id,name,master,last_check,notified_serial,type from domains where name=E'%s'
# gpgsql-insert-comment-query=INSERT INTO comments (domain_id, name, type, modified_at, account, comment) VALUES (%d, E'%s', E'%s', %d, E'%s', E'%s')
# gpgsql-insert-empty-non-terminal-query=insert into records (domain_id,name,type,disabled,auth) values ('%d','%s',null,false,true)
# gpgsql-insert-ent-order-query=insert into records (type,domain_id,disabled,name,ordername,auth) values (null,'%d',false,E'%s',E'%s','%d')
# gpgsql-insert-ent-query=insert into records (type,domain_id,disabled,name,auth) values (null,'%d',false,E'%s','%d')
# gpgsql-insert-record-order-query=insert into records (content,ttl,prio,type,domain_id,disabled,name,ordername,auth) values (E'%s',%d,%d,'%s',%d,%d::bool,E'%s',E'%s','%d')
# gpgsql-insert-record-query=insert into records (content,ttl,prio,type,domain_id,disabled,name,auth) values (E'%s',%d,%d,'%s',%d,%d::bool,E'%s','%d')
# gpgsql-insert-slave-query=insert into domains (type,name,master,account) values('SLAVE',E'%s',E'%s',E'%s')
# gpgsql-insert-zone-query=insert into domains (type,name) values('NATIVE',E'%s')
# gpgsql-list-comments-query=SELECT domain_id,name,type,modified_at,account,comment FROM comments WHERE domain_id=%d
# gpgsql-list-domain-keys-query=select cryptokeys.id, flags, case when active then 1 else 0 end as active, content from domains, cryptokeys where cryptokeys.domain_id=domains.id and name=E'%s'
# gpgsql-list-query=SELECT content,ttl,prio,type,domain_id,disabled::int,name,auth::int FROM records WHERE (disabled=false OR %d::bool) and domain_id='%d' order by name, type
# gpgsql-list-subzone-query=SELECT content,ttl,prio,type,domain_id,disabled::int,name,auth::int FROM records WHERE disabled=false and (name=E'%s' OR name like E'%s') and domain_id='%d'
# gpgsql-master-zone-query=select master from domains where name=E'%s' and type='SLAVE'
# gpgsql-nullify-ordername-and-auth-query=update records set ordername=NULL,auth=false where name=E'%s' and type=E'%s' and domain_id='%d' and disabled=false
# gpgsql-nullify-ordername-and-update-auth-query=update records set ordername=NULL,auth=%d::bool where domain_id='%d' and name='%s' and disabled=false
# gpgsql-remove-domain-key-query=delete from cryptokeys where domain_id=(select id from domains where name=E'%s') and cryptokeys.id=%d
# gpgsql-remove-empty-non-terminals-from-zone-query=delete from records where domain_id='%d' and type is null
# gpgsql-set-auth-on-ds-record-query=update records set auth=true where domain_id='%d' and name='%s' and type='DS' and disabled=false
# gpgsql-set-domain-metadata-query=insert into domainmetadata (domain_id, kind, content) select id, '%s', '%s' from domains where name=E'%s'
# gpgsql-set-order-and-auth-query=update records set ordername=E'%s',auth=%d::bool where name=E'%s' and domain_id='%d' and disabled=false
# gpgsql-set-tsig-key-query=insert into tsigkeys (name,algorithm,secret) values('%s','%s','%s')
# gpgsql-supermaster-query=select account from supermasters where ip='%s' and nameserver=E'%s'
# gpgsql-update-kind-query=update domains set type='%s' where name='%s'
# gpgsql-update-lastcheck-query=update domains set last_check=%d where id=%d
# gpgsql-update-master-query=update domains set master='%s' where name='%s'
# gpgsql-update-serial-query=update domains set notified_serial=%d where id=%d
# gpgsql-zone-lastchange-query=select max(change_date) from records where domain_id=%d
"""
TABLES=['comments','cryptokeys','domainmetadata','domains','records','supermasters','tsigkeys']

class PDNSConfigBuilder(object):
    def __init__(self):
        self.defaultconfig= self._init_config()
        self.prefix=''

    def _init_config(self):
        conf={}
        for line in DEFAULTCONFIG.split('\n'):
            if not line.startswith('# g'):
                continue
            #remove # and leading/trailing whitespace
            line=line[1:].strip()

            #extract the backend
            backend=line[0:line.find('-')]

            if backend not in conf:
                conf[backend]={}

            #extract config option and query
            config_option = line[0:line.find('=')]
            query=line[line.find('=')+1:]

            conf[backend][config_option]=query
        return conf

    def build(self,backend):
        assert backend in self.defaultconfig
        buff=''
        for option in sorted(self.defaultconfig[backend].keys()):
            sql=self.defaultconfig[backend][option]
            for table in TABLES:
                sql=sql.replace(table,self.prefix+table)
            buff=buff+"%s=%s\n"%(option,sql)
        return buff

if __name__=='__main__':
    if len(sys.argv)!=3:
        print "arg: <backend> <prefix>"
        sys.exit(1)

    writer=PDNSConfigBuilder()
    backend=sys.argv[1]
    if backend not in writer.defaultconfig:
        print "unsupported backend. use one of: %s"%(" ".join(writer.defaultconfig.keys()))
        sys.exit(1)

    prefix=sys.argv[2]
    writer.prefix=prefix
    config=writer.build(backend)
    print config
