function changeBillTo(obj){
	var t = $(obj);
	
	if (t.val() != '0') {
		$(".other_billto").hide();
		
		var vs = billToInfo[t.val()];
		
		$("#billAddress").val(vs.address);
		$("#billAttn").val(vs.attn);
		$("#billTel").val(vs.tel);
		$("#billFax").val(vs.fax);
		$("#billEmail").val(vs.email);	
	} else {
		$(".other_billto").show();
		("#billAddress").val('');
		$("#billAttn").val('');
		$("#billTel").val('');
		$("#billFax").val('');
		$("#billEmail").val('');	
	}
}

function changeShipTo(obj){
	var t = $(obj);
	
	if (t.val() != '0') {
		$(".other_shipto").hide();
		
		var vs = shipToInfo[t.val()];
		
		$("#shipAddress").val(vs.address);
		$("#shipAttn").val(vs.attn);
		$("#shipTel").val(vs.tel);
		$("#shipFax").val(vs.fax);
		$("#shipEmail").val(vs.email);
	} else {
		$(".other_shipto").show();
		$("#shipAddress").val('');
		$("#shipAttn").val('');
		$("#shipTel").val('');
		$("#shipFax").val('');
		$("#shipEmail").val('');
	}
}


function changeCountry(obj){
	var t = $(obj);
	
	if(!t.val()){
		$("#country_contact").text("");
		$("#country_mail").html("");
		return;
	}
	
	var vs = contactInfo[t.val()];	
	var persons = []
	for(var i=0;i<vs.person.length;i++){
		var p = vs.person[i];
		persons.push( '<a href="mailto:'+p.persion_email+'">'+ p.persion_name +'</a>');
	}
	
	$("#country_contact").text(vs.phone);
	$("#country_mail").html(persons.join(",<br />"));
}


