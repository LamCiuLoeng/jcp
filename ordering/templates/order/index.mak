<%inherit file="ordering.templates.master"/>

<%
	from ordering.util.mako_filter import b,tp
	from ordering.util.common import Date2Text
%>

<%def name="extTitle()">r-pac - JCPenney</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="/css/JCP-style.css" type="text/css" />
</%def>

<%def name="extJavaScript()">


<script type="text/javascript" src="/js/jquery-impromptu.1.5.js" language="javascript"></script>
<script type="text/javascript" src="/js/numeric.js" language="javascript"></script>
<script type="text/javascript" src="/js/custom/jcp_index.js?v=1" language="javascript"></script>


<script language="JavaScript" type="text/javascript">
	//<![CDATA[
		
	//]]>
</script>
</%def>

<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
  	<td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
  	<td width="64" valign="top" align="left"><a href="/order/index"><img src="/images/images/menu_jcp_g.jpg"/></a></td>
    <td width="23" valign="top" align="left">
    	<img height="21" width="23" src="/images/images/menu_last.jpg"/>
    </td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">JCPenney&nbsp;&nbsp;&gt;&nbsp;&nbsp;Main</div>
<div style="width:1200px;margin-left:100px;">
	<div style="overflow:hidden;margin:5px 0px 5px 0px">
		<form name="DataTable" class="tableform" method="post" action="index">
		<table width="1000" border="0" cellspacing="0" cellpadding="0">
  <tr>
    <td>&nbsp;</td>
  </tr>
  <tr>
    <td><table width="100%" border="0" cellspacing="0" cellpadding="0">
      <tr>
        <td width="800" align="left" valign="top"><table width="100%" border="0" cellspacing="0" cellpadding="0">
          <tr>
            <td width="30" class="title1">&nbsp;</td>
            <td class="title1">&nbsp;</td>
          </tr>
          <tr>
            <td>&nbsp;</td>
            <td height="50">&nbsp;</td>
          </tr>
          <tr>
            <td>&nbsp;</td>
            <td class="title1">JCP Private Branded Merchandise</td>
          </tr>
          <tr>
            <td>&nbsp;</td>
            <td><table width="100%" border="0" cellspacing="0" cellpadding="0">
              <tr>
                <td width="30" height="25"><input type="radio" name="order_type" id="radio" value="order_by_pom" /></td>
                <td class="title2">Order By JCPenney POM</td>
                </tr>
              </table></td>
          </tr>
          <tr>
            <td>&nbsp;</td>
            <td height="20" valign="top"><img src="/images/search_10.jpg" width="460" height="3" /></td>
          </tr>
          <tr>
            <td>&nbsp;</td>
            <td><table width="100%" border="0" cellspacing="0" cellpadding="0">
              <tr>
                <td width="250" align="right"><label for="DataTable_customerPO"><img src="/images/search_07.jpg" width="7" height="7" />&nbsp;&nbsp;JCPenney Purchase Order #&nbsp;:&nbsp;</label></td>
                <td><input name="poNo" type="text" class="input-style1" id="textfield" size="30" onclick="getRadioChecked('radio')"/></td>
                </tr>
              <tr>
                <td height="14" align="right">&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
              </tr>
              <tr>
                <td align="right"><!--label for="DataTable_customerPO3"><img src="/images/search_07.jpg" width="7" height="7" />&nbsp;&nbsp;Vendor PO #&nbsp;:&nbsp;</label--></td>
                <td><!--input name="pom_customerPO" type="text" class="input-style1" id="pom_customerPO" size="30" onclick="getRadioChecked('radio')"/--></td>
              </tr>
              </table></td>
          </tr>
          <tr>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
          </tr>
          <tr>
            <td>&nbsp;</td>
            <td class="title1" style="padding-left:80px">OR</td>
          </tr>
          <tr>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
          </tr>
          <tr>
            <td>&nbsp;</td>
            <td><table width="100%" border="0" cellspacing="0" cellpadding="0">
              <tr>
                <td width="30" height="25"><input type="radio" name="order_type" id="radio2" value="order_by_sub" /></td>
                <td class="title2">Order By JCP Sub/Lot</td>
              </tr>
            </table></td>
          </tr>
          <tr>
            <td>&nbsp;</td>
            <td height="20" valign="top"><img src="/images/search_10.jpg" width="460" height="3" /></td>
            </tr>
          <tr>
            <td>&nbsp;</td>
            <td><table width="100%" border="0" cellspacing="0" cellpadding="0">
              <!--tr>
                <td width="250" height="26"><img src="/images/search_07.jpg" width="7" height="7" />&nbsp;&nbsp;Vendor PO #&nbsp;:&nbsp;&nbsp;</td>
                <td><input name="sub_customerPO" type="text" class="input-style1" id="sub_customerPO" size="30" onclick="getRadioChecked('radio2')"/></td>
              </tr-->
              <tr>
                <td width="250" height="26" align="right"><label for="DataTable_customerPO7"><img src="/images/search_07.jpg" width="7" height="7" />&nbsp;&nbsp;Sub #&nbsp;:&nbsp;&nbsp; </label></td>
                <td><input name="sub" type="text" class="input-style1-3fonts numeric" id="textfield4" size="30" onclick="getRadioChecked('radio2')"/></td>
              </tr>
              <tr>
                <td width="250" height="26" align="right"><label for="DataTable_customerPO18"><img src="/images/search_07.jpg" width="7" height="7" />&nbsp;&nbsp;Lot #&nbsp;:&nbsp;&nbsp; </label></td>
                <td><input name="lot" type="text" class="input-style1-4fonts numeric" id="textfield8" size="30" onclick="getRadioChecked('radio2')"/></td>
              </tr>
              <!--tr>
                <td height="26" align="right"><label for="DataTable_customerPO8">&nbsp;&nbsp;Line #&nbsp;:&nbsp;&nbsp; </label></td>
                <td><input name="line" type="text" class="input-style1-4fonts numeric" id="textfield5" size="30" onclick="getRadioChecked('radio2')"/></td>
              </tr>
              <tr>
                <td height="26" align="right"><label for="DataTable_customerPO9">&nbsp;&nbsp;Sku #&nbsp;:&nbsp;&nbsp; </label></td>
                <td><input name="sku" type="text" class="input-style1" id="textfield6" size="30" onclick="getRadioChecked('radio2')"/></td>
              </tr-->
              <!--tr>
                <td height="26" align="right"><label for="DataTable_customerPO10"><img src="/images/search_07.jpg" width="7" height="7" />&nbsp;&nbsp;Quantity&nbsp;:&nbsp;&nbsp; </label></td>
                <td><input name="qty" type="text" class="input-style1-10fonts numeric" id="textfield7" size="30" value="0" onclick="getRadioChecked('radio2')"/></td>
              </tr-->
              </table></td>
          </tr>
          <tr>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
          </tr>
          <tr>
            <td>&nbsp;</td>
            <td class="title1" style="padding-left:80px">OR</td>
          </tr>
          <tr>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
          </tr>
          <tr>
            <td>&nbsp;</td>
            <td><table width="100%" border="0" cellspacing="0" cellpadding="0">
              <tr>
                <td width="30" height="25"><input type="radio" name="order_type" id="radio3" value="order_by_manual" /></td>
                <td class="title2">Manual order for NON-Barcoded items including care labels</td>
              </tr>
            </table></td>
          </tr>
          <tr>
            <td>&nbsp;</td>
            <td height="20" valign="top"><img src="/images/search_10.jpg" width="460" height="3" /></td>
          </tr>
          <tr>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
          </tr>
          <tr>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
          </tr>
          <tr>
            <td>&nbsp;</td>
            <td class="title1">JCP National Brands</td>
          </tr>
          <tr>
            <td>&nbsp;</td>
            <td><table width="100%" border="0" cellspacing="0" cellpadding="0">
              <tr>
                <td width="30" height="25"><input type="radio" name="order_type" id="radio4" value="order_for_national" /></td>
                <td class="title2">Manual order for all items including barcodes and care labels</td>
              </tr>
            </table></td>
          </tr>
          <tr>
            <td>&nbsp;</td>
            <td height="20" valign="top"><img src="/images/search_10.jpg" width="460" height="3" /></td>
          </tr>
          <tr>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
          </tr>
          <tr>
            <td>&nbsp;</td>
            <td style="padding-left:300px">
              <input value="Continue" style="width: 150px; color: rgb(0, 0, 0);" type="submit" />
            </td>
          </tr>
        </table></td>
        <td align="left" valign="top" style="padding:80px 0px 0px 0px"><img src="/images/search_03.jpg" width="126" height="121" /></td>
      </tr>
    </table></td>
  </tr>
  <tr>
    <td>&nbsp;</td>
  </tr>
</table>
		</form>
	</div>
</div>

