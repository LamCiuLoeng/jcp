<%!
	from repoze.what.predicates import in_group
%>
<%inherit file="ordering.templates.master"/>

<%def name="extTitle()">r-pac - Master</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="/css/thickbox.css" type="text/css" />
</%def>

<%def name="extJavaScript()">
	<script type="text/javascript" src="/js/thickbox-compressed.js" language="javascript"></script>
	<script language="JavaScript" type="text/javascript">
    //<![CDATA[
		function toSearch(){
			$("form").submit();
		}
    //]]>
   </script>
</%def>


<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
    <td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
    <td width="176" valign="top" align="left"><a href="/${funcURL}/index"><img src="/images/images/menu_${funcURL}_g.jpg"/></a></td>
    <td width="64" valign="top" align="left"><a href="#" onclick="toSearch()"><img src="/images/images/menu_search_g.jpg"/></a></td>
    %if in_group("Admin"):
    <td width="64" valign="top" align="left"><a href="/${funcURL}/add"><img src="/images/images/menu_new_g.jpg"/></a></td>
    %endif
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">Master&nbsp;&nbsp;&gt;&nbsp;&nbsp;Search</div>

<div>
	${searchWidget(values,action=("/%s/index" %funcURL))|n}
</div>

<div style="clear:both"><br /></div>

%if result:

	<table class="gridTable" cellpadding="0" cellspacing="0" border="0" style="width:900px">
		<thead>
			<tr><td style="text-align:right;border-right:0px;border-bottom:0px"  colspan="10"><span>${tmpl_context.paginators.result.pager()}, ${tmpl_context.paginators.result.item_count} records</span></td></tr>
			<tr>
				<th width="150">Sub</th>
				<th width="150">Stock</th>
				<th width="150">RFID Number</th>
				<th width="150">Action</th>
			</tr>
		</thead>
		<tbody>
			%for mappingCode in tmpl_context.paginators.result.items:
			<tr>
				<td>
					%if in_group("Admin"):
					<a href="/${funcURL}/update?id=${mappingCode.id}">${mappingCode.sub}</a>
					%else:
					${mappingCode.sub}
					%endif
					&nbsp;
				</td>
				<td>${mappingCode.stock}&nbsp;</td>
				<td>${mappingCode.rfid}&nbsp;</td>
				<td>
					%if in_group("Admin"):
					<a href="/${funcURL}/delete?id=${mappingCode.id}">Delete</a>
					%else:
					&nbsp;
					%endif
					&nbsp;
				</td>
			</tr>
			%endfor
			<tr><td style="text-align:right;border-right:0px;border-bottom:0px"  colspan="10"><span>${tmpl_context.paginators.result.pager()}, ${tmpl_context.paginators.result.item_count} records</span></td></tr>
		</tbody>
	</table>

%endif

