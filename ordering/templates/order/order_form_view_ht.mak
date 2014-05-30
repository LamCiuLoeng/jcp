<%inherit file="ordering.templates.master"/>

<%
	from ordering.util.mako_filter import b, na
	from ordering.util.common import rpacEncrypt
	from repoze.what.predicates import in_group
%>

<%def name="extTitle()">r-pac - JCPenney</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="/css/flora.datepicker.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/jquery.autocomplete.css" type="text/css" />
<!--
<link rel="stylesheet" href="/css/order_form.css" type="text/css" />
-->
<link href="/css/JCP-style.css" rel="stylesheet" type="text/css" />
<link rel="stylesheet" href="/css/thickbox.css" type="text/css" />
<link rel="stylesheet" href="/css/JCP-style.css" type="text/css" />
</%def>

<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery.columnfilters.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery-impromptu.1.5.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.bgiframe.pack.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.autocomplete.pack.js" language="javascript"></script>
<script type="text/javascript" src="/js/ui.datepicker.js" language="javascript"></script>
<script type="text/javascript" src="/js/thickbox-compressed.js" language="javascript"></script>

<script language="JavaScript" type="text/javascript">
	//<![CDATA[
	$(document).ready(function(){
		var content = $("label#wi_content").text();
		$("a#washinstruction_detail").attr("href","/order/ajaxInstruction?cls=wi"+"&val="+content);
	});
	
	function showFCDiv() {
		$("#fc-addition").slideDown();
	}
	
	function closeFCDiv() {
		$("#fc-addition").slideUp();
	}
	
	function toConfirm() {
		var msg = Array();
		
		if( !$("#rfid_country").val() ){msg.push("* Please select the 'Country'!");}
		
		if( msg.length > 0 ){
			$.prompt(msg.join("<br />"),{opacity: 0.6,prefix:'cleanred'});
			return false;
		}else{
			$.prompt("We are going to confirm the order information in our Production System upon your final confirmation.<br /> \
					 Are you sure to confirm the order now?",
	    			{opacity: 0.6,
	    		 	 prefix:'cleanblue',
	    		 	 buttons:{'Yes':true,'No,Go Back':false},
	    		 	 focus : 1,
	    		 	 callback : function(v,m,f){
	    		 	 if(v){
	    		 		$("form").submit();
	    		 	 }
	    		 	}
	    		}
	    	);
		}
	}
	
	//]]>
</script>
</%def>

