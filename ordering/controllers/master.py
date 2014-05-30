# -*- coding: utf-8 -*-
from datetime import datetime as dt
import copy
import random
import os
import traceback

from tg import redirect, flash, expose, request, override_template
from tg.decorators import paginate

from ordering.controllers.basicMaster import *
from ordering.model import *
from ordering.util.common import *
from ordering.util.excel_helper import *
from ordering.widgets.master import *

__all__=["CountryController", "ContactController", "BillToController", "ShipToController",
           "CountryCodeController", "ItemInfoController", "CustomerController", "SpecialValueController",
           "RFIDMappingController", "ComboMappingInfoController"]

#class ItemCodeController(BasicMasterController):
#    url = "itemcode"
#    template = "ordering.templates.masters.index"
#    dbObj  = JCPItemCodeMaster
#    searchWidget = itemCodeSearchFormInstance
#    updateWidget = itemCodeUpdateFormInstance
#    formFields = ["name","description"]


class CountryController(BasicMasterController):
    url="country"
    dbObj=JCPCountry
    template="ordering.templates.masters.index_country"
    searchWidget=countrySearchFormInstance
    updateWidget=countryUpdateFormInstance
    formFields=["name", "phone"]


class ContactController(BasicMasterController):
    url="contact"
    dbObj=JCPContact
    template="ordering.templates.masters.index_contact"
    searchWidget=contactSearchFormInstance
    updateWidget=contactUpdateFormInstance
    formFields=["name", "email", "countryId"]

class BillToController(BasicMasterController):
    url="billto"
    dbObj=JCPBillTo
    template="ordering.templates.masters.index_billto"
    searchWidget=billToSearchFormInstance
    updateWidget=billToUpdateFormInstance
    formFields=["customer_id", "company", "address", "attn", "tel", "fax", "email"]

    def beforeSaveNew(self, kw, params):
        params['is_default']=1
        return params

class ShipToController(BasicMasterController):
    url="shipto"
    dbObj=JCPShipTo
    template="ordering.templates.masters.index_shipto"
    searchWidget=shipToSearchFormInstance
    updateWidget=shipToUpdateFormInstance
    formFields=["customer_id", "company", "address", "attn", "tel", "fax", "email"]

    def beforeSaveNew(self, kw, params):
        params['is_default']=1
        return params

class CountryCodeController(BasicMasterController):
    url="countrycode"
    dbObj=JCPCountryCode
    template="ordering.templates.masters.index_countrycode"
    searchWidget=countryCodeSearchFormInstance
    updateWidget=countryCodeUpdateFormInstance
    formFields=["countryName", "countryCode"]

