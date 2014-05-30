$(document).ready(function(){

    $(".menu-tab li:not(.highlight)").each(function(){
        var orginImg = $(this).css("background-image");
        var replaceImg = "url(/images/images/main_05.jpg)"

        $(this).hover(
            function(){
                $(this).css("background-image",replaceImg);
            },
            function(){
                $(this).css("background-image",orginImg);
            }
        );

    });


    $("#function-menu a img").each(function(){
        var orginImg = $(this).attr("src");
        var replaceImg = orginImg.replace("_g.jpg",".jpg");
        $(this).hover(
            function(){
                $(this).attr("src",replaceImg);
                //alert(replaceImg);
            },
            function(){
                $(this).attr("src",orginImg);
                //alert(orginImg);
            }
        );
    });
});

function historyGo(){
    history.forward(1);
}

function historyBack(){
    history.back(-1);
}

function resetForm(){
    $('form')[0].reset();
}


function show_percentage(id){
	if(id == 16){
		$("form#special_value_template_form2").find(".spv_content").show();
	}else{
		$("form#special_value_template_form2").find(".spv_content").hide();
	}
}
	

var washing_instruction_template = 
		"<form action='' method='post' id='washing_instruction_template_form'><div class='wi-addition-check' info='1' style='display: block;'>" + 
		"		<div style='float: left'>"+ 
		" 			<strong class='fonts-c-369'>&nbsp;&nbsp;Washing Instruction</strong>"+ 
		"  		</div>"+ 
		"		<div style='float: right'>"+ 
		"		<a target='_blank' href='/order/showCode?code=care'><strong>Check All Care Code</strong></a>"+ 
		"		&nbsp;&nbsp;"+ 
		"		<a target='_blank' href='/order/showCode?code=special'><strong>Check All Special Code</strong></a>"+ 
		"		&nbsp;&nbsp;"+ 
		"		<a href='#'   onclick=saveDiv()><strong>Save</strong></a>"+ 
		" 		&nbsp;&nbsp;"+ 
		" 		<!--a href='#><strong>Save All</strong></a>"+ 
		" 		&nbsp;&nbsp;  -->"+ 
		" 		<a href='#'  onclick=destroyDiv()><strong>Close</strong></a>"+ 
		"  		&nbsp;&nbsp;"+ 
		"  		</div>"+ 
		"  		<br>"+ 
		"		<table width='990' cellspacing='0' cellpadding='0' border='0' style='margin:10px 0px 0px 10px'>"+ 
		"		<tbody><tr>"+ 
		"			<td width='250px;' valign='top' class='fonts-c-369'>"+ 
		"          		<select onchange=showIntro('wi_1'); name='wi_1'>"+ 
		"          			<option value='0'>&nbsp;</option>"+ 
		"        			<option value='1'>1</option>"+ 
		"        			<option value='2'>2</option>"+ 
		"        			<option value='3'>3</option>"+ 
		"        			<option value='4'>4</option>"+ 
		"        			<option value='5'>5</option>"+ 
		"        			<option value='6'>6</option>"+ 
		"        			<option value='7'>7</option>"+ 
		"        			<option value='8'>8</option>"+ 
		"        			<option value='9'>9</option>"+ 
		"      			</select>"+ 
		"      			&nbsp;Washing Instructions&nbsp;:"+ 
		"			</td>"+ 
		"			<td id='wi_intro_1'></td>"+ 
		"		</tr>"+ 
		"		<tr>"+ 
		"			<td width='250px;' valign='top' class='fonts-c-369'>"+ 
		"          		<select onchange=showIntro('wi_2'); name='wi_2' class='valid'>"+ 
		"          			<option value='0'>&nbsp;</option>"+ 
		"        			<option value='1'>1</option>"+ 
		"        			<option value='2'>2</option>"+ 
		"        			<option value='3'>3</option>"+ 
		"        			<option value='4'>4</option>"+ 
		"        			<option value='5'>5</option>"+ 
		"        			<option value='6'>6</option>"+ 
		"        			<option value='7'>7</option>"+ 
		"        			<option value='8'>8</option>"+ 
		"        			<option value='9'>9</option>"+ 
		"      			</select>"+ 
		"      			&nbsp;Wash Modifiers&nbsp;:"+ 
		"			</td>"+ 
		"			<td id='wi_intro_2'></td>"+ 
		"		</tr>"+ 
		"		<tr>"+ 
		"			<td width='250px;' valign='top' class='fonts-c-369'>"+ 
		"          		<select onchange=showIntro('wi_3'); name='wi_3'>"+ 
		"          			<option value='0'>&nbsp;</option>"+ 
		"        			<option value='1'>1</option>"+ 
		"        			<option value='2'>2</option>"+ 
		"        			<option value='3'>3</option>"+ 
		"        			<option value='4'>4</option>"+ 
		"        			<option value='5'>5</option>"+ 
		"        			<option value='6'>6</option>"+ 
		"        			<option value='7'>7</option>"+ 
		"        			<option value='8'>8</option>"+ 
		"        			<option value='9'>9</option>"+ 
		"      			</select>"+ 
		"      			&nbsp;Beaching, Dry Cleaning Instructions&nbsp;:"+ 
		"			</td>"+ 
		"			<td id='wi_intro_3'></td>"+ 
		"		</tr>"+ 
		"		<tr>"+ 
		"			<td width='250px;' valign='top' class='fonts-c-369'>"+ 
		"          		<select onchange=showIntro('wi_4'); name='wi_4'>"+ 
		"          			<option value='0'>&nbsp;</option>"+ 
		"        			<option value='1'>1</option>"+ 
		"        			<option value='2'>2</option>"+ 
		"        			<option value='3'>3</option>"+ 
		"        			<option value='4'>4</option>"+ 
		"        			<option value='5'>5</option>"+ 
		"        			<option value='6'>6</option>"+ 
		"        			<option value='7'>7</option>"+ 
		"        			<option value='8'>8</option>"+ 
		"        			<option value='9'>9</option>"+ 
		"      			</select>"+ 
		"      			&nbsp;Drying Instructions&nbsp;:"+ 
		"			</td>"+ 
		"			<td id='wi_intro_4'></td>"+ 
		"		</tr>"+ 
		"		<tr>"+ 
		"			<td width='250px;' valign='top' class='fonts-c-369'>"+ 
		"         		<select onchange=showIntro('wi_5'); name='wi_5'>"+ 
		"          			<option value='0'>&nbsp;</option>"+ 
		"        			<option value='1'>1</option>"+ 
		"        			<option value='2'>2</option>"+ 
		"        			<option value='3'>3</option>"+ 
		"        			<option value='4'>4</option>"+ 
		"        			<option value='5'>5</option>"+ 
		"        			<option value='6'>6</option>"+ 
		"        			<option value='7'>7</option>"+ 
		"        			<option value='8'>8</option>"+ 
		"        			<option value='9'>9</option>"+ 
		"      			</select>"+ 
		"      			&nbsp;Drying Modifiers&nbsp;:"+ 
		"			</td>"+ 
		"			<td id='wi_intro_5'></td>"+ 
		"		</tr>"+ 
		"		<tr>"+ 
		"			<td width='250px;' valign='top' class='fonts-c-369'>"+ 
		"          		<select onchange=showIntro('wi_6'); name='wi_6'>"+ 
		"          			<option value='0'>&nbsp;</option>"+ 
		"        			<option value='1'>1</option>"+ 
		"        			<option value='2'>2</option>"+ 
		"        			<option value='3'>3</option>"+ 
		"        			<option value='4'>4</option>"+ 
		"        			<option value='5'>5</option>"+ 
		"        			<option value='6'>6</option>"+ 
		"        			<option value='7'>7</option>"+ 
		"        			<option value='8'>8</option>"+ 
		"        			<option value='9'>9</option>"+ 
		"      			</select>"+ 
		"      			&nbsp;Ironing Instructions&nbsp;:"+ 
		"			</td>"+ 
		"			<td id='wi_intro_6'></td>"+ 
		"		</tr>"+ 
		"		<tr>"+ 
		"			<td width='250px;' valign='top' class='fonts-c-369'>"+ 
		"        	<select onchange=showIntro('wi_7'); class='valid' name='wi_7'>"+ 
		"        		<option value='0'>&nbsp;</option>"+ 
		"          		<option value='A'>A</option>"+ 
		"          		<option value='B'>B</option>"+ 
		"          		<option value='C'>C</option>"+ 
		"          		<option value='D'>D</option>"+ 
		"          		<option value='E'>E</option>"+ 
		"          		<option value='F'>F</option>"+ 
		"          		<option value='G'>G</option>"+ 
		"          		<option value='H'>H</option>"+ 
		"          		<option value='I'>I</option>"+ 
		"          		<option value='J'>J</option>"+ 
		"          		<option value='K'>K</option>"+ 
		"          		<option value='L'>L</option>"+ 
		"          		<option value='M'>M</option>"+ 
		"          		<option value='N'>N</option>"+ 
		"          		<option value='O'>O</option>"+ 
		"          		<option value='P'>P</option>"+ 
		"          		<option value='Q'>Q</option>"+ 
		"          		<option value='R'>R</option>"+ 
		"          		<option value='S'>S</option>"+ 
		"          		<option value='T'>T</option>"+ 
		"          		<option value='U'>U</option>"+ 
		"          		<option value='V'>V</option>"+ 
		"          		<option value='W'>W</option>"+ 
		"          		<option value='X'>X</option>"+ 
		"          		<option value='Y'>Y</option>"+ 
		"          		<option value='Z'>Z</option>"+ 
		"          		<option value='AA'>AA</option>"+ 
		"          		<option value='AB'>AB</option>"+ 
		"          		<option value='AC'>AC</option>"+ 
		"          		<option value='AD'>AD</option>"+ 
		"        	</select>"+ 
		"        	&nbsp;Special Instructions&nbsp;:"+ 
		"			</td>"+ 
		"			<td id='wi_intro_7'></td>"+ 
		"		</tr>"+ 
		"		<tr>"+ 
		"			<td>&nbsp;</td>"+ 
		"		</tr>"+ 
		"		<tr>"+ 
		"			<td colspan='2'>"+ 
		"            <input type='checkbox' value='wi_copy_all' id='wi_copy_all' name='wi_copy_all'><label for='wi_copy_all'><span class='fonts-c-369'>Checked to save contents for all variable tickets.</span></label></td><td>"+ 
		"		</td></tr>"+ 
		"		<tr>"+ 
		"			<td>&nbsp;</td>"+ 
		"		</tr>"+ 
		"		</tbody></table>"+ 
		"	</div></form>"

