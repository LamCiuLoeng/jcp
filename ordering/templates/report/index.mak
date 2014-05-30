<%inherit file="ordering.templates.master"/>

<%def name="extTitle()">r-pac - JCPenney</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="/css/flora.datepicker.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/jquery.autocomplete.css" type="text/css" />
<link rel="stylesheet" href="/css/thickbox.css" type="text/css" />
</%def>

<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery.columnfilters.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery-impromptu.1.5.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.autocomplete.pack.js" language="javascript"></script>
<script type="text/javascript" src="/js/ui.datepicker.js" language="javascript"></script>
<script type="text/javascript" src="/js/custom/jcp_report.js" language="javascript"></script>
    <script language="JavaScript" type="text/javascript">
    //<![CDATA[
          $(document).ready(function(){
                  //Date Picker
              $('.datePicker').datepicker({ firstDay: 1 , dateFormat: 'dd/mm/yy' });
        });
     //]]>
</script>
</%def>

<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
  	<td width="36" valign="top" align="left">
  		<img src="/images/images/menu_start.jpg"/>
  	</td>
  	<td width="64" valign="top" align="left">
  		<a href="/order/index">
  			<img src="/images/images/menu_jcp_g.jpg"/>
  		</a>
  	</td>
    <td width="64" valign="top" align="left">
        <a href="#" onclick="$('form').submit();">
        	<img src="/images/images/menu_export_g.jpg"/>
        </a>
    </td>
    <td width="64" valign="top" align="left">
    	<a href="#" onclick="resetForm();">
    		<img src="/images/images/menu_reset_g.jpg"/>
    	</a>
    </td>
    <td width="56" valign="top" align="left">
    	<a href="#" onclick="historyBack()">
    		<img height="21" width="54" src="/images/images/menu_back_g.jpg"/>
    	</a>
    </td>
    <td width="56" valign="top" align="left">
    	<a href="#" onclick="historyGo()">
    		<img height="21" width="54" src="/images/images/menu_go_g.jpg"/>
    	</a>
    </td>
    <td width="23" valign="top" align="left">
    	<img height="21" width="23" src="/images/images/menu_last.jpg"/>
    </td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">r-pac-JCPenney&nbsp;&nbsp;&gt;&nbsp;&nbsp;Report</div>
<div style="width:1200px;margin:0px;">
	<div style="overflow:hidden;margin:5px 0px 5px 0px">
		<form name="DataTable" class="tableform" method="post" action="report/export/">
			<div>
				${report_form(value=values)|n}
			</div>
		</form>
	</div>
</div>