class ItemInfoController(BasicMasterController):
    url="iteminfo"
    dbObj=JCPItemInfo
    template="ordering.templates.masters.index_iteminfo"
    searchWidget=itemInfoSearchFormInstance
    updateWidget=itemInfoUpdateFormInstance
    formFields=["item_code",
                "item_type",
                "packaging_code",
                "combo_packaging_code",
                "combo_item",
                "combo_mapping",
                "washing_instruction",
                "fiber_content",
                "country_of_origin",
                "special_value",
                "multi_special_value",
                "path",
                "status",
                "hangtang_pkg_code",
                "label_pkg_code",
                ]

    @expose('ordering.templates.masters.index_iteminfo')
    @paginate("result", items_per_page=20)
    @tabFocus(tab_type="master")
    def index(self, **kw):
        if not kw:
            result=DBSession.query(self.dbObj).all()
        else:
            result=self.searchMaster(kw)
        return {
                "searchWidget" : self.searchWidget,
                "result" : result,
                "funcURL" :self.url,
                "values" : kw,
                }

    def beforeSaveNew(self, kw, params):
        version=JCPItemInfo.get_max_version(pkg_code=params['packaging_code'])
        print version
        params['version']=int(version)+1 if version else 1
        return params

    def beforeSaveUpdate(self, kw, params):
        version=JCPItemInfo.get_max_version(pkg_code=params['packaging_code'])
        params['version']=int(version) if version else 1
        return params
    
    @expose('ordering.templates.masters.item_form')
    @tabFocus(tab_type="master")
    def add(self, **kw):
        return {
                "widget" : self.updateWidget,
                "values" : {},
                "saveURL" : "/%s/saveNew"%self.url,
                "funcURL" :self.url
                }
    
    @expose()
    def upload(self, **kw):
        try:
            relativePath = os.path.join("ordering/public/images","jcpenney")
            fileUpload(kw['item_artwork_files'], relativePath, kw['item_artwork_name'])
        except:
            logfile = open("log.txt", "w")
            traceback.print_exc(None, logfile)
            logfile.close()
    
    @expose()
    def saveNew(self, **kw):
        params = {"issuedBy": request.identity["user"],
                  "lastModifyBy": request.identity["user"],
                  "lastModifyTime": dt.now()
                  }
        combo_mapping_params = {"issuedBy": request.identity["user"],
                                "lastModifyBy": request.identity["user"],
                                "lastModifyTime": dt.now()
                                }
        combo_mapping_fields = ["hangtang_pkg_code",
                                "label_pkg_code",
                                ]
        
        combo_mapping_flag = False

        for f in self.formFields:
            if f in kw.keys() and f not in combo_mapping_fields:
                params[f]=kw[f]
            if f in kw.keys() and len(kw[f]) > 0 and f in combo_mapping_fields:
                combo_mapping_params[f] = kw[f]
                combo_mapping_flag = True
        
        if params['combo_item'] == 'False':
            params.pop('combo_packaging_code')

        item = JCPItemInfo(**params)
        
        if combo_mapping_flag == True:
            combo_mapping = JCPComboMappingInfo(**combo_mapping_params)
            combo_mapping.main_pkg_code = item.packaging_code

            DBSession.add_all([item, combo_mapping])
        else:
            DBSession.add(item)
        flash("Save the new master successfully!")
        redirect("/%s/index"%self.url)
    
    @expose('ordering.templates.masters.item_form')
    @tabFocus(tab_type="master")
    def update(self, **kw):
        obj=getOr404(self.dbObj, kw["id"], "/%s/index"%self.url)
        combo_mapping_obj = JCPComboMappingInfo.get_by_main_code(obj.packaging_code)
        values={}
        combo_mapping_fields = ["hangtang_pkg_code",
                                "label_pkg_code",
                                ]
        
        for f in self.formFields:
            if f not in combo_mapping_fields: values[f]=getattr(obj, f)
            if f in combo_mapping_fields and len(combo_mapping_obj) > 0:
                values[f] = getattr(combo_mapping_obj[0], f)

        return {
                "widget" : self.updateWidget,
                "values" : values,
                "saveURL" : "/%s/saveUpdate?id=%d"%(self.url, obj.id),
                "funcURL" :self.url
                }

    @expose()
    def saveUpdate(self, **kw):
        obj=getOr404(JCPItemInfo, kw["id"], "/%s/index"%self.url)
        combo_mapping_obj = JCPComboMappingInfo.get_by_main_code(obj.packaging_code)
        params = {"lastModifyBy": request.identity["user"],
                  "lastModifyTime": dt.now()
                  }
        combo_mapping_params = {"lastModifyBy": request.identity["user"],
                                "lastModifyTime": dt.now()
                                }
        combo_mapping_fields = ["hangtang_pkg_code",
                                "label_pkg_code",
                                ]
        combo_mapping_flag = False
        
        for f in self.formFields:
            if f in kw.keys() and f not in combo_mapping_fields:
                params[f]=kw[f]
            if f in kw.keys() and len(kw[f]) > 0 and f in combo_mapping_fields:
                combo_mapping_params[f] = kw[f]
                combo_mapping_flag = True

        if params['combo_item'] == 'False':
            params.pop('combo_packaging_code')
        
        for k in params: setattr(obj, k, params[k])
        if combo_mapping_flag == True:
            for key in combo_mapping_params: setattr(combo_mapping_obj[0], key, combo_mapping_params[key])
#       obj.set(**params)
        flash("Update the master successfully!")
        redirect("/%s/index"%self.url)
    
    @expose()
    def export(self, **kw):
        result_data=[]
        current=dt.now()
        dateStr=current.today().strftime("%Y%m%d")
        fileDir=os.path.join(os.path.abspath(os.path.curdir), "report_download", "%s"%dateStr)

        if not os.path.exists(fileDir): os.makedirs(fileDir)

        timeStr=current.time().strftime("%H%M%S")
        rn=random.randint(0, 10000)
        username=request.identity['repoze.who.userid']
        filename=os.path.join(fileDir, "%s_%s_%d.xls"%(username, timeStr, rn))
        templatePath=os.path.join(os.path.abspath(os.path.curdir), "report_download/TEMPLATE/JCP_ITEM_TEMPLATE.xls")
        pe=JCPExcel(templatePath=templatePath, destinationPath=filename)

        try:
            results=self.searchMaster(kw)

            if results:
                for result in results:
                        result_data.append(self._format_value(result))

            pe.inputData(additionInfo=[], data=result_data)
            pe.outputData()

            return serveFile(unicode(filename))
        except:
            traceback.print_exc()
            if pe: pe.clearData()
            flash("Error occur in the Excel Exporting !")
            raise redirect("report")

    def _format_value(self, jcp_item):
        fields=['item_code', 'packaging_code', 'status', 'washing_instruction',
                'fiber_content', 'country_of_origin',  'combo_item', 'combo_packaging_code',
                'combo_mapping', 'special_value', 'multi_special_value', 
                ]
        results=[]

