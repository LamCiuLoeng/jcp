# -*- coding: utf-8 -*-

from datetime import datetime
from tg import expose, redirect, validate, flash, session, request
from tg.decorators import *

# third party imports
from repoze.what import predicates, authorize
from repoze.what.predicates import not_anonymous, in_group, has_permission

#project specific imports
from ordering.lib.base import BaseController
from ordering.model import *

#customer imports
import traceback
from random import randint

#import itemCode
from ordering.util.oracle_helper import *

color_list = ["CORAL COMBO", "PURPLE", "BROWN", "RED COMBO"]
size_list = ["XL", "X", "XML", "MML"]
size_code_list = ["02", "03", "04", "05"]
style_list = ["FL20715Y", "FL20717Y", "FL20819Y", "FIB2010Y"]


__all__ = ['ImportDataController']

class ImportDataController(BaseController):
    #allow_only = authorize.not_anonymous()

    def _decodeCol(self, col):
        if not col:
            return ""
        if type(col) == datetime:
            return col.strftime("%Y-%m-%d")
        return str(col).decode("utf8")

    @expose('ordering.templates.importdata.index')
    def index(self, **kw):
        return dict(rs="testing")


    @expose('ordering.templates.importdata.index')
    def addShipBillTo(self, **kw):
        try:
            ship_list = []
            bill_list = []
            for i in range(10):
                ship = JCPShipTo(company="SHIP-R-PAC shenzhen office--" + str(i),
                                   address="41F Block A, United Plaza, No. 5022 Binhe Road, Futian Central District, Shenzhen-ship--" + str(i),
                                   attn=str(i),
                                   tel="0755-88888888-000" + str(i),
                                   fax="0755-99999999-000" + str(i),
                                   email="ship-service" + str(i) + "@r-pac.com.hk")
                bill = JCPBillTo(company="BILL-R-PAC shenzhen office--" + str(i),
                                   address="41F Block A, United Plaza, No. 5022 Binhe Road, Futian Central District, Shenzhen-bill--" + str(i),
                                   attn=str(i),
                                   tel="0755-88888888-000" + str(i),
                                   fax="0755-99999999-000" + str(i),
                                   email="bill-service" + str(i) + "@r-pac.com.hk")

                ship_list.append(ship)
                bill_list.append(bill)
            DBSession.add_all(ship_list)
            DBSession.add_all(bill_list)
            DBSession.commit()


        except:
            flash("add ship to unsuccessfully")
            traceback.print_exc()
        flash("add ship to successfully")
        return dict()

    @expose("ordering.templates.importdata.index")
    def addItemCode(self, **kw):
        try:
            item_list = []

            db_conn = createConnection()
            cursor = db_conn.cursor()
            sql = "select item_code,full_desc from t_item_hdr where program = 'JC PENNEY'"
            cursor.execute(sql)
            result = cursor.fetchall()
            item_list = [item for item in result]
            db_list = []
            for item in item_list:
                rs = JCPItemCodeMaster(name=str(item[0]).decode("utf8"),
                                       description=str(item[1]).decode("utf8")
                                        )
                db_list.append(rs)

            DBSession.add_all(db_list)
            DBSession.commit()
            flash("add itemCode successfully")
        except:
            traceback.print_exc()
        return dict()


    @expose("ordering.templates.importdata.index")
    def addHeader(self, **kw):
        try:
            header_list = []
            detail_list = []
            for i in range(0, 30):
                header = JCPHeaderPO(poNo=str(randint(12345678, 99999999)),
                                     stock=str(randint(1234, 9999)),
                                     sub=950,
                                     lot=1200,
                                     lotDescription='shirt',
                                     line="01" + str(i),
                                     poDate=datetime.now())

                for i, color in enumerate(color_list):
                    upc = str(randint(123456789012, 999999999999))
                    for j, size in enumerate(size_code_list):
                        detail = JCPDetailPO(header=header,
                                             colorCode=color,
                                             sizeCode=size,
                                             size=size_list[i],
                                             upc=str(upc),
                                             styleNo=style_list[i],
                                             retail="45.00",
                                             quantity=randint(20, 100))
                        detail_list.append(detail)
                header_list.append(header)
            DBSession.add_all(header_list)
            DBSession.add_all(detail_list)
            DBSession.commit()
            flash("Import Data successfully")
        except:
            traceback.print_exc()
        return dict()

    @expose("ordering.templates.importdata.index")
    def updateHeader(self, **kw):
        try:
            header_list = []
            data = DBSession.query(JCPHeaderPO).order_by(JCPHeaderPO.id).all()
            lot = [1101, 1100, 1103, 1021, 1038, 1018]
            for index, row in enumerate(data):
                if index < 12:
                    row.sub = 760
                    if index < 3: row.lot = lot[0]
                    if index >= 3 and index < 6: row.lot = lot[1]
                    if index >= 6 : row.lot = lot[2]
                    row.poNo = str(100000817380 + index)
                else:
                    row.sub = 980
                    if index >= 12 and index < 15: row.lot = lot[3]
                    if index >= 15 and index < 18: row.lot = lot[4]
                    if index >= 18 : row.lot = lot[5]
                    row.poNo = str(100000780171 + index - 12)

                #row.sub = 888
            print 'ok'
            flash("update Data successfully")
            return dict(rs=data)

        except:
            traceback.print_exc()
        return dict()


