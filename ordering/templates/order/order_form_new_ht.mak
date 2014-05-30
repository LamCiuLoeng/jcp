<%inherit file="ordering.templates.master"/>

<%
	from ordering.util.mako_filter import b, na, non_qty
	from repoze.what.predicates import in_group
	from ordering.util.common import SPECIAL_VALUE_LIST
%>

<%def name="extTitle()">r-pac - JCPenney</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="/css/flora.datepicker.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/jquery.autocomplete.css" type="text/css" />
<link rel="stylesheet" href="/css/JCP-style.css" type="text/css" />
<link rel="stylesheet" href="/css/thickbox.css" type="text/css" />
<style type="text/css">
	.input-width{
		width : 300px
	}
	
	#warning {
		font:italic small-caps bold 16px/1.2em Arial;
	}
</style>

</%def>

<%def name="extJavaScript()">
<script type="text/javascript" src="/js/numeric.js" language="javascript"></script>
<script type="text/javascript" src="/js/thickbox-compressed.js" language="javascript"></script>
<script type="text/javascript" src="/js/custom/jcp_special_value_edit.js?v=1" language="javascript"></script>
<%
	billToStr = "var billToInfo = {" + ",".join([''''%d':{'company':'%s','address':'%s','attn':'%s','tel':'%s','fax':'%s','email':'%s'}''' %(bt.id,bt.company if bt.company else '',bt.address if bt.address else '',bt.attn if bt.attn else '',bt.tel if bt.tel else '',bt.fax if bt.fax else '',bt.email if bt.email else '') for bt in billTos]) + "};"

	shipToStr = "var shipToInfo = {" + ",".join([''''%d':{'company':'%s','address':'%s','attn':'%s','tel':'%s','fax':'%s','email':'%s'}''' %(st.id,st.company if st.company else '',st.address if st.address else '',st.attn if st.attn else '',st.tel if st.tel else '',st.fax if st.fax else '',st.email if st.email else '') for st in shipTos]) + "};"
	
	mapping = {}
	for c in countries:
		mapping[c.id] = {"name" : c.name, "phone" : c.phone, "data" : []}
		
	for c in contacts:
		m = mapping.get(c.countryId,None)
		if not m : continue
		m["data"].append("{'persion_name' : '%s','persion_email' : '%s'}" %(c.name,c.email))
		
	
	body = ",".join(["%d : {'name':'%s','phone':'%s','person':[%s]}" %( k,v["name"],v["phone"],",".join(v["data"]) )  for k,v in mapping.iteritems() ])
	contactsInfo = "var contactInfo = {%s};" % body

%>


<script language="JavaScript" type="text/javascript">
	//<![CDATA[
    	${billToStr|n}
    	${shipToStr|n}
    	${contactsInfo|n}
    	
    	function getFileName(obj){
		    var tmp = $(obj);
			var path = tmp.val();
			if( path && path.length > 0){
				var location = path.lastIndexOf("\\") > -1 ?path.lastIndexOf("\\") + 1 : 0;
				var fn = path.substr( location,path.length-location );	
				$("#fileName").val(fn);
            }
        }
	//]]>
</script>
<script type="text/javascript" src="/js/custom/jcp_form_ht.js" language="javascript"></script>
</%def>

