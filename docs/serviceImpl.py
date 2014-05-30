from myServices_services_server import *
from time import time,ctime

from ZSI.ServiceContainer import AsServer

########################################################################
class mySoapServices(myServices):
    def soap_getTime(self,ps):
        try:
            rsp = myServices.soap_getTime(self,ps)
            request = self.request
            
        except Exception,e:
            print str(e),str(type(e))
        return rsp
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        
        
    
    