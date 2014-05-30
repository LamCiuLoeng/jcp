function saveArtwork(){
	$("#artwork-file").submit();
	$(".item-artwork").slideUp();
}

function destroyArtwork(){
	$(".item-artwork").slideUp();
}

function getFileName(obj){
    var tmp = $(obj);
	var path = tmp.val();
	if( path && path.length > 0){
		var location = path.lastIndexOf("\\") > -1 ?path.lastIndexOf("\\") + 1 : 0;
		var fn = path.substr( location,path.length-location );	
		tmp.prev("input[type='text']").val(fn);
	}
}

$(document).ready(function(){
	if($("#combo_item_1:checked").val() == 'False') {
		$("#combo_packaging_code").parent().parent().hide();
	}
	
	if($("#combo_mapping_1:checked").val() == 'False') {
		$("#hangtang_pkg_code").parent().parent().hide();
		$("#label_pkg_code").parent().parent().hide();
	}
	
	if($("#special_value_1:checked").val() == 'False') {
		$("#multi_special_value").parent().parent().hide();
	}
	
	$("<li style='color:red'>Matchbook/Barcode Combo:</li><br />").insertBefore($("#combo_item_0").parent().parent().find("li.label"));
	$("<li style='color:red'>Combo Items:</li><br />").insertBefore($("#combo_mapping_0").parent().parent().find("li.label"));
	$("<li style='color:red'>Special Value:</li><br />").insertBefore($("#special_value_0").parent().parent().find("li.label"));
	
	if ("$.broswer.msie") {
		$("input:radio").click(function(){
			this.blur();
			this.focus();
		});
	}
	
	$("input[name='combo_item']").change(function(){
		if($("#combo_item_0:checked").val() == 'True') {
			$("#combo_packaging_code").parent().parent().show();
			$("<li id='combo_packaging_code_warn' style='color:red'>Make sure this packaging code is set up as an individual item</li>").insertAfter($("#combo_packaging_code").parent());
		}
		
		if($("#combo_item_1:checked").val() == 'False') {
			$("#combo_packaging_code").parent().parent().hide();
			$("#combo_packaging_code_warn").remove();
		}
	});
	
	$("input[name='combo_mapping']").change(function(){
		if($("#combo_mapping_0:checked").val() == 'True') {
			$("#hangtang_pkg_code").parent().parent().show();
			$("#label_pkg_code").parent().parent().show();
			$("<li id='hangtag_pkg_code_warn' style='color:red'>Make sure this packaging code is set up as an individual item</li>").insertAfter($("#hangtang_pkg_code").parent());
			$("<li id='label_pkg_code_warn' style='color:red'>Make sure this packaging code is set up as an individual item</li>").insertAfter($("#label_pkg_code").parent());
		}
		
		if($("#combo_mapping_1:checked").val() == 'False') {
			$("#hangtang_pkg_code").parent().parent().hide();
			$("#label_pkg_code").parent().parent().hide();
			$("#hangtag_pkg_code_warn").remove();
			$("#label_pkg_code_warn").remove();
		}
	});
	
	$("input[name='special_value']").change(function(){
		if($("#special_value_0:checked").val() == 'True') {
			$("#multi_special_value").parent().parent().show();
			$("<li id='special_value_warn' style='color:red'>To enter the special value option, please go to the special value screen.</li>").insertAfter($("#multi_special_value").parent());
		}
		
		if($("#special_value_1:checked").val() == 'False') {
			$("#multi_special_value").parent().parent().hide();
			$("#special_value_warn").remove();
		}
	});
});
