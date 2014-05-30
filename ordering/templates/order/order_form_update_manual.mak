<%inherit file="ordering.templates.master"/>

<%
	from ordering.util.mako_filter import b, na
	from repoze.what.predicates import in_group
	from ordering.util.common import SPECIAL_VALUE_LIST
%>

<%def name="extTitle()">r-pac - JCPenny</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="/css/flora.datepicker.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/jquery.autocomplete.css" type="text/css" />
<!--
<link rel="stylesheet" href="/css/order_form.css" type="text/css" />
-->
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
<script type="text/javascript" src="/js/jquery-impromptu.1.5.js" language="javascript"></script>
<script type="text/javascript" src="/js/ui.datepicker.js" language="javascript"></script>
<script type="text/javascript" src="/js/numeric.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.validate.js" language="javascript"></script>
<script type="text/javascript" src="/js/thickbox-compressed.js" language="javascript"></script>
<script type="text/javascript" src="/js/order_form_edit.js" language="javascript"></script>

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
	contactInfo = "var contactInfo = {%s};" % body

%>


<script language="JavaScript" type="text/javascript">
	//<![CDATA[
    	${billToStr|n}
    	${shipToStr|n}
    	${contactInfo|n}
	//]]>
</script>

<script type="text/javascript" src="/js/custom/jcp_form_manual.js?v=1" language="javascript"></script>

</%def>

<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
  	<td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
  	<td width="64" valign="top" align="left"><a href="${return_url}"><img src="/images/images/menu_jcp_g.jpg"/></a></td>
  	% if in_group('Admin') or in_group('JCP'):
    <td width="64" valign="top" align="left"><a class="confirm" href="#" onclick="toConfirm()"><img src="/images/images/menu_confirm_g.jpg"/></a></td>
    % endif
    <td width="64" valign="top" align="left"><a href="${return_url}" onclick="return toCancel()"><img src="/images/images/menu_cancel_g.jpg"/></a></td>
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">JCPenny&nbsp;&nbsp;&gt;&nbsp;&nbsp;Order Form</div>

