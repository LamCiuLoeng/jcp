from datetime import datetime as dt
from sqlalchemy import *
from sqlalchemy.sql.expression import alias
from sqlalchemy.sql.functions import sum
from sqlalchemy.sql.functions import max
from sqlalchemy.orm import mapper, relation, backref
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode, TypeDecorator, DateTime, Text, Float

from tg import request

from ordering.model import DeclarativeBase, metadata, DBSession
from ordering.model.auth import User


__all__=["JCPHeaderPO", "JCPDetailPO", "JCPCountryCode", "JCPOrderForm",
         "JCPCountry", "JCPContact", "JCPBillTo", "JCPShipTo",
         "JCPInstruction", "MsgHeader", "MsgDetail", "JCPFCInstrHeader",
         "JCPFCInstrDetail", "item_special_value_table", "JCPItemInfo",
         "JCPSpecialValue", "JCPCustomer", "JCPSPVHeader", "JCPSPVDetail",
         "JCPRFIDMappingCode", "JCPUpc", "CustomerSample", "JCPComboMappingInfo"]


DB_DATETIME_FORMAT=""
WEB_DATETIME_FORMAT="%Y/%m/%d"

# 20120201
def getUserID():
    return request.identity["user"].user_id

class RPACDateTime(TypeDecorator):
    impl=DateTime
    def process_bind_param(self, value, dialect):
        if not value : return None
        return dt.strptime(value, WEB_DATETIME_FORMAT)

class MsgHeader(DeclarativeBase):
    __tablename__="msg_header"

    id=Column(Integer, primary_key=True)
    Msg_Nbr=Column("msg_nbr", Unicode(10))
    Msg_Type=Column("msg_type", Unicode(5))
    Msg_Txt=Column("msg_txt", Unicode(100))
    Tkt_Supp=Column("tkt_supp", Unicode(10))
    Merch_Supp=Column("merch_supp", Unicode(10))
    Purchase_Order=Column("purchase_order", Unicode(15))
    Nbr_Detail_Items=Column("nbr_detail_items", Integer, default=0)


class MsgDetail(DeclarativeBase):
    __tablename__="msg_detail"

    id=Column(Integer, primary_key=True)
    headerid=Column("header_id", Integer, ForeignKey("msg_header.id"))
    header=relation(MsgHeader, backref="details")
    Item_Desc=Column("item_desc", Unicode(50))
    Tkt_Stock=Column("tkt_stock", Unicode(10))
    Sub=Column("sub", Unicode(10))
    Lot=Column("lot", Unicode(10))
    Line=Column("line", Unicode(10))
    Color=Column("color", Unicode(50))
    Cntry_Of_Org=Column("cntry_of_org", Unicode(5))
    Sku=Column("sku", Unicode(5))
    Size=Column("size", Unicode(50))
    Metric_Cnvrsn=Column("metric_cnvrsn", Unicode(5))
    Retail=Column("retail", Float)
    Quantity=Column("quantity", Integer)
    GTIN=Column("gtin", Unicode(50))
    PID=Column("pid", Unicode(50))
    Ctlg_Xref=Column("ctlg_xref", Unicode(50))
    Misc_Txt=Column("misc_txt", Unicode(50))
    Misc_Txt2=Column("misc_txt2", Unicode(50))
    RFID=Column("rfid", Unicode(10))
    Brand_Typ=Column("brand_type", Unicode(10))
    Two_Or_More=Column("two_or_more", Unicode(20))

#new add by CL on 2010-06-18
class JCPCustomer(DeclarativeBase):
    __tablename__="jcp_customer"

    id=Column(Integer, primary_key=True)
    name=Column("name", Unicode(100))
    active=Column("active", Integer, default=0)
    lastModifyTime=Column("last_modify_time", DateTime, default=dt.now())
    issuedById=Column("issued_by_id", Integer, ForeignKey('tg_user.user_id'))
    issuedBy=relation(User, primaryjoin=issuedById==User.user_id)
    lastModifyById=Column("last_modify_by_id", Integer, ForeignKey('tg_user.user_id'))
    lastModifyBy=relation(User, primaryjoin=lastModifyById==User.user_id)

    def __unicode__(self): return self.name
    
    @classmethod
    def get_company_by_id(cls, id):
        return DBSession.query(cls).get(id)

