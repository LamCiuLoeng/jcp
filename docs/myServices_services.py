################################################## 
# JCPenney_x0020_Ticket_x0020_Request_x0020_Web_x0020_Service_services.py 
# generated by ZSI.generate.wsdl2python
##################################################


from JCPenney_x0020_Ticket_x0020_Request_x0020_Web_x0020_Service_services_types import *
import urlparse, types
from ZSI.TCcompound import ComplexType, Struct
from ZSI import client
import ZSI
from ZSI.generate.pyclass import pyclass_type

# Locator
class JCPenney_x0020_Ticket_x0020_Request_x0020_Web_x0020_ServiceLocator:
    JCPenney_x0020_Ticket_x0020_Request_x0020_Web_x0020_ServiceSoap_address = "http://jsupplier1.jcpenney.com/trs/wsvcTktInfo.asmx"
    def getJCPenney_x0020_Ticket_x0020_Request_x0020_Web_x0020_ServiceSoapAddress(self):
        return JCPenney_x0020_Ticket_x0020_Request_x0020_Web_x0020_ServiceLocator.JCPenney_x0020_Ticket_x0020_Request_x0020_Web_x0020_ServiceSoap_address
    def getJCPenney_x0020_Ticket_x0020_Request_x0020_Web_x0020_ServiceSoap(self, url=None, **kw):
        return JCPenney_x0020_Ticket_x0020_Request_x0020_Web_x0020_ServiceSoapSOAP(url or JCPenney_x0020_Ticket_x0020_Request_x0020_Web_x0020_ServiceLocator.JCPenney_x0020_Ticket_x0020_Request_x0020_Web_x0020_ServiceSoap_address, **kw)

# Methods
class JCPenney_x0020_Ticket_x0020_Request_x0020_Web_x0020_ServiceSoapSOAP:
    def __init__(self, url, **kw):
        kw.setdefault("readerclass", None)
        kw.setdefault("writerclass", None)
        # no resource properties
        self.binding = client.Binding(url=url, **kw)
        # no ws-addressing

    # op: GetTktInfo
    def GetTktInfo(self, request):
        if isinstance(request, GetTktInfoSoapIn) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="https://supplier.jcpenney.com/trs/wsvcTktInfo/GetTktInfo", **kw)
        # no output wsaction
        response = self.binding.Receive(GetTktInfoSoapOut.typecode)
        return response

GetTktInfoSoapIn = ns0.GetTktInfo_Dec().pyclass

GetTktInfoSoapOut = ns0.GetTktInfoResponse_Dec().pyclass