var special_value_template =
    "<form id='special_value_template_form' action=''><div style='display: block' info='1' class='spv-check'>" +
	"<div style='float: right'> " +
	"<a href='#' onclick='saveDiv()'><strong>Save</strong></a>" +
	"&nbsp;&nbsp;" +
	"<a href='#'  onclick='destroyDiv()'><strong>Close</strong></a>&nbsp;&nbsp;" +
	"</div>" +
	"<table width='990' cellspacing='0' cellpadding='0' border='0' style='margin:10px 0px 0px 10px'>" +
	"	<tbody><tr>" +
	"	  <td height='25' class='fonts-14pt fonts-c-036'>Special Value</td>" +
	"	  <td>&nbsp;</td>" +
	"	  <td class='fonts-14pt fonts-c-036'>&nbsp;</td>" +
	"	</tr>" +
	"	<tr>" +
	"	  <td>" +
	"		<table>" +
	"		  <tbody>" +
	"			<tr>" +
	"			  <td><span class='fonts-c-369'>Parts of special value:</span></td>" +
	"			  <td>" +
	"				<span class='fonts-c-369'>" +
	"				  <select onchange='showSPValueParts(this.options[this.options.selectedIndex].value)' name='spvalue_parts' class='valid'>" +
	"					<option value='0' selected=''>&nbsp;</option>" +
	"					<option value='1'>Part1</option>" +
	"					<option value='2'>Part2</option>" +
	"					<option value='3'>Part3</option>" +
	"					<option value='4'>Part4</option>" +
	"					<option value='5'>Part5</option>" +
	"					<option value='6'>Part6</option>" +
	"				  </select>" +
	"				</span>" +
	"			  </td>" +
	"			</tr>" +
	"		  </tbody>" +
	"		</table>" +
	"	  </td>" +
	"	  <td>&nbsp;</td>" +
	"	  <td>&nbsp;</td>" +
	"	</tr>" +
	"	<tr>" +
	"	  <td valign='top' align='left' colspan='3'>&nbsp;</td>" +
	"	</tr>" +
	"	<tr>" +
	"	  <td valign='top' align='left' colspan='3'><hr size='1' noshade='' style='padding-bottom: 2px;'></td>" +
	"	</tr>" +
	"</tbody></table>" +
	"<div style='float:left;' width='450' class='special_value_part'>{special_value_part}</div></div></form>"

