function showShade() {
	$(".shade").css("display", "inline");
	$(".shade").css("width", $(document).width());
	$(".shade").css("height", $(document).height());
	
	$(".T_iframe").css("display", "inline");
	$(".T_iframe").css("width", $(document).width());
	$(".T_iframe").css("height", $(document).height());
	$(".T_iframe").css({'opacity':'0.0'});
	$(".shade").slideDown();
}

function showWIDiv(obj, id){
	showShade();
	$(".wi-addition-check").attr("info", id);
	for (var idx = 1; idx <= 7; idx++) {
		showIntro('wi_' + idx);
	}
	$(".wi-addition-check").slideDown();
}
		
function showFCDiv(obj, id){
	showShade();
	$(".fc-addition-check").attr("info", id);
	//$(".fc-addition-check .fc_component_color").remove();
	$(".fc-addition-check").slideDown();
}

function showSPVDiv(obj, id){
	showShade();
	$(".special-value-check").attr("info", id);
	$(".special-value-check").slideDown();
}

function showSIDiv(){
	showShade();
	$(".ship-instruction-check").slideDown();
}

function showSPValueDiv(obj, id){
	showShade();
	$(".spv-check").attr("info", id);
	$(".spv-check").slideDown();
}

function showLSDiv(obj){
	if($(obj).attr("checked")){
		showShade();
		$(".ls-addition-check").slideDown();
		for (var idx = 1; idx <= 6; idx++) {
			showIntro('ls_' + idx);
		}
	}else{
		if($("input[name='"+$(obj).attr('name')+"'][checked]").length<1){
			$(".shade").slideUp();
			$(".ls-addition-check").slideUp();
		}
	}
}

function closeDiv(item) {
	$(".shade").slideUp();
	
	if (item == 'FC') {
		$(".fc-addition-check").slideUp();
	} else if (item == 'SPV') {
		$(".special-value-check").slideUp();
	} else if (item == 'WI') {
		$(".wi-addition-check").slideUp();
	} else if (item == 'LS') {
		$(".ls-addition-check").slideUp();
		/*$("#washinstruction").attr("checked", false);*/
				
		var content = '';
		for (var count = 1; count <= 6; count++) {
			content += $("select[name=ls_" + count + "]").val();
		}
				
		$("#labelsystem_detail").text(content);
		$("a#labelsystem_detail").attr("href", "/order/ajaxInstruction?cls=ls" + "&val=" + content);
	} else if (item == 'SI') {
		$(".ship-instruction-check").slideUp();
	} else if (item == 'SPValue') {
		$(".spv-check").slideUp();
	}
}

function composeSPVJSON(part) {
	var spv_json = "'";
	for(var idx = 1; idx <= part; idx++) {
		spv_json += $("select[name='spv_" + idx + "']").val() + '|';
	}
	
	if ($("select[name^='spv_']").find("option:selected").text() == "cashmere blend" && $("#spv_content_part").length > 0) {
		var content_flag = 0;
		var fiber_flag = 0;
		for (var index = 1; index <= 4; index++) {
			if ($("#sp_content_prt_"+index).length > 0 && $("#sp_content_prt_"+index).val() != "" && $("#sp_content_"+index).length > 0 && $("#sp_content_"+index).val() != "") {
				spv_json += $("#sp_content_prt_"+index).val() + '%' + $("#sp_content_"+index).val() + '|';
				content_flag += 1;
				fiber_flag += parseInt($("#sp_content_prt_"+index).val());
			}
		}
		if (parseInt($("#spv_content_part").val()) != content_flag) {
			$.prompt("The number of content is not match your input, please check!",
				 {opacity: 0.6,prefix:'cleanred'});
		
			return false;
		}
		
		if (fiber_flag != 100) {
			$.prompt("The total number of content is not 100%!",
				 {opacity: 0.6,prefix:'cleanred'});
		
			return false;
		}
	}
	
	spv_json = spv_json.substr(0, spv_json.length - 1) + "'";
	
	return spv_json;
}

function saveSPVJSON(part) {
	var spv_json = composeSPVJSON(part);
	
	if (spv_json.indexOf('x') != -1) {
		$.prompt("If the no special value for that part, please select 'N/A'!",
				 {opacity: 0.6,prefix:'cleanred'});
		
		return false;
	}
	
	if( $("#spv_copy_all").attr("checked") ){
		$("input[name^='spv_info_']").each(function(){
			$(this).val(spv_json);
		});
		
		$("input[name^='private_spv_info_']").each(function(){
			$(this).val(spv_json);
		});
		
		$(".SPV_item").each(function(){
			$(this).html("Special Value(s) edited");
		});
	}else{
		var id = $(".special-value-check").attr("info", id);

		$("input[name='spv_info_" + $(".special-value-check").attr("info") + "']").val(spv_json);
		$("input[name='private_spv_info_" + $(".special-value-check").attr("info") + "']").val(spv_json);
		$("a#SPV_" + id).html("Special Value(s) edited");
	}
	closeDiv('SPV');
}

$(document).ready(function() {
	$(".private_brand").hide();
	$(".combo_item").hide();
	
	$("select[name^='spv_']").change(function(){
		if ($(this).find("option:selected").text() == "cashmere blend") {
			$(".spv_content").show();
		} else {
			$(".spv_content").hide();
		}
		
		$.get(
		"/order/ajaxSpecialValueImage",
		{'id': $(this).find("option:selected").val()},
		function(data){
			$(".sp_value").empty('');
			$(".special-value-check").append(data);
		});
	});
});
