<%namespace name="tw" module="tw.core.mako_util"/>

<form ${tw.attrs(
    [('id', context.get('id')),
     ('name', name),
     ('action', action),
     ('method', method),
     ('class', css_class)],
    attrs=attrs
)}>

% if hidden_fields:
    % for field in hidden_fields:
        ${field.display(value_for(field), **args_for(field))}
    % endfor
% endif

<%def name="showGroup(l)">
    <div class="case-list-one">
    	%for field in l:
    		<ul>
    			<li class="label"><label ${tw.attrs([('id', '%s.label' % field.id),('for', field.id)])} class="fieldlabel">${tw.content(field.label_text)}</label></li>
    			<li>${field.display(value_for(field), **args_for(field))}</li>
    		</ul>
    	%endfor
    </div>
</%def>


<%
	gs = [[],[]]
	for index,field in enumerate(fields): gs[index%2].append(field)
%>

%for g in gs:
	${showGroup(g)}
%endfor

<div class="shade"><iframe class="T_iframe"></iframe></div>
<div style="float: left; padding-left: 900px;">
<div>
	<div class="item-artwork">
		<div style="float: left; padding-top: 3px;">
  			<strong class="fonts-c-369">&nbsp;&nbsp;Special Value File</strong>
  		</div>
		<div style="float: right; padding-top: 3px;">
		<a href="#" onclick="saveArtwork()" id="saveDiv"><strong>Save</strong></a>
  		&nbsp;&nbsp;
  		<a href="#"  onclick="destroyArtwork()"  id="closeDiv"><strong>Close</strong></a>
  		&nbsp;&nbsp;
  		</div>
  		<br />
		<table width="990" border="0" cellspacing="0" cellpadding="0" style="margin:10px 0px 0px 10px">
		<tr>
			<td>Special Value File:</td>
		</tr>
		<tr>
			<td>
				<div>
					<input type="text" name="item_artwork_name" id="item_artwork_name" class="width-250 excluded"/>
					&nbsp;&nbsp;
					<input type="file" name="item_artwork_files" id="item_artwork_files" size="60" onchange="getFileName(this);" class="excluded"/>
				</div>
			</td>
		</tr>
		</table>
	</div>
</div>

</form>