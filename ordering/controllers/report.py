# -*- coding: utf-8 -*-
from datetime import datetime as dt
import traceback, os, sys, random

# turbogears imports
from tg import expose, redirect, validate, flash, request, response
from tg.controllers import CUSTOM_CONTENT_TYPE

# third party imports
from paste.fileapp import FileApp
from pylons.controllers.util import forward
from repoze.what import predicates, authorize
from repoze.what.predicates import not_anonymous, in_group, has_permission

# project specific imports
from ordering.lib.base import BaseController
from ordering.model import *
from ordering.util.common import *
from ordering.util.excel_helper import *
from ordering.widgets.order import *

__all__=['ReportController']

class ReportController(BaseController):
    #Uncomment this line if your controller requires an authenticated user
    allow_only=authorize.not_anonymous()
#    allow_only=check_anonymous()

    @expose('ordering.templates.report.index')
    @tabFocus(tab_type="report")
    def index(self):
        try:
            report_form=order_report

            return dict(report_form=report_form, values={})
        except:
            traceback.print_exc()

    @expose()
    def export(self, **kw):
        result_data=[]
        additionInfo=[]
        current=dt.now()
        dateStr=current.today().strftime("%Y%m%d")
        fileDir=os.path.join(os.path.abspath(os.path.curdir), "report_download", "%s"%dateStr)

        if not os.path.exists(fileDir): os.makedirs(fileDir)

        timeStr=current.time().strftime("%H%M%S")
        rn=random.randint(0, 10000)
        username=request.identity['repoze.who.userid']
        filename=os.path.join(fileDir, "%s_%s_%d.xls"%(username, timeStr, rn))
        templatePath=os.path.join(os.path.abspath(os.path.curdir), "report_download/TEMPLATE/JCP_TEMPLATE.xls")
        pe=JCPExcel(templatePath=templatePath, destinationPath=filename)

        query_fields={"orderDate": "Order Date",
                        "customerPO": "PO Number",
                        "tel": "Tel",
                        "requestShipDate": "Request Ship Date",
                        "shipMethod": "Ship Method",
                        "billCompany": "Bill Company",
                        "billAddress": "Bill Address",
                        "billAttn": "Bill Attn",
                        "billTel": "Bill Tel",
                        "billFax": "Bill Fax",
                        "shipCompany": "Ship Company",
                        "shipAddress": "Ship Address",
                        "shipAttn": "Ship Attn",
                        "shipTel": "Ship Tel",
                        "shipFax": "Ship Fax",
                        "brandStyle": "Brand Style",
                        "itemCode": "Item Code",
                        "itemDescription": "Item Description",
                        "careInstr": "Care Instr",
                        "fabricContent": "Fabric Content",
                        "origin": "Origin",
                        "supplier": "Supplier",
                        "rnCode": "RN Code",
                        "wplCode": "WPL Code",
                        "specialInstr": "Special Instr",
                        #"labelCode": "Label System",
                        }

        if kw:
            for k, v in kw.iteritems():
                if kw[k]:
                    additionItem=query_fields[k]+": "+kw[k]
                    additionInfo.append(additionItem)

        try:
            results=self._query_result(**kw)

            if results:
                for result in results:
                        result_data.append(self._format_value(result))

            pe.inputData(additionInfo=additionInfo, data=result_data)
            pe.outputData()

            return serveFile(unicode(filename))
        except:
            traceback.print_exc()
            if pe: pe.clearData()
            flash("Error occur in the Excel Exporting !")
            raise redirect("report")

    def _format_value(self, jcp_form):
        fields=['header', 'orderDate', 'customerPO',
                  'billCompany', 'billAddress',
                  'billAttn', 'billTel', 'billFax', 'billEmail',
                  'shipCompany', 'shipAddress', 'shipAttn', 'shipTel',
                  'shipFax', 'shipEmail',
                  'origin',
                  'rnCode', 'wplCode', 'specialInstr', #'labelCode'
                  ]
        results=[]

#        for index, attr in enumerate(fields):
        for attr in fields:
            result=getattr(jcp_form, attr)

            if isinstance(result, basestring): result=result.decode("utf8")
            elif isinstance(result, dt): result=Date2Text(result).decode("utf8")
            elif isinstance(result, JCPHeaderPO): result=jcp_form.header.poNo
            