class JCPCountry(DeclarativeBase):
    __tablename__="jcp_country"

    id=Column(Integer, primary_key=True)
    name=Column("name", Unicode(40))
    phone=Column("phone", Unicode(50))
    createTime=Column("create_time", DateTime, default=dt.now())
    lastModifyTime=Column("last_modify_time", DateTime, default=dt.now())
    issuedById=Column("issued_by_id", Integer, ForeignKey('tg_user.user_id'))
    issuedBy=relation(User, primaryjoin=issuedById==User.user_id)
    lastModifyById=Column("last_modify_by_id", Integer, ForeignKey('tg_user.user_id'))
    lastModifyBy=relation(User, primaryjoin=lastModifyById==User.user_id)
    histroty=Column("histroty", Unicode(500))
    status=Column("status", Integer, default=0) # 0 is active , 1 is inactive
    active=Column("active", Integer, default=0)

    def __unicode__(self): return self.name
    
    @classmethod
    def get_all_countries(cls):
        return DBSession.query(cls).filter(cls.status == 0).all()

class JCPHeaderPO(DeclarativeBase):
    __tablename__="jcp_header_po"

    id=Column(Integer, primary_key=True)
    poNo=Column("po_no", Unicode(20))
    combo_order=Column("combo_order", Unicode(20), default='2')
    poDate=Column("po_date", DateTime)
    customer_id=Column("customer_id", Integer, ForeignKey("jcp_customer.id"))
    customer=relation(JCPCustomer, backref="orders")
    country_id=Column("country_id", Integer, ForeignKey("jcp_country.id"))
    country=relation(JCPCountry, backref="contact")
    orderType=Column("order_type", Unicode(10))
    remark=Column("remark", Unicode(50))
    rfid_id=Column("rfid_id", Integer)
    status=Column("status", Unicode(10))
    active=Column("active", Integer, default=0)

    def __unicode__(self): return self.poNo

    def total_qty(self):
        return DBSession.query(sum(JCPDetailPO.quantity)).filter(JCPDetailPO.id.in_([item.id for item in self.details])).one()[0]
#        qty = 0
#        for item in self.details:
#            qty += item.quantity
#        
#        return qty

class JCPDetailPO(DeclarativeBase):
    __tablename__="jcp_detail_po"

    id=Column(Integer, primary_key=True)
    headerid=Column("header_id", Integer, ForeignKey("jcp_header_po.id"))
    header=relation(JCPHeaderPO, backref="details")

    stock=Column("stock", Unicode(20))
    sub=Column("sub", Unicode(20))
    lot=Column("lot", Integer, default=0)
    line=Column("line", Unicode(10))
    sizeCode=Column("size_code", Unicode(50))
    description=Column("description", Unicode(200))
    color=Column("color", Unicode(50))
    size=Column("size", Unicode(20))
    cat=Column("cat", Unicode(20))# cat/sku
    pid=Column("pid", Unicode(50))
    upc=Column("upc", Unicode(20))
    misc1=Column("misc1", Unicode(50))
    misc2=Column("misc2", Unicode(50))
    specialValue=Column("special_value", Unicode(50))
    retail=Column("retail", Unicode(20))
    specialPrice=Column("special_price", Unicode(20))
    quantity=Column("quantity", Integer, default=0)
    gtinCode=Column("gtin_code", Unicode(50))
    rfid=Column("rfid", Integer, default=0)
    brand_type=Column("brand_type", Unicode(10))

    washingInstruction=Column("washing_instruction", Unicode(20))
    msgDetailId=Column("msg_detail", Integer, ForeignKey("msg_detail.id"))
    msgDetail=relation(MsgDetail, backref="message")

    # for RFID, 20120201
    epcBegin = Column("epc_begin", Integer)
    epcEnd = Column("epc_end", Integer)    
    epcCodeBegin = Column("epc_code_begin", Unicode(50))
    epcCodeEnd = Column("epc_code_end", Unicode(50))
    # -------------------------------------------------
    
    status=Column("status", Unicode(10))
    type=Column("type", Unicode(10))
    active=Column("active", Integer, default=0)

    def __unicode__(self): return self.id
    
    @classmethod
    def get_by_id(cls, id):
        return DBSession.query(cls).get(id)

class JCPUpc(DeclarativeBase):
    """UPC, for JCP RFID, 20120201"""
    __tablename__ = 'jcp_upc'
    
    id = Column(Integer, primary_key=True)
    upc = Column("upc", Unicode(20))
    lastQty = Column("last_qty", Integer, default=0)
    lastModifyTime = Column("last_modify_time", DateTime, default=dt.now(), onupdate=dt.now)
    lastModifyById = Column("last_modify_by_id", Integer, ForeignKey('tg_user.user_id'), 
                            default=getUserID, onupdate=getUserID)
    lastModifyBy = relation(User, primaryjoin=lastModifyById==User.user_id)
    active = Column("active", Integer, default=0)