<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
  	<td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
  	<td width="64" valign="top" align="left"><a href="${return_url}"><img src="/images/images/menu_jcp_g.jpg"/></a></td>
  	% if in_group('Admin') or in_group('JCP'):
    <td width="64" valign="top" align="left"><a href="#" onclick="toConfirm()"><img src="/images/images/menu_confirm_g.jpg"/></a>    </td>
    % endif
    <td width="64" valign="top" align="left"><a href="${return_url}" onclick="return toCancel()"><img src="/images/images/menu_cancel_g.jpg"/></a></td>
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">JCPenney&nbsp;&nbsp;&gt;&nbsp;&nbsp;Order Form</div>
<form id="orderForm" action="/order/saveHTOrder" enctype="multipart/form-data" method="post">
	<input type="hidden" name="msgID" value="${msgHeader.id}"/>
	<input type="hidden" name="hangtag_code" value="${hangtag_code}" />
	<input type="hidden" name="spv_infos" value="" />
  
  <table width="1000" border="0" cellspacing="0" cellpadding="0">
  <tr>
    <td width="15">&nbsp;</td>
    <td>&nbsp;</td>
  </tr>
  <tr>
    <td>&nbsp;</td>
    <td><table width="100%" border="0" cellspacing="0" cellpadding="0">
      <tr>
        <td width="850" align="left" valign="top"><table width="100%" border="0" cellspacing="0" cellpadding="0">
          <tr>
            <td><table width="100%" border="0" cellspacing="0" cellpadding="0">
              <tr>
                <td width="70"><strong>&nbsp;&nbsp;&nbsp;&nbsp;Ship To&nbsp;:</strong></td>
                <td><img src="/images/search_10.jpg" width="330" height="2" /></td>
              </tr>
            </table></td>
            <td><table width="100%" border="0" cellspacing="0" cellpadding="0">
              <tr>
                <td width="70"><strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Bill To&nbsp;:</strong></td>
                <td><img src="/images/search_10.jpg" width="330" height="2" /></td>
              </tr>
            </table></td>
          </tr>
          <tr>
            <td width="50%" valign="top"><table width="100%" border="0" cellspacing="0" cellpadding="0">
              <tr>
                <td width="120">&nbsp;</td>
                <td width="10">&nbsp;</td>
                <td>&nbsp;</td>
              </tr>
              <tr>
                <td height="26" align="right"><img src="/images/search_07.jpg" width="7" height="7" />&nbsp;Company&nbsp;: </td>
                <td>&nbsp;</td>
                <td>
                <select name="shipCompany" class="input-style1-40fonts" id="shipCompany" onchange="changeShipTo(this)">
                	%if order_form:
                		<option value="-1" selected>${order_form.shipCompany|b}</option>
                	%endif
	          		%for st in shipTos:
	          			% if st.is_default == 1 and order_form is None:
	          				<option value="${st.id}" selected>${st.company|b}</option>
	          			% else:
	          				<option value="${st.id}">${st.company|b}</option>
	          			% endif
	          		%endfor
	          		<option value="0">Other</option>
          		</select>
          		<div class="other_shipto" style="display: None;">
          			<br />
          			<input name="other_shipto" type="text" class="input-style1" size="30" />
          		</div>
                </td>
              </tr>
              <tr>
                <td align="right"><img src="/images/search_07.jpg" width="7" height="7" />&nbsp;Address&nbsp;:&nbsp;</td>
                <td>&nbsp;</td>
                <td>
                	<div class="other_shipto" style="display: None;">
          			<br />
          			</div>
                	% if order_form:
                	<textarea name="shipAddress" cols="45" rows="5" class="textarea-style" id="shipAddress">${order_form.shipAddress|b}</textarea>
                	% else:
                	<textarea name="shipAddress" cols="45" rows="5" class="textarea-style" id="shipAddress"></textarea>
                	% endif
                </td>
              </tr>
              <tr>
                <td height="26" align="right">Phone&nbsp;:</td>
                <td>&nbsp;</td>
                <td>
                	% if order_form:
                	<input name="shipTel" type="text" class="input-style1" id="shipTel" size="30" value="${order_form.shipTel|b}" />
                	% else:
                	<input name="shipTel" type="text" class="input-style1" id="shipTel" size="30" />
                	% endif
                </td>
              </tr>
              <tr>
                <td height="26" align="right">Fax&nbsp;:</td>
                <td>&nbsp;</td>
                <td>
                	% if order_form:
                	<input name="shipFax" type="text" class="input-style1" id="shipFax" size="30" value="${order_form.shipFax|b}" />
                	% else:
                	<input name="shipFax" type="text" class="input-style1" id="shipFax" size="30" />
                	% endif
                </td>
              </tr>
              <tr>
                <td height="26" align="right"><img src="/images/search_07.jpg" width="7" height="7" />&nbsp;Contact&nbsp;:</td>
                <td>&nbsp;</td>
                <td>
                	% if order_form:
                	<input name="shipAttn" type="text" class="input-style1" id="shipAttn" size="30" value="${order_form.shipAttn|b}" />
                	% else:
                	<input name="shipAttn" type="text" class="input-style1" id="shipAttn" size="30" />
                	% endif
                	&nbsp;&nbsp;
                	<a href="#" onclick="clearInput(this,['customerPO', 'supplierNO'])"><img src="/images/clear_input.jpg"/></a>
                </td>
              </tr>
              <tr>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
              </tr>
              <tr>
                <td height="26" align="right"><img src="/images/search_07.jpg" width="7" height="7" />&nbsp;Customer PO&nbsp;:</td>
                <td>&nbsp;</td>
                <td><input name="customerPO" type="text" class="input-style1" id="customerPO" size="30" value="${custom_po}" /></td>
              </tr>
              <tr>
                <td height="26" align="right"><img src="/images/search_07.jpg" width="7" height="7" />&nbsp;Supplier #&nbsp;:</td>
                <td>&nbsp;</td>
                <td><input name="supplierNO" type="text" class="input-style1" id="supplierNO" size="30" /></td>
              </tr>
              <tr>
                <td height="26" align="right"><img src="/images/search_07.jpg" width="7" height="7" />&nbsp;&nbsp;<span class="STYLE3">Country of Origin&nbsp;&nbsp;:&nbsp;</td>
                <td>&nbsp;</td>
                <td><select name="origin" class="input-style1-40fonts" id="select">
                	<option value="">&nbsp;</option>
				% for item in country_code:
        			<option value="${item.id}">${item.countryName}</option>
          		% endfor
			</select>
        </span></td>
              </tr>
              <tr>
                <td height="26" align="right">&nbsp;Item Codes&nbsp;:</td>
                <td>&nbsp;</td>
                <td><textarea name="cust_item_codes" class="input-style1" style="width: 280px; height: 50px;"></textarea></td>
              </tr>
               <tr>
			  	<td colspan="2">&nbsp;</td>
			  	<td>&nbsp;</td>
			  </tr>
              <tr>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
              </tr>
            </table></td>
            <td width="50%" valign="top"><table width="100%" border="0" cellspacing="0" cellpadding="0">
              <tr>
                <td width="120">&nbsp;</td>
                <td width="10">&nbsp;</td>
                <td>&nbsp;</td>
              </tr>
              <tr>
                <td height="26" align="right"><img src="/images/search_07.jpg" width="7" height="7" />&nbsp;Company&nbsp;: </td>
                <td>&nbsp;</td>
                <td>
                <select name="billCompany" class="input-style1-40fonts" id="billCompany" onchange="changeBillTo(this)">
                	%if order_form:
                		<option value="-1" selected>${order_form.billCompany|b}</option>
                	%endif
	          		%for bt in billTos:
	          			% if bt.is_default == 1 and order_form is None:
	          				<option value="${bt.id}" selected>${bt.company|b}</option>
	          			% else:
	          				<option value="${bt.id}">${bt.company|b}</option>
	          			% endif
	          		%endfor
	          		<option value="0">Other</option>
          		</select>
          		<div class="other_billto" style="display: None;">
          			<br />
          			<input name="other_billto" type="text" class="input-style1" size="30" />
          		</div>
                </td>
              </tr>
              <tr>
                <td align="right"><img src="/images/search_07.jpg" width="7" height="7" />&nbsp;Address&nbsp;:&nbsp;</td>
                <td>&nbsp;</td>
                <td>
                	<div class="other_billto" style="display: None;">
          			<br />
          			</div>
                	% if order_form:
                	<textarea name="billAddress" cols="45" rows="5" class="textarea-style" id="billAddress">${order_form.billAddress|b}</textarea>
                	% else:
                	<textarea name="billAddress" cols="45" rows="5" class="textarea-style" id="billAddress"></textarea>
                	% endif
                </td>
              </tr>
              <tr>
                <td height="26" align="right">Phone&nbsp;:</td>
                <td>&nbsp;</td>
                <td>
                	% if order_form:
                	<input name="billTel" type="text" class="input-style1" id="billTel" size="30" value="${order_form.billTel|b}" />
                	% else:
                	<input name="billTel" type="text" class="input-style1" id="billTel" size="30" />
                	% endif
                </td>
              </tr>
              <tr>
                <td height="26" align="right">Fax&nbsp;:</td>
                <td>&nbsp;</td>
                <td>
                	% if order_form:
                	<input name="billFax" type="text" class="input-style1" id="billFax" size="30" value="${order_form.billFax|b}" />
                	% else:
                	<input name="billFax" type="text" class="input-style1" id="billFax" size="30" />
                	% endif
                </td>
              </tr>
              <tr>
                <td height="26" align="right"><img src="/images/search_07.jpg" width="7" height="7" />&nbsp;Contact&nbsp;:</td>
                <td>&nbsp;</td>
                <td>
                	% if order_form:
                	<input name="billAttn" type="text" class="input-style1" id="billAttn" size="30" value="${order_form.billAttn|b}" />
                	% else:
                	<input name="billAttn" type="text" class="input-style1" id="billAttn" size="30" />
                	% endif
                	&nbsp;&nbsp;
                	<a href="#" onclick="clearInput(this,['sendEmailTo'])"><img src="/images/clear_input.jpg"/></a>
                </td>
              </tr>
              <tr>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
              </tr>
              <tr>
                <td height="26" align="right"><img src="/images/search_07.jpg" width="7" height="7" />&nbsp;Packaging Country&nbsp;:</td>
                <td>&nbsp;</td>
                <td>
                <select name="sendEmailTo" id="sendEmailTo" class="input-style1-40fonts required-field" onchange="changeCountry(this)">
					<option></option>
					%for c in countries:
					<option value="${c.id}">${c.name}</option>
					%endfor
            	</select>
                </td>
              </tr>
              <tr>
                <td height="26" align="right">Phone :</td>
                <td>&nbsp;</td>
                <td id="country_contact">&nbsp;</td>
              </tr>
			  <tr>
			  	<td height="26" align="right">Mail to :</td>
			  	<td>&nbsp;</td>
			  	<td id="country_mail">&nbsp;</td>
			  </tr>
              <tr>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
              </tr>
            </table></td>
          </tr>
        </table></td>
        <td align="left" valign="bottom" style="padding:120px 0px 0px 0px"><img src="/images/search_03.jpg" width="126" height="121" /></td>
      </tr>
    </table></td>
  </tr>
  <tr>
    <td>&nbsp;</td>
    <td><img src="/images/search_10.jpg" width="970" height="1" /></td>
  </tr>
  <tr>
    <td>&nbsp;</td>
    <td>&nbsp;</td>
  </tr>
  <tr>
    <td>&nbsp;</td>
    <td><table cellspacing="0" cellpadding="0">
      <tr>
        <td valign="top"><strong>Shipping Instructions:</strong></td>
        <td width="20" valign="top">&nbsp;</td>
        <td valign="top"><textarea name="si_intro" class="input-style1" style="width: 300px; height: 50px;"></textarea></td>
        <td valign="top">
        	% if image_url:
        	<a href="/order/ajaxImage?id=${image_url.id}&height=600&width=900" title="Sample Image" class="thickbox">
        		<img src="/images/jcpenney/${image_url.item_code}.jpg" style="width: 200; height: 100;"/>
        	</a>
        	% else:
        	<img src="/images/noimage.jpg" style="width: 200; height: 50;"/>
        	% endif
        </td>
        </tr>
        <tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
        <tr>
        <td valign="top"><strong>Remark:</strong></td>
        <td width="20" valign="top">&nbsp;</td>
        <td valign="top"><textarea name="remark" class="input-style1" style="width: 300px; height: 50px;"></textarea></td>
        <td valign="top">&nbsp;</td>
        </tr>
        <tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
        <tr>
        <td valign="top"><strong>UPLOAD SHOE IMAGE FILE:</strong></td>
        <td width="20" valign="top">&nbsp;</td>
        <td valign="top"><input type="text" name="fileName" id="fileName" readonly="readonly"/><input type="file" name="sampleFile" id="sampleFile" onchange="getFileName(this);"/></td>
        <td valign="top">&nbsp;</td>
        </tr>
    </table></td>
  </tr>
  <tr>
    <td>&nbsp;</td>
    <td>&nbsp;</td>
  </tr>
  <tr>
    <td>&nbsp;</td>
    <td><img src="/images/error.gif"/><br />
    <strong class="title2">Please note:Merchandise Manufacturers are responsible for verifying that all data fields   are populated with the correct information. <br />
    If there are any discrepancies,   please notify retailticket@jcpenney.com.</strong><br /><br />
    <strong class="title2">If the UPC is blank, we will use the 128c as it's UPC, the 128c formula is: Sub + Lot + Line + SizeCode + '0', eg. an item's sub, lot, <br />
    line, size code is: 723, 2000, 0101, 02, then it's 128c code is: 72320000101020.</strong><br /><br />
    <!--strong class="title2">Please pay attention: some fields for RFID item has its characters limit! Please check art work carefully!</strong-->
    </td>
  </tr>
  <tr>
    <td>&nbsp;</td>
    <td><img src="/images/search_10.jpg" width="970" height="1" /></td>
  </tr>
