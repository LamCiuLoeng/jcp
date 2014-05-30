# -*- coding: utf-8 -*-

from ordering.model import *
from ordering.widgets.components import *

__all__=[#"itemCodeSearchFormInstance","itemCodeUpdateFormInstance",
           "countrySearchFormInstance", "countryUpdateFormInstance",
           "contactSearchFormInstance", "contactUpdateFormInstance",
           "billToSearchFormInstance", "billToUpdateFormInstance",
           "shipToSearchFormInstance", "shipToUpdateFormInstance",
           "countryCodeSearchFormInstance", "countryCodeUpdateFormInstance",
           "itemInfoSearchFormInstance", "itemInfoUpdateFormInstance",
           "customerSearchFormInstance", "customerUpdateFormInstance",
           "specialValueSearchFormInstance", "sepcialValueUpdateFormInstance",
           "sizeSearchFormInstance", "sizeUpdateFormInstance",
           "styleSearchFormInstance", "styleUpdateFormInstance",
           "legLengthSearchFormInstance", "legLengthUpdateFormInstance",
           "legSearchFormInstance", "legUpdateFormInstance",
           "riseSearchFormInstance", "riseUpdateFormInstance",
           "rfidMappingCodeSearchFormInstance", "rfidMappingCodeUpdateFormInstance",
           "comboMappingInfoSearchFormInstance", "comboMappingInfoUpdateFormInstance"
           ]


##--------------------- for master item code
#class ItemCodeSearchForm(RPACForm):
#    fields = [RPACText("name",label_text="Item Code Name")]
#
#itemCodeSearchFormInstance = ItemCodeSearchForm()
#
#class ItemCodeUpdateForm(RPACForm):
#    fields = [RPACText("name",label_text="Item Code Name"),RPACTextarea("description",label_text="Description")]
#
#itemCodeUpdateFormInstance = ItemCodeUpdateForm()


#--------------------- for master country
class CountrySearchForm(RPACForm):
    fields=[RPACText("name", label_text="country"), RPACText("phone", label_text="phone")]
countrySearchFormInstance=CountrySearchForm()

class CountryUpdateForm(RPACForm):
    fields=[RPACText("name", label_text="country"), RPACText("phone", label_text="phone")]
countryUpdateFormInstance=CountryUpdateForm()

#--------------------- for master contact
class ContactSearchForm(RPACForm):
    Countryoptions=DBSession.query(JCPCountry.id, JCPCountry.name).all()
    options=[]
    for v in Countryoptions:
        options.append((unicode(v[0]), unicode(v[1])))
    options.append(("", ""))
    options.reverse()

    fields=[RPACText("name", label_text="contact name"),
              RPACText("email", label_text="email"),
              RPACSelect("countryId", label_text="Country", options=options),
              ]
contactSearchFormInstance=ContactSearchForm()

class ContactUpdateForm(RPACForm):
    Countryoptions=DBSession.query(JCPCountry.id, JCPCountry.name).all()
    options=[]
    for v in Countryoptions:
        options.append((unicode(v[0]), unicode(v[1])))
    options.append(("", ""))
    options.reverse()
    fields=[RPACText("name", label_text="contact name"),
              RPACText("email", label_text="email"),
              RPACSelect("countryId", label_text="Country", options=options),
              ]
contactUpdateFormInstance=ContactUpdateForm()

class BillToSearchForm(RPACForm):
    customers=DBSession.query(JCPCustomer.id, JCPCustomer.name).all()
    options=[]
    for v in customers:
        options.append((unicode(v[0]), unicode(v[1])))

    options.append(('', ''))
    options.reverse()
    fields=[RPACSelect("customer_id", label_text="Customer", options=options),
              RPACText("company", label_text="Company"),
              RPACText("address", label_text="Address"),
              RPACText("attn", label_text="Attn"),
              RPACText("tel", label_text="Tel"),
              RPACText("fax", label_text="Fax"),
              RPACText("email", label_text="E-mail")
              ]
billToSearchFormInstance=BillToSearchForm()

class BillToUpdateForm(RPACForm):
    customers=DBSession.query(JCPCustomer.id, JCPCustomer.name).all()
    options=[]
    for v in customers:
        options.append((unicode(v[0]), unicode(v[1])))

    options.append(('', ''))
    options.reverse()
    fields=[RPACSelect("customer_id", label_text="Customer", options=options),
              RPACText("company", label_text="Company"),
              RPACText("address", label_text="Address"),
              RPACText("attn", label_text="Attn"),
              RPACText("tel", label_text="Tel"),
              RPACText("fax", label_text="Fax"),
              RPACText("email", label_text="E-mail")
              ]