var special_value_template2 = $(".special-value-check")

var type, id;

function fiber_content(){
		var components_or_colors = {}
		var template = $(".fc-addition-check");
		var data = $("input[name='fc_info_"+id+"']").val();
		objs = ["select[name='fc_exclusive_data']", "input[name='fc_cotton_logo']", "input[name='fc_lycra_logo']", "select[name='fc_components']", "input[name='fc_copy_all']"]
		for(i=0; i<=objs.length; i++){
			obj = template.find(objs[i]);
			if(obj.attr('type') == 'checkbox'){
				obj.attr('checked', false);
			}else{
				if(obj.attr('name') == 'fc_exclusive_data'){
						obj.val('None')
					}
				else if(obj.attr('name') == 'fc_components'){
					obj.val('0')
				}
				else{
					obj.val("");
				}
			}
		}
		if(data.length > 0){
			data = data.split("&");
			$.each(data, function(){
				i = this.split("=");
				var name = i[0];
				var value = i[1];
				value = value.split("+").join(" ");
				components_or_colors[name] = value;
				var obj = template.find("*[name='"+name+"']");
				if(obj.attr('type') == 'checkbox'){
					obj.attr('checked', true);
				}else{
					obj.val(value);
				}
			})
		}
		showFCComponents(components_or_colors['fc_components']);
		var colors = new Array();
		if(components_or_colors['fc_components'] > 0){
			for(i=0; i<= components_or_colors['fc_components']; i++){
				index = i + 1
				$("input[name='fc_cc_name"+index+"']").val(components_or_colors["fc_cc_name"+index+""]);
				$("select[name='fc_component"+index+"']").val(components_or_colors["fc_component"+index+""]);
				$("select[name='fc_color"+index+"']").val(components_or_colors["fc_color"+index+""]);
				for(i2=1; i2<=6; i2++){
					$("input[name='fc_percentage"+index+"_"+i2+"']").val(components_or_colors["fc_percentage"+index+"_"+i2+""]);
					$("select[name='fc_content"+index+"_"+i2+"']").val(components_or_colors["fc_content"+index+"_"+i2+""]);
				}
			}
		}
		template.slideDown();
}