class JCPCountryCode(DeclarativeBase):
    __tablename__="jcp_country_code"

    id=Column(Integer, primary_key=True)
    countryName=Column("country_name", Unicode(50))
    countryCode=Column("country_code", Unicode(5))
    lastModifyTime=Column("last_modify_time", DateTime, default=dt.now())
    issuedById=Column("issued_by_id", Integer, ForeignKey('tg_user.user_id'))
    issuedBy=relation(User, primaryjoin=issuedById==User.user_id)
    lastModifyById=Column("last_modify_by_id", Integer, ForeignKey('tg_user.user_id'))
    lastModifyBy=relation(User, primaryjoin=lastModifyById==User.user_id)
    
    @classmethod
    def get_name_by_id(cls, id):
        return DBSession.query(cls.countryName).filter(cls.id == id).one()

class JCPRFIDMappingCode(DeclarativeBase):
    __tablename__="jcp_rfid_mapping_code"

    id=Column(Integer, primary_key=True)
    sub=Column("sub", Unicode(10))
    stock=Column("stock", Unicode(10))
    rfid=Column("rfid", Unicode(10))
    lastModifyTime=Column("last_modify_time", DateTime, default=dt.now())
    issuedById=Column("issued_by_id", Integer, ForeignKey('tg_user.user_id'))
    issuedBy=relation(User, primaryjoin=issuedById==User.user_id)
    lastModifyById=Column("last_modify_by_id", Integer, ForeignKey('tg_user.user_id'))
    lastModifyBy=relation(User, primaryjoin=lastModifyById==User.user_id)
    active=Column("active", Integer, default=0)
    
    @classmethod
    def get_mapping_code(cls, sub, stock):
        mapping_code=DBSession.query(cls.rfid) \
                        .filter(cls.sub==sub) \
                        .filter(cls.stock==stock) \
                        .all()

        return mapping_code[0][0] if mapping_code else False

#class JCPItemCodeMaster(DeclarativeBase):
#    __tablename__ = "jcp_item_code_master"
#
#    id               = Column(Integer, primary_key = True)
#    name             = Column("name",Unicode(100))
#    description      = Column("description",Unicode(1000))
#    createTime       = Column("create_time", DateTime, default = dt.now())
#    lastModifyTime   = Column("last_modify_time", DateTime, default = dt.now())
#    issuedById       = Column("issued_by_id",Integer, ForeignKey('tg_user.user_id'))
#    issuedBy         = relation(User, primaryjoin = issuedById == User.user_id)
#    lastModifyById   = Column("last_modify_by_id",Integer, ForeignKey('tg_user.user_id'))
#    lastModifyBy     = relation(User, primaryjoin = lastModifyById == User.user_id)
#    histroty         = Column("histroty",Unicode(500))
#    status           = Column("status",Integer, default = 0) # 0 is active , 1 is inactive
#
#
#    def __unicode__(self): return self.name


class JCPOrderForm(DeclarativeBase):
    __tablename__="jcp_order_form"

    id=Column(Integer, primary_key=True)
    headerId=Column("header_id", Integer, ForeignKey("jcp_header_po.id"))
    header=relation(JCPHeaderPO, backref="orders") #poNo

    orderDate=Column("order_date", DateTime, default=dt.now)
    customerPO=Column("po_no", Unicode(50))
    supplierNO=Column("supplier_no", Unicode(50))

    billCompany=Column("bill_company", Unicode(100))
    billAddress=Column("bill_address", Unicode(200))
    billAttn=Column("bill_attn", Unicode(50))
    billTel=Column("bill_tel", Unicode(50))
    billFax=Column("bill_fax", Unicode(50))
    billEmail=Column("bill_email", Unicode(50))

    shipCompany=Column("ship_company", Unicode(100))
    shipAddress=Column("ship_address", Unicode(200))
    shipAttn=Column("ship_attn", Unicode(50))
    shipTel=Column("ship_tel", Unicode(50))
    shipFax=Column("ship_fax", Unicode(50))
    shipEmail=Column("ship_email", Unicode(50))

    origin=Column("country_of_origin", Unicode(30))
    rnCode=Column("rn_code", Unicode(20))
    wplCode=Column("rpl_code", Unicode(20))
    specialInstr=Column("special_instr", Unicode(500))
    labelCode=Column("label_code", Unicode(10))
    shipInstruction=Column("ship_instruction", Unicode(500))
    cust_item_codes=Column("cust_item_codes", Unicode(500))

    issuedById=Column("issued_by_id", Integer, ForeignKey('tg_user.user_id'))
    issuedBy=relation(User, primaryjoin=issuedById==User.user_id)
    lastModifyById=Column("last_modify_by_id", Integer, ForeignKey('tg_user.user_id'))
    lastModifyBy=relation(User, primaryjoin=lastModifyById==User.user_id)
    status=Column("status", Unicode(10))
    active=Column("active", Integer, default=0)

    def __unicode__(self): return self.id
    
    @classmethod
    def latest_order_form(cls, user):
        form_id = DBSession.query(max(cls.id)).filter(cls.issuedBy == user).all()
        
        return DBSession.query(cls).get(form_id[0]) if form_id else None