billToUpdateFormInstance=BillToUpdateForm()

class ShipToSearchForm(RPACForm):
    customers=DBSession.query(JCPCustomer.id, JCPCustomer.name).all()
    options=[]
    for v in customers:
        options.append((unicode(v[0]), unicode(v[1])))

    options.append(('', ''))
    options.reverse()
    fields=[RPACSelect("customer_id", label_text="Customer", options=options),
              RPACText("company", label_text="Company"),
              RPACText("address", label_text="Address"),
              RPACText("attn", label_text="Attn"),
              RPACText("tel", label_text="Tel"),
              RPACText("fax", label_text="Fax"),
              RPACText("email", label_text="E-mail")
              ]
shipToSearchFormInstance=ShipToSearchForm()

class ShipToUpdateForm(RPACForm):
    customers=DBSession.query(JCPCustomer.id, JCPCustomer.name).all()
    options=[]
    for v in customers:
        options.append((unicode(v[0]), unicode(v[1])))

    options.append(('', ''))
    options.reverse()
    fields=[RPACSelect("customer_id", label_text="Customer", options=options),
              RPACText("company", label_text="Company"),
              RPACText("address", label_text="Address"),
              RPACText("attn", label_text="Attn"),
              RPACText("tel", label_text="Tel"),
              RPACText("fax", label_text="Fax"),
              RPACText("email", label_text="E-mail")
              ]
shipToUpdateFormInstance=ShipToUpdateForm()

class CountryCodeSearchForm(RPACForm):
    fields=[RPACText("countryName", label_text="Country Name"),
              RPACText("countryCode", label_text="Country Code")]
countryCodeSearchFormInstance=CountryCodeSearchForm()

class CountryCodeUpdateForm(RPACForm):
    fields=[RPACText("countryName", label_text="Country Name"),
              RPACText("countryCode", label_text="Country Code")]
countryCodeUpdateFormInstance=CountryCodeUpdateForm()

class RFIDMappingCodeSearchForm(RPACForm):
    fields=[RPACText("sub", label_text="Sub"),
              RPACText("stock", label_text="Stock Number"),
              RPACText("rfid", label_text="RFID Number"),
              RPACSelect("active", label_text="Status", options=[(0, 'Active'), (1, 'Inactive')]),
              ]
rfidMappingCodeSearchFormInstance=RFIDMappingCodeSearchForm()

class RFIDMappingCodeUpdateForm(RPACForm):
    fields=[RPACText("sub", label_text="Sub"),
              RPACText("stock", label_text="Stock Number"),
              RPACText("rfid", label_text="RFID Number"),
              RPACSelect("active", label_text="Status", options=[(0, 'Active'), (1, 'Inactive')]),
              ]
rfidMappingCodeUpdateFormInstance=RFIDMappingCodeUpdateForm()

class ItemInfoSearchForm(RPACForm):
    part_option=[('-1', 'All')]
    part_option.extend([str(x) for x in range(10)])

    fields=[RPACSelect("item_type", label_text="Type", options=[('0', 'All'), ('1', 'Hangtag'), ('2', 'Care Label'), ('3', 'RFID Sticker')]),
            RPACRadio("combo_item", label_text="Matchbook/Barcoded Combo", options=[("True", "True"), ("False", "False")]),
            RPACText("item_code", label_text="Item Code"),
            RPACText("combo_packaging_code", label_text="Combo Packaging Code"),
            RPACText("packaging_code", label_text="Packaging Code"),
            RPACRadio("combo_mapping", label_text="Combo Items", options=[("True", "True"), ("False", "False")]),
            RPACText("path", label_text="Path"),
            RPACText("hangtang_pkg_code", label_text="Item 1 packaging code"),
            RPACSelect("status", label_text="Status", options=[('2', 'All'), ('0', 'Active'), ('1', 'Inactive')]),
            RPACText("label_pkg_code", label_text="Item 2 packaging code"),
            RPACRadio("washing_instruction", label_text="Washing Instruction", options=[("True", "True"), ("False", "False")]),
            RPACRadio("special_value", label_text="Special Value", options=[("True", "True"), ("False", "False")]),
            RPACRadio("country_of_origin", label_text="Country of Origin", options=[("True", "True"), ("False", "False")]),
            RPACSelect("multi_special_value", label_text="Special Value Part", options=part_option),
            RPACRadio("fiber_content", label_text="Fiber Content", options=[("True", "True"), ("False", "False")]),
            ]
itemInfoSearchFormInstance=ItemInfoSearchForm()

