$(document).ready(function(){
	jQuery.validator.addMethod("isLabelCode", function(value, element) {
		return this.optional(element) || /^[1-8][A-S][1-5][1-2][A-M][1-4]$/.test(value);
	}, "input format: 1A21B4");
	
	$("#orderForm").validate({
		rules:{
			labelCode:{isLabelCode: true}
		},
		showErrors: function(errorMap, errorList){
			this.defaultShowErrors();
		}
	});
	
	
	/*$("select[name^='wi_']").change(function(){
		var t = $(this);
		var p = t.parent("td");
		var values = new Array();
		
		$("select",p).each(function(){
			var tmp = $(this);
			var s = $(":selected",tmp);
			if(s.val()){ 
				values.push(s.text());
			}
		});
		
		var n = t.attr("name");
		
		$("a",p).attr("href","/order/ajaxInstruction?cls="+n.split("_")[0]+"&val="+values.join(""));
		
	});*/
});
		
/*function showWIComponents(value) {
	$(".wi-addition-check").remove("wi_component_color");
	
	for (count = 1; count <= Number(value); ++count) {
		var htmlStr = '<div class="wi_component_color"><br />';
		htmlStr += '<table><tr><td>Component ' + count + '</td></tr>';
		htmlStr += '<tr><td>Enter component or color name; Or select a component or color name from the list.</td></tr>';
		htmlStr += '<tr><td><strong>Component or Color: </strong><input name="wi_cc_name' + count + '" /></td></tr>';
		htmlStr += '<tr><td>Component:&nbsp;&nbsp;<select name="wi_component' + count + '">';
				
		var component_str = '<option selected value="None">None</option>';
		for (idx = 0; idx < 10; ++idx) {
			component_str += '<option value="' + idx + '">' + idx + '</option>';
		}
				
		htmlStr += component_str + '</select>&nbsp;&nbsp;Color:&nbsp;&nbsp;<select name="wi_color' + count + '">';
			
		var color_str = '<option selected value="None">None</option>';
		for (idx = 0; idx < 10; ++idx) {
			color_str += '<option value="' + idx + '">' + idx + '</option>';
		}
				
		htmlStr += color_str + '</select></td></tr>';
				
		var content_str = '';
		for (index = 1; index <= 5; ++index) {
			content_str += '<tr><td>'
			content_str += 'Content ' + index + ': <input name="wi_percentage' + count + "_" + index + '" />&nbsp;&nbsp;%&nbsp;&nbsp;&nbsp;&nbsp;<select name="wi_content' + count + "_" + index + '">';
			var content_options = '<option selected value="None">None</option>';
			for (i = 1; i <= 10; ++i) {
				content_options += '<option value="' + i + '">' + i + '</option>';
			}
				
			content_str += content_options + '</select></td></tr>';
		}
		htmlStr += content_str + '</table></div>'
		$(".wi-addition-check").append(htmlStr);
	}
}*/
		