#        for index, attr in enumerate(fields):
        for attr in fields:
            result=getattr(jcp_item, attr)

            if isinstance(result, basestring): result=result.decode("utf8")
            elif isinstance(result, dt): result=Date2Text(result).decode("utf8")
            elif isinstance(result, bool): result=str(result)
            elif attr == 'status': result = 'Active' if result == 0 else 'Inactive'
            
#            results.append(jcp_form[index])
            results.append(result)
        
        if len(jcp_item.combo_mappings) > 0:
            results.insert(-2, jcp_item.combo_mappings[0].hangtang_pkg_code)
            results.insert(-2, jcp_item.combo_mappings[0].label_pkg_code)
        else:
            for idx in range(2): results.insert(-2, '')
        return results
    
    def searchMaster(self, kw):
        try:
            conditions=[]
            combo_mapping_ids = None
            hangtang_ids = None
            label_ids = None

            if kw.get("item_type", False):
                if int(kw.get("item_type", "")) != 0:
                    conditions.append(JCPItemInfo.item_type == int(kw.get("item_type", "")))
            if kw.get("item_code", False):
                conditions.append(JCPItemInfo.item_code.op("ILIKE")("%%%s%%" % kw.get("item_code", "").strip()))
            if kw.get("packaging_code", False):
                conditions.append(JCPItemInfo.packaging_code.op("ILIKE")("%%%s%%" % kw.get("packaging_code", "").strip()))
            if kw.get("path", False):
                conditions.append(JCPItemInfo.path.op("ILIKE")("%%%s%%" % kw.get("path", "").strip()))
            if kw.get("status", False):
                if int(kw.get("status", "")) != 2:
                    conditions.append(JCPItemInfo.status == int(kw.get("status", "")))
            if kw.get("washing_instruction", False):
                conditions.append(JCPItemInfo.washing_instruction == kw.get("washing_instruction", ""))
            if kw.get("fiber_content", False):
                conditions.append(JCPItemInfo.fiber_content == kw.get("fiber_content", ""))
            if kw.get("combo_item", False):
                conditions.append(JCPItemInfo.combo_item == kw.get("combo_item", ""))
            if kw.get("combo_packaging_code", False):
                conditions.append(JCPItemInfo.combo_packaging_code.op("ILIKE")("%%%s%%" % kw.get("combo_item", "").strip()))
            if kw.get("combo_mapping", False):
                conditions.append(JCPItemInfo.combo_mapping == kw.get("combo_mapping", ""))
            if kw.get("special_value", False):
                conditions.append(JCPItemInfo.special_value == kw.get("special_value", ""))
            if kw.get("multi_special_value", False):
                if int(kw.get("multi_special_value", False)) != -1:
                    conditions.append(JCPItemInfo.multi_special_value == int(kw.get("multi_special_value", "")))
            if kw.get("country_of_origin", False):
                conditions.append(JCPItemInfo.country_of_origin == kw.get("country_of_origin", ""))
            if kw.get("hangtang_pkg_code", False):
                hangtag_ids = DBSession.query(JCPComboMappingInfo.itemId) \
                                .filter(JCPComboMappingInfo.hangtang_pkg_code.op('ILIKE')("%%%s%%"%kw.get("hangtang_pkg_code", "").strip())) \
                                .all()
                combo_mapping_ids = hangtag_ids
            if kw.get("label_pkg_code", False):
                label_ids = DBSession.query(JCPComboMappingInfo.itemId) \
                                .filter(JCPComboMappingInfo.label_pkg_code.op('ILIKE')("%%%s%%"%kw.get("label_pkg_code", "").strip())) \
                                .all()
                combo_mapping_ids = label_ids
            
            if combo_mapping_ids is not None and hangtag_ids is not None:
                combo_mapping_ids = list(set(combo_mapping_ids) & set(hangtag_ids))
            if combo_mapping_ids is not None and label_ids is not None:
                combo_mapping_ids = list(set(combo_mapping_ids) & set(label_ids))
            
            obj=DBSession.query(JCPItemInfo)
            
            if len(conditions):
                for condition in conditions: obj=obj.filter(condition)
                
                if combo_mapping_ids is not None:
                    result = obj.filter(JCPItemInfo.id.in_([id[0] for id in combo_mapping_ids])) \
                                .order_by(JCPItemInfo.item_code).all()
                else:
                    result=obj.order_by(JCPItemInfo.item_code).all()
            else:
                if combo_mapping_ids is not None:
                    result = obj.filter(JCPItemInfo.id.in_([id[0] for id in combo_mapping_ids])) \
                                .order_by(JCPItemInfo.item_code).all()
                else:
                    result=DBSession.query(JCPItemInfo) \
                             .order_by(JCPItemInfo.item_code) \
                             .all()

            return result
        except:
            traceback.print_exc()

