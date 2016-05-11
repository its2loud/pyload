# -*- coding: utf-8 -*-

from module.plugins.internal.misc import threaded
from module.plugins.internal.Addon import Addon
import requests
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning, SNIMissingWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
requests.packages.urllib3.disable_warnings(SNIMissingWarning)

class CaptchaTelegram(Addon):
    __name__    = "CaptchaTelegram"
    __type__    = "hook"
    __version__ = "0.2"
    __status__  = "testing"

    __config__ = [("activated", "bool",   "Activated",          False),
                  ("boturl",    "str",    "Telegram Bot URL",   "https://" ),
                  ("check_client", "bool", "Disable when client is connected", False)]      
 
    __description__ = "Captcha Telegram-Bot Plugin"
    __license__     = "GPLv3"
    __authors__     = [("Christoph Friedrich", "email@dom.tld" )]

    def captcha_task(self, task):

        if "service" in task.data:
            self.log_warning("Service: "+task.data["service"])
            return False

        if not task.isTextual():
            self.log_warning("isTextual: "+str(task.isTextual()))
            return False

        if self.pyload.isClientConnected() and self.config.get('check_client'):
            self.log_warning("Client Connected.")
            return False

        self.log_info("Sending Captcha to Telegram-Bot Server")

        try:
            post_url = self.config.get('boturl')+"/add"
            post_files = {'captcha': open(task.captchaFile, 'rb')}
            r = requests.post(post_url, verify=False, files=post_files)
            self.log_info("Response: "+r.text.replace("\n","")[:50])       
            jr = r.json()
            wait = int(round(jr.get("timeout")-time.time())+5)
            tid = jr.get("tid")
            task.handler.append(self)
            task.data['service'] = self.classname
            task.data['tid'] = tid
            self.log_info("Waiting "+str(wait)+" sec.")
            task.setWaiting(wait)
        except Exception, e:
            self.log_error(str(e)[:50]+"...")
            self.log_info("Abort.")
            return False
        self._process_captcha(task)

    @threaded
    def _process_captcha(self, task):
        try:
            self.log_info("Getting result ["+str(task.data['tid'])+"] from Telegram-Bot Server.")
            post_url = self.config.get('boturl')+"/result"
            post_data = {'tid': task.data['tid']}
            r = requests.post(post_url, verify=False, data=post_data)
            self.log_info("Response: "+r.text[:50])
        except Exception, e:
            self.log_error(str(e)[:50]+"...")
        finally:
            task.setResult(r.text)