function toConfirm(){
	var valid = true;
	var fc_valid = false;
	var wi_valid = false;
	/*var upc_valid = true;*/
	var intRegex = /^\d+$/;
	var msg = Array();

	if( $("#shipCompany").find("option:selected").text().length <= 1  ){msg.push("* Please select the 'Ship To' company!");}
	if( !$.trim($("#shipAddress").val()) ){msg.push("* Please input the 'Ship To' address!");}
	if( !$.trim($("#shipAttn").val()) ){msg.push("* Please input the 'Ship To' contact!");}
	if( $("#billCompany").find("option:selected").text().length <= 1  ){msg.push("* Please select the 'Bill To' company!");}
	if( !$.trim($("#billAttn").val()) ){msg.push("* Please input the 'Bill To' contact!");}
	if( !$.trim($("#billAddress").val()) ){msg.push("* Please input the 'Bill To' address!");}
	if( !$("#customerPO").val() ){msg.push("* Please input the 'Vendor PO#'!");};
	if( !$("#sendEmailTo").val() ){msg.push("* Please select the 'Packaging Country'!");};
	if( !$("select[name='origin']").val()){msg.push("* Please select the 'Country of Origin'!");}
	
	if ($("#rnCode").val() == "" && $("#wplCode").val() == "") {
		msg.push("* Please fill in the field(s) of either MFG RN# or JCP WPL#!");
	}
	
	var isStockInput = false;
	$("input[name^='stock_']").each(function(){
		var t = $(this);
		if( t.val() && t.val()!="0" ){ 
			isStockInput = true;
		}
	});
	
	if(!isStockInput){msg.push("* Please input at least one Stock!");}
	
	var isSubInput = false;
	var isSameSub = true;
	var subFlag = $("input[name='sub_1_ext']").val();
	$("input[name^='sub_']").each(function(){
		var t = $(this);
		if( t.val() && t.val()!="0" ){ isSubInput = true; }
		if( t.attr("name") != "sub_x_ext" && t.val() && t.val() != subFlag){ isSameSub = false; }
	});
	
	if(!isSubInput){msg.push("* Please input at least one Sub!");}
	if(!isSameSub){msg.push("* Please input the same sub!");}
	
	var isSameLot = true;
	var lotFlag = $("input[name='lot_1_ext']").val();
	$("input[name^='lot_']").each(function(){
		var t = $(this);
		
		if( t.attr("name") != "lot_x_ext" && t.val() && t.val() != lotFlag){ isSameLot = false; }
	});
	
	if(!isSameLot){msg.push("* Please input the same lot!");}
	
	var isDescInput = false;
	$("input[name^='description_']").each(function(){
		var t = $(this);
		if( t.val() && t.val()!="0" ){isDescInput = true;}
	});
	
	if(!isDescInput){msg.push("* Please input at least one Lot Description!");}
	
	/*$("input[name^='upc_']").each(function(){
		var t = $(this);
		if( ( t.val() && !intRegex.test(t.val()) ) || ( t.val() && t.val().length != 12 && t.val().length != 14 ) ){ upc_valid = false; }
	});
	if(!upc_valid){msg.push("* Please input the correct UPC number!");}*/
	
	var isRetailInput = false;
    var isRetailFormat = true;
	$("input[name^='retail_']").each(function(){
		var t = $(this);
                reg=/^(\d+\.?)\d+?$/;
		if( t.val() && t.val()!="0" ){
                    isRetailInput = true;
                    
                    if (!reg.test(t.val())) {
                        isRetailFormat = false;
                    }
                }
	});
	
	if(!isRetailInput){msg.push("* Please input at least one Retail!");}
        if(!isRetailFormat){msg.push("* Please input Retail with this format: 8.99 !");}
	
	var isQtyInput = false;
	$("input[name^='quantity_']").each(function(){
		var t = $(this);
		if( t.val() && t.val()!="0" ){isQtyInput = true;}
	});
	if(!isQtyInput){msg.push("* Please input at least one qty!");}

	/*$(".FC_item").each(function() {
		if ($(this).html() != "Edit") {
			fc_valid = true;
		}
	});
	
	if (!fc_valid){ msg.push("* Please input the Fiber content information!"); }
	
	$(".WI_item").each(function() {
		if ($(this).html() != "Edit") {
			wi_valid = true;
		}
	});
	
	if (!wi_valid){ msg.push("* Please input the Washing instruction information!"); }*/
	
	$(".component").each(function(){
		var percentage = 0;
		
		$("input[name^='fc_percentage']",$(this)).each(function(){
			if ($(this).val() != '') {
				percentage += parseInt($(this).val());
			}
		});

		if (percentage != 100) {
			msg.push("* Please check the percentage, the total number should be equal to 100%!");
		}
	});
	
	composeJSON();
	
	/*if (!$("input[name='fc_infos']").val()) { msg.push("Please fill in the fiber content information!"); }
	if (!$("input[name='wi_infos']").val()) { msg.push("Please fill in the washing instruction information!"); }*/
	
	if( msg.length > 0 ){
		$.prompt(msg.join("<br />"),{opacity: 0.6,prefix:'cleanred'});
		return false;
	}else{
		$.prompt("We are going to confirm your order information in our Production System upon your final confirmation.<br /> \
				 Are you sure to confirm the order now?",
	    		{opacity: 0.6,
	    		 prefix:'cleanblue',
	    		 buttons:{'Yes':true,'No,Go Back':false},
	    		 focus : 1,
	    		 callback : function(v,m,f){
	    		 	if(v){
	    		 		$("form").submit();
	    		 	}
	    		 }
	    		}
	    	);
	}
}

confirmFlag = true;
$("input[name^='stock_']").each(function(){
	var t = $(this);
	
	if (t.val() & !t.val() == '0') {
		$.get("/order/ajax_check_status",{pkg_code: t.val()}, function(status){
			if (status == 'inactive') {
				confirmFlag = false;
			}
		});
	}
});

