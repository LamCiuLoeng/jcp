<%inherit file="ordering.templates.master"/>

<%def name="extTitle()">r-pac - Master</%def>
<%def name="extCSS()">
<link rel="stylesheet" href="/css/jquery.autocomplete.css" type="text/css" />
<link rel="stylesheet" href="/css/JCP-style.css" type="text/css" />
</%def>
<%def name="extJavaScript()">
	<script type="text/javascript" src="/js/jquery.autocomplete.pack.js" language="javascript"></script>
	<script type="text/javascript" src="/js/jcp_special_value_ac.js" language="javascript"></script>
	<script type="text/javascript" src="/js/custom/jcp_master_item.js" language="javascript"></script>
	<script language="JavaScript" type="text/javascript">
    //<![CDATA[
		function toSave(){
			$("form").submit();
		}
		function toImport(){
			$(".item-artwork").slideDown();
		}
    //]]>
   </script>
</%def>


<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
    <td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
    <td width="176" valign="top" align="left"><a href="/${funcURL}/index"><img src="/images/images/menu_${funcURL}_g.jpg"/></a></td>
    <td width="64" valign="top" align="left"><a href="#" onclick="toSave()"><img src="/images/images/menu_save_g.jpg"/></a></td>
    <td width="64" valign="top" align="left"><a href="#" onclick="toImport()"><img src="/images/images/menu_import_g.jpg"/></a></td>
    <td width="64" valign="top" align="left"><a href="/${funcURL}/index"><img src="/images/images/menu_cancel_g.jpg"/></a></td>
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">Master&nbsp;&nbsp;&gt;&nbsp;&nbsp;New or Update</div>

<div>
	${widget(values,action=saveURL)|n}
</div>