function showFCComponents(value) {
	$(".fc-addition-check .fc_component_color").remove();
	var component_arr = ['Shell', 'Lining', 'Shell and Lining', 'Out Sole', 'Inner Sole', 'Body Out Sole', 'Body inner Sole', 'Pot Holder', 'Oven Mitt']
	var color_arr = ['Alice Blue','Antique White','Aqua','Aquamarine','Azure','Beige','Bisque','Black','Blanched Almond','Blue','Blue Violet','Brown','Burly Wood','Cadet Blue','Chartreuse','Chocolate','Coral','Cornflower Blue','Corn_silk','Crimson','Cyan','Dark Blue','Dark Cyan','Dark Golden Rod','Dark Gray','Dark Green','Dark Khaki','Dark Magenta','Dark Olive Green','Dark orange','Dark Orchid','Dark Red','Dark Salmon','Dark Sea Green','Dark Slate Blue','Dark Slate Gray','Dark Turquoise','Dark Violet','Deep Pink','Deep Sky Blue','Dim Gray','Dodger Blue','Fire Brick','Floral White','Forest Green','Fuchsia','Gainsboro','Ghost White','Gold','Golden Rod','Gray','Green','Green Yellow','Honey Dew','Hot Pink','Indian Red','Indigo','Ivory','Khaki','Lavender','Lavender Blush','Lawn Green','Lemon Chiffon','Light Blue','Light Coral','Light Cyan','Light Golden Rod Yellow','Light Grey','Light Green','Light Pink','Light Salmon','Light Sea Green','Light Sky Blue','Light Slate Gray','Light Steel Blue','Light Yellow','Lime','Lime Green','Linen','Magenta','Maroon','Medium Aqua Marine','Medium Blue','Medium Orchid','Medium Purple','Medium Sea Green','Medium Slate Blue','Medium Spring Green','Medium Turquoise','Medium Violet Red','Midnight Blue','Mint Cream','Misty Rose','Moccasin','NavajoWhite','Navy','Old Lace','Olive','Olive Drab','Orange','Orange Red','Orchid','Pale Golden Rod','Pale Green','Pale Turquoise','Pale Violet Red','Papaya Whip','Peach Puff','Peru','Pink','Plum','Powder Blue','Purple','Red','Rosy Brown','Royal Blue','Saddle Brown','Salmon','Sandy Brown','Sea Green','Sea Shell','Sienna','Silver','Sky Blue','Slate Blue','Slate Gray','Snow','Spring Green','Steel Blue','Tan','Teal','Thistle','Tomato','Turquoise','Violet','Wheat','White','White Smoke','Yellow','Yellow Green']
	var content_arr = ['ACETATE\ACETATO','ACRYLIC\ACRILICO','BAMBOO','BICONMICROFIBER','BICONSTITUENT','CASHMERE\CACHEMIRA','CATIONICPOLYESTER','CERTIFIED ORGAN GROWNCTN','CERTIFIED ORGANICALLY','CERTIFIEDCOTTON','COMBED COTTON\ALGODON PEINADO','COTTON\ALGODON','COTTONPRESHRUNK','DACRON\DACRON','DACRONPOLYESTER\DACRON POLIESTER','ECOTECRECYCLEDCOTTON','ELASTANE','EXTRAFINEMERINOWOOL','LAMBSWOOL\LANA DE BORREGO','LEATHER\PIEL','LINEN\LINO','LOWPILL ACRYLIC','LYCRA\SPANDEX LYCRA','MICROFIBER\MICROFIBRA','MODAL','NOMEX','NYLON\NILON','ORGANICCOTTON','PIMACOTTON','POLY RAYON','POLYESTER\POLIESTER','PRESHRUNKCOTTON','PURECOTTON','RATTAN','RAYON\RAYON','SHEEPWOOL','SILK\SEDA','SPANDEX','VINYL\VINILO','VISCOSE\VISCOSA','WOOL\LANA','WORSTEDWOOL','OTHER FIBERS']
	for (count = 1; count <= Number(value); ++count) {
		var htmlStr = '<div class="fc_component_color" width="450" style="float:left;"><br />';
		htmlStr += '<table class="component" width="450" border="0" cellpadding="0" cellspacing="0" style="border:#369 solid 2px; margin:10px 0px 0px 10px">';
		htmlStr += '<tbody><tr><td width="20">&nbsp;</td><td>&nbsp;</td><td width="20">';
		htmlStr += '&nbsp;</td></tr><tr><td>&nbsp;</td><td class="fonts-c-036"><strong>Component ' + count + '</strong></td>';
		htmlStr += '</td><td>&nbsp;</td></tr><tr><td>&nbsp;</td><td class="fonts-c-036">';
		htmlStr += 'Enter component or color name; Or select a component or color name from the list.</td>';
		htmlStr += '</td><td>&nbsp;</td></tr><tr><td>&nbsp;</td><td class="fonts-c-036">';
		htmlStr += '<strong>Component or Color: </strong><input name="fc_cc_name' + count + '" /></td>';
		htmlStr += '<td>&nbsp;</td></tr><tr><td>&nbsp;</td><td class="fonts-c-036">';
		htmlStr += 'Component:&nbsp;&nbsp;&nbsp;&nbsp;<select name="fc_component' + count + '" onchange="showValues(' + count + ', this.options[this.options.selectedIndex].value)">';
		//htmlStr += 'Component:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input name="fc_component' + count + '" />';
				
		var component_str = '<option selected value="None">None</option>';
		for (idx = 1; idx <= 5; ++idx) {
			component_str += '<option value="' + component_arr[idx - 1] + '">' + component_arr[idx - 1] + '</option>';
		}
				
		htmlStr += component_str + '</select>&nbsp;&nbsp;</td><td>&nbsp;</td></tr><tr><td>&nbsp;</td><td class="fonts-c-036">Color:&nbsp;&nbsp;<select name="fc_color' + count + '" onchange="showValues(' + count + ', this.options[this.options.selectedIndex].value)">';
		/*htmlStr += '</td><td bgcolor="#CCFFFF">&nbsp;</td></tr><tr><td bgcolor="#CCFFFF">&nbsp;</td><td bgcolor="#CCFFFF" class="fonts-c-036">Color:&nbsp;&nbsp;&nbsp;&nbsp;';
		htmlStr += '<select name="fc_color' + count + '">';*/
				
		var color_str = '<option selected value="None">None</option>';
		for (idx = 1; idx <= color_arr.length; ++idx) {
			color_str += '<option value="' + color_arr[idx - 1] + '">' + color_arr[idx - 1] + '</option>';
		}
				
		htmlStr += color_str + '</select></td><td>&nbsp;</td></tr>';
		//htmlStr += '</td><td bgcolor="#CCFFFF">&nbsp;</td></tr>';
				
		var content_str = '';
		for (index = 1; index <= 5; ++index) {
			content_str += '<tr><td>&nbsp;</td><td class="fonts-c-036">'
			content_str += 'Content ' + index + ': <input class="numeric" name="fc_percentage' + count + "_" + index + '" style="width: 25px;" />&nbsp;&nbsp;%&nbsp;&nbsp;&nbsp;&nbsp;<select name="fc_content' + count + "_" + index + '">';
			var content_options = '<option selected value="None">None</option>';
			for (i = 1; i <= content_arr.length; ++i) {
				content_options += '<option value="' + content_arr[i - 1] + '">' + content_arr[i - 1] + '</option>';
			}
				
			content_str += content_options + '</select></td><td>&nbsp;</td></tr>';
			//content_str += '</td><td bgcolor="#CCFFFF">&nbsp;</td></tr>';
		}
		htmlStr += content_str + '<tr><td>&nbsp;</td><td>&nbsp;</td>';
		htmlStr += '<td>&nbsp;</td></tr></tbody></table></div>'
		$(".fc-addition-check").append(htmlStr);
		$(".numeric").numeric();
	}
}

