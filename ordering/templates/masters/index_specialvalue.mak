<%!
	from repoze.what.predicates import in_group
	from ordering.util.mako_filter import active_item
%>
<%inherit file="ordering.templates.master"/>

<%def name="extTitle()">r-pac - Master</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="/css/thickbox.css" type="text/css" />
<link rel="stylesheet" href="/css/jquery.autocomplete.css" type="text/css" />
</%def>

<%def name="extJavaScript()">
	<script type="text/javascript" src="/js/thickbox-compressed.js" language="javascript"></script>
	<script type="text/javascript" src="/js/jquery.autocomplete.pack.js" language="javascript"></script>
	<script type="text/javascript" src="/js/jcp_special_value_ac.js" language="javascript"></script>
	<script language="JavaScript" type="text/javascript">
    //<![CDATA[
		function toSearch(){
			$("form").attr("action", "/specialvalue/index");
			$("form").submit();
		}
		function toExport(){
			$("form").attr("action", "/specialvalue/export");
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
    <td width="64" valign="top" align="left"><a href="#" onclick="toExport();"><img src="/images/images/menu_export_g.jpg"/></a></td>
    <td width="64" valign="top" align="left"><a href="/${funcURL}/add"><img src="/images/images/menu_new_g.jpg"/></a></td>
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
			<tr><td style="text-align:right;border-right:0px;border-bottom:0px"  colspan="100"><span>${tmpl_context.paginators.result.pager()}, &nbsp;&nbsp;Total ${tmpl_context.paginators.result.item_count} records</span></td></tr>
			<tr>
				<th width="150">Item Code</th>
				<th width="150">Packaging Code</th>
				<th width="150">Special Value Part Number</th>
				<th width="150">Special Value</th>
				<th width="150">Path</th>
				<th width="150">Action</th>
			</tr>
		</thead>
		<tbody>
			%for special_value in tmpl_context.paginators.result.items:
			%for item in special_value.items:
			<tr>
				<td>
					%if in_group("Admin"):
					<a href="/${funcURL}/update?id=${special_value.id}">${item.item_code}</a>
					%else:
					${item.item_code}
					%endif
					&nbsp;
				</td>
				<td>${item.packaging_code|active_item}</td>
				<td>${special_value.part}&nbsp;</td>
				<td>${special_value.value}&nbsp;</td>
				<td>${special_value.path}&nbsp;</td>
				<td>
					%if in_group("Admin"):
					<a href="/${funcURL}/update?id=${special_value.id}">Edit</a>
					&nbsp;&nbsp;|&nbsp;&nbsp;
					<a href="/${funcURL}/delete?id=${special_value.id}&item_id=${item.id}">Delete</a>
					%else:
					&nbsp;
					%endif
					&nbsp;
				</td>
			</tr>
			%endfor
			%endfor
			<tr><td style="text-align:right;border-right:0px;border-bottom:0px"  colspan="100"><span>${tmpl_context.paginators.result.pager()}, &nbsp;&nbsp;Total ${tmpl_context.paginators.result.item_count} records</span></td></tr>
		</tbody>
	</table>

%endif

