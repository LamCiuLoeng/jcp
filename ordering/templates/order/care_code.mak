<%inherit file="ordering.templates.wi_master"/>

<%def name="extTitle()">r-pac - JCPenny</%def>

<%def name="extJavaScript()">
<script type="text/javascript">
	$(document).ready(function(){
		$(".care_code tr:even").addClass("double");
	});
</script>
</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="/css/JCP-style.css" type="text/css" />
<style type="text/css">
	.input-width{
		width : 300px
	}
	
	#warning {
		font:italic small-caps bold 16px/1.2em Arial;
	}
	
	tr.double td{  
		background: #CCCCCC;  
	}
</style>

</%def>

<div width="1200" border="0" cellspacing="0" cellpadding="0">
% if code == 'care':
<div id="care_code_grid" style="width: 100%; float: left;">
	<table cellspacing=0 cellpadding=4 width="100%" border=0 >
  <tbody>
    <tr valign=top>
      <td height="72" background="/images/logo1.jpg" class=elpri><b><br>
      </b></td>
    </tr>
    <tr>
      <td><hr noshade size=1></td>
    </tr>
    <tr>
      <td><table width="100%" border="0" cellspacing="0" cellpadding="0">
        <tr>
          <td width="400"><span class="title1" style="padding-left:15px">Care Code Grid</span></td>
          <td align="left"><span class="el">
            <input type=button value="Close Window" onClick="window.opener=null;window.open('','_self');window.close();">
          </span></td>
          </tr>
      </table></td>
    </tr>
    <tr>
      <td><hr noshade size=1></td>
    </tr>
    <tr valign=top>
      <td><table class="care_code" cellspacing="0" cellpadding="3" rules="all"  border="0" width="100%" height="22"  onclick="sortColumn(event)" bgcolor="#FF0000" ;>
        <TR></TR>
        <TR></TR>
        <thead>
          <tr class="title5">
            <th WIDTH="4%"><STRONG>CARE CODE</STRONG></th>
            <th WIDTH="17%">WASHING INSTRUCTIONS</th>
            <th WIDTH="16%">WASH MODIFIERS</th>
            <th WIDTH="18%">BLEACHING/DRY-CLEANING INSTRUCTIONS</th>
            <th WIDTH="15%">DRYING INSTRUCTIONS</th>  
            <th WIDTH="15%">DRYING MODIFIERS</th>
            <th WIDTH="15%">IRONING INSTRUCTIONS</th>
            </tr>
          </thead>
        % for index in range(1, 10):
    		<tr bgcolor="#FAEBD7">
				<td align="center"><strong>[${index}]</strong></td>
				% for idx in range(1, 7):
				% for item in infos:
				% if item.selection == str(index):
				% if int(item.position) == idx:
				<td><font color="#00008B" class="title2">${item.content.split('||')[0]}</font><br />${item.content.split('||')[1]}</td>
				% endif
				% endif
				% endfor
				% endfor
			</tr>
		% endfor
		</table>
	</td>
    </tr>
        </TBODY>
         </TABLE>
</div>
% else:
<div id="special_instruction" style="width:100%; float: left;">
<table cellspacing=0 cellpadding=4 width="100%" border=0 >
  <tbody>
    <tr valign=top>
      <td height="72" background="/images/logo1.jpg" class=elpri><b><br>
      </b></td>
    </tr>
    <tr>
      <td><hr noshade size=1></td>
    </tr>
    <tr>
      <td><table width="100%" border="0" cellspacing="0" cellpadding="0">
        <tr>
          <td width="400"><span class="title1" style="padding-left:15px">Care Code Grid</span></td>
          <td align="left"><span class="el">
            <input type=button value="Close Window" onClick="window.opener=null;window.open('','_self');window.close();">
          </span></td>
          </tr>
      </table></td>
    </tr>
    <tr>
      <td><hr noshade size=1></td>
    </tr>
    <tr valign=top>
      <td><table class="care_code" cellspacing="0" cellpadding="3" rules="all"  border="0" width="100%" height="22" bgcolor="#FF0000" ;>
        <thead>
          <tr class="title5">
            <th WIDTH="4%"><STRONG>CARE CODE</STRONG></th>
            <th WIDTH="96%">WASHING INSTRUCTIONS</th>
            </tr>
        </thead>
        
        % for item in infos:
			% if int(item.position) == 7:
			<tr bgcolor="#FAEBD7">
				<td align="center"><strong>[${item.selection}]</strong></td> 
				<td><font color="#00008B" class="title2">${item.content.split('||')[0]}</font><br />${item.content.split('||')[1]}</td>
			</tr>
			% endif
		% endfor
        </table>
       </td>
    </tr>
     
      </TBODY>
         </TABLE>
</div>
% endif
</div>