class ItemInfoUpdateForm(RPACForm):
    template = "ordering.templates.widgets.item_form"
    part_option = [x for x in range(10)]

    fields=[RPACSelect("item_type", label_text="Type", options=[(0, 'All'), (1, 'Hangtag'), (2, 'Care Label'), (3, 'RFID Sticker')]),
            RPACRadio("combo_item", label_text="Matchbook/Barcoded Combo", options=[(True, "True"), (False, "False")]),
            RPACText("item_code", label_text="Item Code"),
            RPACText("combo_packaging_code", label_text="Combo Packaging Code"),
            RPACText("packaging_code", label_text="Packaging Code"),
            RPACRadio("combo_mapping", label_text="Combo Items", options=[(True, "True"), (False, "False")]),
            RPACText("path", label_text="Path", default = '/images/jcpenney/'),
            RPACText("hangtang_pkg_code", label_text="Item 1 packaging code"),
            RPACSelect("status", label_text="Status", options=[(2, 'All'), (0, 'Active'), (1, 'Inactive')]),
            RPACText("label_pkg_code", label_text="Item 2 packaging code"),
            RPACRadio("washing_instruction", label_text="Washing Instruction", options=[(True, "True"), (False, "False")],),
            RPACRadio("special_value", label_text="Special Value", options=[(True, "True"), (False, "False")]),
            RPACRadio("country_of_origin", label_text="Country of Origin", options=[(True, "True"), (False, "False")]),
            RPACSelect("multi_special_value", label_text="Special Value Part", options=part_option),
            RPACRadio("fiber_content", label_text="Fiber Content", options=[(True, "True"), (False, "False")]),
            ]
itemInfoUpdateFormInstance=ItemInfoUpdateForm()

class CustomerSearchForm(RPACForm):
    fields=[RPACText("name", label_text="Customer Name")]
customerSearchFormInstance=CustomerSearchForm()

class CustomerUpdateForm(RPACForm):
    fields=[RPACText("name", label_text="Customer Name")]
customerUpdateFormInstance=CustomerUpdateForm()

class SpecialValueSearchForm(RPACForm):
    part_option = [('-1', 'All')]
    part_option.extend([str(x) for x in range(10)])

    fields=[RPACText("item_id", label_text="JCP Item", fieldName='item_id'),
            RPACText("value", label_text="Special Value"),
            RPACSelect("part", label_text="Special Value Part", options=part_option),
            RPACText("path", label_text="Path"),
            ]
specialValueSearchFormInstance=SpecialValueSearchForm()

class SepcialValueUpdateForm(RPACForm):
    template = "ordering.templates.widgets.specialvalue_form"
    part_option=[str(x) for x in range(10)]

    fields=[RPACAjaxText("item_id", label_text="JCP Item"),
            RPACText("value", label_text="Special Value"),
            RPACSelect("part", label_text="Special Value Part", options=part_option),
            RPACText("path", label_text="Path", default = '/images/specialValueImg/'),
            ]
sepcialValueUpdateFormInstance=SepcialValueUpdateForm()

class SizeSearchForm(RPACForm):
    items=DBSession.query(JCPItemInfo.id, JCPItemInfo.item_code).filter(JCPItemInfo.status==0).all()
    options=[]
    for v in items:
        options.append((unicode(v[0]), unicode(v[1])))

    options.append(('', ''))
    options.reverse()

    fields=[RPACSelect("item_id", label_text="JCP Item", options=options),
            RPACText("name", label_text="Size Name"),
            RPACText("description", label_text="Size Description"),
            ]
sizeSearchFormInstance=SizeSearchForm()

class SizeUpdateForm(RPACForm):
    items=DBSession.query(JCPItemInfo.id, JCPItemInfo.item_code).filter(JCPItemInfo.status==0).all()
    options=[]
    for v in items:
        options.append((unicode(v[0]), unicode(v[1])))

    options.append(('', ''))
    options.reverse()

    fields=[RPACSelect("item_id", label_text="JCP Item", options=options),
            RPACText("name", label_text="Size Name"),
            RPACText("description", label_text="Size Description"),
            ]
sizeUpdateFormInstance=SizeUpdateForm()

class StyleSearchForm(RPACForm):
    items=DBSession.query(JCPItemInfo.id, JCPItemInfo.item_code).filter(JCPItemInfo.status==0).all()
    options=[]
    for v in items:
        options.append((unicode(v[0]), unicode(v[1])))

    options.append(('', ''))
    options.reverse()

    fields=[RPACSelect("item_id", label_text="JCP Item", options=options),
            RPACText("name", label_text="Style Name"),
            RPACText("description", label_text="Style Description"),
            ]
styleSearchFormInstance=StyleSearchForm()