<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
  	<td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
  	<td width="64" valign="top" align="left"><a href="${return_url}"><img src="/images/images/menu_jcp_g.jpg"/></a></td>
  	% if in_group("Admin"):
  	<td width="64" valign="top" align="left"><a href="/order/cancelOrder?code=${rpacEncrypt(poheader.id)}"><img src="/images/images/menu_cancel_g.jpg"/></a></td>
  	% endif
  	% if (in_group("Admin") or in_group("AE")) and poheader.status in ['CONFIRM', 'RFID']:
  	<td width="64" valign="top" align="left"><a href="/order/unlockOrder?code=${rpacEncrypt(poheader.id)}"><img src="/images/images/menu_revise_g.jpg"/></a></td>
  	% endif
  	% if (in_group("Admin") or in_group("JCP")) and poheader.status == 'UPDATE':
  	<td width="64" valign="top" align="left"><a href="/order/updateOrder?code=${rpacEncrypt(poheader.id)}"><img src="/images/images/menu_update_g.jpg"/></a></td>
  	% endif
  	% if in_group("Admin") and poheader.orderType == 'AUTO':
  	<td width="64" valign="top" align="left"><a href="/order/exportHTPDFile?code=${rpacEncrypt(poheader.id)}&rfid_flag=${rfid_flag}"><img src="/images/images/menu_export_g.jpg"/></a></td>
  	% endif
  	% if (in_group("AE") or in_group("Admin")) and poheader.status == 'CONFIRM' :
  	<td width="175" valign="top" align="left"><a href="#" onclick="toConfirm()"><img src="/images/images/t2rfid_g.jpg"/></a></td>
  	% endif
  	% if (in_group("Admin") or in_group("AE")) and rfid_url is not None:
  	<td width="175" valign="top" align="left"><a href="${rfid_url}"><img src="/images/images/turn2rfid_g.jpg"/></a></td>
  	% endif
  	<!--td width="64" valign="top" align="left"><a href="/order/viewAttachment?id=${rpacEncrypt(poheader.id)}"><img src="/images/images/menu_attach_g.jpg"/></a></td-->
    <td width="64" valign="top" align="left"><a href="${return_url}"><img src="/images/images/menu_return_g.jpg"/></a></td>
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">JCPenney&nbsp;&nbsp;&gt;&nbsp;&nbsp;Order Form</div>
<form id="orderForm" action="/order/exportRFID" method="post">
<input type="hidden" name="orderID" value="${poheader.id}"/>
  <div style="width:1100px">
  	<table width="1000" border="0" cellspacing="0" cellpadding="0">
  <tr>
    <td width="15">&nbsp;</td>
    <td>&nbsp;</td>
  </tr>
  <tr>
    <td>&nbsp;</td>
    <td><table width="100%" cellspacing="0" cellpadding="0" border="0">
      <tbody><tr>
        <td><table width="100%" cellspacing="0" cellpadding="0" border="0">
          <tbody><tr>
            <td height="40" class="title1">Order Confirmation</td>
            </tr>
          <tr>
            <td class="comment2" style="padding-left: 20px">Your request has been submitted  successfully to for your reference.<br>
              For processing. Thank you for your  order.Please print out this page<br>
              To continue shopping, please select one of  the following Links.</td>
            </tr>
          </tbody></table></td>
        <td><img width="126" height="121" src="/images/search_03.jpg"></td>
      </tr>
    </tbody></table></td>
  </tr>
  <tr>
    <td>&nbsp;</td>
    <td><table width="100%" border="0" cellspacing="0" cellpadding="0">
      <tr>
        <td align="left" valign="top"><table width="100%" border="0" cellspacing="0" cellpadding="0">
          <tr>
            <td><table width="100%" border="0" cellspacing="0" cellpadding="0">
              <tr>
                <td width="70"><strong>&nbsp;&nbsp;&nbsp;&nbsp;Ship To&nbsp;:</strong></td>
                <td><img src="images/search_10.jpg" width="380" height="2" /></td>
                </tr>
              </table></td>
            <td width="10">&nbsp;</td>
            <td><table width="100%" border="0" cellspacing="0" cellpadding="0">
              <tr>
                <td width="70"><strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Bill To&nbsp;:</strong></td>
                <td><img src="images/search_10.jpg" width="380" height="2" /></td>
                </tr>
              </table></td>
            </tr>
          <tr>
            <td width="50%" align="left" valign="top"><table width="100%" border="0" cellspacing="0" cellpadding="0">
              <tr>
                <td width="120">&nbsp;</td>
                <td width="10">&nbsp;</td>
                <td>&nbsp;</td>
                <td width="30">&nbsp;</td>
                </tr>
              <tr>
                <td height="26" align="right" class="title2">Company&nbsp;: </td>
                <td>&nbsp;</td>
                <td class="padding6px">&nbsp;${orderHeder.shipCompany|b}</td>
                <td>&nbsp;</td>
                </tr>
              <tr>
                <td height="26" align="right" class="title2">Address&nbsp;:&nbsp;</td>
                <td>&nbsp;</td>
                <td class="padding6px">&nbsp;${orderHeder.shipAddress|b}</td>
                <td>&nbsp;</td>
                </tr>
              <tr>
                <td height="26" align="right" class="title2">Phone&nbsp;:</td>
                <td>&nbsp;</td>
                <td class="padding6px">&nbsp;${orderHeder.shipTel|b}</td>
                <td>&nbsp;</td>
                </tr>
              <tr>
                <td height="26" align="right" class="title2">Fax&nbsp;:</td>
                <td>&nbsp;</td>
                <td class="padding6px">&nbsp;${orderHeder.shipFax|b}</td>
                <td>&nbsp;</td>
                </tr>
              <tr>
                <td height="26" align="right" class="title2">Contact&nbsp;:</td>
                <td>&nbsp;</td>
                <td class="padding6px">&nbsp;${orderHeder.shipAttn|b}</td>
                <td>&nbsp;</td>
                </tr>
              <tr>
                <td height="26" align="right" class="title2">&nbsp;</td>
                <td>&nbsp;</td>
                <td class="padding6px">&nbsp;</td>
                <td>&nbsp;</td>
              </tr>
              <tr>
                <td height="26" align="right" class="title2">&nbsp;Customer PO&nbsp;:</td>
                <td>&nbsp;</td>
                <td class="padding6px">&nbsp;${orderHeder.customerPO}</td>
                <td>&nbsp;</td>
              </tr>
              <tr>
                <td height="26" align="right" class="title2">&nbsp;Supplier NO&nbsp;:</td>
                <td>&nbsp;</td>
                <td class="padding6px">&nbsp;${orderHeder.supplierNO}</td>
                <td>&nbsp;</td>
              </tr>
              <tr>
                <td height="26" align="right" class="title2"><strong>Country of Origin&nbsp;:</strong></td>
                <td>&nbsp;</td>
                % if country is not None:
                <td class="padding6px">&nbsp;${country.countryName|b}</td>
                % else:
                <td class="padding6px">&nbsp;</td>
                % endif
                <td>&nbsp;</td>
              </tr>
              <tr>
                <td height="26" align="right" class="title2">&nbsp;Ship Instruction&nbsp;:</td>
                <td>&nbsp;</td>
                <td class="padding6px">&nbsp;${orderHeder.shipInstruction}</td>
                <td>&nbsp;</td>
              </tr>
              <tr>
                <td height="26" align="right" class="title2">&nbsp;Item Image&nbsp;:</td>
                <td>&nbsp;</td>
                <td class="padding6px" valign="top" align="left">
                	% if image_url:
        			<a href="/order/ajaxImage?id=${image_url.id}&height=600&width=900" title="Sample Image" class="thickbox">
        				<img src="/images/jcpenney/${image_url.item_code}.jpg" style="width: 200; height: 100;"/>
        			</a>
        			% else:
        			<img src="/images/noimage.jpg" style="width: 200; height: 50;"/>
        			% endif
                </td>
                <td>&nbsp;</td>
              </tr>
              <tr>
                <td height="26" align="right" class="title2">&nbsp;Item Codes&nbsp;:</td>
                <td>&nbsp;</td>
                <td class="padding6px">&nbsp;${orderHeder.cust_item_codes|b}</td>
                <td>&nbsp;</td>
              </tr>
              <tr>
                <td height="26" align="right" class="title2">&nbsp;Remark&nbsp;:</td>
                <td>&nbsp;</td>
                <td class="padding6px">&nbsp;${poheader.remark|b}</td>
                <td>&nbsp;</td>
              </tr>
              </table></td>
            <td>&nbsp;</td>
            <td width="50%" align="left" valign="top"><table width="100%" border="0" cellspacing="0" cellpadding="0">
              <tr>
                <td width="140">&nbsp;</td>
                <td width="10">&nbsp;</td>
                <td>&nbsp;</td>
              </tr>
              <tr>
                <td height="26" align="right" class="title2">Company&nbsp;: </td>
                <td>&nbsp;</td>
                <td class="padding6px">&nbsp;${orderHeder.billCompany|b}</td>
              </tr>
              <tr>
                <td height="26" align="right" class="title2">Address&nbsp;:&nbsp;</td>
                <td>&nbsp;</td>
                <td class="padding6px">&nbsp;${orderHeder.billAddress|b}</td>
              </tr>
              <tr>
                <td height="26" align="right" class="title2">Phone&nbsp;:</td>
                <td>&nbsp;</td>
                <td class="padding6px">&nbsp;${orderHeder.billTel|b}</td>
              </tr>
              <tr>
                <td height="26" align="right" class="title2">Fax&nbsp;:</td>
                <td>&nbsp;</td>
                <td class="padding6px">&nbsp;${orderHeder.billFax|b}</td>
              </tr>
              <tr>
                <td height="26" align="right" class="title2">Contact&nbsp;:</td>
                <td>&nbsp;</td>
                <td class="padding6px">&nbsp;${orderHeder.billAttn|b}</td>
              </tr>
              <tr>
                <td height="26" align="right" class="title2">&nbsp;</td>
                <td>&nbsp;</td>
                <td class="padding6px">&nbsp;</td>
              </tr>
              <tr>
                <td height="26" align="right" class="title2">&nbsp;JCP PO#:</td>
                <td>&nbsp;</td>
                <td class="padding6px">&nbsp;${poheader.poNo}</td>
              </tr>
              <tr>
                <td height="26" align="right" class="title2">&nbsp;Total Quantity:</td>
                <td>&nbsp;</td>
                <td class="padding6px">&nbsp;${poheader.total_qty()}</td>
              </tr>
              <tr>
                <td height="26" align="right" class="title2">&nbsp;Packaging Country:</td>
                <td>&nbsp;</td>
                <td class="padding6px">&nbsp;${poheader.country.name if poheader.country else None}</td>
              </tr>
              <tr>
                <td height="26" align="right" class="title2">&nbsp;Phone:</td>
                <td>&nbsp;</td>
                <td class="padding6px">&nbsp;${poheader.country.phone if poheader.country else None}</td>
              </tr>
              <tr>
                <td height="26" align="right" class="title2">&nbsp;Mail To:</td>
                <td>&nbsp;</td>
                <td class="padding6px">
                	% if poheader.country:
                	% for contact in poheader.country.contacts:
                		&nbsp;<a href="mailto:${contact.email}">${contact.name}</a><br />
                	% endfor
                	% else:
                		&nbsp;
                	% endif
                </td>
              </tr>
              % if (in_group("AE") or in_group("Admin")) and poheader.status == 'CONFIRM':
              <tr>
                <td height="26" align="right" class="title2">&nbsp;Production Country:</td>
                <td>&nbsp;</td>
                <td class="padding6px">
                	<select name="rfid_country" id="rfid_country" class="input-style1-40fonts required-field">
			  		<option></option>
			  		%for c in countries:
			  		<option value="${c.id}">${c.name}</option>
			  		%endfor
			  	</select>
                </td>
              </tr>
              % endif
              <tr>
                <td height="26" align="right" class="title2">&nbsp;SHOE IMAGE:</td>
                <td>&nbsp;</td>
                <td class="padding6px">
                	% if poheader.customer_samples:
                	% for obj in poheader.customer_samples:
                		<a href="/order/download?id=${obj.id}">Download</a><br />
                	% endfor
                	% else:
                		&nbsp;
                	% endif
                </td>
              </tr>
              </table>
              </td>
            </tr>
        </table></td>
        </tr>
    </table></td>
  </tr>
  <tr>
    <td>&nbsp;</td>
    <td><img src="images/search_10.jpg" width="970" height="1" /></td>
  </tr>
