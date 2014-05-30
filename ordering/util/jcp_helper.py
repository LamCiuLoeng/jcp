import xml.dom.minidom, traceback, urllib, httplib
from pyquery import PyQuery as pq
from xml.dom import minidom

from ordering.model import *

queryTemplate="".join(["<TicketInfo_Request>",
                         "<TktSuppNbr>001487</TktSuppNbr>",
                         "<MerchSuppNbr>123456</MerchSuppNbr>",
                         "<PONbr>%s</PONbr>",
                         "<Sub>%s</Sub>",
                         "<Lot>%s</Lot>",
                         "<Line>%s</Line>",
                         "<Sku>%s</Sku>",
                         "</TicketInfo_Request>"
                         ])


def queryJCP(params):
    values=[]
    for f in [#"TktSuppNbr","MerchSuppNbr",
              "PONbr", "Sub", "Lot", "Line", "Sku"]:
        values.append(params[f]  if f in params else "")

    queryStr=urllib.urlencode({'sInRequest': queryTemplate%tuple(values)})
    headers={"Content-type": "application/x-www-form-urlencoded", "Accept": "text/xml"}
    conn=httplib.HTTPSConnection("supplier.jcpenney.com")
    conn.request("POST", "/trs/wsvcTktInfo.asmx/GetTktInfo", queryStr, headers)
    response=conn.getresponse()
    if response.status!=200:
        return (1, response.reason, None)
    data=response.read()
#    response=open("d:/new.xml")
#    for line in response: data=line
#    print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
#    print data
    f=open("d:/kk.txt", "w")
    f.write(data)
    f.close()
    return (0, None, JCPParser(data).getResult())



class JCPParser(object):
    def __init__(self, content=None):
        self.content=content

    def getText(self, nodelist):
        return "".join([n.data for n in nodelist if n.nodeType==n.TEXT_NODE])

    def getResult(self):
        return self._parseContent()

    def setContent(self, content):
        self.content=content


    def _parseContent(self):
        try:
            d=pq(pq(self.content).text())
            hParams={}

            for f in ["Msg_Nbr", "Msg_Type", "Msg_Txt", ]:
                hParams[f]=d(f).text()

            for f in ["Tkt_Supp", "Merch_Supp", "Purchase_Order"]:
                hParams[f]=d(f).attr("number")
            h=MsgHeader(**hParams)


            DBSession.add(h)

            if h.Msg_Type=="I":
                for item in d("Item_Detail"):
                    dParams={}
                    for f in ["Item_Desc", "Sub", "Lot", "Line",
                              "Color", "Cntry_Of_Org", "Sku", "Metric_Cnvrsn",
                              "PID", "RFID", "Brand_Typ", "Two_Or_More"
                              ]:
                        dParams[f]=d(f, item).text()

                    for f in ["Size"]:
                        dParams[f]=d(f, item).text().upper()

                    for f in ["GTIN"]:
                        dParams[f]=d(f, item).attr("number")

                    if d("Ctlg_Xref").find("Ctlg_Item"):
                        lot=d("Ctlg_Item", item).attr("lot")
                        sku=d("Ctlg_Item", item).attr("sku")
                        dParams["Ctlg_Xref"]=''.join([lot, ' ', sku])

                    stock=d("Tkt_Stock", item).attr("number")
                    if stock : dParams["Tkt_Stock"]=stock
                    retail=d("Retail", item).text()
                    if retail : 
                        dParams["Retail"]=int(float(retail)) if float(int(float(retail))) == float(retail) else float(retail)
#                    if retail : dParams["Retail"]=int(float(retail))
                    qty=d("Quantity", item).text()
                    if qty : dParams["Quantity"]=int(qty)

                    dParams["Misc_Txt"], dParams["Misc_Txt2"]=([misc.text for misc in d("Misc_Txt_Detail", item)]+[None, None])[:2]

                    DBSession.add(MsgDetail(header=h, **dParams))
            DBSession.flush()
            return h
        except:
            file=open('log.txt', 'w')
            traceback.print_exc(None, file)
            file.close()
#            traceback.print_exc()
            return None

#    def _parse(self):
#        try:
#            dom = xml.dom.minidom.parseString(self.content)
#            root = dom.getElementsByTagName("string")[0]
#            data = self.getText(root.childNodes).replace("&gt;",">").replace("&lt;","<")
#            msg = xml.dom.minidom.parseString(data)
#            hParams = {"Msg_Nbr":None,"Msg_Type":None,"Msg_Txt":None,"Tkt_Supp":None,"Merch_Supp":None,"Purchase_Order":None}
#            for f in hParams:
#                hParams[f] = self.getText(msg.getElementsByTagName(f)[0].childNodes)
#            h = MsgHeader(**hParams)
#            DBSession.add(h)
#            
#            for item in msg.getElementsByTagName("Item_Detail"):
#                dParams = {"Item_Desc":None,"Sub":None,"Lot":None,"Line":None,"Color":None,"Cntry_Of_Org":None,
#                           "Sku":None,"Size":None,"Metric_Cnvrsn":None,"GTIN":None,"PID":None,"Misc_Txt":None,}
#                for f in dParams:
#                    dParams[f] = self.getText(item.getElementsByTagName(f)[0].childNodes)
#                
#                stock = self.getText(msg.getElementsByTagName("Tkt_Stock")[0].childNodes)
#                if stock : dParams["Tkt_Stock"] = int(stock)
#                retail = self.getText(msg.getElementsByTagName("Retail")[0].childNodes)
#                if retail : dParams["Retail"] = float(retail)
#                qty = self.getText(msg.getElementsByTagName("Quantity")[0].childNodes)
#                if qty : dParams["Quantity"] = int(qty)
#                
#                DBSession.add( MsgDetail(header=h,**dParams) )
#                 
#            DBSession.flush()
#
#            return h
#        except:
#            traceback.print_exc()
#            return None
#        
