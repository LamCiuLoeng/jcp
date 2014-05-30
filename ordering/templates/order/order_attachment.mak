<%inherit file="ordering.templates.master"/>

<%
	from ordering.util.mako_filter import b, na
	from repoze.what.predicates import in_group
	from ordering.util.common import rpacEncrypt
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


<script language="JavaScript" type="text/javascript">
    //<![CDATA[

        function deleteConfirm(){
            if ( confirm("The record will be deleted from DB ,are you sure to continue ?") ){
                    return true;
            }else{
                return false;
            }
        }
        
        function getFileName(obj){
		    var tmp = $(obj);
			var path = tmp.val();
			if( path && path.length > 0){
				var location = path.lastIndexOf("\\") > -1 ?path.lastIndexOf("\\") + 1 : 0;
				var fn = path.substr( location,path.length-location );	
				$("#fileName").val(fn);
				
				var filename = $("#fileName").val().toUpperCase();
                if( filename == "" || ! /\.JP(E)?G$/.test( filename) ){
                    alert("Please select a JPG file!");
                    $("#fileName").val("");
                    $("#filePath").val("");
                    return false;
                }
			}
		}
		
		$(document).ready(function(){
			$("form").submit(function(){
				if(!$("input[name='filePath']").val()){
					alert("Please select one file to upload!");
					return false;
				}
			});
		});
        
        function deleteAttachment(obj){
        	url = $(obj).attr("val");
        	$.post(url,
        		   {},
        		   function(data){
        		   	del_item = data.split("_");
        		   	
        		   	if(del_item[1] == "success") {
        		   		$.prompt("Attachment successfully deleted!",{opacity: 0.6,prefix:'cleanblue',show:'slideDown'});
        		   		$(".gridTable tbody tr#" + del_item[0]).remove();
        		   	};
        		   }
        	);
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
    <td width="64" valign="top" align="left"><a href="/order/viewOrder?code=${rpacEncrypt(poHeader.id)}"><img src="/images/images/menu_cancel_g.jpg"/></a></td>
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">JCPenney&nbsp;&nbsp;&gt;&nbsp;&nbsp;Upload Attachment</div>
<div style="margin: 0px 0px 0px 0px; overflow: hidden;">
  	<div style="margin:10px 0px 0px 0px; overflow: hidden;">
		<form action="/order/uploadSample" enctype="multipart/form-data" method="POST">
			<input type="hidden" name="orderID" value="${poHeader.id}"/>    	
			<!--label for="fileName">File Name : </label><input type="text" name="fileName" id="fileName"/>
			<label for="filePath">File Path : </label><input size="60" type="file" name="filePath" id="filePath" onchange="getFileName(this);"/>
			<input type="submit" value="upload"/-->
		
		<div class="case-list-one">
			<ul style="width:750px">
				<li class="label"><label for="fileName">File Name : </label></li>
				<li><input type="text" name="fileName" id="fileName" style="width: 250px;"/></li>
			</ul>
			<ul style="width:750px">
				<li class="label"><label for="filePath">File Path : </label></li>
				<li><input type="file" name="filePath" id="filePath" onchange="getFileName(this);" size="60"/>&nbsp;&nbsp;<input type="Submit" value="Upload"/></li>
			</ul>
		</div>
		</form>
		
	</div>

	<div style="clear:both;"></div>
    <div style="margin:10px 0px 0px 10px;">
    	<table class="gridTable"  cellpadding="0" cellspacing="0">
      		<thead>
      			<th width="150px">Upload Time</th>
      			<th width="100px">Upload User</th>
      			<th width="500px">File Name</th>
      			<th width="100px">Action</th>
      		</thead>
      		<tbody>
      			% if attachments:
      			% for obj in attachments:
      			<tr id="${obj.id}">
      				<td style="border-left:1px solid #ccc">${obj.createdTime}</td>
      				<td>${obj.issuedBy}</td>
      				<td>${obj.name}</td>
      				<td>
      				<!--a href="#" onclick="deleteAttachment(this)" val="/order/deleteAttachment?pid=${poHeader.id}&amp;fid=${obj.id}">Delete</a-->
      				<a href="/order/ajaxImage?id=${obj.id}&height=600&width=900&type=cust" title="Sample Image" class="thickbox">View</a>
      				</td>
      			</tr>
      			% endfor
      			% endif
      		</tbody>
      	</table>
    </div>
</div>