class JCPContact(DeclarativeBase):
    __tablename__="jcp_contact"

    id=Column(Integer, primary_key=True)
    countryId=Column("country_id", Integer, ForeignKey("jcp_country.id"))
    country=relation(JCPCountry, backref="contacts")
    name=Column("name", Unicode(50))
    email=Column("email", Unicode(100))
    createTime=Column("create_time", DateTime, default=dt.now())
    lastModifyTime=Column("last_modify_time", DateTime, default=dt.now())
    issuedById=Column("issued_by_id", Integer, ForeignKey('tg_user.user_id'))
    issuedBy=relation(User, primaryjoin=issuedById==User.user_id)
    lastModifyById=Column("last_modify_by_id", Integer, ForeignKey('tg_user.user_id'))
    lastModifyBy=relation(User, primaryjoin=lastModifyById==User.user_id)
    histroty=Column("histroty", Unicode(500))
    status=Column("status", Integer, default=0) # 0 is active , 1 is inactive
    active=Column("active", Integer, default=0)

    def __unicode__(self): return self.name


class JCPBillTo(DeclarativeBase):
    __tablename__="jcp_bill_to"

    id=Column(Integer, primary_key=True)
    customer_id=Column("customer_id", Integer, ForeignKey("jcp_customer.id"))
    customer=relation(JCPCustomer, backref="billtos")
    company=Column("company", Unicode(100))
    address=Column("address", Unicode(200))
    attn=Column("attn", Unicode(50))
    tel=Column("tel", Unicode(50))
    fax=Column("fax", Unicode(50))
    email=Column("email", Unicode(100))
    lastModifyTime=Column("last_modify_time", DateTime, default=dt.now())
    issuedById=Column("issued_by_id", Integer, ForeignKey('tg_user.user_id'))
    issuedBy=relation(User, primaryjoin=issuedById==User.user_id)
    lastModifyById=Column("last_modify_by_id", Integer, ForeignKey('tg_user.user_id'))
    lastModifyBy=relation(User, primaryjoin=lastModifyById==User.user_id)
    is_default=Column("is_default", Integer, default=0)

    def __unicode__(self): return self.company

class JCPShipTo(DeclarativeBase):
    __tablename__="jcp_ship_to"

    id=Column(Integer, primary_key=True)
    customer_id=Column("customer_id", Integer, ForeignKey("jcp_customer.id"))
    customer=relation(JCPCustomer, backref="shiptos")
    company=Column("company", Unicode(100))
    address=Column("address", Unicode(200))
    attn=Column("attn", Unicode(50))
    tel=Column("tel", Unicode(50))
    fax=Column("fax", Unicode(50))
    email=Column("email", Unicode(100))
    lastModifyTime=Column("last_modify_time", DateTime, default=dt.now())
    issuedById=Column("issued_by_id", Integer, ForeignKey('tg_user.user_id'))
    issuedBy=relation(User, primaryjoin=issuedById==User.user_id)
    lastModifyById=Column("last_modify_by_id", Integer, ForeignKey('tg_user.user_id'))
    lastModifyBy=relation(User, primaryjoin=lastModifyById==User.user_id)
    is_default=Column("is_default", Integer, default=0)

    def __unicode__(self): return self.company

class JCPInstruction(DeclarativeBase):
    __tablename__="jcp_instruction"

    id=Column(Integer, primary_key=True)
    category=Column("category", Unicode(10))
    position=Column("position", Integer)
    selection=Column("selection", Unicode(10))
    content=Column("content", Text)