</table>
  
  </div>

  <div style="clear:both"><br /></div>

  <table cellspacing="0" cellpadding="0" border="0" width="1500" class="gridTable">
    <thead>
      <tr>
        <td height="35" align="center" width="80" class="wt-td">Stock</td>
        <td align="center" width="60" class="wt-td">Type</td>
        <td align="center" width="60" class="wt-td">Sub</td>
        <td align="center" width="60" class="wt-td">Lot</td>
        <td align="center" width="60" class="wt-td">Line</td>
        <td align="center" width="70" class="wt-td">Size Code</td>
        <td align="center" width="120" class="wt-td">Description</td>
        % if poheader.orderType == 'AUTO':
        <td class="wt-td" align="center" width="80">Brand Type</td>
        % endif
        <td align="center" width="120" class="wt-td">Color</td>
        <td align="center" width="60" class="wt-td">Size</td>
        <td align="center" width="90" class="wt-td">Cat/Sku</td>
        <td align="center" width="150" class="wt-td">Product ID/Style#</td>
        <td align="center" width="120" class="wt-td">UPC</td>
        <td align="center" width="80" class="wt-td">Misc1</td>
        <td align="center" width="80" class="wt-td">Misc2</td>
        <td align="center" width="80" class="wt-td">Special Value</td>
        <td align="center" width="105" class="wt-td">Retail</td>
        <td align="center" width="105" class="wt-td">2 or More</td>
        <td align="center" width="105" class="wt-td">Quantity</td>
        <!-- get epc -->
        <!--td align="center" width="70" class="wt-td">Action</td-->
      </tr>
    </thead>
    <tbody>

	<%
    	podetails.sort(key = lambda x: x.id)
    %>
    %for index,item in enumerate(podetails):
    %if index%2==0:
    <tr class="even">
    %else:
    <tr class="odd">
    %endif
      <td height="25" class="t-td">${item.stock|b}</td>
      % if poheader.orderType == 'AUTO':
      % if item.rfid == 0:
      <td align="center" class="t-td">Ticket</td>
      % elif item.rfid == 1:
      <td align="center" class="t-td">RFID</td>
      % else:
      <td align="center" class="t-td">Barcode</td>
      % endif
      % else:
      <td align="center" class="t-td">&nbsp;</td>
      % endif
      <td align="center" class="t-td">${item.sub|b}</td>
      <td align="center" class="t-td">${item.lot|b}</td>
      <td align="center" class="t-td">${item.line|b}</td>
      <td align="center" class="t-td">${item.sizeCode|b}</td>
      <td align="center" class="t-td">${item.description|b}</td>
      % if poheader.orderType == 'AUTO':
      <td align="center" class="t-td">${item.msgDetail.Brand_Typ|b}</td>
      % endif
      <td align="center" class="t-td">${item.color|b}</td>
      <td align="center" class="t-td">${item.size|b}</td>
      <td align="center" class="t-td">${item.cat|na}</td>
      <td align="center" class="t-td">${item.pid|b}</td>
      <td align="center" class="t-td">${item.upc|b}</td>
      <td align="center" class="t-td">${item.misc1|b}</td>
      <td align="center" class="t-td">${item.misc2|b}</td>
      <td align="center" class="t-td">
      % if item.spvdetails and image_url:
      <a id="fibercontent" class="thickbox" href="/order/ajaxSpecialValues?id=${item.id}&item=${image_url.id}">Special Value(s)</a>
      % endif
      &nbsp;
      </td>
      %if item.retail:
      <td align="center" class="t-td">${item.retail|b}</td>
      %else:
      <td align="center" class="t-td">&nbsp;</td>
      %endif
      <td align="center" class="t-td">${item.specialPrice|b}</td>
      <td align="center" class="t-td">${item.quantity|b}</td>
      ##% if item.upc and item.rfid==1:
      ##<td align="center" class="t-td">
      ##    <a href="/order/getEpc?code=${rpacEncrypt(item.id)}" title="Get EPC"><img src="/images/images/menu_getepc_g.jpg" /></a>
      ##</td>
      ##% else:
      ##<td align="center" class="t-td">&nbsp;</td>
      ##%endif 
    </tr>
    %endfor
    </tbody>
  </table>
</form>