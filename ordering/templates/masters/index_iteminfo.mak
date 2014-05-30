<%!
	from repoze.what.predicates import in_group
	from ordering.util.mako_filter import status_show
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
			$("form").attr("action", "/iteminfo/index");
			$("form").submit();
		}
		function toExport(){
			$("form").attr("action", "/iteminfo/export");
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
				<th width="150">Status</th>
				<th width="150">Washing Instruction</th>
				<th width="150">Fiber Content</th>
				<th width="150">Country of Origin</th>
				<th width="150">Matchbook/Barcoded Combo</th>
				<th width="150">Combo Packaging Code</th>
				<th width="150">Combo Items</th>
				<th width="150">Item 1 packaging code</th>
				<th width="150">Item 2 packaging code</th>
				<th width="150">Special Value</th>
				<th width="150">Special Value Part</th>
				<th width="150">Artwork</th>
			</tr>
		</thead>
		<tbody>
			%for u in tmpl_context.paginators.result.items:
			<tr>
				<td>
					%if in_group("Admin") or in_group("AE"):
					<a href="/${funcURL}/update?id=${u.id}">${u.item_code}</a>
					%else:
					${u.item_code}
					%endif
					&nbsp;
				</td>
				<td>${u.packaging_code}&nbsp;</td>
				<td>${u.status|status_show}&nbsp;</td>
				<td>${u.washing_instruction}&nbsp;</td>
				<td>${u.fiber_content}&nbsp;</td>
				<td>${u.country_of_origin}&nbsp;</td>
				<td>${u.combo_item}&nbsp;</td>
				<td>${u.combo_packaging_code}&nbsp;</td>
				<td>${u.combo_mapping}&nbsp;</td>
				% if len(u.combo_mappings) > 0:
				<td>${u.combo_mappings[0].hangtang_pkg_code}&nbsp;</td>
				<td>${u.combo_mappings[0].label_pkg_code}&nbsp;</td>
				% else:
				<td>&nbsp;</td>
				<td>&nbsp;</td>
				% endif
				<td>${u.special_value}&nbsp;</td>
				<td>${u.multi_special_value}&nbsp;</th>
				<td>
					<a href="/order/ajaxImage?id=${u.id}&height=600&width=900" title="Sample Image" class="thickbox">View</a>
				</td>
			</tr>
			%endfor
			<tr><td style="text-align:right;border-right:0px;border-bottom:0px"  colspan="100"><span>${tmpl_context.paginators.result.pager()}, &nbsp;&nbsp;Total ${tmpl_context.paginators.result.item_count} records</span></td></tr>
		</tbody>
	</table>

%endif