<form id="orderForm" action="/order/saveManualUpdate" method="post">
	<input type="hidden" name="po_id" value="${poheader.id}">
	<input type="hidden" name="form_id" value="${orderHeader.id}">
	<input type="hidden" name="fc_infos" value="" />
	<input type="hidden" name="wi_infos" value="" />
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
            <td width="50%"><table width="100%" border="0" cellspacing="0" cellpadding="0">
              <tr>
                <td width="120">&nbsp;</td>
                <td width="10">&nbsp;</td>
                <td>&nbsp;</td>
              </tr>
              <tr>
                <td height="26" align="right">Company&nbsp;: </td>
                <td>&nbsp;</td>
                <td>
                <select name="shipCompany" class="input-style1-40fonts" id="shipCompany" onchange="changeShipTo(this)">
                	<option value="-1" selected>${orderHeader.shipCompany}</option>
	          		%for st in shipTos:
	          		<option value="${st.id}">${st.company}</option>
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
                <td align="right">Address&nbsp;:&nbsp;</td>
                <td>&nbsp;</td>
                <td>
                	<div class="other_shipto" style="display: None;">
          			<br />
          			</div>
                	<textarea name="shipAddress" cols="45" rows="5" class="textarea-style" id="shipAddress">${orderHeader.shipAddress}</textarea>
                </td>
              </tr>
              <tr>
                <td height="26" align="right">Phone&nbsp;:</td>
                <td>&nbsp;</td>
                <td>
                	<input name="shipTel" type="text" class="input-style1" id="shipTel" size="30" value="${orderHeader.shipTel}" />
                </td>
              </tr>
              <tr>
                <td height="26" align="right">Fax&nbsp;:</td>
                <td>&nbsp;</td>
                <td>
                	<input name="shipFax" type="text" class="input-style1" id="shipFax" size="30" value="${orderHeader.shipFax}" />
                </td>
              </tr>
              <tr>
                <td height="26" align="right">Contact&nbsp;:</td>
                <td>&nbsp;</td>
                <td>
                	<input name="shipAttn" type="text" class="input-style1" id="shipAttn" size="30" value="${orderHeader.shipAttn}" />
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
                <td><input name="customerPO" type="text" class="input-style1" id="customerPO" size="30" value="${orderHeader.customerPO}" /></td>
              </tr>
              <tr>
                <td height="26" align="right">Supplier NO&nbsp;:</td>
                <td>&nbsp;</td>
                <td><input name="supplierNO" type="text" class="input-style1" id="supplierNO" size="30" value="${orderHeader.supplierNO}" /></td>
              </tr>
              <tr>
                <td height="26" align="right">&nbsp;Item Codes&nbsp;:</td>
                <td>&nbsp;</td>
                <td><textarea name="cust_item_codes" class="input-style1" style="width: 280px; height: 50px;">${orderHeader.cust_item_codes}</textarea></td>
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
            <td width="50%"><table width="100%" border="0" cellspacing="0" cellpadding="0">
              <tr>
                <td width="120">&nbsp;</td>
                <td width="10">&nbsp;</td>
                <td>&nbsp;</td>
              </tr>
              <tr>
                <td height="26" align="right">Company&nbsp;: </td>
                <td>&nbsp;</td>
                <td>
                <select name="billCompany" class="input-style1-40fonts" id="billCompany" onchange="changeBillTo(this)">
                	<option value="-1" selected>${orderHeader.billCompany}</option>
	          		%for bt in billTos:
	          		<option value="${bt.id}">${bt.company}</option>
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
                <td align="right">Address&nbsp;:&nbsp;</td>
                <td>&nbsp;</td>
                <td>
                	<div class="other_billto" style="display: None;">
          			<br />
          			</div>
                	<textarea name="billAddress" cols="45" rows="5" class="textarea-style" id="billAddress">${orderHeader.billAddress}</textarea>
                </td>
              </tr>
              <tr>
                <td height="26" align="right">Phone&nbsp;:</td>
                <td>&nbsp;</td>
                <td>
                	<input name="billTel" type="text" class="input-style1" id="billTel" size="30" value="${orderHeader.billTel}" />
                </td>
              </tr>
              <tr>
                <td height="26" align="right">Fax&nbsp;:</td>
                <td>&nbsp;</td>
                <td>
                	<input name="billFax" type="text" class="input-style1" id="billFax" size="30" value="${orderHeader.billFax}" />
                </td>
              </tr>
              <tr>
                <td height="26" align="right">Contact&nbsp;:</td>
                <td>&nbsp;</td>
                <td>
                	<input name="billAttn" type="text" class="input-style1" id="billAttn" size="30" value="${orderHeader.billAttn}" />
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
						%if c.name == poheader.country.name:
						<option value="${c.id}" selected>${c.name}</option>
						%else: 
						<option value="${c.id}">${c.name}</option>
						%endif
						%endfor
            		</select>
                </td>
              </tr>
              <tr>
                <td height="26" align="right">Phone :</td>
                <td>&nbsp;</td>
                <td id="country_contact">&nbsp;${poheader.country.phone}</td>
              </tr>
			  <tr>
			  	<td height="26" align="right">Mail to :</td>
			  	<td>&nbsp;</td>
			  	<td id="country_mail">
			  		% if poheader.country:
                	% for contact in poheader.country.contacts:
                		&nbsp;<a href="mailto:${contact.email}">${contact.name}</a><br />
                	% endfor
                	% else:
                		&nbsp;
                	% endif
			  	</td>
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
    <td><table width="100%" border="0" cellpadding="0" cellspacing="0">
      <tr>
        <td height="28"><label class="title1">VARIABLE DATA</label></td>
        </tr>
      <tr>
        <td><img src="/images/search_07.jpg" width="7" height="7" />&nbsp;&nbsp;<strong><span class="STYLE3">Country of Origin&nbsp;&nbsp;:&nbsp;
			<select name="origin" class="input-style1-40fonts" id="select">
				% for item in country_code:
				% if item.id == int(orderHeader.origin):
					<option value="${item.id}" selected>${item.countryName}</option>
				% else:
					<option value="${item.id}">${item.countryName}</option>
				% endif
          		% endfor
			</select>
        </span></strong></td>
      </tr>
      <tr>
        <td>&nbsp;</td>
      </tr>
      <tr>
        <td><img src="/images/search_07.jpg" width="7" height="7" />&nbsp;&nbsp;<strong>MFG RN#:</strong>
          <input gtbfieldid="90" name="rnCode" id="rnCode" value="${orderHeader.rnCode}" class="input-style1" type="text" />&nbsp;
  	  		<span class="title1">OR</span>&nbsp;&nbsp;&nbsp;&nbsp;<strong>JCP WPL#:</strong> &nbsp;
            <input name="wplCode" type="text" class="input-style1" id="wplCode" value="${orderHeader.wplCode}" gtbfieldid="91" />&nbsp;(Enter either MFG RN# or JCP WPL#)</td>
      </tr>
      <tr>
        <td>&nbsp;</td>
      </tr>
    </table></td>
  </tr>
  <tr>
    <td>&nbsp;</td>
    <td><table cellspacing="0" cellpadding="0">
      <tr>
        <td valign="top"><strong>Shipping Instructions:</strong></td>
		<td width="20">&nbsp;</td>
		<td><textarea name="shipInstruction" class="input-style1" style="width: 300px; height: 50px;">${orderHeader.shipInstruction}</textarea></td>
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
    If there are any discrepancies,   please notify retailticket@jcpenney.com.</strong></td>
  </tr>
  <tr>
    <td>&nbsp;</td>
    <td><img src="/images/search_10.jpg" width="970" height="1" /></td>
  </tr>
</table>
  <div class="shade"><iframe class="T_iframe"></iframe></div>
  <div>
  <div class="fc-addition-check thickbox" style="display:none">
  	<div style="float: right">
  		<a href="#" onclick="saveFCJSON();"><strong>Save</strong></a>
  		&nbsp;&nbsp;
  		<!--a href="#" onclick="saveFCJSONToAll();"><strong>Save All</strong></a>
  		&nbsp;&nbsp;  -->
  		<a href="#" onclick="closeDiv('FC');"><strong>Close</strong></a>&nbsp;&nbsp;
  	</div>
  <table width="990" border="0" cellspacing="0" cellpadding="0" style="margin:10px 0px 0px 10px">
  <tr>
    <td height="25" class="fonts-14pt fonts-c-036">Fiber Content</td>
    <td>&nbsp;</td>
    <td class="fonts-14pt fonts-c-036">&nbsp;</td>
  </tr>
  <tr>
    <td><table>
      <tbody>
        <tr>
          <td><span class="fonts-c-369">Exclusive data:</span></td>
          <td><span class="fonts-c-369">
            <select name="fc_exclusive_data">
				<%
					exclusives = ['None', 'Exclusive of Decoration', 'Exclusive of Elastic', 'Exclusive of Decoration and Exclusive of Elastic',]
				%>
          		% for i in range(4):
        			<option value="${exclusives[i]}">${exclusives[i]}</option>
        		% endfor
      		</select>
          </span></td>
        </tr>
        <tr>
          <td align="right"><span class="fonts-c-369">
            <input type="checkbox" name="fc_cotton_logo" id="fc_cotton_logo" value="true" onclick="setValue(this)" />
          </span></td>
          <td><span class="fonts-c-369">
            <label for="fc_cotton_logo">Cotton Logo(Optional)</label>
          </span></td>
        </tr>
        <tr>
          <td align="right"><span class="fonts-c-369">
            <input type="checkbox" name="fc_lycra_logo" id="fc_lycra_logo" value="true" onclick="setValue(this)" />
          </span></td>
          <td><span class="fonts-c-369">
            <label for="fc_lycra_logo">Lycra Logo(Optional)</label>
          </span></td>
        </tr>
        <tr>
          <td><span class="fonts-c-369">Components or Colors:</span></td>
          <td><span class="fonts-c-369">
            <select name="fc_components" onchange="showFCComponents(this.options[this.options.selectedIndex].value)">
				<option selected value="0">&nbsp;</option>
				<option value="1">Single Component or Color</option>
          		% for i in range(2, 7):
        		<option value="${i}">Multiple - ${i} Components or Colors</option>
        		% endfor
      		</select>
          </span></td>
        </tr>
      </tbody>
    </table></td>
    <td>&nbsp;</td>
    <td>&nbsp;</td>
  </tr>
  <tr>
    <td align="left" valign="top" colspan="3">&nbsp;</td>
  </tr>
  <tr>
  	<td><input type="checkbox" name="fc_copy_all" id="fc_copy_all" value="fc_copy_all"/><label for="fc_copy_all"><span class="fonts-c-369">Checked to save contents for all variable tickets.</span></label></td>
  </tr>
  <tr>
    <td align="left" valign="top" colspan="3"><hr noShade size=1 style="padding-bottom: 2px;"/></td>
  </tr>
  </table>
</div>
</div>
<div>
	<div class="wi-addition-check">
		<div style="float: left">
  			<strong class="fonts-c-369">&nbsp;&nbsp;Washing Instruction</strong>
  		</div>
		<div style="float: right">
		<a href="/order/showCode?code=care" target="_blank"><strong>Check All Care Code</strong></a>
		&nbsp;&nbsp;
		<a href="/order/showCode?code=special" target="_blank"><strong>Check All Special Code</strong></a>
		&nbsp;&nbsp;
		<a href="#" onclick="saveWIJSON();"><strong>Save</strong></a>
  		&nbsp;&nbsp;
  		<!--a href="#" onclick="saveWIJSONToAll();"><strong>Save All</strong></a>
  		&nbsp;&nbsp;  -->
  		<a href="#" onclick="closeDiv('WI');"><strong>Close</strong></a>
  		&nbsp;&nbsp;
  		</div>
  		<br />
		<table  width="990" border="0" cellspacing="0" cellpadding="0" style="margin:10px 0px 0px 10px">
		<%
			label = ['Washing Instructions','Wash Modifiers','Beaching, Dry Cleaning Instructions','Drying Instructions','Drying Modifiers','Ironing Instructions','Special Instructions',]
		%>
		% for idx in range(1, 7):
		<tr>
			<td width="250px;" class="fonts-c-369" valign="top">
          		<select name="wi_${idx}" onchange="showIntro('wi_${idx}');">
          			<option value="0">&nbsp;</option>
          		% for i in range(1, 10):
        			<option value="${i}">${i}</option>
        		% endfor
      			</select>
      			&nbsp;${label[idx - 1]}&nbsp;:
			</td>
			<td id="wi_intro_${idx}">&nbsp;</td>
		</tr>
		% endfor
		<tr>
			<td width="250px;" class="fonts-c-369" valign="top">
        	<%
        		items = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O",
        				 "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC", "AD"]
        	%>
        	<select name="wi_7", onchange="showIntro('wi_7');">
        		<option value="0">&nbsp;</option>
        		% for item in items:
          		<option value="${item}">${item}</option>
          		% endfor
        	</select>
        	&nbsp;${label[idx]}&nbsp;:
			</td>
			<td id="wi_intro_7">&nbsp;</td>
		</tr>
		<tr>
			<td>&nbsp;</td>
		</tr>
		<tr>
			<td colspan="2"><input type="checkbox" name="wi_copy_all" id="wi_copy_all" value="wi_copy_all"/><label for="wi_copy_all"><span class="fonts-c-369">Checked to save contents for all variable tickets.</span></label><td>
		</tr>
		<tr>
			<td>&nbsp;</td>
		</tr>
		</table>
	</div>