function check_status(obj) {
	$.get("/order/ajax_check_status",{pkg_code: $(obj).val()}, function(status){
		if (status == 'inactive') {
			$('.confirm').attr("onclick", '');
			$('.confirm').unbind('click');
			$('.confirm').click(function(){
				$.prompt("* The order contains item(s) cannot be ordered!",
						{
							opactity: 0.6,
							prefix: "cleanred",
							buttons: {
								'Yes': true
							}
						});
				});
				
			/*$.prompt("* The stock " + $(obj).val() + " cannot be booked!",
					 {opactity: 0.6,
					  prefix:"cleanred",
					  buttons:{'Yes':true},
					  focus : 1,
					  callback : function(v,m,f){
					  				if(v){ $(obj).focus(); }}
						});*/
		}
		else {
			$('.confirm').attr("onclick", "");
			$('.confirm').unbind('click');
			$('.confirm').click(function(){toConfirm();});
		}
	});
}

function toCancel(){
	if(confirm("The form hasn't been saved,are you sure to leave the page?")){
		return true;
	}else{
		return false;
	}
}

var INDEX = 1;

function toAdd(){
	INDEX++;
	var c = $(".template");
	var tr = c.clone()
	$("input",tr).each(function(){
		var t = $(this);
		var n = t.attr("name").replace("_x","_"+INDEX);

		t.attr("name",n);
	});
	$("select",tr).each(function(){
		var t = $(this);
		var n = t.attr("name").replace("_x","_"+INDEX);
		var value_id = t.attr("id").replace("_x", "_"+INDEX);

		t.attr("name",n);
		t.attr("id", value_id);
	});
	$("a",tr).each(function(){
		var t = $(this);
		if (t.attr("class") == 'FC_item') {
			var func = function(){
				showDiv(1, INDEX);
			}
		} else if (t.attr("class") == 'WI_item') {
			var func = function() {
				showDiv(2, INDEX);
			}
		}  else if (t.attr("class") == 'SPV_item') {
			var func = function() {
				showDiv(3, INDEX);
			}
		}
		
		var ids = t.attr("id").replace("_x", "_" + INDEX);
		
		t.attr("id", ids);
		t.unbind('click').removeAttr('onclick');
		t.bind('click', func);
	});
	tr.insertBefore(c[0]);
	tr.removeClass("template");
	tr.show();
	$(".numeric").numeric();
	$("input[name^='stock']",tr).focus();
}

$(document).ready(function(){
	$(".numeric").numeric();
	$("form").submit(function(){
		$(".template").remove();
	});
	
});

function composeJSON() {
	var fc_json = "{'";
	var wi_json = "{'";
	var special_value_json = "{'";
	
	$("input[name^='fc_info_']").each(function(){
		if ($(this).val()) {
			fc_json += $(this).attr("name") + "':'" + $(this).val() + "','";
		}
	});
	fc_json = fc_json.substr(0, fc_json.length - 2) + "}";
	
	$("input[name^='wi_info_']").each(function(){
		if ($(this).val()) {
			wi_json += $(this).attr("name") + "':'" + $(this).val() + "','";
		}
	});
	wi_json = wi_json.substr(0, wi_json.length - 2) + "}";
	
	$("input[name^='spvalue_info_']").each(function(){
		if ($(this).val()) {
			special_value_json += $(this).attr("name") + "':'" + $(this).val() + "','";
		}
	});
	special_value_json = special_value_json.substr(0, special_value_json.length - 2) + "}";
	
	$("input[name='fc_infos']").val(fc_json);
	$("input[name='wi_infos']").val(wi_json);
	$("input[name='special_value_infos']").val(special_value_json);
}


function clearInput(obj,exclude){
	var t = $(obj).parents("table")[0];
	
	var excludeStr = "";
	if(exclude.length > 0){ 
		exclude.unshift("");
		exclude.push("");
		excludeStr = exclude.join("|");
	}
	
	$("input,select,textarea",t).each(function(){
		var temp = $(this);
		if( excludeStr.indexOf("|"+temp.attr("id")+"|") < 0 ){temp.val("");}
	});
}