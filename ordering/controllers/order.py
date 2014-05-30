# -*- coding: utf-8 -*-
from datetime import datetime as dt
import traceback, logging, os, copy
import random
import thread
import zipfile
import zlib

# turbogears imports
from tg import expose, redirect, validate, flash, request, response, override_template, config
from tg.decorators import paginate

# third party imports
from sqlalchemy import not_, and_
from sqlalchemy.sql.expression import desc
from repoze.what import predicates, authorize
from repoze.what.predicates import not_anonymous, in_group, has_permission

# project specific imports
from ordering.lib.base import BaseController
from ordering.model import *
from ordering.util.common import *
from ordering.util.common import ACTIVE_ITEM
from ordering.util.common import INACTIVE_ITEM
from ordering.util.common import RFID_NONE_ORDER_LIST
from ordering.widgets.order import *
from ordering.util.jcp_helper import *
from ordering.util.excel_helper import *
from ordering.util.upc2excel import returnEPC, genProducionFile
from ordering.util.rfid_helper import *

import simplejson as json

__all__=['OrderController']

myLock = thread.allocate_lock()

log=logging.getLogger(__name__)

class OrderController(BaseController):

    allow_only=authorize.not_anonymous()

    @expose('ordering.templates.order.index')
    @paginate('collections', items_per_page=25)
    @tabFocus(tab_type="main")
    def index(self, **kw):
        search_form=order_search_form
        if not kw: return dict(search_form=search_form, collections=[], values={})
        gtin_length=set()

        def _check_jcp(po=None, sub=None, lot=None):
            if po:
                flag, reason, data=queryJCP({"PONbr": po})
            else:
                flag, reason, data=queryJCP({"Sub": sub, "Lot": lot})

            if flag!=0:
                flash(reason)
                redirect(request.identity["user"].default_url)
            if data is None:
                flash("Can not get the data for this order!")
                redirect(request.identity["user"].default_url)
            if data.Msg_Type=='E':
                flash(data.Msg_Txt[:50] + '...')
                redirect(request.identity["user"].default_url)
            if data.details[0].RFID == 'NO' and len(data.details[0].GTIN) > 0 and data.details[0].Tkt_Stock == 'NONE':
                flash("Ticket Stock Number (NONE) error in requested data from JCPenney. Please contact with JCPenney to check the Ticket Stock Number. Thank you!")
                redirect(request.identity["user"].default_url)

            status=JCPItemInfo.get_status(pkg_code=data.details[0].Tkt_Stock)
            special_value=JCPItemInfo.get_special_value(pkg_code=data.details[0].Tkt_Stock)
            item=JCPItemInfo.get_item(data.details[0].Tkt_Stock)
            
            if item and item.combo_mapping == False:
                rfid_mapping_code=item.combo_packaging_code
                hangtag_code=item.packaging_code
            elif item and item.combo_mapping == True:
                rfid_mapping_code=JCPComboMappingInfo.get_label_code(item.packaging_code)[0][0]
                hangtag_code=JCPComboMappingInfo.get_hangtag_code(item.packaging_code)[0]
            else:
                rfid_mapping_code=None
                hangtag_code=None

            if status==INACTIVE_ITEM:
                flash("The item is inactive and can not be ordered!")
                redirect(request.identity['user'].default_url)

            for detail in data.details: gtin_length.add(len(detail.GTIN))
            care_infos=self._isCareLabel(data, "msg", "PID")

            if len(gtin_length)>1:
                upcSendTo=[request.identity["user"].email_address]
                upcCCTo=config.jcp_upc_mail.split(";")
                mailContent="The order [%s] have more than one upc type, please contact us!"%po if po else kw.get("sub_customerPO", "")
                self._sendNotifyEmail(upcSendTo, upcCCTo, po if po else kw.get("sub_customerPO", ""), None, mailContent, [], mailContent)
                flash(mailContent)

            return (data, care_infos, special_value, rfid_mapping_code, hangtag_code)

        if kw.get("order_type", None)=="order_by_pom":
            data, care_infos, special_value, rfid_mapping_code, hangtag_code=_check_jcp(po=kw.get("poNo"))

            if any([d.washing_instruction==True and d.fiber_content==True and d.country_of_origin==True for d in care_infos]):
                override_template(self.index, 'mako:ordering.templates.order.order_form_new_carelabel')
                return self.placeOrder(id=data.id, poNo=kw.get("poNo", ""), customerPO=kw.get("pom_customerPO", ""), care_infos=care_infos, special_value=special_value, rfid_mapping_code=rfid_mapping_code, hangtag_code=hangtag_code)
            else:
                override_template(self.index, 'mako:ordering.templates.order.order_form_new_ht')
                return self.placeOrder(id=data.id, poNo=kw.get("poNo", ""), customerPO=kw.get("pom_customerPO", ""), special_value=special_value, rfid_mapping_code=rfid_mapping_code, hangtag_code=hangtag_code)

        elif kw.get("order_type", None)=="order_by_sub":
            data, care_infos, special_value, rfid_mapping_code, hangtag_code=_check_jcp(sub=kw["sub"], lot=kw["lot"])
            
            if any([d.washing_instruction==True and d.fiber_content==True and d.country_of_origin==True for d in care_infos]):
                override_template(self.index, 'mako:ordering.templates.order.order_form_new_carelabel')
                return self.placeOrder(id=data.id, customerPO=kw.get("sub_customerPO", ""), line=kw.get("line", ""), sku=kw.get("sku", ""), care_infos=care_infos, special_value=special_value, rfid_mapping_code=rfid_mapping_code, hangtag_code=hangtag_code)
            else:
                override_template(self.index, 'mako:ordering.templates.order.order_form_new_ht')
                return self.placeOrder(id=data.id, customerPO=kw.get("sub_customerPO", ""), line=kw.get("line", ""), sku=kw.get("sku", ""), special_value=special_value, rfid_mapping_code=rfid_mapping_code, hangtag_code=hangtag_code)

        elif kw.get('order_type', None)=="order_by_manual":
            override_template(self.index, 'mako:ordering.templates.order.order_form_manual')
            return self.manual()
        elif kw.get('order_type', None)=="order_for_national":
            override_template(self.index, 'mako:ordering.templates.order.order_form_manual')
            return self.manual()
        else:
            flash("No such order type!")
            redirect(request.identity["user"].default_url)

    def _isCareLabel(self, headerInfo, type, attr=None):
        #check whether the order is a care label or other product
        #return True if it's a care label order
        try:
            if type=="msg":
                if not attr : attr="pid"
                stock_numbers=[getattr(d, attr) for d in headerInfo.details]
                package_codes=DBSession.query(JCPItemInfo).filter(JCPItemInfo.packaging_code.in_([d.Tkt_Stock for d in headerInfo.details])).all()
            else:
                package_codes=DBSession.query(JCPItemInfo).filter(JCPItemInfo.packaging_code.in_([d.stock for d in headerInfo.details])).all()

            return package_codes
        except:
            traceback.print_exc()
            flash("The service is not avaiable now,please try it later or contact the system administator.", "warn")
            raise

    @expose('ordering.templates.order.search')
    @paginate('collections', items_per_page=25)
    @tabFocus(tab_type="view")
    def search(self, **kw):
        try:
            search_form=order_view_form

            if kw:
                result=self._query_result(kw)

                return dict(search_form=search_form, collections=result, values=kw, return_url=request.identity['user'].default_url)
            else:
                return dict(search_form=search_form, collections=[], values={}, return_url=request.identity['user'].default_url)
        except:
            flash("The service is not avaiable now,please try it later.", status="warn")
            traceback.print_exc()
            redirect(request.identity["user"].default_url)

    def _query_result(self, kw):
        try:
            conditions=[]
            custHeaderIDs = None
            subHeaderIDs = None
            lotHeaderIDs = None
            headerIDs = None

            if kw.get("poNo", False):
                conditions.append(JCPHeaderPO.poNo.op('ILIKE')("%%%s%%"%kw.get("poNo", "").strip()))
            if kw.get("countryId", False):
                conditions.append(JCPHeaderPO.country_id == int(kw.get("countryId", "")))
            if kw.get("customerPO", False) and kw['customerPO']:
                custHeaderIDs = DBSession.query(JCPOrderForm.headerId) \
                                .filter(JCPOrderForm.customerPO.op('ILIKE')("%%%s%%"%kw.get("customerPO", "").strip())) \
                                .all()
                headerIDs = custHeaderIDs
            if kw.get("sub", False):
                subHeaderIDs = DBSession.query(JCPDetailPO.headerid) \
                               .filter(JCPDetailPO.sub == kw.get('sub', '')) \
                               .all()
                headerIDs = subHeaderIDs
            if kw.get("lot", False):
                lotHeaderIDs = DBSession.query(JCPDetailPO.headerid) \
                               .filter(JCPDetailPO.lot == kw.get('lot', '')) \
                               .all()
                headerIDs = lotHeaderIDs
            if kw.get("poStartDate", False) and kw.get("poEndDate", False):
                b_date=dt.strptime(kw.get("poStartDate", '2009-12-1200:00:00')+"00:00:00", "%Y-%m-%d%H:%M:%S")
                e_date=dt.strptime(kw.get("poEndDate", '2009-12-1200:00:00')+"23:59:59", "%Y-%m-%d%H:%M:%S")

                conditions.append(JCPHeaderPO.poDate>=b_date)
                conditions.append(JCPHeaderPO.poDate<=e_date)
            elif kw.get("poStartDate", False):
                b_date=dt.strptime(kw.get("poStartDate", '2009-12-1200:00:00')+"00:00:00", "%Y-%m-%d%H:%M:%S")

                conditions.append(JCPHeaderPO.poDate>=b_date)
            elif kw.get("poEndDate", False):
                e_date=dt.strptime(kw.get("poEndDate", '2009-12-1200:00:00')+"23:59:59", "%Y-%m-%d%H:%M:%S")

                conditions.append(JCPHeaderPO.poDate<=e_date)

            if not authorize.has_permission('CAN_VIEW_FULL_ORDER'): #and request.identity["user"].belong_to_customer_id:
                conditions.append(JCPHeaderPO.customer_id==request.identity["user"].belong_to_customer_id)
            
            if headerIDs is not None and custHeaderIDs is not None:
                headerIDs = list(set(headerIDs) & set(custHeaderIDs))
            if headerIDs is not None and subHeaderIDs is not None:
                headerIDs = list(set(headerIDs) & set(subHeaderIDs))
            if headerIDs is not None and lotHeaderIDs is not None:
                headerIDs = list(set(headerIDs) & set(lotHeaderIDs))
            
            obj=DBSession.query(JCPHeaderPO)
            
            if len(conditions):
                for condition in conditions: obj=obj.filter(condition)
                
                if headerIDs is not None:
                    result=obj.filter(JCPHeaderPO.id.in_([id[0] for id in headerIDs])) \
                            .filter(JCPHeaderPO.active==0) \
                            .order_by(desc(JCPHeaderPO.poDate)) \
                            .all()
                else:
                    result=obj.filter(JCPHeaderPO.active==0) \
                            .order_by(desc(JCPHeaderPO.poDate)) \
                            .all()
            else:
                if headerIDs is not None:
                    result=obj.filter(JCPHeaderPO.id.in_([id[0] for id in headerIDs])) \
                            .filter(JCPHeaderPO.active==0) \
                            .order_by(desc(JCPHeaderPO.poDate)) \
                            .all()
                else:
                    result=DBSession.query(JCPHeaderPO) \
                             .filter(JCPHeaderPO.active==0) \
                             .filter(JCPHeaderPO.id.in_(DBSession.query(JCPOrderForm.headerId))) \
                             .order_by(desc(JCPHeaderPO.poDate)) \
                             .all()

            return result
        except:
            traceback.print_exc()

    @expose()
    def getAjaxField(self, **kw):
        try:
            fieldName=kw["fieldName"]
            value=kw["q"]
            result=[]

            if fieldName=='poNo':
                rs=DBSession.query(JCPHeaderPO).filter(JCPHeaderPO.poNo.like('%%%s%%'%str(value))).all()
                result=["%s|%s" % (v.poNo, v.poNo) for v in rs ]
            elif fieldName=='item_id':
                rs=DBSession.query(JCPItemInfo).filter(JCPItemInfo.item_code.like('%%%s%%'%str(value))) \
                   .filter(JCPItemInfo.status==0).all()
                result=["%s|%d" % (v.item_code, v.id) for v in rs]
            else:
                result=[]

            data="\n".join(result)

            return data
        except:
            traceback.print_exc()

    @expose()
    def ajax_check_status(self, **kw):
        try:
            status=JCPItemInfo.get_status(pkg_code=kw.get('pkg_code', ''))

            if status==INACTIVE_ITEM: return 'inactive'
            else: return 'active'
        except:
            traceback.print_exc()

    @expose()
    @tabFocus(tab_type="main")
    def viewOrder(self, **kw):
        (flag, id)=rpacDecrypt(kw.get("code", ""))
        
        if not flag:
            flash("Please don't access the resource illegally!")
            redirect(request.identity["user"].default_url)

        ph=getOr404(JCPHeaderPO, id)

        if ph.active==1:
            flash("The order has been canceled!", "warn")
            redirect(request.identity["user"].default_url)

        if len(ph.orders)<1 :
            flash("There's no order related to this PO!", "warn")
            redirect(request.identity["user"].default_url)

        img_url=JCPItemInfo.get_item(ph.details[0].msgDetail.Tkt_Stock) if ph.orderType == 'AUTO' else JCPItemInfo.get_item(ph.details[0].stock)
        care_infos=self._isCareLabel(ph, "po")
        countries = JCPCountry.get_all_countries()
        rfid_url = None
        country=DBSession.query(JCPCountryCode).get(int(ph.orders[0].origin)) if ph.orders[0].origin else None
        
        if ph.rfid_id is not None:
            rfid_url = config.rfid_site_url + str(ph.rfid_id)

        if any([d.washing_instruction==True and d.fiber_content==True and d.country_of_origin==True for d in care_infos]):
            override_template(self.viewOrder, 'mako:ordering.templates.order.order_form_view')

            return {"poheader" : ph,
                    "podetails" : ph.details,
                    "orderHeder" : ph.orders[0],
                    'country' : country,
                    'rfid_url': rfid_url,
                    "image_url": img_url,
                    'countries': countries,
                    'return_url': request.identity["user"].default_url,
                    }
        else:
            rfid_flag = 'False'
            
            for detail in ph.details:
                if detail.rfid in [1, 2]:
                    rfid_flag = 'True'
            
            override_template(self.viewOrder, 'mako:ordering.templates.order.order_form_view_ht')

            return {"poheader" : ph,
                    "podetails" : ph.details,
                    "orderHeder" : ph.orders[0],
                    'country' : country,
                    "rfid_flag": rfid_flag,
                    'rfid_url': rfid_url,
                    "image_url": img_url,
                    'countries': countries,
                    'return_url': request.identity["user"].default_url,
                    }

    @expose()
    def saveOrder(self, **kw):
        mh=getOr404(MsgHeader, kw["msgID"])
        DBSession.begin(subtransactions=True)
        try:
            if kw.has_key('national_brand') and not kw['national_brand']:
                raise AttributeError
            elif kw.has_key('private_brand') and not kw['private_brand']:
                raise AttributeError
            elif kw.has_key('combo_selection') and not kw['combo_selection']:
                raise AttributeError
        except AttributeError:
            flash("The order hasn't get enough info to place order!", "warn")
            redirect('/order/index')
            
        try:
            upcFlag=set()
            gtin_length=set()
            ph=JCPHeaderPO(poNo=mh.Purchase_Order, poDate=dt.now(),
                             customer=DBSession.query(JCPCustomer).get(request.identity["user"].belong_to_customer_id) if request.identity["user"].belong_to_customer_id else None,
                             country=DBSession.query(JCPCountry).get(kw.get('sendEmailTo', '')),
                             remark=kw.get('remark', ''),
                             status='CONFIRM', orderType='AUTO')
            
            if kw.has_key("combo_selection") and kw.get("combo_selection", False) != '':
                ph.combo_order = kw.get("combo_selection", False).split("-")[1]
            
            pd_list=[]
            fields=["customerPO", "supplierNO", "billAddress", "billAttn", "billTel", "billFax", "shipAddress",
                      "shipAttn", "shipTel", "shipFax", "origin", "rnCode", "wplCode", "cust_item_codes"]
            params={"header" : ph,
                      "issuedBy" : request.identity["user"],
                      "lastModifyBy" : request.identity["user"],
                      "shipInstruction": kw.get("si_intro", ""),
                      'status': 'CONFIRM'
                      }

            for f in fields:
                params[f]=None if f not in fields or not kw[f] else kw[f]

            this_billto=DBSession.query(JCPBillTo).get(kw['billCompany'])
            this_shipto=DBSession.query(JCPShipTo).get(kw['shipCompany'])
            params['billCompany']=this_billto.company if this_billto else kw.get('other_billto', '')
            params['shipCompany']=this_shipto.company if this_shipto else kw.get('other_shipto', '')
            order=JCPOrderForm(**params)
            add_list=[order, ph]
            national_brand=kw.get("national_brand", False) if kw.has_key("national_brand") else None
            private_brand=kw.get("private_brand", False) if kw.has_key("private_brand") else None

            DBSession.add_all(add_list)

            wi_json=json.loads(kw.get("wi_infos", "").replace("'", '"'))

            for md in mh.details:
                wi_content=''

                for key, val in wi_json.iteritems():
                    if key.split('_')[0] != 'private':
                        if int(key.split('_')[2])==md.id: wi_content=''.join([i.split('=')[1] for i in val.split('&')])
                    else:
                        if int(key.split('_')[4])==md.id: wi_content=''.join([i.split('=')[1] for i in val.split('&')])
                
                retailKey="retail_%d"%md.id
                quantityKey="quantity_%d"%md.id
                private_retail_key="private_retail_%d"%md.id
                private_quantity_key="private_quantity_%d"%md.id
                misc1_key = "misc1_%d"%md.id
                private_misc1_key = "private_misc1_%d"%md.id

                if quantityKey in kw and int(kw[quantityKey])>0:
                    pd=JCPDetailPO(header=ph, stock=md.Tkt_Stock, sub=md.Sub, lot=md.Lot,
                                     line=md.Line, size=md.Size, sizeCode=md.Sku, description=md.Item_Desc,
                                     color=md.Color, cat=md.Ctlg_Xref, pid=md.PID, washingInstruction=wi_content, msgDetail=md,
                                     upc=md.GTIN, misc2=md.Misc_Txt2)

                    if retailKey in kw and kw[retailKey] : pd.retail=kw[retailKey]
                    pd.quantity=int(kw[quantityKey])
                    if pd.upc: upcFlag.add(checkDigit12(pd.upc))
                    else:
                        pd.gtinCode=pd.sub+pd.lot+pd.line+pd.sizeCode+'0'
                        if len(pd.gtinCode)!=14: upcFlag.add(False)
                    
                    if national_brand is not None:
                        pd.stock=national_brand
                        pd.rfid=1
                    
                    pd.misc1 = kw.get(misc1_key, '')

                    pd_list.append(pd)
                
                if private_quantity_key in kw and int(kw[private_quantity_key])>0:
                    pd=JCPDetailPO(header=ph, stock=md.Tkt_Stock, sub=md.Sub, lot=md.Lot,
                                     line=md.Line, size=md.Size, sizeCode=md.Sku, description=md.Item_Desc,
                                     color=md.Color, cat=md.Ctlg_Xref, pid=md.PID, washingInstruction=wi_content, msgDetail=md,
                                     upc=md.GTIN, misc2=md.Misc_Txt2, specialPrice = md.Two_Or_More)

                    if private_retail_key in kw and kw[private_retail_key] : pd.retail=kw[private_retail_key]
                    pd.quantity=int(kw[private_quantity_key])
                    if pd.upc: upcFlag.add(checkDigit12(pd.upc))
                    else:
                        pd.gtinCode=pd.sub+pd.lot+pd.line+pd.sizeCode+'0'
                        if len(pd.gtinCode)!=14: upcFlag.add(False)
                    
                    pd.stock=private_brand.split('-')[1]
                    if kw.has_key("private_brand") and kw["private_brand"]:
                        pd.rfid=1
                    elif kw.has_key("combo_selection") and kw["combo_selection"]:
                        pd.rfid=2
                        
                    pd.misc1 = kw.get(private_misc1_key, '')

                    pd_list.append(pd)

                gtin_length.add(len(md.GTIN))

            DBSession.add_all(pd_list)

            if kw.get("spv_infos", "") and len(kw.get("spv_infos", ""))>1:
                pod_list, spv_values = self._set_specialvalue(kw.get("spv_infos", ""), pd_list)
                
                DBSession.add_all(pod_list)
                DBSession.add_all(spv_values)

            fc_json=json.loads(kw.get("fc_infos", "").replace("'", '"'))
            fc_infos=[]

            for key, val in fc_json.iteritems():
                poDetail=None

                for pd in pd_list:
                    if key.split('_')[0] != 'private':
                        if int(key.split('_')[2])==pd.msgDetail.id and pd.stock == pd.msgDetail.Tkt_Stock: poDetail=pd

                if poDetail:
                    fc_val = dict(i.split('=') for i in val.split('&'))
                    
                    for k, v in fc_val.iteritems():
                        exclusiveData = fc_val['fc_exclusive_data'] if fc_val.has_key('fc_exclusive_data') else None
                        cottonLogo = True if fc_val.has_key('fc_cotton_logo') and fc_val['fc_cotton_logo'] == 'true' else False
                        lycraLogo = True if fc_val.has_key('fc_lycra_logo') and fc_val['fc_lycra_logo'] == 'true' else False

                    fc_header=JCPFCInstrHeader(poDetail=poDetail, exclusiveData=exclusiveData,
                                                 cottonLogo=cottonLogo, lycraLogo=lycraLogo)

                    DBSession.add(fc_header)

                    for fc_detail_idx in range(1, 7):
                        header = fc_header
                        fc_ccName = None
                        fc_component = None
                        fc_color = None
                        
                        if fc_val.has_key('fc_cc_name' + str(fc_detail_idx)):
                            fc_ccName = fc_val['fc_cc_name' + str(fc_detail_idx)]
                        if fc_val.has_key('fc_component' + str(fc_detail_idx)):
                            fc_component = fc_val['fc_component' + str(fc_detail_idx)]
                        if fc_val.has_key('fc_color' + str(fc_detail_idx)):
                            fc_color = fc_val['fc_color' + str(fc_detail_idx)]
                        
                        percentages=[''] * 5
                        contents=[None] * 5
                        
                        for fc_percent_idx in range(1, 6):
                            if fc_val.has_key('fc_percentage' + str(fc_detail_idx) + '_' + str(fc_percent_idx)):
                                percentages[fc_percent_idx - 1] = fc_val['fc_percentage' + str(fc_detail_idx) + '_' + str(fc_percent_idx)]
                            if fc_val.has_key('fc_content' + str(fc_detail_idx) + '_' + str(fc_percent_idx)):
                                contents[fc_percent_idx -1] = fc_val['fc_percentage' + str(fc_detail_idx) + '_' + str(fc_percent_idx)]

                        if fc_ccName is not None:
                            fc_detail=JCPFCInstrDetail(header = header,
                                                       ccName = fc_ccName,
                                                       component = fc_component,
                                                       color = fc_color,
                                                       percentage1 = percentages[0],
                                                       content1 = contents[0],
                                                       percentage2 = percentages[1],
                                                       content2 = contents[1],
                                                       percentage3 = percentages[2],
                                                       content3 = contents[2],
                                                       percentage4 = percentages[3],
                                                       content4 = contents[3],
                                                       percentage5 = percentages[4],
                                                       content5=contents[4]
                                                       )

                            fc_infos.append(fc_detail)

            DBSession.add_all(fc_infos)

            customer=request.identity["user"].belongToCustomer
            addList = self._set_default_billToShipTo(customer, this_billto, this_shipto, [])

            DBSession.add_all(addList)
            
            if kw.get("fileName", '') and len(kw.get("fileName", '')) > 0:
                flag, sample_img = self._uploadSample(ph, kw["fileName"], kw["sampleFile"]) 

            self._construct_email(kw["sendEmailTo"], order, ph, [])

            DBSession.commit()
        except:
            file=open('log.txt', 'a')
            traceback.print_exc(None, file)
            file.close()
            DBSession.rollback()
            flash("The service is not avaiable now,please try it later or contact the system administator.", "warn")
        else:
            if False in upcFlag:
                upcSendTo=[request.identity["user"].email_address]
                upcCCTo=config.jcp_upc_mail.split(";")
                mailContent="The order [%s] got some upc/128c error, please contact us!"%order.customerPO
                self._sendNotifyEmail(upcSendTo, upcCCTo, order.customerPO, ph.id, mailContent, [], mailContent)
                flash(mailContent)
            elif len(gtin_length)>1:
                upcSendTo=[request.identity["user"].email_address]
                upcCCTo=config.jcp_upc_mail.split(";")
                mailContent="The order [%s] have more than one upc type, please contact us!"%order.customerPO
                self._sendNotifyEmail(upcSendTo, upcCCTo, order.customerPO, ph.id, mailContent, [], mailContent)
                flash(mailContent)
            else:
                flash("The order has been save successfully!")
        redirect("/order/viewOrder?code=%s"%(rpacEncrypt(ph.id)))

    @expose()
    def saveHTOrder(self, **kw):
        mh=getOr404(MsgHeader, kw["msgID"])
        DBSession.begin(subtransactions=True)
        try:
            if kw.has_key('national_brand') and not kw['national_brand']:
                raise AttributeError
            elif kw.has_key('private_brand') and not kw['private_brand']:
                raise AttributeError
            elif kw.has_key('combo_selection') and not kw['combo_selection']:
                raise AttributeError
        except AttributeError:
            flash("The order hasn't get enough info to place order!", "warn")
            redirect('/order/index')
        
        try:
            upcFlag=set()
            gtin_length=set()
            addList=[]
            rfid_flag = 'False'
            latest_form = JCPOrderForm.latest_order_form(request.identity["user"])
            ph=JCPHeaderPO(poNo=mh.Purchase_Order, poDate=dt.now(),
                             customer=DBSession.query(JCPCustomer).get(request.identity["user"].belong_to_customer_id) if request.identity["user"].belong_to_customer_id else None,
                             country=DBSession.query(JCPCountry).get(kw.get('sendEmailTo', '')),
                             remark=kw.get('remark', ''),
                             status='CONFIRM', orderType='AUTO')
            
            if kw.has_key("combo_selection") and kw.get("combo_selection", False) != '':
                ph.combo_order = str(int(kw.get("combo_selection", False).split("-")[0]) + 1)
            elif kw.has_key("combo_selection") and kw.get("combo_selection", False) == '':
                ph.combo_order = '2'
            elif kw.has_key("private_brand") and kw.get("private_brand", False) != '':
                ph.combo_order = str(int(kw.get("private_brand", False).split("-")[0]) + 1)
            elif kw.has_key("national_brand"):
                ph.combo_order = '2'
            
            addList.append(ph)
            fields=["customerPO", "supplierNO", "billAddress", "billAttn", "billTel", "billFax", "billEmail",
                      "origin", "shipAddress", "shipAttn", "shipTel", "shipFax", "shipEmail", "cust_item_codes"]
            params={"header" : ph,
                      "issuedBy" : request.identity["user"],
                      "lastModifyBy" : request.identity["user"],
                      "shipInstruction": kw.get("si_intro", ""),
                      'status': 'CONFIRM'
                      }
            for f in fields:
                if f in kw and kw[f] : params[f]=kw[f].strip()
            this_billto=DBSession.query(JCPBillTo).get(kw['billCompany'])
            this_shipto=DBSession.query(JCPShipTo).get(kw['shipCompany'])
            
            if this_billto and this_billto.company and len(this_billto.company) > 1:
                params['billCompany'] = this_billto.company
            elif 'other_billto' in kw.keys() and kw['other_billto']:
                params['billCompany'] = kw['other_billto']
            elif latest_form:
                params['billCompany'] = latest_form.billCompany
                
            if this_shipto and this_shipto.company and len(this_shipto.company) > 1:
                params['shipCompany'] = this_shipto.company
            elif 'other_shipto' in kw.keys() and kw['other_shipto']:
                params['shipCompany'] = kw['other_shipto']
            elif latest_form:
                params['shipCompany'] = latest_form.shipCompany
                
            
            #params['billCompany']=this_billto.company if this_billto else kw.get('other_billto', '')
            #params['shipCompany']=this_shipto.company if this_shipto else kw.get('other_shipto', '')

            order=JCPOrderForm(**params)
            addList.append(order)
            hangtag_flag=False
            private_flag=False
            combo_flag=False

            national_brand=kw.get("national_brand", False) if kw.has_key("national_brand") else None
            if kw.has_key("private_brand") and kw["private_brand"] and national_brand is not None:
                private_brand = kw.get("private_brand", False)
            elif kw.has_key("combo_selection") and kw["combo_selection"] and national_brand is not None:
                private_brand = kw.get("combo_selection", False)
            elif kw.has_key("private_brand") and kw["private_brand"] and "national_brand" not in kw.keys():
                private_brand = kw.get("private_brand", False)
            elif kw.has_key("combo_selection") and kw["combo_selection"] and "national_brand" not in kw.keys():
                private_brand = kw.get("combo_selection", False)
            else:
                private_brand = None
            
            if kw.has_key("private_brand") and kw["private_brand"]:
                if kw.get("private_brand", False).split("-")[0]== '0':
                    hangtag_flag = True
                    private_flag = True
                elif kw.get("private_brand", False).split("-")[0] == "1":
                    hangtag_flag = True
                elif kw.get("private_brand", False).split("-")[0] == "2":
                    private_flag = True
            
            if kw.has_key("combo_selection") and kw["combo_selection"]:
                if kw.get("combo_selection", False).split("-")[0] == '0':
                    hangtag_flag = True
                    combo_flag = True
                elif kw.get("combo_selection", False).split("-")[0] == "1":
                    hangtag_flag = True
                elif kw.get("combo_selection", False).split("-")[0] == "2":
                    combo_flag = True
            
            if 'private_brand' not in kw.keys() or 'combo_selection' in kw.keys():
                hangtag_flag = True
            
            poDetails=[]
            
            for md in mh.details:
                dParams={"header" : ph, "stock" : kw.get('hangtag_code', ''), "sub" : md.Sub, "lot" : md.Lot, "line" : md.Line, "size" : md.Size,
                           "sizeCode" : md.Sku, "description" : md.Item_Desc, "color" : md.Color, "cat" : md.Ctlg_Xref, "pid" : md.PID,
                           'upc' : md.GTIN, 'misc2': md.Misc_Txt2, 'msgDetail' : md,
                           'brand_type' : md.Brand_Typ, 'specialPrice' : md.Two_Or_More
                           }

                poDetail=None

                retailKey="retail_%d"%md.id
                quantityKey="quantity_%d"%md.id
                private_retail_key="private_retail_%d"%md.id
                combo_retail_key="combo_retail_%d"%md.id
                private_quantity_key="private_quantity_%d"%md.id
                combo_quantity_key="combo_quantity_%d"%md.id
                misc1_key="misc1_%d"%md.id
                private_misc1_key="private_misc1_%d"%md.id
                combo_misc1_key="combo_misc1_%d"%md.id