class JCPFCInstrHeader(DeclarativeBase):
    __tablename__="jcp_fc_instr_header"

    id=Column(Integer, primary_key=True)
    podetailid=Column("po_detail_id", Integer, ForeignKey("jcp_detail_po.id"))
    poDetail=relation(JCPDetailPO, backref="fcdetails")
    exclusiveData=Column("exclusive_data", Unicode(60))
    cottonLogo=Column("cotton_logo", Boolean)
    lycraLogo=Column("lycra_logo", Boolean)

class JCPFCInstrDetail(DeclarativeBase):
    __tablename__="jcp_fc_instr_detail"

    id=Column(Integer, primary_key=True)
    headerid=Column("header_id", Integer, ForeignKey("jcp_fc_instr_header.id"))
    header=relation(JCPFCInstrHeader, backref="fcdetails")
    ccName=Column("cc_name", Unicode(50))
    component=Column("component", Unicode(20))
    color=Column("color", Unicode(20))
    percentage1=Column("percentage_1", Unicode(10))
    content1=Column("content_1", Unicode(50))
    percentage2=Column("percentage_2", Unicode(10))
    content2=Column("content_2", Unicode(50))
    percentage3=Column("percentage_3", Unicode(10))
    content3=Column("content_3", Unicode(50))
    percentage4=Column("percentage_4", Unicode(10))
    content4=Column("content_4", Unicode(50))
    percentage5=Column("percentage_5", Unicode(10))
    content5=Column("content_5", Unicode(50))

class JCPSPVHeader(DeclarativeBase):
    __tablename__="jcp_spv_header"

    id=Column(Integer, primary_key=True)
    podetailid=Column("po_detail_id", Integer, ForeignKey("jcp_detail_po.id"))
    poDetail=relation(JCPDetailPO, backref="spvdetails")

class JCPSPVDetail(DeclarativeBase):
    __tablename__="jcp_spv_detail"

    id=Column(Integer, primary_key=True)
    headerid=Column("header_id", Integer, ForeignKey("jcp_spv_header.id"))
    header=relation(JCPSPVHeader, backref="spvaluedetails")
    value=Column(Unicode(40))
    part=Column(Integer, default=0)