function washing_instruction(){
	var template = washing_instruction_template
	var data = $("input[name='wi_info_"+id+"']").val();
	$("body").append(template);
	if(data.length > 0){
		data = data.split("&");
		$.each(data, function(){
			var i = this.split("=");
			var name = i[0];
			var value = i[1];
			if(name == 'wi_copy_all'){
				$("input[name='"+name+"']").attr('checked', true);
			}
			else{
				$("select[name='"+name+"']").val(value).change();
			}
		})
	}
	$("form#washing_instruction_template_form").slideDown();
}

function special_value(){
	var special_value_part = new Array();
	var template = special_value_template;
	var data = $("input[name='spvalue_info_"+id+"']").val()
	if(data.length > 0){
		data = data.split("&");
		$.each(data, function(){
			i = this.split("=");
			var name = i[0];
			var value = i[1];
			if(name == 'spvalue_parts'){
				template = template.replace("<option value='0' selected=''>", 
													"<option value='0'>").replace("<option value='"+value+"'>", "<option value='"+value+"' selected=''>")
			}else if(name.search('spvalue_part_') > -1){
				var index = name.split("_")[2];
				special_value_part.push("<br /><label for='"+name+"'>Part "+index+":</label>&nbsp;<input type='text' name='"+name+"' value='"+value+"'>")
			}
		})
		if(special_value_part.length > 0) special_value_part = special_value_part.join("");
	}
	if(special_value_part.length > 0){
		template = template.replace("{special_value_part}", special_value_part);
	}
	else{
		template = template.replace("{special_value_part}", "");
	}
	$("body").append(template);
	$("form#special_value_template_form").slideDown();
}