function showSPValueParts(value) {
	$(".special_value_part").remove();
	
	var htmlStr = '<div class="special_value_part" width="450" style="float:left;">';
	
	for (count = 1; count <= Number(value); ++count) {
		htmlStr += '<br /><label for="spvalue_part" />Part ' + count + ':&nbsp;';
		htmlStr += '<input type="text" name="spvalue_part_'+ count + '"/>';
	}
	
	htmlStr += '</div>'
		
	$(".spv-check").append(htmlStr);
}

function setValue(obj){
	if($(obj).attr("checked")){
		$(obj).val('true');
	}else{
		$(obj).val('false');
	}
}

function showIntro(item) {
	var intro_category = item.split("_")[0];
	var intro_item = $("select[name=" + item + "]").val();
	var intro_pos = Number(item.split("_")[1]);
	
	$.get(
		"/order/ajaxSearchIntro",
		{'category': intro_category, 'item': intro_item, 'pos': intro_pos},
		function(data){
			$("#" + intro_category + "_intro_" + intro_pos).html(data);
		}
	);
	
	return false;
}

function composeFCJSON() {
	var exclusive_data = $("select[name='fc_exclusive_data']").val();
	
	if ($("input[name='fc_cotton_logo']").attr("checked")) {
		var fc_cotton_logo = 'true';
	} else {
		var fc_cotton_logo = 'false';
	}
	
	if ($("input[name='fc_lycra_logo']").attr("checked")) {
		var fc_lycra_logo = 'true';
	} else {
		var fc_lycra_logo = 'false';
	}
	
	var count = Number($("select[name='fc_components']").val());
	var fc_json = "{'exclusive_data':'" + exclusive_data + "','fc_cotton_logo':'" + fc_cotton_logo + "','fc_lycra_logo':'" + fc_lycra_logo + "','components':";
	
	var com_str = "[";
	for (var idx = 1; idx <= count; idx++) {
		var cc_name = $("input[name='fc_cc_name" + count + "']").val();
		var component = $("select[name='fc_component" + count + "']").val();
		var color = $("select[name='fc_color" + count + "']").val();
		
		com_str += "{'cc_name':'" + cc_name + "','component':'" + component + "','color':'" + color + "','percent':["; 

		for (var index = 1; index <=5; index++) {
			var fc_percentage = $("input[name='fc_percentage" + count + "_" + index + "']").val();
			var fc_content = $("select[name='fc_content" + count + "_" + index + "']").val();
			
			com_str += "{'fc_percentage':'" + fc_percentage + "','fc_content':'" + fc_content + "'},";
		}
		
		com_str = com_str.substr(0, com_str.length - 1) + "]},";
	}
	
	fc_json += com_str.substr(0, com_str.length - 1) + "]}";
	
	return fc_json;
}

