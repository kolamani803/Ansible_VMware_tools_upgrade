from ansible.plugins.callback import CallbackBase
import requests as req
from requests.auth import HTTPBasicAuth


class CallbackModule(CallbackBase):
    
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'callback'
    CALLBACK_NAME = 'CAllAPI'

    def __init__(self):
        super(CallbackModule, self).__init__()

    def v2_playbook_on_play_start(self, play):
        
        self.vm = play.get_variable_manager()
        
    def v2_playbook_on_stats(self, result):
        
        output= result.__dict__
        job_status= output['custom']['_run']['responseoutput']
        job_message= output['custom']['_run']['responseMessage']
        job_error= output['custom']['_run']['errorMessage']
        #print(output)
        vars = self.vm.get_vars()
        http_headersupdate= {'content-type': 'application/json','x-api-key': 'AIzaSyClzfrOzB818x55FASHvX4JuGQciR9lv7q'}
        URL = vars['callbackUrl']
        
        if (URL != "" and job_status == "success") :
            data = {"status": job_status ,"message": job_message, "error": " "}
            payload= str(data)
            response_gen = req.request("POST",URL,  headers=http_headersupdate, auth=HTTPBasicAuth(vars['snow_username'], vars['snow_password']), data = payload)
            #print (response_gen.text)
        elif (URL != "" and job_status == "failed"):
            data = {"status": job_status ,"message": job_message, "error": job_error}
            payload= str(data)
            response_gen = req.request("POST",URL,  headers=http_headersupdate, auth=HTTPBasicAuth(vars['snow_username'], vars['snow_password']), data = payload)
        elif (URL != "" and job_status == "unreachable"):
            data = {"status": job_status ,"message": job_message, "error": job_error}
            payload= str(data)
            response_gen = req.request("POST",URL,  headers=http_headersupdate, auth=HTTPBasicAuth(vars['snow_username'], vars['snow_password']), data = payload)
        else:
            print('')  

    
 
    