class CustomerController(BasicMasterController):
    url="customer"
    dbObj=JCPCustomer
    template="ordering.templates.masters.index_customer"
    searchWidget=customerSearchFormInstance
    updateWidget=customerUpdateFormInstance
    formFields=["name"]

class RFIDMappingController(BasicMasterController):
    url="rfidmapping"
    dbObj=JCPRFIDMappingCode
    template="ordering.templates.masters.index_rfidmappingcode"
    searchWidget=rfidMappingCodeSearchFormInstance
    updateWidget=rfidMappingCodeUpdateFormInstance
    formFields=["sub", "stock", "rfid", "active",]

class SpecialValueController(BasicMasterController):
    url="specialvalue"
    dbObj=JCPSpecialValue
    template="ordering.templates.masters.index_specialvalue"
    searchWidget=specialValueSearchFormInstance
    updateWidget=sepcialValueUpdateFormInstance
    formFields=["item_id", "value", "part", "path"]

    @expose('ordering.templates.masters.index_specialvalue')
    @paginate("result", items_per_page=20)
    @tabFocus(tab_type="master")
    def index(self, **kw):
        if not kw:
            result=DBSession.query(self.dbObj).filter(self.dbObj.status == 0).all()
        else:
            result=self.searchMaster(kw)
        return {
                "searchWidget" : self.searchWidget,
                "result" : result,
                "funcURL" :self.url,
                "values" : kw,
                }
        
    def searchMaster(self, kw):
        try:
            conditions=[]

            if kw.get("item_id", False):
                conditions.append(JCPSpecialValue.items.any(JCPItemInfo.item_code.op("ILIKE")("%%%s%%"%kw.get("item_id"))))
            if kw.get("value", False):
                conditions.append(JCPSpecialValue.value.like("%s"%kw.get("value", False)))
            if kw.get("part", False):
                if int(kw.get("part", False)) != -1:
                    conditions.append(JCPSpecialValue.part=="%d"%int(kw.get("part", False)))
            if kw.get("path", False):
                conditions.append(JCPSpecialValue.path.like("%s"%kw.get("path", False)))

            if len(conditions):
                obj=DBSession.query(JCPSpecialValue)

                for condition in conditions: obj=obj.filter(condition)

                result=obj.filter(self.dbObj.status == 0).all()
            else:
                result=DBSession.query(JCPSpecialValue).filter(self.dbObj.status == 0).all()

            return result
        except:
            traceback.print_exc()

    @expose('ordering.templates.masters.specialvalue_form')
    @tabFocus(tab_type="master")
    def add(self, **kw):
        return {
                "widget" : self.updateWidget,
                "values" : {},
                "saveURL" : "/%s/saveNew"%self.url,
                "funcURL" :self.url
                }

    @expose()
    def saveNew(self, **kw):
        params={"issuedBy":request.identity["user"], "lastModifyBy":request.identity["user"], "lastModifyTime":dt.now()}

        for f in self.formFields:
            if f in kw and f!='item_id' : params[f]=kw[f]

        special_value_obj=JCPSpecialValue(**params)

        if kw.get("item_id", False):
            item_obj=DBSession.query(JCPItemInfo).filter(JCPItemInfo.item_code=="%s"%kw.get("item_id", False)).one()
            special_value_obj.items.append(item_obj)

        DBSession.add(special_value_obj)
        flash("Save the new master successfully!")
        redirect("/%s/index"%self.url)

    @expose('ordering.templates.masters.specialvalue_form')
    @tabFocus(tab_type="master")
    def update(self, **kw):
        obj=getOr404(self.dbObj, kw["id"], "/%s/index"%self.url)
        values={}
        for f in self.formFields :
            if f!='item_id': values[f]=getattr(obj, f)

        return {
                "widget" : self.updateWidget,
                "values" : values,
                "saveURL" : "/%s/saveUpdate?id=%d"%(self.url, obj.id),
                "funcURL" :self.url
                }

    @expose()
    def saveUpdate(self, **kw):
        obj=getOr404(JCPSpecialValue, kw["id"], "/%s/index"%self.url)
        params={"lastModifyBy":request.identity["user"], "lastModifyTime":dt.now()}
        for f in self.formFields:
            if f in kw and f!='item_id' : params[f]=kw[f] if kw[f] else None

        for k in params : setattr(obj, k, params[k])
        if kw.get("item_id", False):
            item_obj=DBSession.query(JCPItemInfo).filter(JCPItemInfo.item_code=="%s"%kw.get("item_id", False)).one()
            obj.items.append(item_obj)
