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
	
	<script src="/js/jquery-1.3.2.js" type="text/javascript"></script>
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

<%def name="header()"></%def>


<%def name="footer()">
<div id="footer"><span style="margin-right:40px">Copyright r-pac International Corp.</span></div>
</%def>