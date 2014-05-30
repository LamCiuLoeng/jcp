# -*- coding: utf-8 -*-
import logging, re
import traceback

from tg import expose, flash, require, url, request, redirect, response, config
from tgext.admin.tgadminconfig import TGAdminConfig
from tgext.admin.controller import AdminController
from repoze.what import predicates, authorize
from repoze.what.predicates import not_anonymous, in_group, has_permission

from ordering.lib.base import BaseController
from ordering.model import DBSession, metadata
from ordering import model

from ordering.controllers.order import OrderController
#from ordering.controllers.importdata import *
from ordering.controllers.master import *
from ordering.controllers.report import *
from ordering.controllers.access import *
from ordering.controllers.importdata import *

from ordering.util.common import *

__all__=['RootController']

log=logging.getLogger(__name__)

class RootController(BaseController):

    order=OrderController()
    report=ReportController()
#    importdata = ImportDataController()
    country=CountryController()
#    itemcode = ItemCodeController()
    contact=ContactController()
    access=AccessController()
    billto=BillToController()
    shipto=ShipToController()
    countrycode=CountryCodeController()
    iteminfo=ItemInfoController()
    customer=CustomerController()
    specialvalue=SpecialValueController()
    rfidmapping=RFIDMappingController()
    combomapping=ComboMappingInfoController()

    @require(not_anonymous())
    @expose('ordering.templates.index')
    @tabFocus(tab_type="main")
    def index(self):
        """Handle the front-page."""
#        if 'logged_in' not in session.keys(): redirect('/logout_handler')
        redirect('/order/index')

    @expose('ordering.templates.login')
    def login(self, came_from=url('/')):
        """Start the user login."""
        if request.identity: redirect(came_from)
        login_counter=request.environ['repoze.who.logins']
        if login_counter>0: flash('Wrong credentials', 'warning')

        return dict(page='login', login_counter=str(login_counter), came_from=came_from)

    @expose()
    def post_login(self, came_from=url('/')):
        if not request.identity:
            login_counter=request.environ['repoze.who.logins']+1
            redirect(url('/login', came_from=came_from, __logins=login_counter))
        userid=request.identity['repoze.who.userid']

        if any([came_from.find(url_add) for url_add in ['index', 'master', 'access']])!=-1 and has_permission('CAN_VIEW_FULL_ORDER') is not None:
#            session['logged_in']=True
#            session.save()
            came_from=request.identity["user"].default_url

        redirect(came_from)

    @expose()
    def post_logout(self, came_from=url('/')):
        session.clear()
        session.save()
        redirect(came_from)

    @require(not_anonymous())
    @expose('ordering.templates.page_master')
    @tabFocus(tab_type="master")
    def master(self):
        """Handle the front-page."""
        return {}

    @expose("ordering.templates.register")
    def register(self, **kw):
        return {}

    @expose()
    def save_register(self, **kw):
        errMsg=[]
        emailReg="^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
        new_objects = []
        DBSession.begin(subtransactions=True)
        
        try:
            if not kw.get("user_name", False):
                errMsg.append("User name can't be blank!")
            else:
                try:
                    DBSession.query(User).filter(User.user_name == kw["user_name"]).one()
                    errMsg.append("The user name has been exist!")
                except:
                    pass
    
            if not kw.get("password", False):
                errMsg.append("Password can't be blank")
            if kw.get("password", None)!=kw.get("repassword", None):
                errMsg.append("The password and confirmed password not match!")
    
            def check_email(email):
                return re.search(emailReg, email)
    
            if not kw.get("email_address", False):
                errMsg.append("E-mail address can't be blank!")
            elif None in map(check_email, kw['email_address'].split(';')):
    #        elif not re.search(emailReg, kw["email_address"]):
                errMsg.append("E-mail address is in a wrong format!")
            
            if not kw.get("company", False) and not kw.get("new_company", False):
                errMsg.append("Please select company or input your company name!")
    
            if errMsg:
                msg="<ul>"
                for m in errMsg: msg+="<li>"+m+"</li>"
                msg+="</ul>"
    
                flash(msg, "warn")
                try:
                    redirect("/register")
                except:
                    pass
            else:
                if kw.get("company", False) and kw["company"] != 'None':
                    customer = JCPCustomer.get_company_by_id(kw["company"])
                else:
                    customer = JCPCustomer(name = kw['new_company'])
                    DBSession.add(customer)
        
                try:
                    g=DBSession.query(Group).filter_by(group_name="JCP").one()
                except:
                    g=Group(group_name="JCP")
                    new_objects.append(g)
        #            DBSession.add(g)
        
                if len(customer.billtos) == 0:
                    bill_to = JCPBillTo(customer = customer,
                                        company = customer.name,
                                        email = kw.get("email_address", False),
                                        is_default = 1)
        
                    bill_to.address = kw.get("billto_address", False) if kw.get("billto_address", False) and kw["billto_address"] else ''
                    bill_to.attn = kw.get("contact", False) if kw.get("contact", False) and kw["contact"] else ''
                    bill_to.tel = kw.get("billto_tel", False) if kw.get("billto_tel", False) and kw["billto_tel"] else ''
                    bill_to.fax = kw.get("billto_fax", False) if kw.get("billto_fax", False) and kw["billto_fax"] else ''
                    
                    new_objects.append(bill_to)
                
                if len(customer.shiptos) == 0:
                    ship_to = JCPShipTo(customer = customer,
                                        company = customer.name,
                                        email = kw.get("email_address", False),
                                        is_default = 1)
                    
                    ship_to.address = kw.get("shipto_address", False) if kw.get("shipto_address", False) and kw["shipto_address"] else ''
                    ship_to.attn = kw.get("contact", False) if kw.get("contact", False) and kw["contact"] else ''
                    ship_to.tel = kw.get("shipto_tel", False) if kw.get("shipto_tel", False) and kw["shipto_tel"] else ''
                    ship_to.fax = kw.get("shipto_fax", False) if kw.get("shipto_fax", False) and kw["shipto_fax"] else ''
                    
                    new_objects.append(ship_to)
        
                u=User(user_name=kw["user_name"],
                       email_address=kw["email_address"].strip(),
                       password=kw["password"].strip(),
                       company=kw["company"])
        
                if kw.get("customer", False)!='None': u.belong_to_customer_id=customer.id
                g.users.append(u)
                new_objects.append(u)
                DBSession.add_all(new_objects)
        
                send_from="r-pac-JCPenney-ordering-system"
                send_to=[kw["email_address"], ]
                subject="registration"
                text=["Dear %s :"%kw["user_name"],
                        "Congratulation.",
                        "Your registration on the r-pac JCPenney ordering system have completed successfully.",
                        "Here's your account info:",
                        "User Name : %s"%kw["user_name"],
                        "Password : %s"%kw["password"],
                        "You could login in the system via the link below :",
                        config.website_url,
                        "Thanks.",
                        "r-pac International Corp."
                        ]
        
                sendEmail(send_from, send_to, subject, "\n".join(text))
                flash("Thank you for your registration! You could login with your account info now.")
                
                DBSession.commit()
        except:
            DBSession.rollback()
            file = open("log.txt", 'a')
            traceback.print_exc(None, file)
            file.close()
            flash("The service is not avaiable now,please try it later or contact the system administator.", "warn")
        finally:
            redirect("/login")


