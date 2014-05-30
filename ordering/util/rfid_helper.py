# -*- coding: utf-8 -*-
import traceback

from suds.client import Client

from tg import config

from ordering.model import *

__all__ = ['sendRFID']

def sendRFID(order_data, area):
    try:
        client = Client(config.rfid_service)
        poHeader, poDetails = parse_data(order_data, area, client)
        result = client.service.JCPDataInsert(poHeader, poDetails)
        
        return result
    except:
        traceback.print_exc()

def parse_data(order_data, area, client):
    orderHeader = client.factory.create("JCPHeader")
    orderDetails = client.factory.create("ArrayOfJCPDetail")
    #detail_list = []
    
    orderHeader.CustomPO = order_data.orders[0].customerPO
    orderHeader.JESMO = 'JESMO#'
    orderHeader.ItemCode = order_data.orders[0].cust_item_codes
    orderHeader.ShipAddress = order_data.orders[0].shipAddress
    orderHeader.BillAddress = order_data.orders[0].billAddress
    
#    if order_data.orders[0].upc is None or order_data.orders[0].upc == '':
#        orderHeader.JCP_type = 'P'
#    else:
#        orderHeader.JCP_type = 'N'

    if order_data.details[0].upc is not None and len(order_data.details[0].upc) > 1:
        orderHeader.JCP_type = 'N'
    else:
        orderHeader.JCP_type = 'P'
    
    orderHeader.Import_type = 'A'
    orderHeader.Area = area
    
    for detail in order_data.details:
        orderDetail = client.factory.create("JCPDetail")
        orderDetail.Stock = detail.stock
        orderDetail.Sub = detail.sub
        orderDetail.Lot = detail.lot
        orderDetail.Line = detail.line
        orderDetail.SizeCode = detail.sizeCode
        orderDetail.Description = detail.description
        orderDetail.Color = detail.color
        orderDetail.Size = detail.size
        orderDetail.Cat = detail.cat
        orderDetail.UPC = detail.upc
        orderDetail.Retail = detail.retail
        orderDetail.QTY = detail.quantity
        orderDetail.Supplier = detail.header.orders[0].supplierNO
        orderDetail.Style = detail.header.remark
        orderDetail.PID = detail.pid
        orderDetail.MISC1 = detail.misc1
        orderDetail.MISC2 = detail.misc2
        
        sp_values = []
        if detail.spvdetails:
            for sp_detail in detail.spvdetails[0].spvaluedetails:
                sp_values.append(sp_detail.value)
        
        orderDetail.SpecialValue = '|'.join(sp_values)
        orderDetail.More = detail.specialPrice

        orderDetails['JCPDetail'].append(orderDetail)
    
    return (orderHeader, orderDetails)

