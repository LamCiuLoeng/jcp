# -*- coding: utf-8 -*-

from datetime import date, datetime
import traceback, os, smtplib, StringIO, base64, hashlib
import random

from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
from email.header import Header

from tg import expose, redirect, validate, flash, config, response, session
from repoze.what import authorize
from repoze.what.predicates import not_anonymous

from ordering.model import *

DISPLAY_DATE_FORMAT="%Y-%m-%d"
ACTIVE_ITEM=0
INACTIVE_ITEM=1


__all__=["tabFocus", "Date2Text", "getOr404", "sendEmail",
         "number2alphabet", "serveFile", "rpacEncrypt", "rpacDecrypt",
         "getCustomer", "checkDigit12", "check_anonymous", "gerRandomStr",
         "SPECIAL_VALUE_LIST", 'RFID_NONE_ORDER_LIST', 'FIELDS', 'EXCEL_TITLES',
         'allAlpha', 'SourceError', 'fileUpload']

def tabFocus(tab_type=""):
    def decorator(fun):
        def returnFun(*args, **keywordArgs):
            returnVal=fun(*args, **keywordArgs)
            if type(returnVal)==dict and "tab_focus" not in returnVal:
                returnVal["tab_focus"]=tab_type
            return returnVal
        return returnFun
    return decorator


def Date2Text(value=None, dateTimeFormat=DISPLAY_DATE_FORMAT, defaultNow=False):
    if not value and defaultNow : value=datetime.now()

    format=dateTimeFormat
    result=value

    if isinstance(value, date):
        try:
            result=value.strftime(format)
        except:
            traceback.print_exc()
    elif hasattr(value, "strftime"):
        try:
            result=value.strftime(format)
        except:
            traceback.print_exc()

    if not result:
        result=""

    return result

def getOr404(obj, id, redirect_url="/index", message="The record deosn't exist!"):
    try:
        v=DBSession.query(obj).get(id)
        if v : return v
        else : raise "No such obj"
    except:
        traceback.print_exc()
        flash(message)
        redirect(redirect_url)

#This method is used in MS Excel to convert the header column from number to alphalbet
def number2alphabet(n):
    result=[]
    while n>=0:
        if n>26:
            result.insert(0, n%26)
            n/=26
        else:
            result.insert(0, n)
            break
    return "".join([chr(r+64) for r in result ]) if result else None

def sendEmail(send_from, send_to, subject, text, cc_to=[], files=[], server="192.168.42.13"):
    assert type(send_to)==list
    assert type(files)==list

    msg=MIMEMultipart()
    msg.set_charset("utf-8")
    msg['From']=send_from
    msg['To']=COMMASPACE.join(send_to)

    if cc_to:
        assert type(cc_to)==list
        msg['cc']=COMMASPACE.join(cc_to)
        send_to.extend(cc_to)

    msg['Date']=formatdate(localtime=True)
    msg['Subject']=subject

    msg.attach(MIMEText(text))

    for f in files:
        part = MIMEBase('application', "octet-stream")
        if isinstance(f, basestring):
            part.set_payload(open(f, "rb").read())
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % Header(os.path.basename(f), 'utf-8'))
        elif hasattr(f, "file_path") and hasattr(f, "file_name"):
            part.set_payload(open(f.file_path, "rb").read())
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % Header(f.file_name, 'utf-8'))
        msg.attach(part)

    smtp=smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()

def advancedSendMail(send_from, send_to, subject, text, html, cc_to = [], files = [], server = "192.168.42.13"):
    assert type(send_to) == list
    assert type(files) == list

    if not text and not html:
        raise "No content to send!"
    elif text and not html :
        msg = MIMEText(text, "plain",_charset='utf-8') #fix the default encoding problem
    elif not text and html:
        msg = MIMEText(html, "html",_charset='utf-8') #fix the default encoding problem
    else:
        msg = MIMEMultipart("alternative")
        msg.attach(MIMEText(text, "plain",_charset='utf-8'))
        msg.attach(MIMEText(html, "html",_charset='utf-8'))

    msg.set_charset("utf-8")
    if len(files) > 0 :
        tmpmsg = msg
        msg = MIMEMultipart()
        msg.attach(tmpmsg)

    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)

    if cc_to:
        assert type(cc_to) == list
        msg['cc'] = COMMASPACE.join(cc_to)
        send_to.extend(cc_to)

    msg['Date'] = formatdate(localtime = True)
    msg['Subject'] = subject

    for f in files:
        part = MIMEBase('application', "octet-stream")
        if isinstance(f, basestring):
            part.set_payload(open(f, "rb").read())
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % Header(os.path.basename(f), 'utf-8'))
        elif hasattr(f, "file_path") and hasattr(f, "file_name"):
            part.set_payload(open(f.file_path, "rb").read())
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % Header(f.file_name, 'utf-8'))
        msg.attach(part)

    smtp = smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()