</div>
  <div style="clear:both">
	<input type="image" src="/images/new_item.jpg" onclick="toAdd();return false;"/>
  </div>
  
  
	<br />
  
  <table cellspacing="0" cellpadding="0" border="0" class="gridTable">
    <thead>
      <tr>

        <td height="35" align="center" width="80" class="wt-td">Stock</td>
        <td align="center" width="60" class="wt-td">Sub</td>
        <td align="center" width="60" class="wt-td">Lot</td>
        <td align="center" width="60" class="wt-td">Line</td>
        <td align="center" width="70" class="wt-td">Size Code</td>
        <td align="center" width="120" class="wt-td">Lot Description</td>
        <td align="center" width="120" class="wt-td">Fiber Content</td>
      	<td align="center" width="120" class="wt-td">Washing Instruction</td>
        <td align="center" width="120" class="wt-td">Color</td>
        <td align="center" width="60" class="wt-td">Size</td>
        <td align="center" width="90" class="wt-td">Cat/Sku</td>
        <td align="center" width="150" class="wt-td">Product ID/Style#</td>
        <td align="center" width="120" class="wt-td">UPC</td>
        <td align="center" width="80" class="wt-td">Special Value</td>
        <td align="center" width="105" class="wt-td">Retail</td>
        <td align="center" width="105" class="wt-td">Quantity</td>
  	
      </tr>
    </thead>
    <tbody>
	%for detail in podetails:
   <tr>
      <td height="25" class="t-td"><input type="text" class="required" name="stock_${detail.id}_ext" onblur="check_status(this);" value="${detail.stock}" style="width:40px"/></td>
      <td align="center" class="t-td"><input type="text" class="required" name="sub_${detail.id}_ext" value="${detail.sub}" style="width:40px"/></td>
      <td align="center" class="t-td"><input type="text" class="numeric" name="lot_${detail.id}_ext" value="${detail.lot}" style="width:50px"/></td>
      <td align="center" class="t-td"><input type="text" name="line_${detail.id}_ext" value="${detail.line}" style="width:40px"/></td>
      <td align="center" class="t-td"><input type="text" name="sizeCode_${detail.id}_ext" value="${detail.sizeCode}" style="width:80px"/></td>
      <td align="center" class="t-td"><input type="text" class="required" name="description_${detail.id}_ext" value="${detail.description}"/></td>
      <td align="center" class="t-td"><a id="FC_${detail.id}" class="FC_item" href="#" onclick="showFCDiv(this, ${detail.id})">Edit</a></td>
      <td align="center" class="t-td"><a id="WI_${detail.id}" class="WI_item" href="#" onclick="showWIDiv(this, ${detail.id})">Edit</a></td>
      <td align="center" class="t-td"><input type="text" name="colorCode_${detail.id}_ext" value="${detail.color}" style="width:100px"/></td>
      <td align="center" class="t-td"><input type="text" name="size_${detail.id}_ext" value="${detail.size}" style="width:80px"/></td>
      <td align="center" class="t-td"><input type="text" name="cat_${detail.id}_ext" value="${detail.cat}" style="width:100px"/></td>
      <td align="center" class="t-td"><input type="text" name="styleNo_${detail.id}_ext" value="${detail.pid}"/></td>
      <td align="center" class="t-td"><input type="text" name="upc_${detail.id}_ext" value="${detail.upc}" style="width:100px"/></td>
      <td align="center" class="t-td">
      % if special_value:
      	<select name="specialValue_${detail.id}_ext" id="specialValue_${detail.id}_ext">
      		%for value in SPECIAL_VALUE_LIST:
      		%if detail.specialValue == value:
      			<option value="${value}" selected>${value}</option>
      		%else:
      			<option value="${value}">${value}</option>
      		%endif
      		%endfor
         </select>
      % else:
      	&nbsp;
      % endif
      </td>
      <td align="center" class="t-td"><input type="text" class="required numeric" name="retail_${detail.id}_ext" value="${detail.retail}" style="text-align:right;width:100px;"></td>
      <td align="center" class="bt-td">
      	<input type="text" class="required numeric" name="quantity_${detail.id}_ext" value="${detail.quantity}" style="text-align:right;width:100px;">
      	<input type="hidden" name="detail_id_${detail.id}" value="${detail.id}">
      	<input type="hidden" name="fc_info_${detail.id}" value="" />
		<input type="hidden" name="wi_info_${detail.id}" value="" />
      </td>
    </tr>
    %endfor


    <tr class="template" style="display:none">
      <td height="25" class="t-td"><input type="text" name="stock_x_ext" onblur="check_status(this);" value="" style="width:40px"/></td>
      <td align="center" class="t-td"><input type="text" name="sub_x_ext" value="" style="width:40px"/></td>
      <td align="center" class="t-td"><input type="text"name="lot_x_ext" value="" class="numeric" style="width:50px"/></td>
      <td align="center" class="t-td"><input type="text" name="line_x_ext" value="" style="width:40px"/></td>
      <td align="center" class="t-td"><input type="text" name="sizeCode_x_ext" value="" style="width:80px"/></td>
      <td align="center" class="t-td"><input type="text" name="description_x_ext" value=""/></td>
      <td align="center" class="t-td"><a id="FC_x" class="FC_item" href="#" onclick="showFCDiv(this, x)">Edit</a></td>
      <td align="center" class="t-td"><a id="WI_x" class="WI_item" href="#" onclick="showWIDiv(this, x)">Edit</a></td>
      <td align="center" class="t-td"><input type="text" name="colorCode_x_ext" value="" style="width:100px"/></td>
      <td align="center" class="t-td"><input type="text" name="size_x_ext" value="" style="width:80px"/></td>
      <td align="center" class="t-td"><input type="text" name="cat_x_ext" value="" style="width:100px"/></td>
      <td align="center" class="t-td"><input type="text" name="styleNo_x_ext" value=""/></td>
      <td align="center" class="t-td"><input type="text" name="upc_x_ext" value="" style="width:100px"/></td>
      <td align="center" class="t-td">
      	% if special_value:
      	<select name="specialValue_x_ext" id="specialValue_x_ext">
      		%for value in SPECIAL_VALUE_LIST:
      		%if detail.specialValue == value:
      			<option value="${value}" selected>${value}</option>
      		%else:
      			<option value="${value}">${value}</option>
      		%endif
      		%endfor
         </select>
      % else:
      	&nbsp;
      % endif
      </td>
      <td align="center" class="t-td"><input type="text" size="14" name="retail_x_ext" style="text-align:right;width:100px"></td>
      <td align="center" class="bt-td">
      	<input type="text" name="quantity_x_ext" style="text-align:right;width:100px;">
      	<input type="hidden" name="fc_info_x" value="" />
		<input type="hidden" name="wi_info_x" value="" />
      </td>
    </tr>
    </tbody>
  </table>
<div style="float: left; padding-left: 900px;">
<br />
% if in_group('Admin') or in_group('JCP'):
<a class="confirm" href="#" onclick="toConfirm()"><img src="/images/images/menu_confirm_g.jpg"/></a>
&nbsp;&nbsp;
% endif
<a href="${return_url}" onclick="return toCancel()"><img src="/images/images/menu_cancel_g.jpg"/></a>
</div>
</form>