function special_value2(){
	var count = 0;
	var template = $(".special-value-check")
	template.find(".spv_content").hide();
	template.find("select[name='spv_1']").val("x");
	template.find("select[name='spv_2']").val("x");
	template.find("input[name='spv_copy_all']").attr('checked', false);
	template.find("select[name='spvcontent_part']").val("2");
	for(i=1; i<=4; i++){
		template.find("input[name='sp_content_prt_"+i+"']").val("");
		template.find("input[name='sp_content_"+i+"']").val("");
	}
	var data = $("input[name='spv_info_"+id+"']").val();
	if(data.length > 0){
		data = data.split("&");
		$.each(data, function(index){
			var i = this.split("=");
			var name = i[0];
			var value = i[1];
			if(name == 'spv_1' || name == 'spvcontent_part'){
				if(name == 'spv_1' && value == 16){
					template.find(".spv_content").show();
				}
				template.find("select[name='"+name+"']").val(value);
			}
			if(name == 'spv_2'){
				template.find("select[name='spv_2']").val(value);
			}
			if(name == 'spv_copy_all'){
				template.find("input[name='spv_copy_all']").attr('checked', true);
			}
			if(name.search("sp_content_prt_") > -1){
				template.find("input[name='"+name+"']").val(value);
			}
			if(name.search("sp_content_") > -1){
				template.find("input[name='"+name+"']").val(value);
			}
		})
	}
	template.slideDown();
}

function special_value3(){
	var count = 0;
	var template = $(".rfid-special-value-check")
	template.find(".spv_content").hide();
	template.find("select[name='spv_1']").val("x");
	template.find("select[name='spv_2']").val("x");
	template.find("input[name='spv_copy_all']").attr('checked', false);
	template.find("select[name='spvcontent_part']").val("2");
	for(i=1; i<=4; i++){
		template.find("input[name='sp_content_prt_"+i+"']").val("");
		template.find("input[name='sp_content_"+i+"']").val("");
	}
	var data = $("input[name='spv_info_"+id+"']").val();
	if(data.length > 0){
		data = data.split("&");
		$.each(data, function(index){
			var i = this.split("=");
			var name = i[0];
			var value = i[1];
			if(name == 'spv_1' || name == 'spvcontent_part'){
				if(name == 'spv_1' && value == 16){
					template.find(".spv_content").show();
				}
				template.find("select[name='"+name+"']").val(value);
			}
			if(name == 'spv_2'){
				template.find("select[name='spv_2']").val(value);
			}
			if(name == 'spv_copy_all'){
				template.find("input[name='spv_copy_all']").attr('checked', true);
			}
			if(name.search("sp_content_prt_") > -1){
				template.find("input[name='"+name+"']").val(value);
			}
			if(name.search("sp_content_") > -1){
				template.find("input[name='"+name+"']").val(value);
			}
		})
	}
	template.slideDown();
}

function special_value4(){
	var count = 0;
	var template = $(".combo-special-value-check")
	template.find(".spv_content").hide();
	template.find("select[name='spv_1']").val("x");
	template.find("select[name='spv_2']").val("x");
	template.find("input[name='spv_copy_all']").attr('checked', false);
	template.find("select[name='spvcontent_part']").val("2");
	for(i=1; i<=4; i++){
		template.find("input[name='sp_content_prt_"+i+"']").val("");
		template.find("input[name='sp_content_"+i+"']").val("");
	}
	var data = $("input[name='spv_info_"+id+"']").val();
	if(data.length > 0){
		data = data.split("&");
		$.each(data, function(index){
			var i = this.split("=");
			var name = i[0];
			var value = i[1];
			if(name == 'spv_1' || name == 'spvcontent_part'){
				if(name == 'spv_1' && value == 16){
					template.find(".spv_content").show();
				}
				template.find("select[name='"+name+"']").val(value);
			}
			if(name == 'spv_2'){
				template.find("select[name='spv_2']").val(value);
			}
			if(name == 'spv_copy_all'){
				template.find("input[name='spv_copy_all']").attr('checked', true);
			}
			if(name.search("sp_content_prt_") > -1){
				template.find("input[name='"+name+"']").val(value);
			}
			if(name.search("sp_content_") > -1){
				template.find("input[name='"+name+"']").val(value);
			}
		})
	}
	template.slideDown();
}

function showDiv(t, i){
	showShade();
	id = i;
	type = t;
	if(type == 1){
		fiber_content();
	}
	else if(type == 2){
		washing_instruction();
	}
	else if(type == 3){
		special_value();
	}
	else if(type == 4){
		special_value2();
	}
	else if(type == 5){
		special_value3();
	}
	else if(type == 6){
		special_value4();
	}
}

