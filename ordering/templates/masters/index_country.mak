<%!
	from repoze.what.predicates import in_group
%>
<%inherit file="ordering.templates.master"/>

<%def name="extTitle()">r-pac - Master</%def>

<%def name="extJavaScript()">
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

	<table class="gridTable" cellpadding="0" cellspacing="0" border="0">
		<thead>
			<tr><td style="text-align:right;border-right:0px;border-bottom:0px"  colspan="5"><span>${tmpl_context.paginators.result.pager()}, ${tmpl_context.paginators.result.item_count} records</span></td></tr>
			<tr>
				<th width="40">ID</th>
				<th width="120">Name</th>
				<th width="120">Phone</th>
				<th width="150">Create Time</th>
				<th width="150">Last Update Time</th>
			</tr>
		</thead>
		<tbody>
			%for u in tmpl_context.paginators.result.items:
			<tr>
				<td>${u.id}&nbsp;</td>
				<td>
					%if in_group("Admin"):
					<a href="/${funcURL}/update?id=${u.id}" class="${'required link-text' if u.status==1 else 'link-text'}">${u.name}</a>
					%else:
					${u.name}
					%endif
					&nbsp;
				</td>
				<td>${u.phone}&nbsp;</td>
				<td>${u.createTime.strftime("%Y/%m/%d") if u.createTime else ""}&nbsp;</td>
				<td>${u.lastModifyTime.strftime("%Y/%m/%d") if u.lastModifyTime else ""}&nbsp;</td>
			</tr>
			%endfor
			<tr><td style="text-align:right;border-right:0px;border-bottom:0px"  colspan="10"><span>${tmpl_context.paginators.result.pager()}, ${tmpl_context.paginators.result.item_count} records</span></td></tr>
		</tbody>
	</table>

%endif