class StyleUpdateForm(RPACForm):
    items=DBSession.query(JCPItemInfo.id, JCPItemInfo.item_code).filter(JCPItemInfo.status==0).all()
    options=[]
    for v in items:
        options.append((unicode(v[0]), unicode(v[1])))

    options.append(('', ''))
    options.reverse()

    fields=[RPACSelect("item_id", label_text="JCP Item", options=options),
            RPACText("name", label_text="Style Name"),
            RPACText("description", label_text="Style Description"),
            ]
styleUpdateFormInstance=StyleUpdateForm()

class LegLengthSearchForm(RPACForm):
    items=DBSession.query(JCPItemInfo.id, JCPItemInfo.item_code).filter(JCPItemInfo.status==0).all()
    options=[]
    for v in items:
        options.append((unicode(v[0]), unicode(v[1])))

    options.append(('', ''))
    options.reverse()

    fields=[RPACSelect("item_id", label_text="JCP Item", options=options),
            RPACText("name", label_text="Leg Length Name"),
            RPACText("description", label_text="Leg Length Description"),
            ]
legLengthSearchFormInstance=LegLengthSearchForm()

class LegLengthUpdateForm(RPACForm):
    items=DBSession.query(JCPItemInfo.id, JCPItemInfo.item_code).filter(JCPItemInfo.status==0).all()
    options=[]
    for v in items:
        options.append((unicode(v[0]), unicode(v[1])))

    options.append(('', ''))
    options.reverse()

    fields=[RPACSelect("item_id", label_text="JCP Item", options=options),
            RPACText("name", label_text="Leg Length Name"),
            RPACText("description", label_text="Leg Length Description"),
            ]
legLengthUpdateFormInstance=LegLengthUpdateForm()

class LegSearchForm(RPACForm):
    items=DBSession.query(JCPItemInfo.id, JCPItemInfo.item_code).filter(JCPItemInfo.status==0).all()
    options=[]
    for v in items:
        options.append((unicode(v[0]), unicode(v[1])))

    options.append(('', ''))
    options.reverse()

    fields=[RPACSelect("item_id", label_text="JCP Item", options=options),
            RPACText("name", label_text="Leg Name"),
            RPACText("description", label_text="Leg Description")
            ]
legSearchFormInstance=LegSearchForm()

class LegUpdateForm(RPACForm):
    items=DBSession.query(JCPItemInfo.id, JCPItemInfo.item_code).filter(JCPItemInfo.status==0).all()
    options=[]
    for v in items:
        options.append((unicode(v[0]), unicode(v[1])))

    options.append(('', ''))
    options.reverse()

    fields=[RPACSelect("item_id", label_text="JCP Item", options=options),
            RPACText("name", label_text="Leg Name"),
            RPACText("description", label_text="Leg Description"),
            ]
legUpdateFormInstance=LegUpdateForm()

class RiseSearchForm(RPACForm):
    items=DBSession.query(JCPItemInfo.id, JCPItemInfo.item_code).filter(JCPItemInfo.status==0).all()
    options=[]
    for v in items:
        options.append((unicode(v[0]), unicode(v[1])))

    options.append(('', ''))
    options.reverse()

    fields=[RPACSelect("item_id", label_text="JCP Item", options=options),
            RPACText("name", label_text="Rise Name"),
            RPACText("description", label_text="Rise Description")]
riseSearchFormInstance=RiseSearchForm()

class RiseUpdateForm(RPACForm):
    items=DBSession.query(JCPItemInfo.id, JCPItemInfo.item_code).filter(JCPItemInfo.status==0).all()
    options=[]
    for v in items:
        options.append((unicode(v[0]), unicode(v[1])))

    options.append(('', ''))
    options.reverse()

    fields=[RPACSelect("item_id", label_text="JCP Item", options=options),
            RPACText("name", label_text="Rise Name"),
            RPACText("description", label_text="Rise Description")]
riseUpdateFormInstance=RiseUpdateForm()

class ComboMappingInfoSearchForm(RPACForm):
    fields=[RPACText("main_pkg_code", label_text="Main Packaging Code"),
            RPACText("hangtang_pkg_code", label_text="HangTag Packaging Code"),
            RPACText("label_pkg_code", label_text="Label Packaging Code"),
            ]
comboMappingInfoSearchFormInstance=ComboMappingInfoSearchForm()

class ComboMappingInfoUpdateForm(RPACForm):
    fields=[RPACText("main_pkg_code", label_text="Main Packaging Code"),
            RPACText("hangtang_pkg_code", label_text="HangTag Packaging Code"),
            RPACText("label_pkg_code", label_text="Label Packaging Code"),
            ]
comboMappingInfoUpdateFormInstance=ComboMappingInfoUpdateForm()