#                if quantityKey in kw and int(kw[quantityKey])>0 :
                if hangtag_flag == True and quantityKey in kw and int(kw[quantityKey])>0:
                    if retailKey in kw and kw[retailKey] : dParams["retail"]=kw[retailKey]
                    
                    dParams["quantity"]=int(kw[quantityKey])
                    
                    if dParams["upc"]: upcFlag.add(checkDigit12(dParams["upc"]))
                    else:
                        dParams["gtinCode"]=dParams["sub"]+dParams["lot"]+dParams["line"]+dParams["sizeCode"]+'0'
                        if len(dParams["gtinCode"])!=14: upcFlag.add(False)

                    if national_brand not in ['', None] and private_brand is None:
                        dParams["stock"]=national_brand
                        dParams["rfid"]=1
                        rfid_flag = 'True'
                    
                    dParams['misc1'] = kw.get(misc1_key, '')
                    dParams['type'] = 'Hangtag'

                    poDetail=JCPDetailPO(**dParams)
                    poDetails.append(poDetail)
                
                if private_flag == True and private_quantity_key in kw and int(kw[private_quantity_key])>0:
#                if private_quantity_key in kw and int(kw[private_quantity_key])>0:
                    if private_retail_key in kw and kw[private_retail_key] : dParams["retail"]=kw[private_retail_key]
                    
                    dParams["quantity"]=int(kw[private_quantity_key])
                    
                    if dParams["upc"]: upcFlag.add(checkDigit12(dParams["upc"]))
                    else:
                        dParams["gtinCode"]=dParams["sub"]+dParams["lot"]+dParams["line"]+dParams["sizeCode"]+'0'
                        if len(dParams["gtinCode"])!=14: upcFlag.add(False)

                    dParams["stock"]=private_brand.split('-')[1] if private_brand is not None else None
