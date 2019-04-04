# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from googleapiclient.discovery import build
from urllib import request
from django.conf import settings
import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from dns import resolver
import shodan


@shared_task(name=('advanced_crawler'))
def advanced_crawler(url, depth=1, mobile_emulation=False, allow_external=False):
    chrome_driver_path = settings.CHROME_DRIVER_PATH
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--ignore-certificate-errors')

    # handle mobile version crawler
    if mobile_emulation:
        device_emulation = {"deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }
    else:
        device_emulation = {"deviceMetrics": { "width": 1920, "height": 1080}}

    chrome_options.add_experimental_option("mobileEmulation", device_emulation)

    #initialisation of result object
    result = {'data':[]}

    #initialisation of links list
    links=[]
    links.append(url)

    #test lines, to remove
    with webdriver.Chrome(chrome_driver_path,chrome_options = chrome_options ) as driver:
        print('driver path: %s' % chrome_driver_path)
        driver.get(url)
        print(driver.page_source)

    for i in range(depth):

        for url in links:
            #get sourcecode using selenium
            try:
                with webdriver.Chrome(chrome_driver_path,chrome_options = chrome_options ) as driver:
                    driver.get(url)
                    source_code = driver.page_source
                    domain = url.split('/', 3)[0]
            except:
                print('error with get url: '+url)
                continue

            links = []
            #find urls in source code using bs4
            soup = BeautifulSoup(source_code)

            for link in soup.findAll('a', href=True):
                link=link['href']
                links.append(link)

            # take care of relative links
            for idx, item in enumerate(links):
                try:
                    if links[idx][0]=='/':
                        actual = links[idx]
                        links[idx] = domain+actual
                except:
                    pass
                
            # put out false positives
            for idx, item in enumerate(links):
                if links[idx][0:3]!='http':
                    del links[idx]

            links = list(set(links))

            # adding data to the result object for this page
            result['data'].append({'url':url, 'source_code':source_code, 'links':links})
            #remove external domain in links
            if not allow_external:
                for idx, item in enumerate(links):
                    if domain not in links[idx]:
                        del links[idx]
    return result

@shared_task(name=('google_search'))
def google_search(query, num=None, dateRestrict=None, exactTerms=None, fileType=None, gl=None, linkSite=None,\
    lr=None, orTerms=None, relatedSite=None, sort=None, siteSearch=None, searchType=None):

    #importing user-specific settings:
    with open(settings.TASKS_CONF_FILE, 'r') as file:
        for line in file:
            if 'GOOGLE_API' in line:
                google_api=line.replace('GOOGLE_API=','').replace('\n','')
            elif 'GOOGLE_CSE_ID' in line:
                google_cse_id=line.replace('GOOGLE_CSE_ID=','').replace('\n','')


    service = build("customsearch", "v1", developerKey=google_api)

    #num=number of results
    #cx=id du custom search engine
    #filter=0 pour desactiver le filtre de google qui empeche d'avoir des resultas similaires, nous voulons tous les resultats, meme similaires
    #dateRestrict=recherche sur une periode donnee, se fait du style: dateRestrict='y1' pour il y a un an, m2=il y a 2 mois, d5=il y a 5 jours, w6= il y a 6 semaines
    #exactTerms=termes qui doivent obligatoirement etre trouves
    #fileType=rechercher type de fichier specifique
    #gl=geolocation de la requete, sous forme de code pays: fr, uk, us, de ...
    #linkSite=tous les resultats doivent contenir un lien vers cette url
    #lr=restriction langue des resultats, sous forme lang_codepays: lang_fr, lang_de, lang_en ...
    #orTerms=string qui doit etre contenu dans chaque document retourne par la recherche
    #relatedSite=chaque resultat doit etre relie a
    #siteSearch=chaque resultat doit etre d'un domaine particulier
    #sort=string expression pour classer les resultats
    #searchType=recherche d'image ou web

    res = service.cse().list(
      q=query, cx=google_cse_id, filter='0',
      num=num, dateRestrict=dateRestrict, exactTerms=exactTerms, fileType=fileType, gl=gl, linkSite=linkSite,\
      lr=lr, orTerms=orTerms, relatedSite=relatedSite, sort=sort, siteSearch=siteSearch, searchType=searchType ).execute()
    print(res)
    return res

@shared_task(name=('pgp_search'))
def pgp_search(querry):
    
    d = ["pgp.mit.edu","pgp.key-server.io"]
    q = querry.replace(' ','%20')
    data = {'data':[]}
    for s in d:
        try:
            res = request.urlopen("https://" + s + "/pks/lookup?search=" + q + "&op=index").read().decode('utf-8')
            res = res.split("""<a href="/pks/lookup?op=vindex&amp;search=""")[1:]
            for element in res:
                public_key = element.split('"')[0]
                name = element.split('">')[1].split('&lt;')[0]
                email = element.split('&lt;')[1].split('&gt;')[0]
                data['data'].append({'name':name, 'email':email, 'public_key_fingerprint':public_key})
        except Exception as e: 
            print(e)
            pass
    return data

@shared_task(name=('ct_search'))
def ct_search(keyword):
    try:
        result =[item['name_value'] for item in json.load(request.urlopen("https://crt.sh/?q=%"+keyword+"&output=json"))]
        result.extend([item['name_value'] for item in json.load(request.urlopen("https://crt.sh/?q="+keyword+"%&output=json"))])
        result = list(set(result))
        result = {'domains': result}
    except:
        return {'domains': []}
    return result

@shared_task(name=('dns_lookup'))
def dns_lookup(query, type_A=True, type_AAAA=False, type_CNAME=False, type_NS=False, type_MX=False, type_TXT=False, type_ALL=False):

    all_record_type = ['A','AAAA', 'AFSDB', 'APL', 'CAA', 'CDNSKEY', 'CERT', 'CNAME', 'DHCID', 'DLV', 'DNAME', 'DS', 'HIP', 'IPSECKEY', 'KEY', 'KX', \
    'LOC', 'MX', 'NAPTR', 'NS', 'NSEC', 'NSEC3', 'NSEC3PARAM', 'OPENPGPKEY', 'PTR', 'RRSIG', 'RP', 'SIG', 'SMIMEA', 'SOA', 'SRV', 'SSHFP', 'TA', 'TKEY', \
    'TLSA', 'TSIG', 'TXT', 'URI']

    record_types_to_query = []

    if type_A:
        record_types_to_query.append('A')
    if type_AAAA:
        record_types_to_query.append('AAAA')
    if type_CNAME:
        record_types_to_query.append('CNAME')
    if type_NS:
        record_types_to_query.append('NS')
    if type_MX:
        record_types_to_query.append('MX')
    if type_TXT:
        record_types_to_query.append('TXT')
    if type_ALL:
        record_types_to_query = all_record_type

    resolver_instance = resolver.Resolver()

    res = {'data':[]}

    for record_type in record_types_to_query:
        try:
            if record_type == 'CNAME':
                result = resolver_instance.query(query, 'CNAME')
                [res['data'].append({'query':str(query), 'record_type':'CNAME', 'result':str(e)}) for e in result]
                while len(result) >= 1:
                    for data in result:
                        result = resolver_instance.query(str(data), 'CNAME')
                        [res['data'].append({'query':str(data), 'record_type':'CNAME', 'result':str(e)}) for e in result]
            else:
                result = resolver_instance.query(query, record_type)
                for data in result:
                    res['data'].append({'query': query, 'record_type':record_type, 'result':str(data)})
        except:
            pass
    return res


    ##### dns records type informations:
    # A 	1 	RFC 1035[1] 	Address record 	Returns a 32-bit IPv4 address, most commonly used to map hostnames to an IP address of the host, but it is also used for DNSBLs, storing subnet masks in RFC 1101, etc.
    # AAAA 	28 	RFC 3596[2] 	IPv6 address record 	Returns a 128-bit IPv6 address, most commonly used to map hostnames to an IP address of the host.
    # AFSDB 	18 	RFC 1183 	AFS database record 	Location of database servers of an AFS cell. This record is commonly used by AFS clients to contact AFS cells outside their local domain. A subtype of this record is used by the obsolete DCE/DFS file system.
    # APL 	42 	RFC 3123 	Address Prefix List 	Specify lists of address ranges, e.g. in CIDR format, for various address families. Experimental.
    # CAA 	257 	RFC 6844 	Certification Authority Authorization 	DNS Certification Authority Authorization, constraining acceptable CAs for a host/domain
    # CDNSKEY 	60 	RFC 7344 		Child copy of DNSKEY record, for transfer to parent
    # CDS 	59 	RFC 7344 	Child DS 	Child copy of DS record, for transfer to parent
    # CERT 	37 	RFC 4398 	Certificate record 	Stores PKIX, SPKI, PGP, etc.
    # CNAME 	5 	RFC 1035[1] 	Canonical name record 	Alias of one name to another: the DNS lookup will continue by retrying the lookup with the new name.
    # DHCID 	49 	RFC 4701 	DHCP identifier 	Used in conjunction with the FQDN option to DHCP
    # DLV 	32769 	RFC 4431 	DNSSEC Lookaside Validation record 	For publishing DNSSEC trust anchors outside of the DNS delegation chain. Uses the same format as the DS record. RFC 5074 describes a way of using these records.
    # DNAME 	39 	RFC 6672 		Alias for a name and all its subnames, unlike CNAME, which is an alias for only the exact name. Like a CNAME record, the DNS lookup will continue by retrying the lookup with the new name.
    # DNSKEY 	48 	RFC 4034 	DNS Key record 	The key record used in DNSSEC. Uses the same format as the KEY record.
    # DS 	43 	RFC 4034 	Delegation signer 	The record used to identify the DNSSEC signing key of a delegated zone
    # HIP 	55 	RFC 8005 	Host Identity Protocol 	Method of separating the end-point identifier and locator roles of IP addresses.
    # IPSECKEY 	45 	RFC 4025 	IPsec Key 	Key record that can be used with IPsec
    # KEY 	25 	RFC 2535[3] and RFC 2930[4] 	Key record 	Used only for SIG(0) (RFC 2931) and TKEY (RFC 2930).[5] RFC 3445 eliminated their use for application keys and limited their use to DNSSEC.[6] RFC 3755 designates DNSKEY as the replacement within DNSSEC.[7] RFC 4025 designates IPSECKEY as the replacement for use with IPsec.[8]
    # KX 	36 	RFC 2230 	Key Exchanger record 	Used with some cryptographic systems (not including DNSSEC) to identify a key management agent for the associated domain-name. Note that this has nothing to do with DNS Security. It is Informational status, rather than being on the IETF standards-track. It has always had limited deployment, but is still in use.
    # LOC 	29 	RFC 1876 	Location record 	Specifies a geographical location associated with a domain name
    # MX 	15 	RFC 1035[1] and RFC 7505 	Mail exchange record 	Maps a domain name to a list of message transfer agents for that domain
    # NAPTR 	35 	RFC 3403 	Naming Authority Pointer 	Allows regular-expression-based rewriting of domain names which can then be used as URIs, further domain names to lookups, etc.
    # NS 	2 	RFC 1035[1] 	Name server record 	Delegates a DNS zone to use the given authoritative name servers
    # NSEC 	47 	RFC 4034 	Next Secure record 	Part of DNSSEC—used to prove a name does not exist. Uses the same format as the (obsolete) NXT record.
    # NSEC3 	50 	RFC 5155 	Next Secure record version 3 	An extension to DNSSEC that allows proof of nonexistence for a name without permitting zonewalking
    # NSEC3PARAM 	51 	RFC 5155 	NSEC3 parameters 	Parameter record for use with NSEC3
    # OPENPGPKEY 	61 	RFC 7929 	OpenPGP public key record 	A DNS-based Authentication of Named Entities (DANE) method for publishing and locating OpenPGP public keys in DNS for a specific email address using an OPENPGPKEY DNS resource record.
    # PTR 	12 	RFC 1035[1] 	Pointer record 	Pointer to a canonical name. Unlike a CNAME, DNS processing stops and just the name is returned. The most common use is for implementing reverse DNS lookups, but other uses include such things as DNS-SD.
    # RRSIG 	46 	RFC 4034 	DNSSEC signature 	Signature for a DNSSEC-secured record set. Uses the same format as the SIG record.
    # RP 	17 	RFC 1183 	Responsible Person 	Information about the responsible person(s) for the domain. Usually an email address with the @ replaced by a .
    # SIG 	24 	RFC 2535 	Signature 	Signature record used in SIG(0) (RFC 2931) and TKEY (RFC 2930).[7] RFC 3755 designated RRSIG as the replacement for SIG for use within DNSSEC.[7]
    # SMIMEA 	53 	RFC 8162[9] 	S/MIME cert association[10] 	Associates an S/MIME certificate with a domain name for sender authentication.
    # SOA 	6 	RFC 1035[1] and RFC 2308[11] 	Start of [a zone of] authority record 	Specifies authoritative information about a DNS zone, including the primary name server, the email of the domain administrator, the domain serial number, and several timers relating to refreshing the zone.
    # SRV 	33 	RFC 2782 	Service locator 	Generalized service location record, used for newer protocols instead of creating protocol-specific records such as MX.
    # SSHFP 	44 	RFC 4255 	SSH Public Key Fingerprint 	Resource record for publishing SSH public host key fingerprints in the DNS System, in order to aid in verifying the authenticity of the host. RFC 6594 defines ECC SSH keys and SHA-256 hashes. See the IANA SSHFP RR parameters registry for details.
    # TA 	32768 	N/A 	DNSSEC Trust Authorities 	Part of a deployment proposal for DNSSEC without a signed DNS root. See the IANA database and Weiler Spec for details. Uses the same format as the DS record.
    # TKEY 	249 	RFC 2930 	Transaction Key record 	A method of providing keying material to be used with TSIG that is encrypted under the public key in an accompanying KEY RR.[12]
    # TLSA 	52 	RFC 6698 	TLSA certificate association 	A record for DANE. RFC 6698 defines "The TLSA DNS resource record is used to associate a TLS server certificate or public key with the domain name where the record is found, thus forming a 'TLSA certificate association'".
    # TSIG 	250 	RFC 2845 	Transaction Signature 	Can be used to authenticate dynamic updates as coming from an approved client, or to authenticate responses as coming from an approved recursive name server[13] similar to DNSSEC.
    # TXT 	16 	RFC 1035[1] 	Text record 	Originally for arbitrary human-readable text in a DNS record. Since the early 1990s, however, this record more often carries machine-readable data, such as specified by RFC 1464, opportunistic encryption, Sender Policy Framework, DKIM, DMARC, DNS-SD, etc.
    # URI 	256 	RFC 7553 	Uniform Resource Identifier 	Can be used for publishing mappings from hostnames to URIs. 

@shared_task(name=('simple_crawler'))
def simple_crawler(url, depth=1, allow_external=False):

    domain = url.split('/')[2]
    print(domain)
    current_depth = 0
    data = {'data':[]}
    links = []
    links.append(url)

    while current_depth < depth:
        for url in links:
            try:
                source_code = request.urlopen(url).read().decode('utf-8')
            except:
                continue
            #find urls in source code using bs4
            soup = BeautifulSoup(source_code)
            links = []
            for link in soup.findAll('a', href=True):
                link=link['href']
                links.append(link)

            # keeping unique values in links
            links = list(set(links))
            data['data'].append({'url':url, 'source_code':source_code, 'links':links})

            if not allow_external:
                for idx, link in enumerate(links):
                    if domain not in link:
                        del links[idx]
            current_depth +=1
    return data

@shared_task(name=('shodan_search'))
def shodan_search(query):
        #importing user-specific settings:
    with open(settings.TASKS_CONF_FILE, 'r') as file:
        for line in file:
            if 'SHODAN_API_KEY' in line:
                shodan_api_key=line.replace('SHODAN_API_KEY=','').replace('\n','')

    api = shodan.Shodan(shodan_api_key)

    res = {'res':[]}
    try:
        results = api.search(query)

        for result in results['matches']:
            # print('IP: {}'.format(result['ip_str']))
            ip = result['ip_str']
            hostnames = result['hostnames']
            domains = result['domains']
            shodan_id = result['_shodan']['id']
            location = {'lon':result['location']['longitude'], 'lat':result['location']['latitude']}
            port = result['port']
            data = result['data']
            res['res'].append({'ip':ip, 'hostnames':hostnames, 'domains':domains, 'shodan_id':shodan_id, 'location':location, 'port':port, 'banner':data})
    except shodan.APIError as e:
        print('Error: {}'.format(e))
    return res