</table>
% if image_url and image_url.item_type == 3:
&nbsp;
% else:
<%include file="ordering.templates.order.new_rfid_selection" />
% endif
<table class="gridTable" border="0" cellpadding="0" cellspacing="0" width="1200">
  <thead>
    <tr>
      <td class="wt-td" align="center" height="35" width="50">Stock</td>
      <td class="wt-td" align="center" width="50">Type</td>
      <td class="wt-td" align="center" width="50">Sub</td>
      <td class="wt-td" align="center" width="50">Lot</td>
      <td class="wt-td" align="center" width="50">Line</td>
      <td class="wt-td" align="center" width="50">Size Code</td>
      <td class="wt-td" align="center" width="120">Description</td>
      <td class="wt-td" align="center" width="80">Brand Type</td>
      <td class="wt-td" align="center" width="100">Color</td>
      <td class="wt-td" align="center" width="80">Size</td>
      <td class="wt-td" align="center" width="50">Cat/Sku</td>
      <td class="wt-td" align="center" width="100">Product ID/Style#</td>
      <td class="wt-td" align="center" width="100">UPC</td>
      <td class="wt-td" align="center" width="80">Misc1</td>
      <td class="wt-td" align="center" width="80">Misc2</td>
      <td class="wt-td" align="center" width="80">Special Value</td>
      <td class="wt-td" align="center" width="100">Retail</td>
      <td class="wt-td" align="center" width="100">2 or More</td>
      <td class="wt-td" align="center" width="100">Quantity</td>
    </tr>
  </thead>
  <tbody>
    %for index,item in enumerate(msgDetail):
    %if index%2==0:
    <tr class="even hangtag">
    %else:
    <tr class="odd hangtag">
    %endif
      <td height="25" class="t-td">${hangtag_code|b}</td>
      <td align="center" class="t-td">Ticket</td>
      <td align="center" class="t-td">${item.Sub|b}</td>
      <td align="center" class="t-td">${item.Lot|b}</td>
      <td align="center" class="t-td">${item.Line|b}</td>
      <td align="center" class="t-td">${item.Sku|b}</td>
      <td align="center" class="t-td">${item.Item_Desc|b}</td>
      <td align="center" class="t-td">${item.Brand_Typ|b}</td>
      <td align="center" class="t-td">${item.Color|b}</td>
      <td align="center" class="t-td">${item.Size|b}</td>
      <td align="center" class="t-td">${item.Ctlg_Xref|na}</td>
      <td align="center" class="t-td">${item.PID|b}</td>
      <td align="center" class="t-td">${item.GTIN|b}</td>
      <td align="center" class="t-td">
      	<input type="text" size="10" name="misc1_${item.id}" style="text-align:right" value="${item.Misc_Txt|b}">
      </td>
      <td align="center" class="t-td">
      	${item.Misc_Txt2|b}
      	% if special_value:
      	<input type="hidden" name="spv_info_${item.id}" value="" />
      	% endif
      </td>
      <td align="center" class="t-td">
      	% if special_value:
      	<a id="SPV_${item.id}" class="SPV_item" href="#" onclick="showDiv(4, ${item.id})">Edit</a>
        % else:
        &nbsp;
        % endif
      </td>
      <td align="center" class="t-td"><input type="text" size="10" name="retail_${item.id}" class="numeric" style="text-align:right" value="${item.Retail}"></td>
      <td align="center" class="t-td">${item.Two_Or_More|b}</td>
      <td align="center" class="bt-td"><input type="text" size="10" name="quantity_${item.id}" class="numeric" value="${item.Quantity|non_qty}" style="text-align:right"></td>
    </tr>
    %if index%2==0:
    <tr class="odd private_brand">
    %else:
    <tr class="even private_brand">
    %endif
      <td height="25" class="t-td">${rfid_mapping_code|b}</td>
      <td align="center" class="t-td">RFID</td>
      <td align="center" class="t-td">${item.Sub|b}</td>
      <td align="center" class="t-td">${item.Lot|b}</td>
      <td align="center" class="t-td">${item.Line|b}</td>
      <td align="center" class="t-td">${item.Sku|b}</td>
      <td align="center" class="t-td">${item.Item_Desc|b}</td>
      <td align="center" class="t-td">${item.Brand_Typ|b}</td>
      <td align="center" class="t-td">${item.Color|b}</td>
      <td align="center" class="t-td">${item.Size|b}</td>
      <td align="center" class="t-td">${item.Ctlg_Xref|na}</td>
      <td align="center" class="t-td">${item.PID|b}</td>
      <td align="center" class="t-td">${item.GTIN|b}</td>
      <td align="center" class="t-td">
      	<input type="text" size="10" name="private_misc1_${item.id}" style="text-align:right" value="${item.Misc_Txt|b}">
      </td>
      <td align="center" class="t-td">
      	${item.Misc_Txt2|b}
      	% if special_value:
      	<input type="hidden" name="private_spv_info_${item.id}" value="" />
      	% endif
      </td>
      <td align="center" class="t-td">
      	% if rfid_special_flag:
      	<a id="private_SPV_${item.id}" class="private_SPV_item" href="#" onclick="showDiv(5, ${item.id})">Edit</a>
        % else:
        &nbsp;
        % endif
      </td>
      <td align="center" class="t-td"><input type="text" size="10" name="private_retail_${item.id}" class="numeric" style="text-align:right" value="${item.Retail}"></td>
      <td align="center" class="t-td">${item.Two_Or_More|b}</td>
      <td align="center" class="bt-td"><input type="text" size="10" name="private_quantity_${item.id}" class="numeric" value="${item.Quantity|non_qty}" style="text-align:right"></td>
    </tr>
    %if index%2==0:
    <tr class="even combo_item">
    %else:
    <tr class="odd combo_item">
    %endif
      %if combo_item and combo_item != 'TBD':
      <td height="25" class="t-td">${combo_item.packaging_code|b}</td>
      %elif combo_item == 'TBD':
      <td height="25" class="t-td">${combo_item|b}</td>
      %else:
      <td height="25" class="t-td">${hangtag_code|b}</td>
      %endif
      <td align="center" class="t-td">Barcode</td>
      <td align="center" class="t-td">${item.Sub|b}</td>
      <td align="center" class="t-td">${item.Lot|b}</td>
      <td align="center" class="t-td">${item.Line|b}</td>
      <td align="center" class="t-td">${item.Sku|b}</td>
      <td align="center" class="t-td">${item.Item_Desc|b}</td>
      <td align="center" class="t-td">${item.Brand_Typ|b}</td>
      <td align="center" class="t-td">${item.Color|b}</td>
      <td align="center" class="t-td">${item.Size|b}</td>
      <td align="center" class="t-td">${item.Ctlg_Xref|na}</td>
      <td align="center" class="t-td">${item.PID|b}</td>
      <td align="center" class="t-td">${item.GTIN|b}</td>
      <td align="center" class="t-td">
      	<input type="text" size="10" name="combo_misc1_${item.id}" style="text-align:right" value="${item.Misc_Txt|b}">
      </td>
      <td align="center" class="t-td">
      	${item.Misc_Txt2|b}
      	% if special_value:
      	<input type="hidden" name="combo_spv_info_${item.id}" value="" />
      	% endif
      </td>
      <td align="center" class="t-td">
      	% if combo_special_flag == True:
      	<a id="combo_SPV_${item.id}" class="combo_SPV_item" href="#" onclick="showDiv(6, ${item.id})">Edit</a>
        % else:
        &nbsp;
        % endif
      </td>
      <td align="center" class="t-td"><input type="text" size="10" name="combo_retail_${item.id}" class="numeric" style="text-align:right" value="${item.Retail}"></td>
      <td align="center" class="t-td">${item.Two_Or_More|b}</td>
      <td align="center" class="bt-td"><input type="text" size="10" name="combo_quantity_${item.id}" class="numeric" value="${item.Quantity|non_qty}" style="text-align:right"></td>
    </tr>
    %endfor
  </tbody>
