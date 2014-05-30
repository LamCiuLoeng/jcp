<%!
	from tg.flash import get_flash,get_status
	from repoze.what.predicates import not_anonymous,in_group
%>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title>${self.extTitle()}</title>
	<link href="/images/favicon.ico" type="images/x-icon" rel="shortcut icon" />
	<link href="/css/screen.css" rel="stylesheet" type="text/css" />
	<link href="/css/all.css" rel="stylesheet" type="text/css" />
	${self.extCSS()}

	<script src="/js/jquery.1.7.1.min.js" type="text/javascript"></script>
	<script type="text/javascript" src="/js/jquery-impromptu.1.5.js" language="javascript"></script>
	<script src="/js/menu.js" type="text/javascript"></script>
	
	%if get_flash():
	<script language="JavaScript" type="text/javascript">
	    //<![CDATA[
		  $(document).ready(function(){
		  	%if get_status() == "ok":
		  		$.prompt("${get_flash()}",{opacity: 0.6,prefix:'cleanblue'});
		  	%elif get_status() == "warn":
		  		$.prompt("${get_flash()}",{opacity: 0.6,prefix:'cleanred'});
		  	%endif
		  });
	    //]]>
	</script>
	%endif


	${self.extJavaScript()}

</head>

<body>
	<div id="page-div">
		${self.header()}
		${self.body()}
	</div>
	<div style="clear:both"></div>
	${self.footer()}
</body>

</html>


<%def name="extTitle()">r-pac - rtrack</%def>
<%def name="extCSS()"></%def>
<%def name="extJavaScript()"></%def>

<%def name="header()">
<div>
<table width="100%" border="0" cellspacing="0" cellpadding="0">
  <tr>
    <td width="200" valign="middle"><img src="/images/logo.jpg" width="737" height="72" /></td>
    <td valign="middle" bgcolor="#EDF6FF">
    	<div id="pageLogin"><span class="welcome">Welcome :</span> ${request.identity["user"]} | <a href="/">Home</a> | <a href="/logout_handler">Logout</a> | <a href="/help.html" target="_blank">Help</a></div>
    </td>
  </tr>
</table>
</div>

<div class="menu-tab">
    <ul>
    	% if in_group("JCP") or in_group("Admin") or in_group("JCP_POWER_GROUP"):
        <li class="${'highlight' if tab_focus=='main' else ''}"><a href="/order/index">Main</a></li>
        % endif
        <li class="${'highlight' if tab_focus=='view' else ''}"><a href="/order/search">Tracking</a></li>
        <li class="${'highlight' if tab_focus=='report' else ''}"><a href="/report">Report</a></li>
        % if in_group("AE") or in_group("Admin"):
        <li class="${'highlight' if tab_focus=='master' else ''}"><a href="/master">Master</a></li>
        % endif
        %if in_group("Admin"):
        <li class="${'highlight' if tab_focus=='access' else ''}"><a href="/access">Access</a></li>
        %endif
    </ul>
</div>

<div style="clear:both"></div>

</%def>


<%def name="footer()">
<div id="footer">
	<span style="margin-right:40px">Copyright r-pac International Corp.</span>
</div>
</%def>