function composeSPValueJSON() {
	var count = Number($("select[name='spvalue_parts']").val());
	var sp_value_json = "{'";

	for (var idx = 1; idx <= count; idx++) {
		sp_value_json += "spvalue_part_" + idx + "':'" + $("input[name='spvalue_part_" + idx +"']").val() + "','";
	}
	
	sp_value_json = sp_value_json.substr(0, sp_value_json.length - 2) + "}";
	
	return sp_value_json;
}

function composeWIJSON() {
	//var wi_intros = ["WI_1", "WI_2", "WI_3", "WI_4", "WI_5", "WI_6", "WI_7"];
	var wi_json = "'";
	for(var idx = 1; idx <= 7; idx++) {
		wi_json += $("select[name='wi_" + idx + "']").val();
	}
	wi_json += "'";
	
	return wi_json;
}


/* update by CL on 2010-06-08 */
function saveFCJSON() {
	var fc_json = composeFCJSON();
	
	if( $("#fc_copy_all").attr("checked") ){
		$("input[name^='fc_info_']").each(function(){
			$(this).val(fc_json);
		});
		
		$(".FC_item").each(function(){
			$(this).html($("select[name='fc_components']").find("option:selected").text());
		});
	}else{
		var id = $(".fc-addition-check").attr("info", id);
		$("a#FC_" + id).html($("select[name='fc_components']").find("option:selected").text());
		$("input[name='fc_info_" + $(".fc-addition-check").attr("info") + "']").val(fc_json);
	}
	closeDiv('FC');
}

function saveWIJSON(){
	var wi_json = composeWIJSON();

	if (wi_json.indexOf('0', 0) != -1) {
			$.prompt("Please complete the input of Wash Instruction!", {
				opacity: 0.6,
				prefix: 'cleanred'
			});
	}else if( $("#wi_copy_all").attr("checked") ){
		$("input[name^='wi_info_']").each(function(){
			$(this).val(wi_json);
		});
		
		$(".WI_item").each(function(){
			$(this).html(wi_json.replace(/\'/g, ""));
		});
	}else{
		var id = $(".wi-addition-check").attr("info", id);
		var content = '';
		
		for (var count = 1; count <= 7; count++) {
			content += $("select[name=wi_" + count + "]").val();
		}
			
		$("a#WI_" + id).html(content);
		$("input[name='wi_info_" + $(".wi-addition-check").attr("info") + "']").val(wi_json);
	}
	
	closeDiv('WI');
}

function saveSPValueJSON() {
	var spvalue_json = composeSPValueJSON();
	
	var id = $(".spv-check").attr("info", id);
	$("a#SPV_" + id).html("Special value added.");
	$("input[name='spvalue_info_" + $(".spv-check").attr("info") + "']").val(spvalue_json);
	
	closeDiv('SPValue');
}

function showValues(count, value) {
	$("input[name='fc_cc_name" + count + "']").val(value);
}

/*
function saveFCJSON() {
	var fc_json = composeFCJSON();
	var id = $(".fc-addition-check").attr("info", id);

	$("a#FC_" + id).html($("select[name='fc_components']").find("option:selected").text());
	$("input[name='fc_info_" + $(".fc-addition-check").attr("info") + "']").val(fc_json);
	
	closeDiv('FC');
}


function saveFCJSONToAll() {
	var fc_json = composeFCJSON();
	
	$("input[name^='fc_info_']").each(function(){
		$(this).val(fc_json);
	});
	
	$(".FC_item").each(function(){
		$(this).html($("select[name='fc_components']").find("option:selected").text());
	});
	
	closeDiv('FC');
}


function saveWIJSON() {
	var wi_json = composeWIJSON();
	var id = $(".wi-addition-check").attr("info", id);
	var content = '';
	
	for (var count = 1; count <= 7; count++) {
		content += $("select[name=wi_" + count + "]").val();
	}
		
	$("a#WI_" + id).html(content);
	$("input[name='wi_info_" + $(".wi-addition-check").attr("info") + "']").val(wi_json);
	
	closeDiv('WI');
}


function saveWIJSONToAll() {
	var wi_json = composeWIJSON();
	
	$("input[name^='wi_info_']").each(function(){
		$(this).val(wi_json);
	});
	
	$(".WI_item").each(function(){
		$(this).html(wi_json.replace(/\'/g, ""));
	});
	
	closeDiv('WI');
}

*/