</table>
<div class="shade"><iframe class="T_iframe"></iframe></div>
<div style="float: left; padding-left: 900px;">
<div>
	<div class="special-value-check">
		<div style="float: left; padding-top: 3px;">
  			<strong class="fonts-c-369">&nbsp;&nbsp;Special Value</strong>
  		</div>
		<div style="float: right; padding-top: 3px;">
		% if image_url:
		<a href="#" onclick="saveDiv()" id="saveDiv"><strong>Save</strong></a>
		% endif
  		&nbsp;&nbsp;
  		<a href="#"  onclick="destroyDiv()"  id="closeDiv"><strong>Close</strong></a>
  		&nbsp;&nbsp;
  		</div>
  		<br />
		<table width="990" border="0" cellspacing="0" cellpadding="0" style="margin:10px 0px 0px 10px">
		% if image_url:
		% for idx in range(image_url.multi_special_value):
		<tr>
			<%
				values = []
				for value in sp_values:
					if value.part == idx + 1:
						values.append(value)
			%>
			<td width="250px;" id="spvalue_${idx}" align="right"><b>SPV Name(Special Value ${idx+1}) :</b>&nbsp;</td>
			<td class="fonts-c-369" valign="top" align="left">
          		<select name="spv_${idx+1}">
          			<option value="x">&nbsp;</option>
          			<option value="n">N/A</option>
          		% for value in values:
        			<option value="${value.id}">${value.value}</option>
        		% endfor
      			</select>
			</td>
		</tr>
		% endfor
		% endif
		<tr>
			<td>&nbsp;</td>
		</tr>
		<tr>
			<td colspan="2"><input type="checkbox" name="spv_copy_all" id="spv_copy_all" value="spv_copy_all"/><label for="spv_copy_all"><span class="fonts-c-369">Checked to save contents for all variable tickets.</span></label><td>
		</tr>
		<tr>
			<td>&nbsp;</td>
		</tr>
		</table>
		% if image_url and image_url.fiber_content == True:
		<table  width="990" border="0" cellspacing="0" cellpadding="0" style="margin:10px 0px 0px 10px; display: None;" class="spv_content">
		<tr><td></td><td></td></tr>
		<tr><td>Please input content and percentage:</td>
		<td>
			<select id="spv_content_part" name="spvcontent_part">
				<option value="2">2</option>
				<option value="3">3</option>
				<option value="4">4</option>
			</select>
		</td>
		</tr>
		% for index in range(1, 5):
		<tr>
			<td width="250px;" align="right"><input id="sp_content_prt_${index}" name="sp_content_prt_${index}" class="numeric" align="right" />%&nbsp;</td>
			<td class="fonts-c-369" valign="top" align="left"><input id="sp_content_${index}" name="sp_content_${index}" align="left" /></td>
		</tr>
		% endfor
		</table>
		% endif
	</div>
	<div class="rfid-special-value-check">
		<div style="float: left; padding-top: 3px;">
  			<strong class="fonts-c-369">&nbsp;&nbsp;Special Value</strong>
  		</div>
		<div style="float: right; padding-top: 3px;">
		% if image_url:
		<a href="#" onclick="saveDiv()" id="saveDiv"><strong>Save</strong></a>
		% endif
  		&nbsp;&nbsp;
  		<a href="#"  onclick="destroyDiv()"  id="closeDiv"><strong>Close</strong></a>
  		&nbsp;&nbsp;
  		</div>
  		<br />
		<table width="990" border="0" cellspacing="0" cellpadding="0" style="margin:10px 0px 0px 10px">
		% if rfid_special_item:
		% for idx in range(rfid_special_item.multi_special_value):
		<tr>
			<%
				values = []
				for value in rfid_special_value:
					if value.part == idx + 1:
						values.append(value)
			%>
			<td width="250px;" id="spvalue_${idx}" align="right"><b>SPV Name(Special Value ${idx+1}) :</b>&nbsp;</td>
			<td class="fonts-c-369" valign="top" align="left">
          		<select name="spv_${idx+1}">
          			<option value="x">&nbsp;</option>
          			<option value="n">N/A</option>
          		% for value in values:
        			<option value="${value.id}">${value.value}</option>
        		% endfor
      			</select>
			</td>
		</tr>
		% endfor
		% endif
		<tr>
			<td>&nbsp;</td>
		</tr>
		<tr>
			<td colspan="2"><input type="checkbox" name="spv_copy_all" id="spv_copy_all" value="spv_copy_all"/><label for="spv_copy_all"><span class="fonts-c-369">Checked to save contents for all variable tickets.</span></label><td>
		</tr>
		<tr>
			<td>&nbsp;</td>
		</tr>
		</table>
		% if image_url and image_url.fiber_content == True:
		<table  width="990" border="0" cellspacing="0" cellpadding="0" style="margin:10px 0px 0px 10px; display: None;" class="spv_content">
		<tr><td></td><td></td></tr>
		<tr><td>Please input content and percentage:</td>
		<td>
			<select id="spv_content_part" name="spvcontent_part">
				<option value="2">2</option>
				<option value="3">3</option>
				<option value="4">4</option>
			</select>
		</td>
		</tr>
		% for index in range(1, 5):
		<tr>
			<td width="250px;" align="right"><input id="sp_content_prt_${index}" name="sp_content_prt_${index}" class="numeric" align="right" />%&nbsp;</td>
			<td class="fonts-c-369" valign="top" align="left"><input id="sp_content_${index}" name="sp_content_${index}" align="left" /></td>
		</tr>
		% endfor
		</table>
		% endif
	</div>
	<div class="combo-special-value-check">
		<div style="float: left; padding-top: 3px;">
  			<strong class="fonts-c-369">&nbsp;&nbsp;Special Value</strong>
  		</div>
		<div style="float: right; padding-top: 3px;">
		% if image_url:
		<a href="#" onclick="saveDiv()" id="saveDiv"><strong>Save</strong></a>
		% endif
  		&nbsp;&nbsp;
  		<a href="#"  onclick="destroyDiv()"  id="closeDiv"><strong>Close</strong></a>
  		&nbsp;&nbsp;
  		</div>
  		<br />
		<table width="990" border="0" cellspacing="0" cellpadding="0" style="margin:10px 0px 0px 10px">
		% if combo_special_item is not None:
		% for idx in range(combo_special_item.multi_special_value):
		<tr>
			<%
				values = []
				for value in combo_special_value:
					if value.part == idx + 1:
						values.append(value)
			%>
			<td width="250px;" id="spvalue_${idx}" align="right"><b>SPV Name(Special Value ${idx+1}) :</b>&nbsp;</td>
			<td class="fonts-c-369" valign="top" align="left">
          		<select name="spv_${idx+1}">
          			<option value="x">&nbsp;</option>
          			<option value="n">N/A</option>
          		% for value in values:
        			<option value="${value.id}">${value.value}</option>
        		% endfor
      			</select>
			</td>
		</tr>
		% endfor
		% endif
		<tr>
			<td>&nbsp;</td>
		</tr>
		<tr>
			<td colspan="2"><input type="checkbox" name="spv_copy_all" id="spv_copy_all" value="spv_copy_all"/><label for="spv_copy_all"><span class="fonts-c-369">Checked to save contents for all variable tickets.</span></label><td>
		</tr>
		<tr>
			<td>&nbsp;</td>
		</tr>
		</table>
		% if image_url and image_url.fiber_content == True:
		<table  width="990" border="0" cellspacing="0" cellpadding="0" style="margin:10px 0px 0px 10px; display: None;" class="spv_content">
		<tr><td></td><td></td></tr>
		<tr><td>Please input content and percentage:</td>
		<td>
			<select id="spv_content_part" name="spvcontent_part">
				<option value="2">2</option>
				<option value="3">3</option>
				<option value="4">4</option>
			</select>
		</td>
		</tr>
		% for index in range(1, 5):
		<tr>
			<td width="250px;" align="right"><input id="sp_content_prt_${index}" name="sp_content_prt_${index}" class="numeric" align="right" />%&nbsp;</td>
			<td class="fonts-c-369" valign="top" align="left"><input id="sp_content_${index}" name="sp_content_${index}" align="left" /></td>
		</tr>
		% endfor
		</table>
		% endif
	</div>
</div>
<br />
% if in_group('Admin') or in_group('JCP'):
<a href="#" onclick="toConfirm()"><img src="/images/images/menu_confirm_g.jpg"/></a>
&nbsp;&nbsp;
% endif
<a href="${return_url}" onclick="return toCancel()"><img src="/images/images/menu_cancel_g.jpg"/></a>
</div>
</form>

