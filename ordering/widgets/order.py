# -*- coding: utf-8 -*-
from ordering.model import *
from ordering.model.jcpenny import *
from ordering.widgets.components import *

__all__ = ["order_search_form", "order_header_info", "order_detail_info", "order_report",
           "sub_search_form", "order_view_form"]

class OrderSearchForm(RPACForm):
    fields = [RPACAjaxText("poNo", label_text="JCP POM#")]

order_search_form = OrderSearchForm()

class SubSearchForm(RPACForm):
    fields = [RPACAjaxText("sub", label_text="JCP Sub#"),
              RPACText("lot", label_text="JCP lot#"), ]

sub_search_form = SubSearchForm()

class OrderViewForm(RPACForm):
    Countryoptions=DBSession.query(JCPCountry.id, JCPCountry.name).all()
    options=[]
    for v in Countryoptions:
        options.append((unicode(v[0]), unicode(v[1])))
    options.append(("", ""))
    options.reverse()
    
    fields = [RPACSearchText("poNo", label_text="POM#"),
              RPACSearchText("customerPO", label_text="Customer PO#"),
              RPACSelect("countryId", label_text="Country", options=options),
              RPACSearchText("sub", label_text="SUB#"),
              RPACSearchText("lot", label_text="LOT#"),
              RPACCalendarPicker("poStartDate", label_text="PO Date(from)"),
              RPACCalendarPicker("poEndDate", label_text="PO Date(to)")]

order_view_form = OrderViewForm()

class OrderHeaderDisplay(RPACDesplay):
    fields = [RPACText("poNo", label_text="JCP POM#"),
              RPACText("stock", label_text="Stock#"),
              RPACText("sub", label_text="JCP Sub#"),
              RPACText("lot", label_text="JCP lot#"),
              RPACText("lotDescription", label_text="Lot Description"),
              RPACText("line", label_text="Line"),
              RPACText("fiberContent", label_text="Fiber Content"),
              RPACText("washCode", label_text="Wash Code"),
              RPACText("Cat", label_text="Cat"),
              RPACText("poDate", label_text="PO Date"),
              RPACText("importDate", label_text="Import Date")]

order_header_info = OrderHeaderDisplay()

class OrderDetailDisplay(RPACDesplay):
    template = "ordering.templates.widgets.order_detail"
    
    fields = [RPACText("colorCode", label_text="Color Code"),
              RPACText("sizeCode", label_text="Size Code"),
              RPACText("size", label_text="Size"),
              RPACText("upc", label_text="UPC"),
              RPACText("styleNo", label_text="Style Number"),
              RPACText("retail", label_text="Retail"),
              RPACText("quantity", label_text="Quantity")]

order_detail_info = OrderDetailDisplay()

class OrderReportForm(RPACForm):
    fields = [RPACCalendarPicker("orderDate", label_text="Order Date"),
              RPACText("customerPO", label_text="Customer PO#"),
              RPACText("billCompany", label_text="Bill Company"),
              RPACText("billAddress", label_text="Bill Address"),
              RPACText("billAttn", label_text="Bill Attn"),
              RPACText("billTel", label_text="Bill Tel"),
              RPACText("billFax", label_text="Bill Fax"),
              RPACText("shipCompany", label_text="Ship Company"),
              RPACText("shipAddress", label_text="Ship Address"),
              RPACText("shipAttn", label_text="Ship Attn"),
              RPACText("shipTel", label_text="Ship Tel"),
              RPACText("shipFax", label_text="Ship Fax"),
              RPACText("origin", label_text="Origin"),
              RPACText("rnCode", label_text="RN Code"),
              RPACText("wplCode", label_text="WPL Code"),
              RPACText("specialInstr", label_text="Special Instruction"),
              #RPACText("labelCode", label_text = "Label System")
              ]

order_report = OrderReportForm()