def serveFile(fileName, contentType="application/x-download", contentDisposition="attachment", charset="utf-8"):
    response.headers['Content-type']='application/x-download' if not contentType else contentType
    response.headers['Content-Disposition']="%s;filename=%s"%(contentDisposition, Header(os.path.basename(fileName), charset))
    f=open(fileName, 'rb')
    content="".join(f.readlines())
    f.close()
    return content

def defaultIfNone(blackList=[None, ], default=""):
    def returnFun(value):
        defaultValue=default() if callable(default) else default
        if value in blackList:
            return defaultValue
        else:
            try:
                return str(value)
            except:
                try:
                    return repr(value)
                except:
                    pass
        return defaultValue
    return returnFun

null2blank=defaultIfNone(blackList=[None, "NULL", "null", "None"])


def rpacEncrypt(v):
    c=base64.b64encode(unicode(v))
    e=hashlib.md5()
    e.update("r-pac%sjcp"%unicode(v))
    k=e.hexdigest()[5:15]
    return c+k

def rpacDecrypt(enStr):
    if not enStr or len(enStr)<10 : return (False, None)
    k=enStr[-10:]
    c=base64.b64decode(enStr[:-10])

    e=hashlib.md5()
    e.update("r-pac%sjcp"%unicode(c))
    kk=e.hexdigest()[5:15]

    if k!=kk : return (False, None)
    return (True, c)

def getCustomer():
    return DBSession.query(JCPCustomer).filter_by(active=0).order_by(JCPCustomer.id).all()

def checkDigit12(upc):
    upc="0"+upc
    prefix=upc[:-1]
    checkdigit=int(upc[-1])
    result=0
    for i, v in enumerate(list(prefix)):
        if i%2:
            result+=int(v)*3
        else:
            result+=int(v)*1
    q=result%10
    if q!=0:
        q=10-q
    if q==checkdigit:
        return True
    else:
        return False

#def check_logout():
#    def returnFunc():
#        if 'logged_in' not in session.keys(): redirect('/logout_handler')

class check_anonymous(not_anonymous):
    def evaluate(self, environ, credentials):
        if 'logged_in' not in session.keys(): redirect('/logout_handler')
        if not credentials:
            self.unmet()

numberAlpha=[str(a) for a in range(10)]
lowerAlpha=[chr(a) for a in range(ord("a"), ord("z")+1)]
upperAlpha=[chr(a) for a in range(ord("A"), ord("Z")+1)]
allAlpha=numberAlpha+lowerAlpha+upperAlpha
gerRandomStr=lambda str_length, randomRange=numberAlpha : "".join(random.sample(randomRange, str_length))

SPECIAL_VALUE_LIST=sorted(['', 'Carpenter', 'Cargo', '5 Pocket', 'Corduroy', 'Twill Pant',
                      'Capri', 'Bermuda Short', 'Skort', 'Plaid Short', 'Straight Leg',
                      'Flare Leg', 'Fashion Short', 'Convertible Pant', 'Denim Legging', 'Skirt',
                      'Skinny', 'Boot Cut', 'Skirt and Legging Set', 'Fashion Jean', 'Jean',
                      'Slim Jean', '2 Pack Leggings', 'Favorite Sleepshirt', 'Favorite Lace Cami', 'Favorite Crew', 'Favorite Vneck',
                      'Favorite Cami', 'Favorite Tank', 'Favorite Polo', 'Favorite Hoodie', 'Favorite Thermal', 'Favorite Crop',
                      'Favorite Yoga Pant', 'Flare', 'Boot', 'Straight', 'Reversible', 'Swimwear',
                      'Swimwear Coverup', 'Favorite Scoop', 'None'])

RFID_NONE_ORDER_LIST = [('126', 'N'), ('128', 'P'), ('022', ''), ('023', ''),
                        ('024', ''), ('026', ''), ('028', ''), ('067', ''),
                        ('610', ''), ('523', ''), ('014', ''), ('016', ''),
                        ('063', ''), ('064', ''), ('609', ''), ('010', ''),
                        ('011', ''), ('012', ''), ('664', ''),]

FIELDS = ["stock", "sub", "lot", "line",
          "sizeCode", "description", "color", "size",
          "cat", "pid", "upc", "gtinCode",
          "misc1", "misc2", "retail", "specialPrice", "quantity",]

EXCEL_TITLES = ["Stock", "Sub", "Lot", "Line",
                "Size Code", "Description", "Color", "Size",
                "Cat", "PID/style #", "UPC", "128c",
                "MISC1", "MISC2", "Retail", "2 or More",
                "QTY","Customer PO", "Supplier PO#", "Country of Origin"]

class SourceError(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)

def fileUpload(kw_param, relativePath, fileName):
    try:
        absPath=os.path.join(os.path.abspath(os.path.curdir), relativePath)
        if not os.path.exists(absPath):
            os.makedirs(absPath)
        fn=fileName if not callable(fileName) else fileName()
        targetFileName=os.path.join(absPath, fn)

        f=open(targetFileName, "wb")
        f.write(kw_param.file.read())
        f.close()
        return targetFileName
    except:
        traceback.print_exc()
        return None