#                    if kw.has_key("private_brand") and kw["private_brand"]:
                    dParams["rfid"]=1
#                    elif kw.has_key("combo_selection") and kw["combo_selection"]:
#                        dParams["rfid"]=2
                    rfid_flag = 'True'
                    
                    dParams['misc1'] = kw.get(private_misc1_key, '')
                    dParams['type'] = 'Sticker'

                    poDetail=JCPDetailPO(**dParams)
                    poDetails.append(poDetail)
                
                if combo_flag == True and combo_quantity_key in kw and int(kw[combo_quantity_key])>0:
#                if private_quantity_key in kw and int(kw[private_quantity_key])>0:
                    if combo_retail_key in kw and kw[combo_retail_key] : dParams["retail"]=kw[combo_retail_key]
                    
                    dParams["quantity"]=int(kw[combo_quantity_key])
                    
                    if dParams["upc"]: upcFlag.add(checkDigit12(dParams["upc"]))
                    else:
                        dParams["gtinCode"]=dParams["sub"]+dParams["lot"]+dParams["line"]+dParams["sizeCode"]+'0'
                        if len(dParams["gtinCode"])!=14: upcFlag.add(False)

                    dParams["stock"]=private_brand.split('-')[1] if private_brand is not None else None
#                    if kw.has_key("private_brand") and kw["private_brand"]:
#                        dParams["rfid"]=1
#                    elif kw.has_key("combo_selection") and kw["combo_selection"]:
                    dParams["rfid"]=2
                    rfid_flag = 'True'
                    
                    dParams['misc1'] = kw.get(private_misc1_key, '')
                    dParams['type'] = 'Sticker'

                    poDetail=JCPDetailPO(**dParams)
                    poDetails.append(poDetail)

                gtin_length.add(len(md.GTIN))

            DBSession.add_all(poDetails)

            customer=request.identity["user"].belongToCustomer
            addList = self._set_default_billToShipTo(customer, this_billto, this_shipto, addList)

            DBSession.add_all(addList)

            if kw.get("spv_infos", "") and len(kw.get("spv_infos", ""))>1:
                pod_list, spv_values = self._set_specialvalue(kw.get("spv_infos", ""), poDetails)

                DBSession.add_all(pod_list)
                DBSession.add_all(spv_values)
            
            if kw.get("fileName", '') and len(kw.get("fileName", '')) > 0:
                flag, sample_img = self._uploadSample(ph, kw["fileName"], kw["sampleFile"]) 
            pd_file, filename=self.exportHTPDFile(code=rpacEncrypt(ph.id), rfid_flag = rfid_flag)

            self._construct_email(kw["sendEmailTo"], order, ph, [filename])

            DBSession.commit()
        except:
            file=open('log.txt', 'a')
            traceback.print_exc(None, file)
            file.close()
            DBSession.rollback()
            flash("The service is not avaiable now,please try it later or contact the system administator.", "warn")
        else:
            if False in upcFlag:
                upcSendTo=[request.identity["user"].email_address]
                upcCCTo=config.jcp_upc_mail.split(";")
                mailContent="The order [%s] got some upc/128c error, please contact us!"%order.customerPO
                self._sendNotifyEmail(upcSendTo, upcCCTo, order.customerPO, ph.id, mailContent, [], mailContent)
                flash(mailContent)
            elif len(gtin_length)>1:
                upcSendTo=[request.identity["user"].email_address]
                upcCCTo=config.jcp_upc_mail.split(";")
                mailContent="The order [%s] have more than one upc type, please contact us!"%order.customerPO
                self._sendNotifyEmail(upcSendTo, upcCCTo, order.customerPO, ph.id, mailContent, [], mailContent)
                flash(mailContent)
            else:
                flash("The order has been save successfully!")
        redirect("/order/viewOrder?code=%s"%(rpacEncrypt(ph.id)))

    def _format_value(self, detail):
        def _handle_attr(attr):
            result=getattr(detail, attr)

            if isinstance(result, basestring): result=result.decode("utf8")
            elif isinstance(result, dt): result=Date2Text(result).decode("utf8")
            elif isinstance(result, JCPHeaderPO): result=result.poNo
            
            return result
        
        results = map(_handle_attr, FIELDS)
        