item_special_value_table=Table('jcp_item_special_value', metadata,
    Column('item_id', Integer, ForeignKey('jcp_item_info.id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    Column('special_value_id', Integer, ForeignKey('jcp_special_value.id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
)

class JCPItemInfo(DeclarativeBase):
    __tablename__="jcp_item_info"

    id=Column(Integer, primary_key=True)
    item_code=Column(Unicode(20))
    packaging_code=Column(Unicode(4))
    combo_packaging_code=Column(Unicode(4))
    combo_item=Column(Boolean, default=False)
    washing_instruction=Column(Boolean)
    fiber_content=Column(Boolean)
    country_of_origin=Column(Boolean)
    special_value=Column(Boolean)
    combo_mapping=Column(Boolean, default=False)
    multi_special_value=Column(Integer, default=0)
    values=relation('JCPSpecialValue', secondary=item_special_value_table, backref="jcpitems")
    path=Column(Unicode(100))
    status=Column("status", Integer, default=0) # 0 is active , 1 is inactive
    version=Column(Integer, default=1)
    lastModifyTime=Column("last_modify_time", DateTime, default=dt.now())
    issuedById=Column("issued_by_id", Integer, ForeignKey('tg_user.user_id'))
    issuedBy=relation(User, primaryjoin=issuedById==User.user_id)
    lastModifyById=Column("last_modify_by_id", Integer, ForeignKey('tg_user.user_id'))
    lastModifyBy=relation(User, primaryjoin=lastModifyById==User.user_id)
    
    item_type = Column(Integer, default=1) # 1 is hangtag, 2 is care label, 3 is sticker

    @classmethod
    def get_max_version(cls, pkg_code):
        version=DBSession.query(max(cls.version)) \
                 .filter(cls.packaging_code==pkg_code) \
                 .all()

        return version[0][0] if version else 1

    @classmethod
    def get_status(cls, pkg_code):
        version=cls.get_max_version(pkg_code=pkg_code)

        status=DBSession.query(cls.status) \
                .filter(cls.packaging_code==pkg_code) \
                .filter(cls.version==version) \
                .all()

        return status[0][0] if status else 0

    @classmethod
    def get_special_value(cls, pkg_code):
        version=cls.get_max_version(pkg_code=pkg_code)

        special_value=DBSession.query(cls.special_value) \
                        .filter(cls.packaging_code==pkg_code) \
                        .filter(cls.version==version) \
                        .all()

        return special_value[0][0] if special_value else False
    
    @classmethod
    def get_item(cls, pkg_code):
        version=cls.get_max_version(pkg_code=pkg_code)
        status=cls.get_status(pkg_code=pkg_code)
        item = DBSession.query(cls) \
                .filter(cls.packaging_code==pkg_code) \
                .filter(cls.version==version) \
                .filter(cls.status==status) \
                .all()
        
        return item[0] if item else None
    
    @classmethod
    def get_img_item(cls, pkg_code):
        version=cls.get_max_version(pkg_code=pkg_code)
        #status=cls.get_status(pkg_code=pkg_code)
        item = DBSession.query(cls) \
                .filter(cls.packaging_code==pkg_code) \
                .filter(cls.version==version) \
                .all()
        
        return item[0] if item else None

class JCPSpecialValue(DeclarativeBase):
    __tablename__="jcp_special_value"

    id=Column(Integer, primary_key=True)
    value=Column(Unicode(40))
    part=Column(Integer)
    path=Column(Unicode(100))
    status=Column(Integer, default=0) #0 = active, 1 = inactive
    items=relation(JCPItemInfo, secondary=item_special_value_table, backref="specialvalues")
    lastModifyTime=Column("last_modify_time", DateTime, default=dt.now())
    issuedById=Column("issued_by_id", Integer, ForeignKey('tg_user.user_id'))
    issuedBy=relation(User, primaryjoin=issuedById==User.user_id)
    lastModifyById=Column("last_modify_by_id", Integer, ForeignKey('tg_user.user_id'))
    lastModifyBy=relation(User, primaryjoin=lastModifyById==User.user_id)
    
    @classmethod
    def get_special_value(cls, id):
        return DBSession.query(cls).get(id)
    
    @classmethod
    def get_by_part_value(cls, item_id, part, value):
        return DBSession.query(cls).filter(cls.items[0].id == item_id)\
                        .filter(cls.part == part)\
                        .filter(cls.value == value)\
                        .first()

class CustomerSample(DeclarativeBase):
    __tablename__="jcp_customer_sample"

    id=Column(Integer, primary_key=True)
    name=Column("name", Unicode(100))
    path=Column("path", Unicode(200))
    headerid=Column("header_id", Integer, ForeignKey("jcp_header_po.id"))
    header=relation(JCPHeaderPO, backref="customer_samples")
    comment=Column("comment", Unicode(500))
    size=Column("size", Unicode(100))
    createdTime=Column("created_time", DateTime, default=dt.now())
    issuedById=Column("issued_by_id", Integer, ForeignKey('tg_user.user_id'))
    issuedBy=relation(User, primaryjoin=issuedById==User.user_id)
    status=Column("status", Integer, default=0)

class JCPComboMappingInfo(DeclarativeBase):
    __tablename__="jcp_combo_mapping_info"

    id=Column(Integer, primary_key=True)
    item=relation(JCPItemInfo, backref="combo_mappings")
    itemId=Column('item_id', Integer, ForeignKey("jcp_item_info.id"))
    main_pkg_code=Column(Unicode(4))
    hangtang_pkg_code=Column(Unicode(4))
    label_pkg_code=Column(Unicode(4))
    status=Column("status", Integer, default=0) # 0 is active , 1 is inactive
    lastModifyTime=Column("last_modify_time", DateTime, default=dt.now())
    issuedById=Column("issued_by_id", Integer, ForeignKey('tg_user.user_id'))
    issuedBy=relation(User, primaryjoin=issuedById==User.user_id)
    lastModifyById=Column("last_modify_by_id", Integer, ForeignKey('tg_user.user_id'))
    lastModifyBy=relation(User, primaryjoin=lastModifyById==User.user_id)
    
    @classmethod
    def get_by_main_code(cls, main_pkg_code):
        return DBSession.query(cls).filter(cls.main_pkg_code == main_pkg_code).all()
    
    @classmethod
    def get_label_code(cls, main_pkg_code):
        return DBSession.query(cls.label_pkg_code).filter(cls.main_pkg_code == main_pkg_code).all()
    
    @classmethod
    def get_hangtag_code(cls, main_pkg_code):
        return DBSession.query(cls.hangtang_pkg_code)\
                .filter(cls.main_pkg_code == main_pkg_code)\
                .first()