#       obj.set(**params)
        flash("Update the master successfully!")
        redirect("/%s/index"%self.url)
    
    @expose()
    def export(self, **kw):
        result_data=[]
        current=dt.now()
        dateStr=current.today().strftime("%Y%m%d")
        fileDir=os.path.join(os.path.abspath(os.path.curdir), "report_download", "%s"%dateStr)

        if not os.path.exists(fileDir): os.makedirs(fileDir)

        timeStr=current.time().strftime("%H%M%S")
        rn=random.randint(0, 10000)
        username=request.identity['repoze.who.userid']
        filename=os.path.join(fileDir, "%s_%s_%d.xls"%(username, timeStr, rn))
        templatePath=os.path.join(os.path.abspath(os.path.curdir), "report_download/TEMPLATE/JCP_SPECIAL_VALUE_TEMPLATE.xls")
        pe=JCPExcel(templatePath=templatePath, destinationPath=filename)

        try:
            results=self.searchMaster(kw)

            if results:
                for result in results:
                        result_data.append(self._format_value(result))

            pe.inputData(additionInfo=[], data=result_data)
            pe.outputData()

            return serveFile(unicode(filename))
        except:
            traceback.print_exc()
            if pe: pe.clearData()
            flash("Error occur in the Excel Exporting !")
            raise redirect("report")

    def _format_value(self, special_value):
        fields=['part', 'value', 'path',]
        results=[]

#        for index, attr in enumerate(fields):
        for attr in fields:
            result=getattr(special_value, attr)

            if isinstance(result, basestring): result=result.decode("utf8")
#            elif isinstance(result, dt): result=Date2Text(result).decode("utf8")
#            elif isinstance(result, bool): result=str(result)
#            elif attr == 'status': result = 'Active' if result == 0 else 'Inactive'
            
#            results.append(jcp_form[index])
            results.append(result)
        
        if len(special_value.items) > 0:
            results.insert(0, special_value.items[0].packaging_code)
            results.insert(0, special_value.items[0].item_code)
        else:
            for idx in range(2): results.insert(0, '')
        return results
    
    @expose()
    def upload(self, filename, file, **kw):
        try:
            relativePath = os.path.join("ordering/public/images","specialValueImg")
            
            fileUpload(file, relativePath, filename)
        except:
            logfile = open("log.txt", "w")
            traceback.print_exc(None, logfile)
            logfile.close()

    @expose()
    def delete(self, **kw):
        obj=getOr404(self.dbObj, kw["id"], "/%s/index"%self.url)
        obj.lastModifyBy=request.identity["user"]
        obj.lastModifyTime=dt.now()
        obj.status=1

        item_obj=DBSession.query(JCPItemInfo).filter(JCPItemInfo.id=="%d"%int(kw.get("item_id", False))).one()
        if item_obj in obj.items: obj.items.remove(item_obj)

        flash("Delete the master successfully!")
        redirect("/%s/index"%self.url)

class ComboMappingInfoController(BasicMasterController):
    url="combomapping"
    dbObj=JCPComboMappingInfo
    template="ordering.templates.masters.index_combomappinginfo"
    searchWidget=comboMappingInfoSearchFormInstance
    updateWidget=comboMappingInfoUpdateFormInstance
    formFields=["main_pkg_code",
                "hangtang_pkg_code",
                "label_pkg_code",
                ]