#        if detail.header.orderType == 'AUTO':
#            item = JCPItemInfo.get_item(detail.msgDetail.Tkt_Stock)
#        else:
        item = JCPItemInfo.get_item(detail.stock)
        
        if item is not None:
            if detail.header.orderType == 'AUTO':
                sp_list = [''] * item.multi_special_value
            else:
                sp_list = [''] * len(detail.spvdetails[0].spvaluedetails)
        
            if detail.spvdetails:
                for sp_detail in detail.spvdetails[0].spvaluedetails:
                    if sp_detail.part != 0: sp_list[sp_detail.part - 1] = sp_detail.value
                
                for sp_detail in detail.spvdetails[0].spvaluedetails:
                    if sp_detail.part == 0: sp_list.append(sp_detail.value)

            for sp_item in sp_list:
                results.insert(-1, sp_item)
        
        #results.append(detail.header.orders[0].customerPO)
        supplierNo = '19963-8' if detail.header.orders[0].supplierNO.startswith('7') else detail.header.orders[0].supplierNO
        results.extend([detail.header.orders[0].customerPO, supplierNo, JCPCountryCode.get_name_by_id(int(detail.header.orders[0].origin))[0]])
        
        return results

    def _genHTProductionFile(self, header, time, rfid_flag):
        pe = None
        
        try:
            current=dt.now()
            dateStr=current.today().strftime("%Y%m%d")
            timeStr=current.time().strftime("%H%M%S")
            fileDir=os.path.join(os.path.abspath(os.path.curdir), "report_download", "%s"%dateStr)
    
            if not os.path.exists(fileDir): os.makedirs(fileDir)
    
            username=request.identity['repoze.who.userid']
            filename=os.path.join(fileDir, "%s_%s%s.xls"%(username, dateStr, timeStr))
            details = header.details

            if rfid_flag == 'True' and time == 0:
                new_details = filter(lambda item: item.rfid == 0, header.details)
            elif rfid_flag == 'True' and time == 1:
                new_details = filter(lambda item: item.rfid in [1, 2], header.details)
            
            if rfid_flag == 'True' and time == 0 and header.combo_order == '3':
                new_details = filter(lambda item: item.rfid in [1, 2], header.details)
            elif rfid_flag == 'True' and time == 0 and header.combo_order == '2':
                new_details = filter(lambda item: item.rfid in [1, 2], header.details)
            
            if rfid_flag == 'True':
                total_qty = sum([detail.quantity for detail in new_details])
                data=map(self._format_value, new_details)
            else:
                total_qty = sum([detail.quantity for detail in details])
                data=map(self._format_value, details)
                
            templatePath=os.path.join(os.path.abspath(os.path.curdir), "report_download/TEMPLATE/JCP_HANGTAG_PRDFILE_TEMPLATE.xls")
            pe=HangTagProductionExcel(templatePath=templatePath, destinationPath=filename)
            if header.orderType == 'AUTO':
                hangtag_item = JCPItemInfo.get_item(header.details[0].msgDetail.Tkt_Stock)
            else:
                hangtag_item = JCPItemInfo.get_item(header.details[0].stock)
            real_titles = copy.deepcopy(EXCEL_TITLES)
            extra_info_list = [hangtag_item, real_titles]
            
            def set_combo_package(item):
                item[0] = sticker_item.packaging_code
                
                return item
            element_length = max([len(element) for element in data])
            for i in range(element_length - len(EXCEL_TITLES)):
                real_titles.insert(-4, ''.join(['Special Value ', str(i + 1)]))
            
            for element in data:
                if len(element) < element_length:
                    for i in range(element_length - len(element)):
                        element.insert(-4, '')
            
            if (time == 1 or header.combo_order == '3') and hangtag_item is not None and rfid_flag != 'True':
                sticker_item = JCPItemInfo.get_item(hangtag_item.combo_packaging_code)
                data = map(set_combo_package, data)
                extra_info_list.remove(hangtag_item)
                extra_info_list.insert(0, sticker_item)
                extra_info_list.append('Sticker')
            
            coo = DBSession.query(JCPCountryCode).get(header.orders[0].origin)
            extra_info_list.append(coo)
            extra_info_list.append(total_qty)
            pe.inputData(extra_info = extra_info_list, header=header, data=data)
            pe.outputData()
            
            return filename
        except:
            file=open('log.txt', 'a')
            traceback.print_exc(None, file)
            file.close()
            if pe: pe.clearData()
            flash("Error occur in the generating production file !")

    @expose("ordering.templates.order.order_form_manual")
    @tabFocus(tab_type="main")
    def manual(self, **kw):
        try:
            countries=DBSession.query(JCPCountry).filter_by(active=0).order_by(JCPCountry.name).all()
            contacts=DBSession.query(JCPContact).filter_by(active=0).order_by(JCPContact.id).all()
            custom_po=kw.get('custom_po', '')
            country_code=DBSession.query(JCPCountryCode).order_by(JCPCountryCode.id).all()
            customer=request.identity["user"].belongToCustomer

            billTos, shipTos = self._get_billToShipTo(customer)
            last_billto=[item for item in billTos if item.is_default==1][0]
            last_shipto=[item for item in shipTos if item.is_default==1][0]

            return {"billTos" : billTos,
                    "shipTos" : shipTos,
                    "countries": countries,
                    "contacts": contacts,
                    'custom_po': custom_po,
                    'country_code': country_code,
                    'last_billto': last_billto,
                    'last_shipto': last_shipto,
                    'return_url': request.identity["user"].default_url,
                    }
        except AttributeError:
            redirect(request.identity["user"].default_url)
        except:
            file=open('log.txt', 'a')
            traceback.print_exc(None, file)
            file.close()
            flash("The service is not avaiable now,please try it later or contact the system administator.", "warn")
            redirect(request.identity["user"].default_url)


    @expose()
    def saveManual(self, **kw):
