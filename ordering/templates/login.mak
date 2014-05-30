<%!
	from tg.flash import get_flash,get_status
%>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
    <meta content="text/html; charset=utf-8" http-equiv="content-type">
	<title>r-pac - Login</title>
    <link href="/images/favicon.ico" type="images/x-icon" rel="shortcut icon">   
    <link media="screen" href="/css/screen.css" type="text/css" rel="stylesheet">
    <style type="text/css">
    	body {
			margin-left: 0px;
			margin-top: 0px;
			margin-right: 0px;
			margin-bottom: 0px;
		}
		.nav-tree {
			FONT-WEIGHT: bold; FONT-SIZE: 11px; MARGIN: 5px 0px 0px 10px; FONT-FAMILY: Arial,Helvetica,sans-serif
		}
		a:link {
			font-family: Arial, Helvetica, sans-serif;
			font-size: 10px;
			line-height: normal;
			font-weight: bold;
			text-decoration: underline;
		}
		a:visited {
			font-family: Arial, Helvetica, sans-serif;
			font-size: 10px;
			line-height: normal;
			font-weight: bold;
			text-decoration: underline;
		}
		a:hover {
			font-family: Arial, Helvetica, sans-serif;
			font-size: 10px;
			line-height: normal;
			font-weight: bold;
			text-decoration: underline;
		}
		a:active {
			font-family: Arial, Helvetica, sans-serif;
			font-size: 10px;
			line-height: normal;
			font-weight: bold;
			text-decoration: underline;
		}
		.STYLE2 {
			color: #FF0000;
			font-size: 12px;
			font-family: Arial, Helvetica, sans-serif;
			font-weight: bold;
		}
    </style>
    

    <script src="/js/jquery-1.3.2.js" type="text/javascript"></script>
    <script type="text/javascript" src="/js/jquery-impromptu.1.5.js" language="javascript"></script>
    
    <script type="text/javascript" language="JavaScript">
	//
	    $(document).ready(function(){
	        if ($.browser.msie && $.browser.version <'7.0' ){
				$("#warn_table").show();
			}
	    });
	    
	    function new_register() {
			window.location = "/register";
		}
	//
	</script>
	
	%if get_flash():
	<script language="JavaScript" type="text/javascript">
	    //<![CDATA[
		  $(document).ready(function(){
		  	%if get_status() == "ok":
		  		$.prompt("${get_flash()|n}",{opacity: 0.6,prefix:'cleanblue'});
		  	%elif get_status() == "warn":
		  		$.prompt("${get_flash()|n}",{opacity: 0.6,prefix:'cleanred'});
		  	%endif
		  });
	    //]]>
	</script>
	%endif

</head>
<body onload="document.getElementById('login_name').focus()">
<br/>
<br/>
<br/>
<br/>
<form action="${tg.url('/login_handler', came_from = came_from.encode('utf-8'), __logins = login_counter.encode('utf-8'))}" method="POST">
	<table width="624" border="0" align="center" cellpadding="0" cellspacing="0">
	  <tr>
	    <td width="372" align="left" valign="top"><table width="100%" border="0" cellspacing="0" cellpadding="0">
	      <tr>
	        <td><img src="/images/JCP-login_03.jpg" width="372" height="79" /></td>
	      </tr>
	      <tr>
	        <td style="background:url('/images/JCP-login_08.jpg')"><table width="100%" border="0" cellspacing="0" cellpadding="0">
	          <tr>
	            <td align="left" width="130"><img src="/images/JCP-login_06.jpg" height="112" /></td>
	            <td align="left" valign="top" class="nav-tree" onclick="new_register();" style="background:url('/images/JCP-login_07.jpg')">&nbsp;</td>
	          </tr>
	          
	        </table></td>
	      </tr>
	      <tr>
	        <td height="83" background="images/JCP-login_08.jpg" bgcolor="#FFFFFF" style="padding: 0px 20px 0 20px"><table width="100%" border="0" cellspacing="0" cellpadding="0">
	          <tr>
	            <td width="260"><table width="260" border="0" cellspacing="0" cellpadding="0">
	              <tr>
	                <td height="30"><span class="nav-tree">Login :</span></td>
	                <td align="right"><input id="login_name" style="width: 180px" name="login" /></td>
	              </tr>
	              <tr>
	                <td height="30"><span class="nav-tree">Password :</span></td>
	                <td align="right"><input id="login_password" style="WIDTH: 180px" type="password" name="password" /></td>
	              </tr>
	            </table></td>
	            <td align="right">&nbsp;&nbsp;<input type='image' src="/images/JCP-login_11.jpg" width="55" height="52" /></td>
	          </tr>
	        </table></td>
	      </tr>
	      <tr>
	        <td><img src="/images/JCP-login_14.jpg" width="372" height="29" /></td>
	      </tr>
	      <tr>
	        <td>&nbsp;</td>
	      </tr>
	    </table></td>
	    <td align="left" class="nav-tree" valign="top" background="/images/JCP-login_04.jpg" style="padding:0px 20px 0px 20px; color: red">
	    	<br />
	    	<br />
	    	<br />
	    	<br />
	    	<br />
	    	<br />
	    	<br />
	    	<!--br />
	    	Please note:
	    	<br />
	    	This order is being processed with the new red square retail price format.
	    	<br />
	    	Please verify your retail price point during this transition period at JCP.-->
	    </td>
	    <!--td align="left" valign="top" background="/images/JCP-login_04.jpg"><img src="/images/JCP-login_04.jpg" width="252" height="303" /></td-->
	  </tr>
	</table>
	<table width="600" border="0" align="center" cellpadding="0" cellspacing="0" style="display:none" id="warn_table">
	  <tr>
	    <td><span class="STYLE2">*You are using IE 6,it's recommended to upgrade your browser to IE 7 or higher to get the better view.</span></td>
	  </tr>
	</table>
</form>
    
</body>
</html>