function saveDiv(){
	if(type == 1){
		var b = new Array();
		var d = {}
		var template = $(".fc-addition-check");
		template.find("input, select").each(function(){
			if($(this).attr('type') == 'checkbox' && $(this).is(":checked") == false){
			}else{
				d[$(this).attr('name')] = $(this).val();
				b.push($(this).attr('name')+"="+$(this).val());
			}	
		})
		if(d['fc_components'] > 0){
			for(i=1; i<=d['fc_components']; i++){
				var total = 0;
				for(i2=1; i2<=5; i2++){
					var fc_percentage = $("input[name='fc_percentage"+i+"_"+i2+"']").val();
					if(fc_percentage != undefined && fc_percentage.length > 0){
						total += parseInt(fc_percentage);
					}
				}
				if(total != 100){
					$.prompt("The total number of content is not 100%!", {opacity: 0.6,prefix:'cleanred', zIndex:10001});
					$("#cleanredbox").attr('style', "z-index: 3");
					
					return false;
				}
			}
		}
		if(d['fc_copy_all'] != undefined && d['fc_copy_all'].length > 0){
			$("a[id^='FC_']").html("Multiple - "+template.find("select[name='fc_components']").val()+" Components or Colors");
			$("input[name^='fc_info_']").val(b.join("&"));
		}
		$("input[name='fc_info_"+id+"']").val(b.join("&"))
		$("#FC_"+id+"").html("Multiple - "+template.find("select[name='fc_components']").val()+" Components or Colors");
		template.hide();
	}
	else if(type == 2){
		var wi_copy_all;
		var data = $("form#washing_instruction_template_form").serialize()
		$("input[name='wi_info_"+id+"']").val(data)
		d = data.split("&")
		var p = new Array();
		$.each(d, function(){
			i = this.split("=")
			if(i[0] != 'wi_copy_all'){
				p.push(i[1]);
			}else{
				wi_copy_all = i[1];
			}
		})
		if(wi_copy_all != undefined && wi_copy_all.length > 0){
			$("input[name^='wi_info_']").val(data)
			$("a[id^='WI_']").html(p.join(""));
		}
		$("#WI_"+id+"").html(p.join(""));
		$("form#washing_instruction_template_form").remove();
	}
	else if(type == 3){
		$("input[name='spvalue_info_"+id+"']").val($("form#special_value_template_form").serialize());
		$("#SPV_"+id+"").html("Special value added.");
		$("form#special_value_template_form").remove();
	}
	else if(type == 4){
		var dict = {}
		var count = 0;
		var serializes = new Array();
		$(".special-value-check").find("input, select").each(function(){
			var name = $(this).attr('name');
			var value = $(this).val();
			if($(this).attr('type') == 'checkbox' && $(this).prop('checked') == false){
				
			}else{
				if(name.search('sp_content_prt_') > -1 && value.length > 0){
					count += 1;
				}
				serializes.push(name+"="+value);
				dict[name] = value;
			}
		})
		var percentage = 0;
		if(dict['spv_1'] == 16){
			for(i=1; i<=dict['spvcontent_part']; i++){
				percentage += parseInt(dict["sp_content_prt_"+i+""]);
			}
		}
		if(dict['spv_1'] == 'x'){
			$.prompt("If the no special value for that part, please select 'N/A'!", {opacity: 0.6,prefix:'cleanred', zIndex:3});
			$("#cleanredbox").attr('style', "z-index: 3");
			return false;
		}
		if(dict['spv_1'] == 16 && count != dict['spvcontent_part']){
			$.prompt("The number of content is not match your input, please check!", {opacity: 0.6,prefix:'cleanred',zindex:3});
			$("#cleanredbox").attr('style', "z-index: 3");
			return false
		}
		if(dict['spv_1'] == 16 && percentage != 100){
			$.prompt("The total number of content is not 100%!", {opacity: 0.6,prefix:'cleanred', zindex:3});
			$("#cleanredbox").attr('style', "z-index: 3");
			return false;
		}
		if(serializes.length > 0){
			$("input[name='spv_info_"+id+"']").val(serializes.join("&"));
		}
		if(dict['spv_copy_all'] != undefined && dict['spv_copy_all'].length > 0){
			$("a[id^='SPV_']").html("Special Value(s) edited");
			$("input[name^='spv_info_']").val(serializes.join("&"));
		}else{
			$("#SPV_"+id+"").html("Special Value(s) edited");
		}
		$(".special-value-check").hide();
	}
	else if(type == 5){
		var dict = {}
		var count = 0;
		var serializes = new Array();
		$(".rfid-special-value-check").find("input, select").each(function(){
			var name = $(this).attr('name');
			var value = $(this).val();
			if($(this).attr('type') == 'checkbox' && $(this).prop('checked') == false){
				
			}else{
				if(name.search('sp_content_prt_') > -1 && value.length > 0){
					count += 1;
				}
				serializes.push(name+"="+value);
				dict[name] = value;
			}
		})
		var percentage = 0;
		if(dict['spv_1'] == 16){
			for(i=1; i<=dict['spvcontent_part']; i++){
				percentage += parseInt(dict["sp_content_prt_"+i+""]);
			}
		}
		if(dict['spv_1'] == 'x'){
			$.prompt("If the no special value for that part, please select 'N/A'!", {opacity: 0.6,prefix:'cleanred', zIndex:3});
			$("#cleanredbox").attr('style', "z-index: 3");
			return false;
		}
		if(dict['spv_1'] == 16 && count != dict['spvcontent_part']){
			$.prompt("The number of content is not match your input, please check!", {opacity: 0.6,prefix:'cleanred',zindex:3});
			$("#cleanredbox").attr('style', "z-index: 3");
			return false
		}
		if(dict['spv_1'] == 16 && percentage != 100){
			$.prompt("The total number of content is not 100%!", {opacity: 0.6,prefix:'cleanred', zindex:3});
			$("#cleanredbox").attr('style', "z-index: 3");
			return false;
		}
		if(serializes.length > 0){
			$("input[name='private_spv_info_"+id+"']").val(serializes.join("&"));
		}
		if(dict['spv_copy_all'] != undefined && dict['spv_copy_all'].length > 0){
			$("a[id^='private_SPV_']").html("Special Value(s) edited");
			$("input[name^='private_spv_info_']").val(serializes.join("&"));
		}else{
			$("#private_SPV_"+id+"").html("Special Value(s) edited");
		}
		$(".rfid-special-value-check").hide();
	}
	else if(type == 6){
		var dict = {}
		var count = 0;
		var serializes = new Array();
		$(".combo-special-value-check").find("input, select").each(function(){
			var name = $(this).attr('name');
			var value = $(this).val();
			if($(this).attr('type') == 'checkbox' && $(this).prop('checked') == false){
				
			}else{
				if(name.search('sp_content_prt_') > -1 && value.length > 0){
					count += 1;
				}
				serializes.push(name+"="+value);
				dict[name] = value;
			}
		})
		var percentage = 0;
		if(dict['spv_1'] == 16){
			for(i=1; i<=dict['spvcontent_part']; i++){
				percentage += parseInt(dict["sp_content_prt_"+i+""]);
			}
		}
		if(dict['spv_1'] == 'x'){
			$.prompt("If the no special value for that part, please select 'N/A'!", {opacity: 0.6,prefix:'cleanred', zIndex:3});
			$("#cleanredbox").attr('style', "z-index: 3");
			return false;
		}
		if(dict['spv_1'] == 16 && count != dict['spvcontent_part']){
			$.prompt("The number of content is not match your input, please check!", {opacity: 0.6,prefix:'cleanred',zindex:3});
			$("#cleanredbox").attr('style', "z-index: 3");
			return false
		}
		if(dict['spv_1'] == 16 && percentage != 100){
			$.prompt("The total number of content is not 100%!", {opacity: 0.6,prefix:'cleanred', zindex:3});
			$("#cleanredbox").attr('style', "z-index: 3");
			return false;
		}
		if(serializes.length > 0){
			$("input[name='combo_spv_info_"+id+"']").val(serializes.join("&"));
		}
		if(dict['spv_copy_all'] != undefined && dict['spv_copy_all'].length > 0){
			$("a[id^='combo_SPV_']").html("Special Value(s) edited");
			$("input[name^='combo_spv_info_']").val(serializes.join("&"));
		}else{
			$("#combo_SPV_"+id+"").html("Special Value(s) edited");
		}
		$(".combo-special-value-check").hide();
	}
	$(".shade").slideUp();
}

function destroyDiv(){
	$(".shade").slideUp();
	if(type == 1){
		$(".fc-addition-check").hide();
	}else if(type == 2){
		$("form#washing_instruction_template_form").remove();
	}
	else if(type == 3){
		$("form#special_value_template_form").remove();
	}
	else if(type == 4){
		$(".special-value-check").hide();
	}
	else if(type == 5){
		$(".rfid-special-value-check").hide();
	}
	else if(type == 6){
		$(".combo-special-value-check").hide();
	}
}