#        DBSession.begin()
        def getUpper(item): return item.upper()

        objs={}
        rfid_flag = 'False'

        for k in kw:
            if k.endswith("_ext"):
                name, index, ext=k.split("_")
                if index not in objs:
                    objs[index]={name:kw[k]}
                else:
                    objs[index][name]=kw[k]

        if not objs:
            flash("No item is ordered!", "warn")
            redirect(request.identity["user"].default_url)

        po_header=None
        detailFields=[("stock", None), ("sub", None), ("lot", int), ("description", None), ("line", None)
                          , ("cat", None), ("color", None), ("sizeCode", None), ("size", getUpper), ("upc", None),
                        ("pid", None),("specialValue", None), ("retail", None), ("quantity", None)]

        newObjs=[]
        details=[]

        srtObjs=sorted(objs.items(), key=lambda x: x[0])
        for k in srtObjs:
            v=k[1]
            if not po_header:
                headerParams={'status'    : 'CONFIRM',
                                  'orderType' : 'MANUAL'}
                headerParams["poDate"]=dt.now()
                if request.identity["user"].belong_to_customer_id: headerParams["customer"]=DBSession.query(JCPCustomer).get(request.identity["user"].belong_to_customer_id)
                headerParams["country"]=DBSession.query(JCPCountry).get(kw.get('sendEmailTo', ''))
                po_header=JCPHeaderPO(**headerParams)
                newObjs.append(po_header)

            detailParams={}
            for df, fun in detailFields:
                if df in v and df=='stock':
                    status=JCPItemInfo.get_status(pkg_code=v[df])

                    try:
                        if status==INACTIVE_ITEM:
                            raise AttributeError
                    except AttributeError:
                        flash("The order contains item cannot be ordered!", "warn")
                        redirect('/order/index')
                if df in v and v[df]:
                    detailParams[df]=fun(v[df]) if fun else v[df]
            detail=JCPDetailPO(header=po_header, **detailParams)
            details.append(detail)

        newObjs.extend(details)

        orderFormFields=[("customerPO", None),("supplierNO", None), ("billCompany", lambda v:DBSession.query(JCPBillTo).get(v)),
                            ("billAddress", None), ("billAttn", None),
                            ("billTel", None), ("billFax", None), ("billEmail", None),
                            ("shipCompany", lambda v:DBSession.query(JCPShipTo).get(v)),
                            ("shipAddress", None), ("shipAttn", None), ("shipTel", None),
                            ("shipFax", None), ("shipEmail", None),
                            ("origin", None), ("rnCode", None), ("wplCode", None), ("cust_item_codes", None)]
        orderFormParams={}
        for off, fun in orderFormFields:
            if off in kw and kw[off]:
                orderFormParams[off]=kw[off] if not fun else fun(kw[off])

        orderFormParams["issuedBy"]=request.identity["user"]
        orderFormParams["lastModifyBy"]=request.identity["user"]
        orderFormParams["billCompany"]=kw["other_billto"] if not orderFormParams["billCompany"] else orderFormParams["billCompany"].company
        orderFormParams["shipCompany"]=kw["other_shipto"] if not orderFormParams["shipCompany"] else orderFormParams["shipCompany"].company
        orderFormParams['status']='CONFIRM'

        if kw.get("si_intro", ""): orderFormParams["shipInstruction"]=kw.get("si_intro", "")

        order=JCPOrderForm(header=po_header, **orderFormParams)
        newObjs.append(order)

        DBSession.begin(subtransactions=True)
        try:
            DBSession.add_all(newObjs)

            fc_json=json.loads(kw.get("fc_infos", "").replace("'", '"')) if len(kw["fc_infos"])>1 else None
            wi_json=json.loads(kw.get("wi_infos", "").replace("'", '"')) if len(kw["wi_infos"])>1 else None
            special_value_json=json.loads(kw.get("special_value_infos", "").replace("'", '"')) if len(kw["special_value_infos"])>1 else None
            
            fc_infos=[]
            length=len(details)

            if fc_json:
                for key, val in fc_json.iteritems():
                    if not (key.split('_')[2]=='x'):
                        idx=int(key.split('_')[2])
                        if idx<=length: poDetail=details[idx-1]

                        fc_val = dict(i.split('=') for i in val.split('&'))
                    
                        for k, v in fc_val.iteritems():
                            exclusiveData = fc_val['fc_exclusive_data'] if fc_val.has_key('fc_exclusive_data') else None
                            cottonLogo = True if fc_val.has_key('fc_cotton_logo') and fc_val['fc_cotton_logo'] == 'true' else False
                            lycraLogo = True if fc_val.has_key('fc_lycra_logo') and fc_val['fc_lycra_logo'] == 'true' else False

                            fc_header=JCPFCInstrHeader(poDetail=poDetail, exclusiveData=exclusiveData,
                                                 cottonLogo=cottonLogo, lycraLogo=lycraLogo)

                        DBSession.add(fc_header)

                        for fc_detail_idx in range(1, 7):
                            header = fc_header
                            fc_ccName = None
                            fc_component = None
                            fc_color = None
                        
                            if fc_val.has_key('fc_cc_name' + str(fc_detail_idx)):
                                fc_ccName = fc_val['fc_cc_name' + str(fc_detail_idx)]
                            if fc_val.has_key('fc_component' + str(fc_detail_idx)):
                                fc_component = fc_val['fc_component' + str(fc_detail_idx)]
                            if fc_val.has_key('fc_color' + str(fc_detail_idx)):
                                fc_color = fc_val['fc_color' + str(fc_detail_idx)]
                        
                            percentages=[''] * 5
                            contents=[None] * 5
                        
                            for fc_percent_idx in range(1, 6):
                                if fc_val.has_key('fc_percentage' + str(fc_detail_idx) + '_' + str(fc_percent_idx)):
                                    percentages[fc_percent_idx - 1] = fc_val['fc_percentage' + str(fc_detail_idx) + '_' + str(fc_percent_idx)]
                                if fc_val.has_key('fc_content' + str(fc_detail_idx) + '_' + str(fc_percent_idx)):
                                    contents[fc_percent_idx -1] = fc_val['fc_percentage' + str(fc_detail_idx) + '_' + str(fc_percent_idx)]

                            if fc_ccName is not None:
                                fc_detail=JCPFCInstrDetail(header = header,
                                                       ccName = fc_ccName,
                                                       component = fc_component,
                                                       color = fc_color,
                                                       percentage1 = percentages[0],
                                                       content1 = contents[0],
                                                       percentage2 = percentages[1],
                                                       content2 = contents[1],
                                                       percentage3 = percentages[2],
                                                       content3 = contents[2],
                                                       percentage4 = percentages[3],
                                                       content4 = contents[3],
                                                       percentage5 = percentages[4],
                                                       content5=contents[4]
                                                       )

                                fc_infos.append(fc_detail)

            if wi_json:
                for key, val in wi_json.iteritems():
                    if not (key.split('_')[2]=='x'):
                        idx=int(key.split('_')[2])
                        if idx<=length:
                            details[idx-1].washingInstruction=''.join([i.split('=')[1] for i in val.split('&')])
                            details[idx-1].pid='manual'
            
            spv_values = []
            if special_value_json:
                
                for key, val in special_value_json.iteritems():
                    if not (key.split('_')[2] == 'x'):
                        idx = int(key.split('_')[2])
                        if idx <= length: poDetail = details[idx - 1]
    
                        if poDetail:
                            spv_header = JCPSPVHeader(poDetail = poDetail)
    
                            DBSession.add(spv_header)
                            sp_vals = dict(i.split('=') for i in val.split('&'))
                            
                            for k, v in sp_vals.iteritems():
                                if k.startswith('spvalue_part_'):
                                    spv_value = JCPSPVDetail(header = spv_header, value = v, part = int(k[-1]))
                                    
                                    spv_values.append(spv_value)

            
            DBSession.add_all(fc_infos)
            DBSession.add_all(spv_values)
            DBSession.add_all(details)

            this_billto=DBSession.query(JCPBillTo).get(kw['billCompany'])
            this_shipto=DBSession.query(JCPShipTo).get(kw['shipCompany'])
            customer=request.identity["user"].belongToCustomer
            addList = self._set_default_billToShipTo(customer, this_billto, this_shipto, [])
            
            if kw.get("fileName", '') and len(kw.get("fileName", '')) > 0:
                flag, sample_img = self._uploadSample(po_header, kw["fileName"], kw["sampleFile"])

            DBSession.add_all(addList)

            pd_file, filename=self.exportHTPDFile(code=rpacEncrypt(po_header.id), rfid_flag = rfid_flag)
            
            self._construct_email(kw["sendEmailTo"], order, po_header, [filename])

            DBSession.commit()
        except:
            traceback.print_exc()
            DBSession.rollback()
            flash("The service is not avaiable now,please try it later or contact the system administator.", "warn")
            raise
        else:
            flash("The manual order has been confirmed successfully!")
        redirect("/order/viewOrder?code=%s"%(rpacEncrypt(po_header.id)))

    @expose()
    def ajaxInstruction(self, cls, **kw):
        contents={}
        instrValues=kw["val"]

        ivs=list(instrValues)
        if len(ivs)==8:
            ivs=ivs[:6]+[instrValues[6:]]

        content_html="<table><tr><td>"
        for index, val in enumerate(ivs):
            content=DBSession.query(JCPInstruction) \
                      .filter(JCPInstruction.category==cls.upper()) \
                      .filter(JCPInstruction.position==(index+1)) \
                      .filter(JCPInstruction.selection==val) \
                      .one()

            content_html+=val+"&nbsp;&nbsp;</td><td>"+str(content.content).decode("utf8")+"</td></tr><tr><td>"

        content_html=content_html[:-9]+"</table>"

        return content_html


    @expose("ordering.templates.order.order_form_new")
    @tabFocus(tab_type="main")
    def placeOrder(self, **kw):
        try:
            mh=getOr404(MsgHeader, kw["id"])
            customer=request.identity["user"].belongToCustomer

            billTos, shipTos = self._get_billToShipTo(customer)
            last_billto=[item for item in billTos if item.is_default==1][0]
            last_shipto=[item for item in shipTos if item.is_default==1][0]
            
            order_form = JCPOrderForm.latest_order_form(request.identity['user'])
            
            countries=DBSession.query(JCPCountry).filter_by(active=0).order_by(JCPCountry.name).all()
            contacts=DBSession.query(JCPContact).filter_by(active=0).order_by(JCPContact.id).all()
            custom_po=kw.get('customerPO', '')
            #qty=kw.get('qty', '0')
            order_flag=0
            rfid = mh.details[0].RFID
            img_url=JCPItemInfo.get_item(mh.details[0].Tkt_Stock)
            rfid_order_flag = 'YES' if (mh.details[0].Sub, mh.details[0].Brand_Typ) not in RFID_NONE_ORDER_LIST and (img_url or mh.details[0].Brand_Typ == 'N') else 'NO'
            special_value=kw.get('special_value', False)
            rfid_mapping_code=kw.get('rfid_mapping_code', 'TBD')
            hangtag_code=kw.get('hangtag_code', False)
            country_code=DBSession.query(JCPCountryCode).order_by(JCPCountryCode.id).all()
            
            if hangtag_code is not None and img_url is not None:
                if hangtag_code == img_url.packaging_code:
                    combo_item=DBSession.query(JCPItemInfo.packaging_code).filter(JCPItemInfo.packaging_code==img_url.combo_packaging_code).first() if img_url else None
                else:
                    combo_item=JCPItemInfo.get_item(rfid_mapping_code)
            else:
                hangtag_code=mh.details[0].Tkt_Stock
                combo_item='TBD'
            
            sticker_code = None
            
            if img_url is not None and rfid_mapping_code != img_url.combo_packaging_code:
                sticker_code = rfid_mapping_code
                rfid_mapping_code = img_url.combo_packaging_code
            
            rfid_special_value = None
            rfid_special_flag = False
            rfid_special_item = JCPItemInfo.get_item(rfid_mapping_code)
            if rfid_mapping_code and rfid_special_item:
                rfid_special_value = rfid_special_item.values
            if rfid_special_item:
                rfid_special_flag = rfid_special_item.special_value
            
            combo_special_value = None
            combo_special_item = None
            combo_special_flag = False
            if combo_item and isinstance(combo_item, JCPItemInfo):
                combo_special_item = combo_item
                combo_special_value = combo_item.values
            elif combo_item and JCPItemInfo.get_item(combo_item[0]):
                combo_special_item = JCPItemInfo.get_item(combo_item[0])
                combo_special_value = combo_special_item.values
            
            if combo_special_item:
                combo_special_flag = combo_special_item.special_value 
            
            if img_url is None:
                sendTo = config.jcp_item_mail.split(";")
                title = "The item need set up"
                content = "\n".join([
                    "The item with this package code: '%s' is not yet set up, please check and set up." % hangtag_code,
                    "\n\n************************************************************************************",
                    "This e-mail is sent by the r-pac JCPenny ordering system automatically.",
                    "Please don't reply this e-mail directly!",
                    "Notice: If the stock is empty or miss the special value in the order, please contact with us.",
                    "************************************************************************************"
                    ])
                self._sendNotifyEmail(sendTo, None, None, None, content, [], title)
            
            return {"msgHeader": mh,
                    "msgDetail": mh.details,
                    "rfid": rfid,
                    "brand_type": mh.details[0].Brand_Typ,
                    "stock_flag": mh.details[0].Tkt_Stock,
                    "billTos": billTos,
                    "shipTos": shipTos,
                    "order_form": order_form,
                    "countries": countries,
                    "contacts": contacts,
                    "image_url": img_url,
                    "combo_item": combo_item,
                    "order_flag": order_flag,
                    'custom_po': custom_po,
                    'country_code': country_code,
                    'special_value': special_value,
                    'rfid_mapping_code': rfid_mapping_code,
                    'sticker_code': sticker_code,
                    'hangtag_code': hangtag_code,
                    'combo_flag': img_url.combo_item if img_url else False,
                    #'qty' : qty,
                    'rfid_order_flag': rfid_order_flag,
                    'last_billto': last_billto,
                    'last_shipto': last_shipto,
                    'return_url': request.identity["user"].default_url,
                    'sp_values': img_url.values if img_url else None,
                    'rfid_special_value': rfid_special_value,
                    'combo_special_value': combo_special_value,
                    'rfid_special_item': rfid_special_item,
                    'combo_special_item': combo_special_item,
                    'rfid_special_flag': rfid_special_flag,
                    'combo_special_flag': combo_special_flag,
                   }
        except:
            file=open('log.txt', 'a')
            traceback.print_exc(None, file)
            file.close()
            flash("The service is not avaiable now,please try it later or contact the system administator.", "warn")
            redirect(request.identity["user"].default_url)

    @expose()
    def ajaxSearchIntro(self, category, item, pos):
        content=DBSession.query(JCPInstruction.content) \
                      .filter(JCPInstruction.category==category.upper()) \
                      .filter(JCPInstruction.position==int(pos)) \
                      .filter(JCPInstruction.selection==str(item)) \
                      .first()

        return content


    def _sendNotifyEmail(self, sendTo, ccTo, customerPO, hederID, content=None, attach=[], title=None):
        sendFrom="r-pac-JCPenny-ordering-system"
        if title:
            subject=title
        else:
            subject="Order[%s] has been confirmed successfully!"%customerPO
        if content :
            text=content
        else:
            text="\n".join([
                    "Thank you for your confirmation!", "You could view the order's detail information via the link below:",
                    "%s/order/viewOrder?code=%s"%(config.website_url, rpacEncrypt(hederID)),
                    "\n\n************************************************************************************",
                    "This e-mail is sent by the r-pac JCPenny ordering system automatically.",
                    "Please don't reply this e-mail directly!",
                    "Notice: If the stock is empty or miss the special value in the order, please contact with us.",
                    "************************************************************************************"
                    ])

        sendEmail(sendFrom, sendTo, subject, text, ccTo, attach)

    @expose()
    def ajaxFiberContent(self, id, **kw):
        fc_header=DBSession.query(JCPFCInstrHeader) \
                        .filter(JCPFCInstrHeader.podetailid==JCPDetailPO.id) \
                        .filter(JCPDetailPO.id==id) \
                        .first()

        content_html='<div id="fc-addition"><div style="margin:0px 0px 0px 5px; float: left">'
        content_html+='<label class="fonts-14pt fonts-c-036">Fiber Content</label></div><br /><table><tbody><tr><td>'
        content_html+='<span class="fonts-c-369">Exclusive data:</span></td><td><span class="fonts-c-369">'+fc_header.exclusiveData
        content_html+='</span></td></tr><tr><td align="right"><span class="fonts-c-369">'

        if fc_header.cottonLogo:
            content_html+='<input type="checkbox" name="fc_cotton_logo" id="fc_cotton_logo" checked />'
        else:
            content_html+='<input type="checkbox" name="fc_cotton_logo" id="fc_cotton_logo" />'

        content_html+='</span></td><td><span class="fonts-c-369"><label for="cotton_logo">Cotton Logo(Optional)</label>'
        content_html+='</span></td></tr><tr><td align="right"><span class="fonts-c-369">'

        if fc_header.lycraLogo:
            content_html+='<input type="checkbox" name="fc_lycra_logo" id="fc_lycra_logo" checked />'
        else:
            content_html+='<input type="checkbox" name="fc_lycra_logo" id="fc_lycra_logo" />'

        content_html+='</span></td><td><span class="fonts-c-369"><label for="lycra_logo">Lycra Logo(Optional)</label>'
        content_html+='</span></td></tr></tbody></table>'

        for index, detail in enumerate(fc_header.fcdetails):
            content_html+='<div width="500" style="float:left;" class="fc_component_color">'
            content_html+='<table width="450" border="0" cellpadding="0" cellspacing="0" style="border:#369 solid 2px; margin:10px 0px 0px 10px">'
            content_html+='<tbody><tr><td width="20" bgcolor="#CCFFFF">&nbsp;</td><td bgcolor="#CCFFFF">&nbsp;</td><td width="20" bgcolor="#CCFFFF">'
            content_html+='&nbsp;</td></tr><tr><td bgcolor="#CCFFFF">&nbsp;</td><td bgcolor="#CCFFFF" class="fonts-c-036">Component&nbsp;&nbsp;'+str(index+1)
            content_html+='</td><td bgcolor="#CCFFFF">&nbsp;</td></tr><tr><td bgcolor="#CCFFFF">&nbsp;</td><td bgcolor="#CCFFFF" class="fonts-c-036">'
            content_html+='<strong>Component or Color: </strong>'+detail.ccName+'</td><td bgcolor="#CCFFFF">&nbsp;</td></tr><tr>'
            content_html+='<td bgcolor="#CCFFFF">&nbsp;</td><td bgcolor="#CCFFFF" class="fonts-c-036">Component:&nbsp;&nbsp;'+detail.component
            content_html+='&nbsp;&nbsp;Color:&nbsp;&nbsp;'+detail.color+'</td><td bgcolor="#CCFFFF">&nbsp;</td></tr>'

            if detail.percentage1:
                content_html+='<tr><td bgcolor="#CCFFFF">&nbsp;</td><td bgcolor="#CCFFFF" class="fonts-c-036">Content: '
                content_html+=detail.percentage1+'%&nbsp;&nbsp;'+detail.content1+'</td><td bgcolor="#CCFFFF">&nbsp;</td>'
                content_html+='</tr>'

            if detail.percentage2:
                content_html+='<tr><td bgcolor="#CCFFFF">&nbsp;</td><td bgcolor="#CCFFFF" class="fonts-c-036">Content: '
                content_html+=detail.percentage2+'%&nbsp;&nbsp;'+detail.content2+'</td><td bgcolor="#CCFFFF">&nbsp;</td>'
                content_html+='</tr>'

            if detail.percentage3:
                content_html+='<tr><td bgcolor="#CCFFFF">&nbsp;</td><td bgcolor="#CCFFFF" class="fonts-c-036">Content: '
                content_html+=detail.percentage3+'%&nbsp;&nbsp;'+detail.content3+'</td><td bgcolor="#CCFFFF">&nbsp;</td>'
                content_html+='</tr>'

            if detail.percentage4:
                content_html+='<tr><td bgcolor="#CCFFFF">&nbsp;</td><td bgcolor="#CCFFFF" class="fonts-c-036">Content: '
                content_html+=detail.percentage4+'%&nbsp;&nbsp;'+detail.content4+'</td><td bgcolor="#CCFFFF">&nbsp;</td>'
                content_html+='</tr>'

            if detail.percentage5:
                content_html+='<tr><td bgcolor="#CCFFFF">&nbsp;</td><td bgcolor="#CCFFFF" class="fonts-c-036">Content: '
                content_html+=detail.percentage5+'%&nbsp;&nbsp;'+detail.content5+'</td><td bgcolor="#CCFFFF">&nbsp;</td>'
                content_html+='</tr>'

            content_html+='<tr><td bgcolor="#CCFFFF">&nbsp;</td><td bgcolor="#CCFFFF">&nbsp;</td><td bgcolor="#CCFFFF">&nbsp;</td>'
            content_html+='</tr></tbody></table></div></div>'

        return content_html

    @expose()
    def ajaxWashingInstruction(self, id, **kw):
        wi_intros=DBSession.query(JCPDetailPO).get(id)
        content_html=self.ajaxInstruction(cls='wi', val=wi_intros.washingInstruction)

        return content_html

    @expose()
    def ajaxImage(self, id, **kw):
        if kw.get('type', '') == 'cust':
            img=DBSession.query(CustomerSample).get(id)
            src='/images/attachment_upload/' +img.path[41:]
            package = ''
            itemCode = ''
        else:
            img=DBSession.query(JCPItemInfo).get(id)
            src = img.path + img.item_code + '.jpg'
            package = img.packaging_code
            itemCode = img.item_code

        if not img:
            return '<h1>Sorry</h1><p>No such item\' sample image could be viewed.</p>'

        content_html='<table cellspacing=0 cellpadding=4 width="100%" border=0><tbody><tr valign=top>'
        content_html+='<td class=elpri colspan=2><b><img src="/images/logo.jpg" width="100%" height="72"></b></td>'
        content_html+='</tr><tr><td align="left" valign="top"><table width="100%" border="0" cellspacing="0" cellpadding="0">'
        content_html+='<tr><td width="50" class="title1">&nbsp;</td><td height="40" class="title1"><strong>Ticket Stock Number&nbsp;:&nbsp;'
        content_html+='</strong><font color="#00008B" class="title2">'+package+'</font></td></tr><tr><td>&nbsp;</td>'
        content_html+='<td height="30" class="title3">The sample image of variable ticket <font color="#A0522D">'+itemCode+'</font>: </td></tr>'
        content_html+='</table></td><td class=el align=middle>&nbsp;</td>'
        content_html+='</tr><tr><td colspan=2><hr noshade size=1></td></tr><tr valign=top><td colspan=2 style="padding:10px 50px 10 50px">'
        content_html+='<img src="'+ src +'" width="476" height="502"></tr><tr valign=top>'
        content_html+='<td colspan=2><hr noshade size=1></tr></tbody></table>'

        return content_html
    
    @expose()
    def showNBrandImg(self, name, **kw):
        content_html='<table cellspacing=0 cellpadding=4 width="100%" border=0><tbody><tr valign=top>'
        content_html+='<td class=elpri colspan=2><b><img src="/images/logo.jpg" width="100%" height="72"></b></td>'
        content_html+='</tr><tr><td align="left" valign="top"><table width="100%" border="0" cellspacing="0" cellpadding="0">'
        content_html+='<tr><td width="50" class="title1">&nbsp;</td><td height="40" class="title1"><strong>Ticket Stock Number&nbsp;:&nbsp;'
        content_html+='</strong><font color="#00008B" class="title2">'+name+'</font></td></tr><tr><td>&nbsp;</td>'
        content_html+='<td height="30" class="title3">The sample image of variable ticket <font color="#A0522D">'+name+'</font>: </td></tr>'
        content_html+='</table></td><td class=el align=middle>&nbsp;</td>'
        content_html+='</tr><tr><td colspan=2><hr noshade size=1></td></tr><tr valign=top><td colspan=2 style="padding:10px 50px 10 50px">'
        content_html+='<img src="/images/national-brand/'+name+'.jpg" width="476" height="502"></tr><tr valign=top>'
        content_html+='<td colspan=2><hr noshade size=1></tr></tbody></table>'

        return content_html

    @expose()
    def ajaxSpecialValues(self, id, **kw):
        spv_header=DBSession.query(JCPSPVHeader) \
                        .filter(JCPSPVHeader.podetailid==JCPDetailPO.id) \
                        .filter(JCPDetailPO.id==id) \
                        .one()
        
        jcp_detail = JCPDetailPO.get_by_id(id)
        item = JCPItemInfo.get_item(jcp_detail.stock)

        content_html='<div id="sp_value"><div style="margin:0px 0px 0px 5px; float: left">'
        content_html+='<label class="fonts-14pt fonts-c-036">Special Value(s)</label></div><br /><br /><table><tbody>'

        for index in range(item.multi_special_value):
            content_html+='<tr><td><span class="fonts-c-369">Special Value Name <b>'+str(index+1)+'</b>: </span></td><td><span class="fonts-c-369">'

            for detail in spv_header.spvaluedetails:
                if detail.part==index+1:
                    content_html+='<b>'+detail.value+'</b></span></td></tr>'
                    break
            else:
                content_html+='<b>N/A</b></span></td></tr>'

        for detail in spv_header.spvaluedetails:
            if detail.part == 0:
                content_html+='<tr><td><span class="fonts-c-369">Fiber Content: </span></td><td><span class="fonts-c-369">'
                content_html+='<b>'+detail.value+'</b></span></td></tr>'
        content_html+='</tbody></table></div>'

        return content_html
    
    @expose()
    def ajaxSpecialValueImage(self, id):
        spv = JCPSpecialValue.get_special_value(id) if id.isdigit() else None
        content_html = ''
        
        if spv:
            src = ''.join([spv.path, '/', spv.items[0].item_code, '-', str(spv.part), '-', spv.value[-1], '.jpg'])
            content_html='<div class="sp_value"><div style="margin:0px 0px 0px 5px; float: left">'
            content_html+='<label class="fonts-14pt fonts-c-036">Special Value(s)</label></div><br /><br /><table><tbody>'
            content_html+='<tr><td><img src="'+src+'" /></td></tr>'
            content_html+='</tbody></table></div>'

        return content_html

    @expose('ordering.templates.order.care_code')
    def showCode(self, **kw):
        codes=DBSession.query(JCPInstruction).filter(JCPInstruction.category=='FC') \
                .order_by(JCPInstruction.position).order_by(JCPInstruction.selection).all()

        return dict(infos=codes, code=kw.get("code", ""))

    @expose()
    @tabFocus(tab_type="main")
    def cancelOrder(self, **kw):
        (flag, id)=rpacDecrypt(kw.get("code", ""))
        if not flag:
            flash("Please don't access the resource illegally!")
            redirect(request.identity["user"].default_url)

        ph=getOr404(JCPHeaderPO, id)

        if len(ph.orders)<1 :
            flash("There's no order related to this PO!", "warn")
            redirect(request.identity["user"].default_url)

        try:
            ph.active=1

            for order_form in ph.orders: order_form.active=1

            DBSession.add(ph)
            flash("The order has been canceled successfully!")
        except:
            traceback.print_exc()
            flash("There's an error occured during cancel this order!")
        redirect(request.identity["user"].default_url)

    @expose()
    @tabFocus(tab_type="main")
    def unlockOrder(self, **kw):
        (flag, id)=rpacDecrypt(kw.get("code", ""))
        if not flag:
            flash("Please don't access the resource illegally!")
            redirect(request.identity["user"].default_url)

        ph=getOr404(JCPHeaderPO, id)

        if len(ph.orders)<1:
            flash("There's no order related to this PO!", "warn")
            redirect(request.identity["user"].default_url)
        elif ph.status not in ["CONFIRM", 'RFID']:
            flash("The order cann't be modified, please confirm the correct order!", 'warn')
            redirect(request.identity["user"].default_url)

        try:
            ph.status='UPDATE'
            for order_form in ph.orders: order_form.status='UPDATE'

            DBSession.add(ph)
            flash("The order has been unlocked successfully!")
        except:
            traceback.print_exc()
            flash("There's an error occured during cancel this order!")
        redirect(request.identity["user"].default_url)

    @expose()
    @tabFocus(tab_type="main")
    def updateOrder(self, **kw):
        (flag, id)=rpacDecrypt(kw.get("code", ""))

        if not flag:
            flash("Please don't access the resource illegally!")
            redirect(request.identity["user"].default_url)

        ph=getOr404(JCPHeaderPO, id)

        if ph.status in ['CONFIRM', 'RFID']:
            flash("The order has not been authorized to modify!", "warn")
            redirect(request.identity["user"].default_url)

        if len(ph.orders)<1:
            flash("There's no order related to this PO!", "warn")
            redirect(request.identity["user"].default_url)

        status=JCPItemInfo.get_status(pkg_code=ph.details[0].stock)
        special_value=JCPItemInfo.get_special_value(pkg_code=ph.details[0].stock)

        if status==INACTIVE_ITEM:
            flash("The item is inactive and can not be ordered!")
            redirect(request.identity['user'].default_url)

        img_url=JCPItemInfo.get_item(ph.details[0].msgDetail.Tkt_Stock)
        combo_item=DBSession.query(JCPItemInfo.packaging_code).filter(JCPItemInfo.packaging_code==img_url.combo_packaging_code).first() if img_url else None
        care_infos=self._isCareLabel(ph, "po")
        country_code=DBSession.query(JCPCountryCode).order_by(JCPCountryCode.id).all()
        customer=request.identity["user"].belongToCustomer

        billTos, shipTos = self._get_billToShipTo(customer)

        countries=DBSession.query(JCPCountry).filter_by(active=0).order_by(JCPCountry.name).all()
        contacts=DBSession.query(JCPContact).filter_by(active=0).order_by(JCPContact.id).all()
        
        rfid_order_flag = 'YES' if (ph.details[0].sub, ph.details[0].brand_type) not in RFID_NONE_ORDER_LIST and (img_url or ph.details[0].brand_type == 'N') else 'NO'
        
        if care_infos:
            rfid = 'NO'
        else:
            rfid = ph.details[0].msgDetail.RFID

        if any([d.washing_instruction==True and d.fiber_content==True and d.country_of_origin==True for d in care_infos]):
            if ph.orderType=='AUTO':
                override_template(self.updateOrder, 'mako:ordering.templates.order.order_form_update_carelabel')
            else:
                override_template(self.updateOrder, 'mako:ordering.templates.order.order_form_update_manual')

            country=DBSession.query(JCPCountryCode).get(int(ph.orders[0].origin))

            return {"poheader"     : ph,
                    "podetails"    : ph.details,
                    "orderHeader"  : ph.orders[0],
                    "rfid"         : rfid,
                    "combo_item"   : combo_item[0] if combo_item else None,
                    "brand_type"   : ph.details[0].brand_type,
                    "rfid_order_flag": rfid_order_flag,
                    'country'      : country,
                    "image_url"    : img_url,
                    'billTos'      : billTos,
                    'shipTos'      : shipTos,
                    'countries'    : countries,
                    'contacts'     : contacts,
                    'country_code' : country_code,
                    'return_url': request.identity["user"].default_url,
                    'special_value' : special_value,
                    'sp_values': img_url.values if img_url else None,
                    }
        else:
            if ph.orderType=='AUTO' :
                override_template(self.updateOrder, 'mako:ordering.templates.order.order_form_update_ht')
            else:
                override_template(self.updateOrder, 'mako:ordering.templates.order.order_form_update_manual')

            return {"poheader"     : ph,
                    "podetails"    : ph.details,
                    "orderHeader"  : ph.orders[0],
                    "rfid"         : rfid,
                    "combo_item"   : combo_item[0] if combo_item else None,
                    "brand_type"   : ph.details[0].brand_type,
                    "rfid_order_flag": rfid_order_flag,
                    "image_url"    : img_url,
                    'billTos'      : billTos,
                    'shipTos'      : shipTos,
                    'countries'    : countries,
                    'contacts'     : contacts,
                    'country_code' : country_code,
                    'return_url': request.identity["user"].default_url,
                    'special_value' : special_value,
                    'sp_values': img_url.values if img_url else None,
                    }

    @expose()
    def saveManualUpdate(self, **kw):

        def getUpper(item): return item.upper()

        po_header=DBSession.query(JCPHeaderPO).get(int(kw.get('po_id', '')))
        po_header.customer=DBSession.query(JCPCustomer).get(request.identity["user"].belong_to_customer_id) if request.identity["user"].belong_to_customer_id else None
        po_header.country=DBSession.query(JCPCountry).get(kw.get('sendEmailTo', ''))
        po_header.status='CONFIRM'
        order=DBSession.query(JCPOrderForm).get(int(kw.get('form_id', '')))

        objs={}
        for k in kw:
            if k.endswith("_ext"):
                name, index, ext=k.split("_")
                if index not in objs:
                    objs[index]={name:kw[k]}
                else:
                    objs[index][name]=kw[k]

        if not objs:
            flash("No item is ordered!", "warn")
            redirect(request.identity["user"].default_url)

        detailFields=[("stock", None),
                        ("sub", None),
                        ("lot", int),
                        ("description", None),
                        ("line", None),
                        ("cat", None),
                        ("color", None),
                        ("sizeCode", None),
                        ("size", getUpper),
                        ("upc", None),
                        ("specialValue", None),
                        ("retail", None),
                        ("quantity", int)
                        ]

        details=[]

        srtObjs=sorted(objs.items(), key=lambda x: x[0])
        for k in srtObjs:
            v=k[1]
            detail=DBSession.query(JCPDetailPO).get(int(kw.get('detail_id_'+k[0], ''))) if kw.get('detail_id_'+k[0]) else None
            detailParams={}

            for df, fun in detailFields:
                if df in v and df=='stock':
                    status=JCPItemInfo.get_status(pkg_code=v[df])

                    try:
                        if status==INACTIVE_ITEM:
                            raise AttributeError
                    except AttributeError:
                        flash("The order contains item cannot be ordered!", "warn")
                        redirect('/order/index')

                if df in v and v[df]: detailParams[df]=fun(v[df]) if fun else v[df]

            if detail:
                for key, val in detailParams.iteritems():
                    if key in dir(detail): setattr(detail, key, val)
            else: detail=JCPDetailPO(header=po_header, **detailParams)

            details.append(detail)

        orderFormFields=["customerPO",
                         "supplierNO",
                         "billAddress",
                           "billAttn",
                           "billTel",
                           "billFax",
                           "billEmail",
                           "shipAddress",
                           "shipAttn",
                           "shipTel",
                           "shipFax",
                           "shipEmail",
                           "origin",
                           "rnCode",
                           "wplCode",
                           "cust_item_codes",
                           'shipInstruction',
                           ]

        orderFormParams={"lastModifyBy" : request.identity["user"],
                           'status'       : 'CONFIRM'
                           }
        for off in orderFormFields:
            if off in kw and kw[off]: orderFormParams[off]=kw[off]

        this_billto=None
        this_shipto=None

        if int(kw['billCompany'])!=-1 :
            this_billto=DBSession.query(JCPBillTo).get(int(kw['billCompany']))
            orderFormParams['billCompany']=this_billto.company if this_billto else kw['other_billto']
        if int(kw['shipCompany'])!=-1 :
            this_shipto=DBSession.query(JCPShipTo).get(int(kw['shipCompany']))
            orderFormParams['shipCompany']=this_shipto.company if this_shipto else kw['other_shipto']

        for key, val in orderFormParams.iteritems():
            if key in dir(order): setattr(order, key, val)

        DBSession.begin(subtransactions=True)
        try:
            DBSession.add_all([po_header, order])

            fc_json=json.loads(kw.get("fc_infos", "").replace("'", '"')) if len(kw["fc_infos"])>1 else None
            wi_json=json.loads(kw.get("wi_infos", "").replace("'", '"')) if len(kw["wi_infos"])>1 else None
            fc_infos=[]
            length=len(details)

            if fc_json:
                for key, val in fc_json.iteritems():
                    if not (key.split('_')[2]=='x'):
                        idx=key.split('_')[2]

                        if int(idx)<=length:
                            poDetail=details[int(idx)]
                        else:
                            poDetail=DBSession.query(JCPDetailPO).get(int(idx))
                            if poDetail.fcdetails: DBSession.delete(poDetail.fcdetails[0])

                        for k, v in val.iteritems():
                            fc_header_params={'exclusiveData' : val['exclusive_data'],
                                                'cottonLogo'    : True if val['fc_cotton_logo']=='true' else False,
                                                'lycraLogo'     : True if val['fc_lycra_logo']=='true' else False,
                                                }

                        fc_header=JCPFCInstrHeader(poDetail=poDetail, **fc_header_params)

                        DBSession.add(fc_header)
                        fc_details=val['components']

                        for item in fc_details:
                            fc_detail_params={'header'    : fc_header,
                                                'ccName'    : item['cc_name'],
                                                'component' : item['component'],
                                                'color'     : item['color'],
                                                }

                            for index, percent_item in enumerate(item['percent']):
                                fc_detail_params['percentage'+str(index+1)]=percent_item['fc_percentage']
                                fc_detail_params['content'+str(index+1)]=percent_item['fc_content']

                            fc_detail=JCPFCInstrDetail(**fc_detail_params)
                            fc_infos.append(fc_detail)

            if wi_json:
                for key, val in wi_json.iteritems():
                    if not (key.split('_')[2]=='x'):
                        idx=key.split('_')[2]
                        details[int(idx)].washingInstruction=val
                        details[int(idx)].pid='manual'

            DBSession.add_all(fc_infos)
            DBSession.add_all(details)

            customer=request.identity["user"].belongToCustomer
            addList = self._set_default_billToShipTo(self, customer, this_billto, this_shipto, [])

            DBSession.add_all(addList)
            DBSession.flush()

            self._construct_email(kw["sendEmailTo"], order, po_header, [])

            DBSession.commit()
        except:
            file=open('log.txt', 'a')
            traceback.print_exc(None, file)
            file.close()
            DBSession.rollback()
            flash("The service is not avaiable now,please try it later or contact the system administator.", "warn")
            raise
        else:
            flash("The manual order has been confirmed successfully!")
        redirect("/order/viewOrder?code=%s"%(rpacEncrypt(po_header.id)))

    @expose()
    def saveHTUpdate(self, **kw):
        DBSession.begin(subtransactions=True)
        try:
            upcFlag=set()
            gtin_length=set()
            addList=[]
            rfid_flag = 'False'
            po_header=DBSession.query(JCPHeaderPO).get(int(kw.get('po_id', '')))
            po_header.country=DBSession.query(JCPCountry).get(kw.get('sendEmailTo', ''))
            po_header.status='CONFIRM'
            po_header.remark=kw.get('remark', '')

            if kw.has_key("combo_selection") and kw.get("combo_selection", False) != '':            
                po_header.combo_order = kw.get("combo_selection", False).split("-")[1]
            
            national_brand=kw.get("national_brand", False) if kw.has_key("national_brand") else None
            addList.append(po_header)

            order=DBSession.query(JCPOrderForm).get(int(kw.get('form_id', '')))

            fields=["customerPO",
                    "supplierNO",
                      "billAddress",
                      "billAttn",
                      "billTel",
                      "billFax",
                      "billEmail",
                      "shipAddress",
                      "shipAttn",
                      "shipTel",
                      "shipFax",
                      "shipEmail",
                      "cust_item_codes",
                      "shipInstruction"
                      ]
            params={'status'       : 'CONFIRM',
                      "lastModifyBy" : request.identity["user"],
                      }

            for f in fields:
                if f in kw and kw[f] : params[f]=kw[f]
            
            this_billto=None
            this_shipto=None

            if int(kw['billCompany'])!=-1 :
                this_billto=DBSession.query(JCPBillTo).get(int(kw['billCompany']))
                params['billCompany']=this_billto.company if this_billto else kw('other_billto', '')
            if int(kw['shipCompany'])!=-1 :
                this_shipto=DBSession.query(JCPShipTo).get(int(kw['shipCompany']))
                params['shipCompany']=this_shipto.company if this_shipto else kw('other_shipto', '')
            
            for key, val in params.iteritems():
                if key in dir(order): setattr(order, key, val)

            addList.append(order)

            for detail in po_header.details:
                detail.retail=kw.get('retail_%d'%detail.id)
                detail.quantity=int(kw.get('quantity_%d'%detail.id))

                if detail.upc: upcFlag.add(checkDigit12(detail.upc))
                else: upcFlag.add(len(detail.gtinCode)==14)
                
                if national_brand not in ['', None]: detail.stock=national_brand
                if detail.rfid == 1: rfid_flag = 'True'
                    
                addList.append(detail)
                gtin_length.add(len(detail.upc))

            customer=request.identity["user"].belongToCustomer
            addList = self._set_default_billToShipTo(self, customer, this_billto, this_shipto, addList)

            if kw.get("spv_infos", "") and len(kw.get("spv_infos", ""))>1:
                spv_json=json.loads(kw.get("spv_infos", "").replace("'", '"'))
                spv_values=[]
                pod_list=[]

                for key, val in spv_json.iteritems():
                    poDetail=None

                    for pd in po_header.details:
                        if int(key.split('_')[2])==pd.id:
                            poDetail=pd
                            if pd.spvdetails: DBSession.delete(pd.spvdetails[0])

                    if poDetail:
                        spv_header=JCPSPVHeader(poDetail=poDetail)

                        DBSession.add(spv_header)
                        
                        spv_details = dict(item.split('=') for item in val.split('&'))

                        for k, v in spv_details.iteritems():
                            if k.startswith("spv_"):
                                if v.isdigit():
                                    sp_value=DBSession.query(JCPSpecialValue).get(int(v))
                                    spv_value=JCPSPVDetail(header=spv_header, value=sp_value.value, part=sp_value.part)
    
                                    spv_values.append(spv_value)
                                else:
                                    poDetail.specialValue = 'N/A'
                                
                                    pod_list.append(poDetail)
                            elif k.startswith("sp_content_part_"):
                                spv_value=JCPSPVDetail(header=spv_header, value=v)
                                
                                spv_values.append(spv_value)

                DBSession.add_all(spv_values)
                DBSession.add_all(pod_list)

            DBSession.add_all(addList)
            DBSession.flush()

            pd_file, filename=self.exportHTPDFile(code=rpacEncrypt(po_header.id), rfid_flag = rfid_flag)
            
            self._construct_email(kw["sendEmailTo"], order, po_header, [filename])
            
            DBSession.commit()
        except:
            file=open('log.txt', 'a')
            traceback.print_exc(None, file)
            file.close()
            DBSession.rollback()
            flash("The service is not avaiable now,please try it later or contact the system administator.", "warn")
        else:
            if False in upcFlag:
                upcSendTo=[request.identity["user"].email_address]
                upcCCTo=config.jcp_upc_mail.split(";")
                mailContent="The order [%s] got some upc/128c error, please contact us!"%order.customerPO
                self._sendNotifyEmail(upcSendTo, upcCCTo, order.customerPO, ph.id, mailContent, [], mailContent)
                flash(mailContent)
            elif len(gtin_length)>1:
                upcSendTo=[request.identity["user"].email_address]
                upcCCTo=config.jcp_upc_mail.split(";")
                mailContent="The order [%s] have more than one upc type, please contact us!"%order.customerPO
                self._sendNotifyEmail(upcSendTo, upcCCTo, order.customerPO, ph.id, mailContent, [], mailContent)
                flash(mailContent)
            else:
                flash("The order has been save successfully!")
        redirect("/order/viewOrder?code=%s"%(rpacEncrypt(po_header.id)))

    @expose()
    def saveCLUpdate(self, **kw):
        DBSession.begin(subtransactions=True)
        try:
            upcFlag=set()
            gtin_length=set()
            ph=DBSession.query(JCPHeaderPO).get(int(kw.get('po_id', '')))
            ph.country=DBSession.query(JCPCountry).get(kw.get('sendEmailTo', ''))
            ph.status='CONFIRM'
            ph.remark=kw.get('remark', '')
            
            if kw.has_key("combo_selection") and kw.get("combo_selection", False) != '':
                ph.combo_order = kw.get("combo_selection", False).split("-")[1]
            
            order=DBSession.query(JCPOrderForm).get(int(kw.get('form_id', '')))
            national_brand=kw.get("national_brand", False) if kw.has_key("national_brand") else None
            pd_list=[]

            fields=["customerPO",
                    "supperliNO",
                      "billAddress",
                      "billAttn",
                      "billTel",
                      "billFax",
                      "shipAddress",
                      "shipAttn",
                      "shipTel",
                      "shipFax",
                      "origin",
                      "rnCode",
                      "wplCode",
                      "cust_item_codes",
                      "shipInstruction"
                      ]
            params={"lastModifyBy" : request.identity["user"],
                      'status'       : 'CONFIRM',
                      }

            this_billto=None
            this_shipto=None

            if int(kw['billCompany'])!=-1 :
                this_billto=DBSession.query(JCPBillTo).get(int(kw['billCompany']))
                params['billCompany']=this_billto.company if this_billto else kw('other_billto', '')
            if int(kw['shipCompany'])!=-1 :
                this_shipto=DBSession.query(JCPShipTo).get(int(kw['shipCompany']))
                params['shipCompany']=this_shipto.company if this_shipto else kw('other_shipto', '')

            for f in fields:
                params[f]=None if f not in fields or not kw[f] else kw[f]
            for key, val in params.iteritems():
                if key in dir(order): setattr(order, key, val)
            add_list=[order, ph]
            DBSession.add_all(add_list)

            fc_json=json.loads(kw.get("fc_infos", "").replace("'", '"')) if len(kw["fc_infos"])>1 else None
            wi_json=json.loads(kw.get("wi_infos", "").replace("'", '"')) if len(kw["wi_infos"])>1 else None
            fc_infos=[]

            for md in ph.details:
                wi_content=''

                if wi_json:
                    for key, val in wi_json.iteritems():
                        if int(key.split('_')[2])==md.id: wi_content=val

                md.retail=kw["retail_%d"%md.id]
                md.quantity=int(kw["quantity_%d"%md.id])
                md.washingInstruction=wi_content if wi_content!='' else md.washingInstruction
                
                if md.upc: upcFlag.add(checkDigit12(md.upc))
                else: upcFlag.add(len(md.gtinCode)==14)
                
                if national_brand is not None: md.stock=national_brand
                
                pd_list.append(md)
                gtin_length.add(len(md.upc))

            DBSession.add_all(pd_list)

            if fc_json:
                fc_header_params={}
                for key, val in fc_json.iteritems():
                    for pd in pd_list:
                        if int(key.split('_')[2])==pd.id:
                            fc_header_params['poDetail']=pd
                            DBSession.delete(pd.fcdetails[0])

                    for k, v in val.iteritems():
                        if k=='exclusive_data': fc_header_params['exclusiveData']=v
                        elif k=='fc_cotton_logo': fc_header_params['cottonLogo']=True if v=='true' else False
                        elif k=='fc_lycra_logo': fc_header_params['lycraLogo']=True if v=='true' else False

                    fc_header=JCPFCInstrHeader(**fc_header_params)
                    DBSession.add(fc_header)

                    fc_details=val['components']

                    for item in fc_details:
                        fc_detail_params={'header'    : fc_header,
                                            'ccName'    : item['cc_name'],
                                            'component' : item['component'],
                                            'color'     : item['color'],
                                            }

                        for index, percent_item in enumerate(item['percent']):
                            fc_detail_params['percentage'+str(index+1)]=percent_item['fc_percentage']
                            fc_detail_params['content'+str(index+1)]=percent_item['fc_content']

                        fc_detail=JCPFCInstrDetail(**fc_detail_params)
                        fc_infos.append(fc_detail)

            DBSession.add_all(fc_infos)

            if kw.get("spv_infos", "") and len(kw.get("spv_infos", ""))>1:
                spv_json=json.loads(kw.get("spv_infos", "").replace("'", '"'))
                spv_values=[]
                pod_list=[]

                for key, val in spv_json.iteritems():
                    poDetail=None

                    for pd in pd_list:
                        if int(key.split('_')[2])==pd.id:
                            poDetail=pd
                            if pd.spvdetails: DBSession.delete(pd.spvdetails[0])

                    if poDetail:
                        spv_header=JCPSPVHeader(poDetail=poDetail)

                        DBSession.add(spv_header)

                        spv_details = dict(item.split('=') for item in val.split('&'))

                        for k, v in spv_details.iteritems():
                            if k.startswith("spv_"):
                                if v.isdigit():
                                    sp_value=DBSession.query(JCPSpecialValue).get(int(v))
                                    spv_value=JCPSPVDetail(header=spv_header, value=sp_value.value, part=sp_value.part)
    
                                    spv_values.append(spv_value)
                                else:
                                    poDetail.specialValue = 'N/A'
                                
                                    pod_list.append(poDetail)
                            elif k.startswith("sp_content_part_"):
                                spv_value=JCPSPVDetail(header=spv_header, value=v)
                                
                                spv_values.append(spv_value)

                DBSession.add_all(spv_values)
                DBSession.add_all(pod_list)

            customer=request.identity["user"].belongToCustomer
            addList = self._set_default_billToShipTo(customer, this_billto, this_shipto, [])

            DBSession.add_all(addList)

            self._construct_email(kw["sendEmailTo"], order, ph, [])
            
            DBSession.commit()
        except:
            file=open('log.txt', 'a')
            traceback.print_exc(None, file)
            file.close()
            DBSession.rollback()
            flash("The service is not avaiable now,please try it later or contact the system administator.", "warn")
        else:
            if False in upcFlag:
                upcSendTo=[request.identity["user"].email_address]
                upcCCTo=config.jcp_upc_mail.split(";")
                mailContent="The order [%s] got some upc/128c error, please contact us!"%order.customerPO
                self._sendNotifyEmail(upcSendTo, upcCCTo, order.customerPO, ph.id, mailContent, [], mailContent)
                flash(mailContent)
            elif len(gtin_length)>1:
                upcSendTo=[request.identity["user"].email_address]
                upcCCTo=config.jcp_upc_mail.split(";")
                mailContent="The order [%s] have more than one upc type, please contact us!"%order.customerPO
                self._sendNotifyEmail(upcSendTo, upcCCTo, order.customerPO, ph.id, mailContent, [], mailContent)
                flash(mailContent)
            else:
                flash("The order has been save successfully!")
            redirect("/order/viewOrder?code=%s"%(rpacEncrypt(ph.id)))

    @expose()
    def exportHTPDFile(self, **kw):
        (flag, id)=rpacDecrypt(kw.get("code", ""))

        if not flag:
            flash("Please don't access the resource illegally!")
            return None
        
        ph=getOr404(JCPHeaderPO, id)
        file_list = []
        order_type_dict = {'1': 2, '2': 1, '3': 1} #if kw.get('rfid_flag', '') and kw["rfid_flag"] == 'True' else {'1': 2, '2': 1, '3': 1}
        current=dt.now()
        dateStr=current.today().strftime("%Y%m%d")
        fileDir=os.path.join(os.path.abspath(os.path.curdir), "report_download", "%s"%dateStr)
        
        if not os.path.exists(fileDir): os.makedirs(fileDir)
        
        for time in range(order_type_dict[ph.combo_order]):
            file_list.append(self._genHTProductionFile(ph, time, kw['rfid_flag']))
        
        pd_zip_file = os.path.join(fileDir, "export_%s%d.zip" % (dt.now().strftime("%Y%m%d%H%M%S"), random.randint(1, 1000)))
        out_zip_file = zipfile.ZipFile(pd_zip_file, "w", zlib.DEFLATED)
        
        for fl in file_list:
            out_zip_file.write(os.path.abspath(str(fl)), os.path.basename(str(fl)))
        out_zip_file.close()
        
        try:
            for fl in file_list:
                os.remove(fl)
        except:
            pass
        
        return (serveFile(unicode(pd_zip_file)), pd_zip_file)
    
    # for rfid, 20120202
    @expose()
    def getEpc(self, **kw):
        (flag, id)=rpacDecrypt(kw.get("code", ""))

        if not flag:
            flash("Please don't access the resource illegally!")
            redirect(request.identity["user"].default_url)

        detail = getOr404(JCPDetailPO, id)

        if detail.active==1:
            flash("The item has been canceled!", "warn")
            redirect(request.identity["user"].default_url)
        if not detail.upc:
            flash("The UPC is null!", "warn")
            redirect(request.identity["user"].default_url)

        # epc already done
        if detail.epcBegin and detail.epcEnd and detail.epcCodeBegin and detail.epcCodeEnd:
            epcFile = genProducionFile(detail.upc, detail.epcBegin, int(detail.quantity))
            if not epcFile:
                flash("The service is not available now ,please try it later.")
                redirect('/order/viewOrder?code=%s'%rpacEncrypt(detail.header.id))
            else:
                return serveFile(epcFile)
        DBSession.begin(subtransactions=True)
        try:
            myLock.acquire()
            upcObj = DBSession.query(JCPUpc).with_lockmode('update').filter(
                                        and_(JCPUpc.upc==detail.upc, JCPUpc.active==0)).first()
            if upcObj:
                beginNo = upcObj.lastQty + 1
                endNo = upcObj.lastQty  + int(detail.quantity)
                epcCodeStart = returnEPC(beginNo, upcObj.upc, 1)[0]
                epcCodeEnd = returnEPC(endNo, upcObj.upc, 1)[0]
                upcObj.lastQty += int(detail.quantity)
                detail.epcBegin = beginNo
                detail.epcEnd = endNo
                detail.epcCodeBegin = epcCodeStart
                detail.epcCodeEnd = epcCodeEnd
            else:
                upcObj = JCPUpc()
                upcObj.upc = detail.upc
                upcObj.lastQty = int(detail.quantity)
                beginNo = 1
                endNo = upcObj.lastQty
                epcCodeStart = returnEPC(beginNo, upcObj.upc, 1)[0]
                epcCodeEnd = returnEPC(endNo, upcObj.upc, 1)[0]
                detail.epcBegin = beginNo
                detail.epcEnd = endNo
                detail.epcCodeBegin = epcCodeStart
                detail.epcCodeEnd = epcCodeEnd
                DBSession.add(upcObj)   
            # download epc
            epcFile = genProducionFile(detail.upc, detail.epcBegin, int(detail.quantity))
            if not epcFile:
                flash("The service is not available now ,please try it later.")
                redirect('/order/viewOrder?code=%s'%rpacEncrypt(detail.header.id))
            else:
                return serveFile(epcFile)
        except:
            traceback.print_exc()
            DBSession.rollback()
            flash("The service is not available now ,please try it later.")
            redirect('/order/viewOrder?code=%s'%rpacEncrypt(detail.header.id))
        finally:
            myLock.release()
    
    @expose()
    def exportRFID(self, **kw):
        DBSession.begin(subtransactions=True)
        try:
            ph=getOr404(JCPHeaderPO, int(kw.get("orderID")))
            send_result = sendRFID(ph, int(kw.get('rfid_country', '')))
            
            if send_result != -1:
                ph.status = 'RFID'
                ph.rfid_id = send_result
                
                DBSession.add(ph)
                
                country = DBSession.query(JCPCountry).get(kw["rfid_country"])
                sendTo=[request.identity["user"].email_address]
                for c in country.contacts: sendTo.append(c.email)
                
                ccTo = config.jcp_email_cc.split(";")
                title = "Order[%s] has transformed to produce successfully!" % ph.orders[0].customerPO
                content="\n".join([
                    "Thank you for your confirmation!",
                    "You could find the detail transformed information via the link below:",
                    "%s"%config.rfid_site_url + str(ph.rfid_id),
                    "\n\n************************************************************************************",
                    "This e-mail is sent by the r-pac JCPenny ordering system automatically.",
                    "Please don't reply this e-mail directly!",
                    "************************************************************************************"
                    ])
                
                self._sendNotifyEmail(sendTo, ccTo, ph.orders[0].customerPO, ph.id, content, [], title)
                
                DBSession.commit()
                flash("The order transformed to RFID production successfully!")
            elif send_result == -1:
                flash("The order hasn't tranformed successfylly!")
        except:
            DBSession.rollback()
            traceback.print_exc()
            flash("The service is not available now ,please try it later.")
        
        redirect('/order/viewOrder?code=%s'%rpacEncrypt(ph.id))
    
    @expose("ordering.templates.order.order_attachment")
    @tabFocus(tab_type="main")
    def viewAttachment(self, id, **kw):
        (flag, id)=rpacDecrypt(id)
        
        if not flag:
            flash("Please don't access the resource illegally!")
            redirect(request.identity["user"].default_url)

        ph=getOr404(JCPHeaderPO, id)
        
        try:
            if not ph.customer_samples: attachments=[]
            else:   attachments=ph.customer_samples
        except:
            traceback.print_exc()
            flash("Error occur on the server side!")
            redirect('/order/viewOrder?code=%s'%rpacEncrypt(detail.header.id))
        return {"poHeader": ph,
                "return_url": request.identity["user"].default_url,
                "attachments": attachments}
    
    @expose()
    def uploadSample(self, **kw):
        try:
            ph=getOr404(JCPHeaderPO, int(kw.get("orderID")))
        except:
            traceback.print_exc()
            flash("The record doesn't exit!")
            raise redirect("/order/index")

        try:
            relativePath=os.path.join("ordering\public\images", "attachment_upload")
            saveName=Date2Text(dateTimeFormat="%Y%m%d%H%M%S" , defaultNow=True)+str(random.randint(1000, 9999))+os.path.splitext(kw["filePath"].filename)[1]
            fileUpload(kw["filePath"], relativePath, saveName)
            u=CustomerSample(name=kw["fileName"], path=os.path.join(relativePath, saveName), issuedBy=request.identity["user"], header=ph)
        except:
            traceback.print_exc()
            flash("Error occur on the server side!")
            raise redirect("/order/viewOrder?code=" + rpacEncrypt(ph.id))
        flash("The file has been uploaded successfully!")
        raise redirect("/order/viewAttachment/%s"%rpacEncrypt(ph.id))

    def _uploadSample(self, ph, fileName, file):
        try:
            relativePath=os.path.join("ordering\public\images", "attachment_upload")
            saveName=Date2Text(dateTimeFormat="%Y%m%d%H%M%S" , defaultNow=True)+str(random.randint(1000, 9999))+os.path.splitext(fileName)[1]
            fileUpload(file, relativePath, saveName)
            u=CustomerSample(name=fileName, path=os.path.join(relativePath, saveName), issuedBy=request.identity["user"], header=ph)
            
            return ('Success', u)
        except:
            traceback.print_exc()
            flash("Error occur on the server side!")
            return ('Fail', None)
    
    @expose()
    def download(self, **kw):
        sample = DBSession.query(CustomerSample).get(kw.get('id', ''))
        pd_zip_file = os.path.join(os.path.dirname(sample.path), "export_%s%d.zip" % (dt.now().strftime("%Y%m%d%H%M%S"), random.randint(1, 1000)))
        out_zip_file = zipfile.ZipFile(pd_zip_file, "w", zlib.DEFLATED)
        
        out_zip_file.write(os.path.abspath(str(sample.path)), os.path.basename(str(sample.path)))
        out_zip_file.close()
        
        return (serveFile(unicode(pd_zip_file)), pd_zip_file)

    def _get_billToShipTo(self, customer):
        billTos=customer.billtos if customer else DBSession.query(JCPBillTo).order_by(JCPBillTo.company).all()
        shipTos=customer.shiptos if customer else DBSession.query(JCPShipTo).order_by(JCPShipTo.company).all()
        
        return (billTos, shipTos)
    
    def _set_default_billToShipTo(self, customer, this_billto, this_shipto, addList):
        last_billto = None
        last_shipto = None
        
        if this_billto:
            if customer:
                for billto in customer.billtos:
                    if billto.is_default == 1: last_billto = billto

            if last_billto and this_billto.is_default != last_billto.is_default:
                this_billto.is_default = 1
                last_billto.is_default = 0
                
                addList.extend([this_billto, last_billto])
            else:
                this_billto.is_default = 1
                
                addList.append(this_billto)

        if this_shipto:
            if customer:
                for shipto in customer.shiptos:
                    if shipto.is_default == 1: last_shipto = shipto

            if last_shipto and  this_shipto.is_default != last_shipto.is_default:
                this_shipto.is_default = 1
                last_shipto.is_default = 0
                
                addList.extend([this_shipto, last_shipto])
            else:
                this_shipto.is_default = 1
                
                addList.append(this_shipto)
            
        return addList
    
    def _construct_email(self, sendEmailTo, order, po_header, attachment):
        sendTo=[request.identity["user"].email_address]
        country = DBSession.query(JCPCountry).get(sendEmailTo)
        
        if country.name in ['Mexico', 'Shanghai', 'US', 'El Salvador', 'Bangladesh', 'India', "Pakistán"]:
            for c in country.contacts:
                if c.status == 0:
                    sendTo.append(c.email)
        elif country.name == 'Honduras':
            country = DBSession.query(JCPCountry).filter(JCPCountry.name == 'El Salvador').one()
            
            for c in country.contacts:
                if c.status == 0:
                    sendTo.append(c.email)
        
        ccTo=config.jcp_email_cc.split(";")
        self._sendNotifyEmail(sendTo, ccTo, order.customerPO, po_header.id, None, attachment)
    
    def _set_specialvalue(self, spv_infos, poDetails):
        spv_json=json.loads(spv_infos.replace("'", '"'))
        spv_values=[]
        pod_list=[]
        
        for key, val in spv_json.iteritems():
            poDetail=None

            for pd in poDetails:
                if key.split('_')[0] not in ['private', 'combo']:
                    if int(key.split('_')[2])==pd.msgDetail.id and pd.type == 'Hangtag': poDetail=pd
                if key.split('_')[0] == 'private':
                    if int(key.split('_')[3])==pd.msgDetail.id and pd.type == 'Sticker': poDetail=pd
                if key.split('_')[0] == 'combo':
                    if int(key.split('_')[3])==pd.msgDetail.id and pd.type == 'Sticker': poDetail=pd

            if poDetail:
                spv_header=JCPSPVHeader(poDetail=poDetail)

                DBSession.add(spv_header)

                spv_details = dict(item.split('=') for item in val.split('&'))

                for k, v in spv_details.iteritems():
                    if k.startswith("spv_"):
                        if v.isdigit():
                            sp_value=DBSession.query(JCPSpecialValue).get(int(v))
                            spv_value=JCPSPVDetail(header=spv_header, value=sp_value.value, part=sp_value.part)

                            spv_values.append(spv_value)
                        else:
                            poDetail.specialValue = 'N/A'
                        
                            pod_list.append(poDetail)
                    elif k.startswith("sp_content_part_"):
                        spv_value=JCPSPVDetail(header=spv_header, value=v)
                        
                        spv_values.append(spv_value)
        
        return (pod_list, spv_values)
