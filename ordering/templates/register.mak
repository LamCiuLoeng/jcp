<%!
	from tg.flash import get_flash,get_status
%>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
    <meta content="text/html; charset=utf-8" http-equiv="content-type">
	<title>r-pac - Register</title>
    <link href="/images/favicon.ico" type="images/x-icon" rel="shortcut icon" />
	<style type="text/css">
		body{
			padding : 0px;
			margin : 0px;
			text-align: center;
			font-family : Verdana,Arial,Helvetica,sans-serif;
			font-size : 14px;
		}
		
		#body-div {
			margin-right: auto;
			margin-left: auto;
			width : 1000px;
			border : 1px solid #eee;
		}
	
		#formDiv {
			margin-right: auto; 
			margin-left: auto;
			text-align : left;
		}
		
		.labeltd {
			width : 200px;
			font-weight : bold;
		}
		
		.inputtext {
			width : 300px;
		}
		
		#footer{
			background-color:#336699;
			clear:both;
			color:#FFFFFF;
			font-family:verdana;
			font-size:10px;
			margin-top:20px;
			padding:5px;
			text-align:right;
		}
		
		.require{
			color:red;
		}
		
		.noted{
			color:#666666;
			font-size:0.76em;
		}
    </style>
	
	
    <script src="/js/jquery-1.3.2.js" type="text/javascript"></script>
    <script type="text/javascript" src="/js/jquery-impromptu.1.5.js" language="javascript"></script>
    
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


	<script language="JavaScript" type="text/javascript">
	//<![CDATA[
		$(document).ready(function(){
			$("form").submit(function(){
				var msg = new Array();
				if(!$("#user_name").val()){
					msg.push("The 'User Name' could not be blank!");
				}
				if ($("#user_name").val().indexOf(" ") > -1) {
					msg.push("The 'User Name' could not contain blank!");
				}
				if(!$("#password").val()){
					msg.push("The 'Password' could not be blank!");
				}
				if($("#password").val()!=$("#repassword").val()){
					msg.push("The 'Password' and 'Confirmed Password' are not match!");
				}
				if(!$("#email_address").val()){
					msg.push("The 'E-mail' could not be blank!");
				}
				
				var emailReg = /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/;
				var emailArr = $("#email_address").val().split(";");
				
				$.each(emailArr, function(index, value) {
				    if(!emailReg.test(value)){
                        msg.push("The 'E-mail' is in a wrong format!");
                    }
				});
				
				if($("select#company option:selected").val() == "None") {
				    if ($("#new_company").val().length <= 0) {
				        msg.push("Please select Company or input your Company Name!");
				    }
				}
				
				if(msg.length > 0){
					alert(msg.join("\n"));
					return false;
				}
				return true;
			});
		});
		
		
		function toCancel(){
			window.location.href = "/index";
		}
		
	//]]>
	</script>
		
</head>
<body>
	<div id="body-div">
		<div id="header">
			<table width="100%" border="0" cellspacing="0" cellpadding="0">
				<tr>
					<td valign="middle">
						<img src="/images/logo.jpg" width="100%" height="72" />
					</td>
				</tr>
			</table>
		</div>
	    <div id="formDiv">
	    	
	    	<form action="/save_register" method="post">
	    		<table align="center" border="0" cellpadding="0" cellspacing="0" width="800px">
	    			<tr>
	    				<td colspan="2">Business Contact Information</td>
	    			</tr>
	    			<tr>
	    				<td>&nbsp;</td>
	    			</tr>
	    			<tr>
	    				<td class="labeltd"><label for="user_name">User Name</label><span class="require">*</span></td><td><input type="text" class="inputtext" name="user_name" id="user_name"/></td>
	    			</tr>
	    			<tr>
			    		<td class="labeltd"><label for="password">Password</label><span class="require">*</span></td><td><input type="password" class="inputtext" name="password" id="password"/></td>
	    			</tr>
	    			<tr>
			    		<td class="labeltd"><label for="repassword">Confirmed Password</label></td><td><input type="password" class="inputtext" name="repassword" id="repassword"/></td>
	    			</tr>
	    			<tr>
			    		<td class="labeltd"><label for="email_address">E-mail</label><span class="require">*</span></td><td><input type="text" class="inputtext" name="email_address" id="email_address"/></td>
	    			</tr>
	    			<tr>
                        <td class="labeltd"><label for="contact">Contact</label><span class="require">*</span></td><td><input type="text" class="inputtext" name="contact" id="contact"/></td>
                    </tr>
                    <tr>
                        <td class="labeltd"><label for="customer">Company</label></td>
                        <td>
                            <%!
                                from ordering.util.common import getCustomer
                                customers = getCustomer()
                            %>
                            <select name="company" id="company">
                                <option value="None">&nbsp;</option>
                                % for customer in customers:
                                <option value="${customer.id}">${customer.name}</option>
                                % endfor
                            </select>
                        </td>
                    </tr>
                    <tr>
                        <td class="labeltd"><label for="billto_address">BillTo Address</label></td><td><input type="text" class="inputtext" name="billto_address" id="billto_address"/></td>
                    </tr>
                    <tr>
                        <td class="labeltd"><label for="billto_tel">BillTo Phone</label></td><td><input type="text" class="inputtext" name="billto_tel" id="billto_tel"/></td>
                    </tr>
                    <tr>
                        <td class="labeltd"><label for="billto_fax">BillTo Fax</label></td><td><input type="text" class="inputtext" name="billto_fax" id="billto_fax"/></td>
                    </tr>
                    <tr>
                        <td class="labeltd"><label for="shipto_address">ShipTo Address</label></td><td><input type="text" class="inputtext" name="shipto_address" id="shipto_address"/></td>
                    </tr>
                    <tr>
                        <td class="labeltd"><label for="shipto_tel">ShipTo Phone</label></td><td><input type="text" class="inputtext" name="shipto_tel" id="shipto_tel"/></td>
                    </tr>
                    <tr>
                        <td class="labeltd"><label for="shipto_fax">ShipTo Fax</label></td><td><input type="text" class="inputtext" name="shipto_fax" id="shipto_fax"/></td>
                    </tr>
	    			<tr>
			    		<td class="labeltd"><label for="new_company">Company(New User)</label></td><td><input type="text" class="inputtext" name="new_company" id="new_company"/></td>
	    			</tr>
	    			<tr>
	    				<td>&nbsp;</td>
	    			</tr>
	    			<tr>
	    				<td colspan="2"><p class="noted">Asterisks (<span class="require">*</span>) indicate fields required to complete this transaction.</p></td>
	    			</tr>
	    			<tr>
	    				<td colspan="2"><p class="noted"><b>Privacy : </b>This data, at any time revocable by you, may be stored by r-pac or an affiliate on an international server and used by r-pac or an affiliate.</p></td>
	    			</tr>
	    			<tr>
	    				<td>&nbsp;</td>
	    			</tr>
	    			<tr>
			    		<td style="text-align:right;" colspan="2"><input type="submit" value="Submit"/>&nbsp;&nbsp;&nbsp;<input type="button" value="Cancel" onclick="toCancel()"/></td>
	    			</tr>
	    		</table>
	    	</form>
	    </div>
	    <div id="footer">
	    	 Copyright r-pac International Corp.
	    </div>
    </div>
</body>
</html>