#            results.append(jcp_form[index])
            results.append(result)

        return results

    def _query_result(self, **kw):
        try:
            conditions=[]

            if kw.get("orderDate", False):
                date=dt.strptime(kw.get("orderDate", '2009-12-1200:00:00')+"00:00:00", "%Y-%m-%d%H:%M:%S")
                conditions.append(JCPOrderForm.orderDate>=date)
            if kw.get("customerPO", False):
                conditions.append(JCPOrderForm.customerPO.like("%%%s%%"%kw.get("customerPO", "")))
            if kw.get("labelCode", False):
                conditions.append(JCPOrderForm.labelCode.like("%%%s%%"%kw.get("labelCode", "")))
            if kw.get("tel", False):
                conditions.append(JCPOrderForm.tel.like("%%%s%%"%kw.get("tel", "")))
            if kw.get("requestShipDate", False):
                date=dt.strptime(kw.get("requestShipDate", '2009-12-1200:00:00')+"23:59:59", "%Y-%m-%d%H:%M:%S")
                conditions.append(JCPOrderForm.requestShipDate==date)
            if kw.get("shipMethod", False):
                conditions.append(JCPOrderForm.shipMethod.like("%%%s%%"%kw.get("shipMethod", "")))
            if kw.get("billCompany", False):
                conditions.append(JCPOrderForm.billCompany.like("%%%s%%"%kw.get("billCompany", "")))
            if kw.get("billAddress", False):
                conditions.append(JCPOrderForm.billAddress.like("%%%s%%"%kw.get("billAddress", "")))
            if kw.get("billAttn", False):
                conditions.append(JCPOrderForm.billAttn.like("%%%s%%"%kw.get("billAttn", "")))
            if kw.get("billTel", False):
                conditions.append(JCPOrderForm.billTel.like("%%%s%%"%kw.get("billTel", "")))
            if kw.get("billFax", False):
                conditions.append(JCPOrderForm.billFax.like("%%%s%%"%kw.get("billFax", "")))
            if kw.get("shipCompany", False):
                conditions.append(JCPOrderForm.shipCompany.like("%%%s%%"%kw.get("shipCompany", "")))
            if kw.get("shipAddress", False):
                conditions.append(JCPOrderForm.shipAddress.like("%%%s%%"%kw.get("shipAddress", "")))
            if kw.get("shipAttn", False):
                conditions.append(JCPOrderForm.shipAttn.like("%%%s%%"%kw.get("shipAttn", "")))
            if kw.get("shipTel", False):
                conditions.append(JCPOrderForm.shipTel.like("%%%s%%"%kw.get("shipTel", "")))
            if kw.get("shipFax", False):
                conditions.append(JCPOrderForm.shipFax.like("%%%s%%"%kw.get("shipFax", "")))
            if kw.get("brandStyle", False):
                conditions.append(JCPOrderForm.brandStyle.like("%%%s%%"%kw.get("brandStyle", "")))
            if kw.get("itemCode", False):
                conditions.append(JCPOrderForm.itemCodeid==JCPItemCodeMaster.id)
                conditions.append(JCPItemCodeMaster.id==kw.get("itemCode", ""))
            if kw.get("itemDescription", False):
                conditions.append(JCPOrderForm.itemDescription.like("%%%s%%"%kw.get("itemDescription", "")))
            if kw.get("careInstr", False):
                conditions.append(JCPOrderForm.careInstr.like("%%%s%%"%kw.get("careInstr", "")))
            if kw.get("fabricContent", False):
                conditions.append(JCPOrderForm.fabricContent.like("%%%s%%"%kw.get("fabricContent", "")))
            if kw.get("origin", False):
                conditions.append(JCPOrderForm.origin.like("%%%s%%"%kw.get("origin", "")))
            if kw.get("supplier", False):
                conditions.append(JCPOrderForm.supplier.like("%%%s%%"%kw.get("supplier", "")))
            if kw.get("rnCode", False):
                conditions.append(JCPOrderForm.rnCode.like("%%%s%%"%kw.get("rnCode", "")))
            if kw.get("wplCode", False):
                conditions.append(JCPOrderForm.wplCode.like("%%%s%%"%kw.get("wplCode", "")))
            if kw.get("specialInstr", False):
                conditions.append(JCPOrderForm.specialInstr.like("%%%s%%"%kw.get("specialInstr", "")))

            if not authorize.has_permission('VIEW_FULL_ORDER') and request.identity["user"].belong_to_customer_id:
                conditions.append(JCPOrderForm.headerId==JCPHeaderPO.id)
                conditions.append(JCPHeaderPO.customer_id==request.identity["user"].belong_to_customer_id)

            if len(conditions):
                obj=DBSession.query(JCPOrderForm)

                for condition in conditions: obj=obj.filter(condition)

                result=obj.filter(JCPOrderForm.active==0).all()
            else:
                result=DBSession.query(JCPOrderForm).filter(JCPOrderForm.active==0).all()
#                conn = DBSession.connection()
#                
#                result = conn.execute("""select header.po_no,
#                       form.order_date,
#                       form.po_no,
#                       form.bill_company,
#                       form.bill_address,
#                       form.bill_attn,
#                       form.bill_tel,
#                       form.bill_fax,
#                       form.bill_email,
#                       form.ship_company,
#                       form.ship_address,
#                       form.ship_attn,
#                       form.ship_tel,
#                       form.ship_fax,
#                       form.ship_email,
#                       sum(detail.quantity),
#                       detail.sub,
#                       detail.lot,
#                       detail.stock
#                  from jcp_header_po header,
#                       jcp_detail_po detail,
#                       jcp_order_form form
#                 where header.active = 0
#                   and header.order_type = 'AUTO'
#                   and header.combo_order in ('2', '3')
#                   and header.id = form.header_id
#                   and header.id = detail.header_id
#                   and header.po_date > '2013-1-1 00:00:00'
#                   and header.po_date < '2013-6-1 00:00:00'
#                 group by detail.sub,
#                       detail.lot,
#                       detail.stock,
#                       header.po_no,
#                       form.order_date,
#                       form.po_no,
#                       form.bill_company,
#                       form.bill_address,
#                       form.bill_attn,
#                       form.bill_tel,
#                       form.bill_fax,
#                       form.bill_email,
#                       form.ship_company,
#                       form.ship_address,
#                       form.ship_attn,
#                       form.ship_tel,
#                       form.ship_fax,
#                       form.ship_email
#                 order by form.order_date""")

#            print '*' * 20, '\n', dir(result[0])
            
            return result
        except:
            traceback.print_exc()
