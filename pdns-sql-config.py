#!/usr/bin/python
import sys

# get this using the command:
# pdns_server --no-config --config --launch=gmysql,gpgsql 2>/dev/null | grep 'query='
DEFAULTCONFIG="""
# gmysql-activate-domain-key-query=update cryptokeys set active=1 where domain_id=(select id from domains where name=?) and  cryptokeys.id=?
# gmysql-add-domain-key-query=insert into cryptokeys (domain_id, flags, active, published, content) select id, ?, ?, ?, ? from domains where name=?
# gmysql-any-id-query=SELECT content,ttl,prio,type,domain_id,disabled,name,auth FROM records WHERE disabled=0 and name=? and domain_id=?
# gmysql-any-query=SELECT content,ttl,prio,type,domain_id,disabled,name,auth FROM records WHERE disabled=0 and name=?
# gmysql-basic-query=SELECT content,ttl,prio,type,domain_id,disabled,name,auth FROM records WHERE disabled=0 and type=? and name=?
# gmysql-clear-domain-all-keys-query=delete from cryptokeys where domain_id=(select id from domains where name=?)
# gmysql-clear-domain-all-metadata-query=delete from domainmetadata where domain_id=(select id from domains where name=?)
# gmysql-clear-domain-metadata-query=delete from domainmetadata where domain_id=(select id from domains where name=?) and domainmetadata.kind=?
# gmysql-deactivate-domain-key-query=update cryptokeys set active=0 where domain_id=(select id from domains where name=?) and  cryptokeys.id=?
# gmysql-delete-comment-rrset-query=DELETE FROM comments WHERE domain_id=? AND name=? AND type=?
# gmysql-delete-comments-query=DELETE FROM comments WHERE domain_id=?
# gmysql-delete-domain-query=delete from domains where name=?
# gmysql-delete-empty-non-terminal-query=delete from records where domain_id=? and name=? and type is null
# gmysql-delete-names-query=delete from records where domain_id=? and name=?
# gmysql-delete-rrset-query=delete from records where domain_id=? and name=? and type=?
# gmysql-delete-tsig-key-query=delete from tsigkeys where name=?
# gmysql-delete-zone-query=delete from records where domain_id=?
# gmysql-get-all-domain-metadata-query=select kind,content from domains, domainmetadata where domainmetadata.domain_id=domains.id and name=?
# gmysql-get-all-domains-query=select domains.id, domains.name, records.content, domains.type, domains.master, domains.notified_serial, domains.last_check, domains.account from domains LEFT JOIN records ON records.domain_id=domains.id AND records.type='SOA' AND records.name=domains.name WHERE records.disabled=0 OR ?
# gmysql-get-domain-metadata-query=select content from domains, domainmetadata where domainmetadata.domain_id=domains.id and name=? and domainmetadata.kind=?
# gmysql-get-last-inserted-key-id-query=select LAST_INSERT_ID()
# gmysql-get-order-after-query=select ordername from records where ordername > ? and domain_id=? and disabled=0 and ordername is not null order by 1 asc limit 1
# gmysql-get-order-before-query=select ordername, name from records where ordername <= ? and domain_id=? and disabled=0 and ordername is not null order by 1 desc limit 1
# gmysql-get-order-first-query=select ordername from records where domain_id=? and disabled=0 and ordername is not null order by 1 asc limit 1
# gmysql-get-order-last-query=select ordername, name from records where ordername != '' and domain_id=? and disabled=0 and ordername is not null order by 1 desc limit 1
# gmysql-get-tsig-key-query=select algorithm, secret from tsigkeys where name=?
# gmysql-get-tsig-keys-query=select name,algorithm, secret from tsigkeys
# gmysql-id-query=SELECT content,ttl,prio,type,domain_id,disabled,name,auth FROM records WHERE disabled=0 and type=? and name=? and domain_id=?
# gmysql-info-all-master-query=select d.id, d.name, d.notified_serial, r.content from records r join domains d on r.name=d.name where r.type='SOA' and r.disabled=0 and d.type='MASTER'
# gmysql-info-all-slaves-query=select id,name,master,last_check from domains where type='SLAVE'
# gmysql-info-zone-query=select id,name,master,last_check,notified_serial,type,account from domains where name=?
# gmysql-insert-comment-query=INSERT INTO comments (domain_id, name, type, modified_at, account, comment) VALUES (?, ?, ?, ?, ?, ?)
# gmysql-insert-empty-non-terminal-order-query=insert into records (type,domain_id,disabled,name,ordername,auth,content,ttl,prio) values (null,?,0,?,?,?,NULL,NULL,NULL)
# gmysql-insert-record-query=insert into records (content,ttl,prio,type,domain_id,disabled,name,ordername,auth) values (?,?,?,?,?,?,?,?,?)
# gmysql-insert-zone-query=insert into domains (type,name,master,account,last_check,notified_serial) values(?,?,?,?,NULL,NULL)
# gmysql-list-comments-query=SELECT domain_id,name,type,modified_at,account,comment FROM comments WHERE domain_id=?
# gmysql-list-domain-keys-query=select cryptokeys.id, flags, active, published, content from domains, cryptokeys where cryptokeys.domain_id=domains.id and name=?
# gmysql-list-query=SELECT content,ttl,prio,type,domain_id,disabled,name,auth FROM records WHERE (disabled=0 OR ?) and domain_id=? order by name, type
# gmysql-list-subzone-query=SELECT content,ttl,prio,type,domain_id,disabled,name,auth FROM records WHERE disabled=0 and (name=? OR name like ?) and domain_id=?
# gmysql-nullify-ordername-and-update-auth-query=update records set ordername=NULL,auth=? where domain_id=? and name=? and disabled=0
# gmysql-nullify-ordername-and-update-auth-type-query=update records set ordername=NULL,auth=? where domain_id=? and name=? and type=? and disabled=0
# gmysql-publish-domain-key-query=update cryptokeys set published=1 where domain_id=(select id from domains where name=?) and  cryptokeys.id=?
# gmysql-remove-domain-key-query=delete from cryptokeys where domain_id=(select id from domains where name=?) and cryptokeys.id=?
# gmysql-remove-empty-non-terminals-from-zone-query=delete from records where domain_id=? and type is null
# gmysql-search-comments-query=SELECT domain_id,name,type,modified_at,account,comment FROM comments WHERE name LIKE ? OR comment LIKE ? LIMIT ?
# gmysql-search-records-query=SELECT content,ttl,prio,type,domain_id,disabled,name,auth FROM records WHERE name LIKE ? OR content LIKE ? LIMIT ?
# gmysql-set-domain-metadata-query=insert into domainmetadata (domain_id, kind, content) select id, ?, ? from domains where name=?
# gmysql-set-tsig-key-query=replace into tsigkeys (name,algorithm,secret) values(?,?,?)
# gmysql-supermaster-query=select account from supermasters where ip=? and nameserver=?
# gmysql-unpublish-domain-key-query=update cryptokeys set published=0 where domain_id=(select id from domains where name=?) and  cryptokeys.id=?
# gmysql-update-account-query=update domains set account=? where name=?
# gmysql-update-kind-query=update domains set type=? where name=?
# gmysql-update-lastcheck-query=update domains set last_check=? where id=?
# gmysql-update-master-query=update domains set master=? where name=?
# gmysql-update-ordername-and-auth-query=update records set ordername=?,auth=? where domain_id=? and name=? and disabled=0
# gmysql-update-ordername-and-auth-type-query=update records set ordername=?,auth=? where domain_id=? and name=? and type=? and disabled=0
# gmysql-update-serial-query=update domains set notified_serial=? where id=?
# gpgsql-activate-domain-key-query=update cryptokeys set active=true where domain_id=(select id from domains where name=$1) and  cryptokeys.id=$2
# gpgsql-add-domain-key-query=insert into cryptokeys (domain_id, flags, active, published, content) select id, $1, $2, $3, $4 from domains where name=$5
# gpgsql-any-id-query=SELECT content,ttl,prio,type,domain_id,disabled::int,name,auth::int FROM records WHERE disabled=false and name=$1 and domain_id=$2
# gpgsql-any-query=SELECT content,ttl,prio,type,domain_id,disabled::int,name,auth::int FROM records WHERE disabled=false and name=$1
# gpgsql-basic-query=SELECT content,ttl,prio,type,domain_id,disabled::int,name,auth::int FROM records WHERE disabled=false and type=$1 and name=$2
# gpgsql-clear-domain-all-keys-query=delete from cryptokeys where domain_id=(select id from domains where name=$1)
# gpgsql-clear-domain-all-metadata-query=delete from domainmetadata where domain_id=(select id from domains where name=$1)
# gpgsql-clear-domain-metadata-query=delete from domainmetadata where domain_id=(select id from domains where name=$1) and domainmetadata.kind=$2
# gpgsql-deactivate-domain-key-query=update cryptokeys set active=false where domain_id=(select id from domains where name=$1) and  cryptokeys.id=$2
# gpgsql-delete-comment-rrset-query=DELETE FROM comments WHERE domain_id=$1 AND name=$2 AND type=$3
# gpgsql-delete-comments-query=DELETE FROM comments WHERE domain_id=$1
# gpgsql-delete-domain-query=delete from domains where name=$1
# gpgsql-delete-empty-non-terminal-query=delete from records where domain_id=$1 and name=$2 and type is null
# gpgsql-delete-names-query=delete from records where domain_id=$1 and name=$2
# gpgsql-delete-rrset-query=delete from records where domain_id=$1 and name=$2 and type=$3
# gpgsql-delete-tsig-key-query=delete from tsigkeys where name=$1
# gpgsql-delete-zone-query=delete from records where domain_id=$1
# gpgsql-get-all-domain-metadata-query=select kind,content from domains, domainmetadata where domainmetadata.domain_id=domains.id and name=$1
# gpgsql-get-all-domains-query=select domains.id, domains.name, records.content, domains.type, domains.master, domains.notified_serial, domains.last_check, domains.account from domains LEFT JOIN records ON records.domain_id=domains.id AND records.type='SOA' AND records.name=domains.name WHERE records.disabled=false OR $1
# gpgsql-get-domain-metadata-query=select content from domains, domainmetadata where domainmetadata.domain_id=domains.id and name=$1 and domainmetadata.kind=$2
# gpgsql-get-last-inserted-key-id-query=select lastval()
# gpgsql-get-order-after-query=select ordername from records where disabled=false and ordername ~>~ $1 and domain_id=$2 and ordername is not null order by 1 using ~<~ limit 1
# gpgsql-get-order-before-query=select ordername, name from records where disabled=false and ordername ~<=~ $1 and domain_id=$2 and ordername is not null order by 1 using ~>~ limit 1
# gpgsql-get-order-first-query=select ordername from records where disabled=false and domain_id=$1 and ordername is not null order by 1 using ~<~ limit 1
# gpgsql-get-order-last-query=select ordername, name from records where disabled=false and ordername != '' and domain_id=$1 and ordername is not null order by 1 using ~>~ limit 1
# gpgsql-get-tsig-key-query=select algorithm, secret from tsigkeys where name=$1
# gpgsql-get-tsig-keys-query=select name,algorithm, secret from tsigkeys
# gpgsql-id-query=SELECT content,ttl,prio,type,domain_id,disabled::int,name,auth::int FROM records WHERE disabled=false and type=$1 and name=$2 and domain_id=$3
# gpgsql-info-all-master-query=select domains.id, domains.name, domains.notified_serial, records.content from records join domains on records.name=domains.name where records.type='SOA' and records.disabled=false and domains.type='MASTER'
# gpgsql-info-all-slaves-query=select id,name,master,last_check from domains where type='SLAVE'
# gpgsql-info-zone-query=select id,name,master,last_check,notified_serial,type,account from domains where name=$1
# gpgsql-insert-comment-query=INSERT INTO comments (domain_id, name, type, modified_at, account, comment) VALUES ($1, $2, $3, $4, $5, $6)
# gpgsql-insert-empty-non-terminal-order-query=insert into records (type,domain_id,disabled,name,ordername,auth,ttl,prio,content) values (null,$1,false,$2,$3,$4,null,null,null)
# gpgsql-insert-record-query=insert into records (content,ttl,prio,type,domain_id,disabled,name,ordername,auth) values ($1,$2,$3,$4,$5,$6,$7,$8,$9)
# gpgsql-insert-zone-query=insert into domains (type,name,master,account,last_check, notified_serial) values($1,$2,$3,$4,null,null)
# gpgsql-list-comments-query=SELECT domain_id,name,type,modified_at,account,comment FROM comments WHERE domain_id=$1
# gpgsql-list-domain-keys-query=select cryptokeys.id, flags, case when active then 1 else 0 end as active, case when published then 1 else 0 end as published, content from domains, cryptokeys where cryptokeys.domain_id=domains.id and name=$1
# gpgsql-list-query=SELECT content,ttl,prio,type,domain_id,disabled::int,name,auth::int FROM records WHERE (disabled=false OR $1) and domain_id=$2 order by name, type
# gpgsql-list-subzone-query=SELECT content,ttl,prio,type,domain_id,disabled::int,name,auth::int FROM records WHERE disabled=false and (name=$1 OR name like $2) and domain_id=$3
# gpgsql-nullify-ordername-and-update-auth-query=update records set ordername=NULL,auth=$1 where domain_id=$2 and name=$3 and disabled=false
# gpgsql-nullify-ordername-and-update-auth-type-query=update records set ordername=NULL,auth=$1 where domain_id=$2 and name=$3 and type=$4 and disabled=false
# gpgsql-publish-domain-key-query=update cryptokeys set published=true where domain_id=(select id from domains where name=$1) and  cryptokeys.id=$2
# gpgsql-remove-domain-key-query=delete from cryptokeys where domain_id=(select id from domains where name=$1) and cryptokeys.id=$2
# gpgsql-remove-empty-non-terminals-from-zone-query=delete from records where domain_id=$1 and type is null
# gpgsql-search-comments-query=SELECT domain_id,name,type,modified_at,account,comment FROM comments WHERE name LIKE $1 OR comment LIKE $2 LIMIT $3
# gpgsql-search-records-query=SELECT content,ttl,prio,type,domain_id,disabled::int,name,auth::int FROM records WHERE name LIKE $1 OR content LIKE $2 LIMIT $3
# gpgsql-set-domain-metadata-query=insert into domainmetadata (domain_id, kind, content) select id, $1, $2 from domains where name=$3
# gpgsql-set-tsig-key-query=insert into tsigkeys (name,algorithm,secret) values($1,$2,$3)
# gpgsql-supermaster-query=select account from supermasters where ip=$1 and nameserver=$2
# gpgsql-unpublish-domain-key-query=update cryptokeys set published=false where domain_id=(select id from domains where name=$1) and  cryptokeys.id=$2
# gpgsql-update-account-query=update domains set account=$1 where name=$2
# gpgsql-update-kind-query=update domains set type=$1 where name=$2
# gpgsql-update-lastcheck-query=update domains set last_check=$1 where id=$2
# gpgsql-update-master-query=update domains set master=$1 where name=$2
# gpgsql-update-ordername-and-auth-query=update records set ordername=$1,auth=$2 where domain_id=$3 and name=$4 and disabled=false
# gpgsql-update-ordername-and-auth-type-query=update records set ordername=$1,auth=$2 where domain_id=$3 and name=$4 and type=$5 and disabled=false
# gpgsql-update-serial-query=update domains set notified_serial=$1 where id=$2
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
