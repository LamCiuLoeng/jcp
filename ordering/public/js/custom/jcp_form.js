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
		$("#billAddress").val('');
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
	var msg = Array();
	
	if( $("#shipCompany").find("option:selected").text().length <= 1  ){msg.push("* Please select the 'Ship To' company!");}
	if( !$.trim($("#shipAddress").val()) ){msg.push("* Please input the 'Ship To' address!");}
	if( !$.trim($("#shipAttn").val()) ){msg.push("* Please input the 'Ship To' contact!");}
	if( $("#billCompany").find("option:selected").text().length <= 1  ){msg.push("* Please select the 'Bill To' company!");}
	if( !$.trim($("#billAddress").val()) ){msg.push("* Please input the 'Bill To' address!");}
	if( !$.trim($("#billAttn").val()) ){msg.push("* Please input the 'Bill To' contact!");}
	if( !$("#customerPO").val() ){msg.push("* Please input the 'Vendor PO#'!");};
	if( !$("#sendEmailTo").val() ){msg.push("* Please select the 'Packaging Country'!");};
	if( !$("#supplierNO").val() ){msg.push("* Please input the 'supplier#'!");}
	if( !$("select[name='origin']").val()){msg.push("* Please select the 'Country of Origin'!");}
	
	if( $(".rfid_selection").length >= 1 && $(".rfid_selection").val() == "" ) {
		msg.push("* Please select the 'Order Option'!");
	}
	
	if( $(".national_selection").length >= 1 && $(".national_selection").val() == "" ) {
		msg.push("* Please select the 'Stock Number'!");
	}
	
	if ($("#rnCode").val() == "" && $("#wplCode").val() == "") {
		msg.push("* Please fill in the field(s) of either MFG RN# or JCP WPL#!");
	}
	
	var isRetailInput = false;
	var isRetailFormat = true;
	$("input[name^='retail_']").each(function(){
		var t = $(this);
		reg = /^\d+?$/;
		
		if( t.val() && t.val()!="0" ){
			isRetailInput = true;
			
			if(!reg.test(t.val())) {
				isRetailFormat = false;
			}
		}
	});
	
	$("input[name^='private_retail_']").each(function(){
		var t = $(this);
		reg=/^\d+?$/;
		
		if( t.val() && t.val()!="0" ){
			isRetailInput = true;
			
			if (!reg.test(t.val())) {
				isRetailFormat = false;
			}
		}
	});
	
	if(!isRetailInput){msg.push("* Please input at least one Retail!");}
	if(!isRetailFormat){msg.push("* Please input Retail with Integer format, do not contain decimal or cent !");}
	
	var isQtyInput = false;
	var isQtyFormat = true;
	$("input[name^='quantity_']").each(function(){
		var t = $(this);
		reg = /^\d+?$/;
		if( t.val() && t.val()!="0" ){isQtyInput = true;}
		if(!reg.test(t.val())){ isQtyFormat = false; }
	});
	
	$("input[name^='private_quantity_']").each(function(){
		var t = $(this);
		reg = /^\d+?$/;
		if( t.val() && t.val()!="0" ){isQtyInput = true;}
		if(!reg.test(t.val())){ isQtyFormat = false; }
	});
	
	if(!isQtyInput){msg.push("* Please input at least one qty!");}
	if(!isQtyFormat){msg.push("* Please input Quantity with Integer format, do not contain decimal or blank space !");}
	
	$(".FC_item").each(function() {
		if ($(this).html() != "Edit") {
			fc_valid = true;
		}
	});
	
	var isSPVInput = true;
	$("input[name^='spv_info_']").each(function(){
		var t = $(this);
		var id = $(this).attr("name").split("_")[2];
                
		if( $("input[name='quantity_" + id + "']").val() && $("input[name='quantity_" + id + "']").val() != '0' && !t.val() ){
			isSPVInput = false;
		}
	});
	
	if(!isSPVInput){msg.push("* Please Input Special Value at least for One Item!");}
	if (!fc_valid){msg.push("* Please input the Fiber content information!");}
	
	$(".WI_item").each(function() {
		if ($(this).html() != "Edit") {
			wi_valid = true;
		}
	});
	
	if (!wi_valid){msg.push("* Please input the Washing instruction information!");}
	
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
	
	if ($("input[name='fc_infos']").val() && $("input[name='fc_infos']").val().indexOf("percent") < 0 ) { 
		msg.push("Please fill in the fiber content information complete!");
	}
	
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

function toConfirmUpdate(){
	var valid = true;
	var msg = Array();
	
	if( !$("#shipCompany").val() ){msg.push("* Please select the 'Ship To' company!");}
	if( !$.trim($("#shipAddress").val()) ){msg.push("* Please input the 'Ship To' address!");}
	if( !$("#billCompany").val() ){msg.push("* Please select the 'Bill To' company!");}
	if( !$.trim($("#billAddress").val()) ){msg.push("* Please input the 'Bill To' address!");}
	if( !$("#customerPO").val() ){msg.push("* Please input the 'Vendor PO#'!");};
	if( !$("#sendEmailTo").val() ){msg.push("* Please select the 'Packaging Country'!");};
	if( !$("#supplierNO").val() ){msg.push("* Please input the 'supplier#'!");}
	if( !$("select[name='origin']").val()){msg.push("* Please select the 'Country of Origin'!");}
	
	if( $(".rfid_selection").length >= 1 && $(".rfid_selection").val() == "" ) {
		msg.push("* Please select the 'Order Option'!");
	}
	
	if( $(".national_selection").length >= 1 && $(".national_selection").val() == "" ) {
		msg.push("* Please select the 'Stock Number'!");
	}
	
	if ($("#rnCode").val() == "" && $("#wplCode").val() == "") {
		msg.push("* Please fill in the field(s) of either MFG RN# or JCP WPL#!");
	}
	
	var isRetailInput = false;
    var isRetailFormat = true;
	$("input[name^='retail_']").each(function(){
		var t = $(this);
		reg=/^\d+?$/;
		
		if( t.val() && t.val()!="0" ){
			isRetailInput = true;
			
			if (!reg.test(t.val())) {
				isRetailFormat = false;
			}
		}
	});
	
	$("input[name^='private_retail_']").each(function(){
		var t = $(this);
		reg=/^\d+?$/;
		
		if( t.val() && t.val()!="0" ){
			isRetailInput = true;
			
			if (!reg.test(t.val())) {
				isRetailFormat = false;
			}
		}
	});
	
	if(!isRetailInput){msg.push("* Please input at least one Retail!");}
	if(!isRetailFormat) {msg.push("* Please input Retail with Integer format, do not contain decimal or cent !");}
	
	var isQtyInput = false;
	var isQtyFormat = true;
	$("input[name^='quantity_']").each(function(){
		var t = $(this);
		reg = /^\d+?$/;
		if( t.val() && t.val()!="0" ){isQtyInput = true;}
		if(!reg.test(t.val())){ isQtyFormat = false; }
	});
	
	$("input[name^='private_quantity_']").each(function(){
		var t = $(this);
		reg = /^\d+?$/;
		if( t.val() && t.val()!="0" ){isQtyInput = true;}
		if(!reg.test(t.val())){ isQtyFormat = false; }
	});
	
	if(!isQtyInput){msg.push("* Please input at least one qty!");}
	if(!isQtyFormat){msg.push("* Please input Quantity with Integer format, do not contain decimal or blank space !");}
	
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
	
	if ($("input[name='fc_infos']").val() && $("input[name='fc_infos']").val().indexOf("percent") < 0 ) { 
		msg.push("Please fill in the fiber content information complete!");
	}
	
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

function toCancel(){
	if(confirm("The form hasn't been saved,are you sure to leave the page?")){
		return true;
	}else{
		return false;
	}
}

$(document).ready(function(){
	$origin_rfid = $(".gridTable tbody tr:first").find("td:first").html();
	$table_length = $(".gridTable tbody tr").length;
	
	$(".rfid_selection").change(
			function(){
				$option_value = $(this).val();
				
				if ($option_value.substring(0, 1) == '0') {
					$(".gridTable tbody tr").each(function(){
						if ($(".gridTable tbody tr").length / 2 < $table_length) {
							$(this).clone().insertAfter(this);
						}
					});
					
					$(".gridTable tbody tr:odd").each(function(){
						$(this).attr("class", "odd");
						
						if ($(this).find("td:first").attr("name") != "private_brand") {
							if ($option_value.length > 2) {
								$(this).find("td:first").html($option_value.split("-")[1]);
							}
							
							$(this).find("td:first").attr("name", "private_brand");
						}
						
						if ($(this).find("input[name^=private_retail_" + "]").attr("name")) {
							$ext_retail_id = $(this).find("input[name^=private_retail_" + "]").attr("name");
						} else if ($(this).find("input[name^=retail_" + "]").attr("name")) {
							$ext_retail_id = "private_" + $(this).find("input[name^=retail_" + "]").attr("name");
						}
						
						if ($(this).find("input[name^=private_quantity_" + "]").attr("name")) {
							$ext_quantity_id = $(this).find("input[name^=private_quantity_" + "]").attr("name");
						} else if ($(this).find("input[name^=quantity_" + "]").attr("name")) {
							$ext_quantity_id = "private_" + $(this).find("input[name^=quantity_" + "]").attr("name");
						}
						
						if ($(this).find("input[name^=private_spv_info_" + "]").attr("name")) {
							$ext_spv_id = $(this).find("input[name^=private_spv_info_" + "]").attr("name");
						} else if ($(this).find("input[name^=spv_info_" + "]").attr("name")) {
							$ext_spv_id = "private_" + $(this).find("input[name^=spv_info_" + "]").attr("name");
						}
						
						if ($(this).find("input[name^=private_fc_info_" + "]").attr("name")) {
							$ext_fc_id = $(this).find("input[name^=private_fc_info_" + "]").attr("name");
						} else if ($(this).find("input[name^=fc_info_" + "]").attr("name")) {
							$ext_fc_id = "private_" + $(this).find("input[name^=fc_info_" + "]").attr("name");
						}
						
						if ($(this).find("input[name^=private_wi_info_" + "]").attr("name")) {
							$ext_wi_id = $(this).find("input[name^=private_wi_info_" + "]").attr("name");
						} else if ($(this).find("input[name^=wi_info_" + "]").attr("name")) {
							$ext_wi_id = "private_" + $(this).find("input[name^=wi_info_" + "]").attr("name");
						}
						
						if ($(this).find("input[name^=private_misc1_" + "]").attr("name")) {
							$ext_misc1_id = $(this).find("input[name^=private_misc1_" + "]").attr("name");
						} else if ($(this).find("input[name^=misc1_" + "]").attr("name")) {
							$ext_misc1_id = "private_" + $(this).find("input[name^=misc1_" + "]").attr("name");
						}
						
						$("input[name^=retail_"+"]",this).attr("name", $ext_retail_id);
						$("input[name^=quantity_"+"]",this).attr("name", $ext_quantity_id);
						if(typeof($ext_spv_id) != 'undefined') {$("input[name^=spv_info_"+"]",this).attr("name", $ext_spv_id);}
						$("input[name^=fc_info_"+"]",this).attr("name", $ext_fc_id);
						$("input[name^=wi_info_"+"]",this).attr("name", $ext_wi_id);
						$("input[name^=misc1_"+"]",this).attr("name", $ext_misc1_id);
						
						$(this).find("td:eq(8)").find("a").hide()
						$(this).find("td:eq(9)").find("a").hide();
						$(this).find("td:eq(17)").find("a").hide();
						$(this).find("td:eq(1)").html($option_value.split("-")[3]);
					});
					
					$(".gridTable tbody tr:even").each(function(){
						$(this).attr("class", "even");
						
						if ($(this).find("td:first").attr("name") == "private_brand") {
							$(this).find("td:first").removeAttr("name");
							$(this).find("td:first").html($origin_rfid);
							
							if ($(this).find("input[name^=private_retail_" + "]").attr("name")) {
								$retail_id = $(this).find("input[name^=private_retail_" + "]").attr("name");
							} else if ($(this).find("input[name^=retail_" + "]").attr("name")) {
								$retail_id = "private_" + $(this).find("input[name^=retail_" + "]").attr("name");
							}
							
							if ($(this).find("input[name^=private_quantity_" + "]").attr("name")) {
								$quantity_id = $(this).find("input[name^=private_quantity_" + "]").attr("name");
							} else if ($(this).find("input[name^=quantity_" + "]").attr("name")) {
								$quantity_id = "private_" + $(this).find("input[name^=quantity_" + "]").attr("name");
							}
							
							if ($(this).find("input[name^=private_spv_info_" + "]").attr("name")) {
								$spv_id = $(this).find("input[name^=private_spv_info_" + "]").attr("name");
							} else if ($(this).find("input[name^=spv_info_" + "]").attr("name")) {
								$spv_id = "private_" + $(this).find("input[name^=spv_info_" + "]").attr("name");
							}
							
							if ($(this).find("input[name^=private_fc_" + "]").attr("name")) {
								$fc_id = $(this).find("input[name^=private_fc_" + "]").attr("name");
							} else if ($(this).find("input[name^=fc_info_" + "]").attr("name")) {
								$fc_id = "private_" + $(this).find("input[name^=fc_info_" + "]").attr("name");
							}
							
							if ($(this).find("input[name^=private_wi_info_" + "]").attr("name")) {
								$wi_id = $(this).find("input[name^=private_wi_info_" + "]").attr("name");
							} else if ($(this).find("input[name^=wi_info_" + "]").attr("name")) {
								$wi_id = "private_" + $(this).find("input[name^=wi_info_" + "]").attr("name");
							}
							
							if ($(this).find("input[name^=private_misc1_" + "]").attr("name")) {
								$misc1_id = $(this).find("input[name^=private_misc1_" + "]").attr("name");
							} else if ($(this).find("input[name^=misc1_" + "]").attr("name")) {
								$misc1_id = "private_" + $(this).find("input[name^=misc1_" + "]").attr("name");
							}
							
							$(this).find("input[name^=private_retail_"+"]").attr("name", $retail_id.substring(8, $retail_id.length));
							$(this).find("input[name^=private_quantity_"+"]").attr("name", $quantity_id.substring(8, $quantity_id.length));
							if (typeof($spv_id) != 'undefined') { $(this).find("input[name^=private_spv_info_"+"]").attr("name", $spv_id.substring(8, $spv_id.length)); }
							$(this).find("input[name^=private_fc_info_"+"]").attr("name", $fc_id.substring(8, $fc_id.length));
							$(this).find("input[name^=private_wi_info_"+"]").attr("name", $wi_id.substring(8, $wi_id.length));
							$(this).find("input[name^=private_misc1_"+"]").attr("name", $misc1_id.substring(8, $misc1_id.length));
						}
						
						$(this).find("td:eq(8)").find("a").show();
						$(this).find("td:eq(9)").find("a").show();
						$(this).find("td:eq(17)").find("a").show();
						$(this).find("td:eq(1)").html($option_value.split("-")[2]);
					});
				} else if ($option_value.substring(0, 1) == '1') {
					if ($(".gridTable tbody tr:first-child td:first").html() != $(".gridTable tbody tr:nth-child(2) td:first").html() && $(".gridTable tbody tr").length > 1) {
						$(".gridTable tbody tr:nth-child(even)").remove();
					}
					
					$(".gridTable tbody tr").each(function(){
						$(this).attr("class", "even");
						
						if ($(this).find("td:first").attr("name") == "private_brand") {
							$(this).find("td:first").removeAttr("name");
							$(this).find("td:first").html($origin_rfid);
							
							if ($(this).find("input[name^=private_retail_" + "]").attr("name")) {
								$retail_id = $(this).find("input[name^=private_retail_" + "]").attr("name");
							} else if ($(this).find("input[name^=retail_" + "]").attr("name")) {
								$retail_id = "private_" + $(this).find("input[name^=retail_" + "]").attr("name");
							}
							
							if ($(this).find("input[name^=private_quantity_" + "]").attr("name")) {
								$quantity_id = $(this).find("input[name^=private_quantity_" + "]").attr("name");
							} else if ($(this).find("input[name^=quantity_" + "]").attr("name")) {
								$quantity_id = "private_" + $(this).find("input[name^=quantity_" + "]").attr("name");
							}
							
							if ($(this).find("input[name^=private_spv_info_" + "]").attr("name")) {
								$spv_id = $(this).find("input[name^=private_spv_info_" + "]").attr("name");
							} else if ($(this).find("input[name^=spv_info_" + "]").attr("name")) {
								$spv_id = "private_" + $(this).find("input[name^=spv_info_" + "]").attr("name");
							}
							
							if ($(this).find("input[name^=private_fc_" + "]").attr("name")) {
								$fc_id = $(this).find("input[name^=private_fc_" + "]").attr("name");
							} else if ($(this).find("input[name^=fc_info_" + "]").attr("name")) {
								$fc_id = "private_" + $(this).find("input[name^=fc_info_" + "]").attr("name");
							}
							
							if ($(this).find("input[name^=private_wi_info_" + "]").attr("name")) {
								$wi_id = $(this).find("input[name^=private_wi_info_" + "]").attr("name");
							} else if ($(this).find("input[name^=wi_info_" + "]").attr("name")) {
								$wi_id = "private_" + $(this).find("input[name^=wi_info_" + "]").attr("name");
							}
							
							if ($(this).find("input[name^=private_misc1_" + "]").attr("name")) {
								$misc1_id = $(this).find("input[name^=private_misc1_" + "]").attr("name");
							} else if ($(this).find("input[name^=misc1_" + "]").attr("name")) {
								$misc1_id = "private_" + $(this).find("input[name^=misc1_" + "]").attr("name");
							}
							
							$(this).find("input[name^=private_retail_"+"]").attr("name", $retail_id.substring(8, $retail_id.length));
							$(this).find("input[name^=private_quantity_"+"]").attr("name", $quantity_id.substring(8, $quantity_id.length));
							if (typeof($spv_id) != 'undefined') { $(this).find("input[name^=private_spv_info_"+"]").attr("name", $spv_id.substring(8, $spv_id.length)); }
							$(this).find("input[name^=private_fc_info_"+"]").attr("name", $fc_id.substring(8, $fc_id.length));
							$(this).find("input[name^=private_wi_info_"+"]").attr("name", $wi_id.substring(8, $wi_id.length));
							$(this).find("input[name^=private_misc1_"+"]").attr("name", $misc1_id.substring(8, $misc1_id.length));
							
							$("#FC_" + $even_fc_id.split("_")[3]).show();
					    	$("#WI_" + $even_wi_id.split("_")[3]).show();
					    	$("#SPV_" + $even_spv_id.split("_")[3]).show();
						} else {
							$even_retail_id = $(this).find("input[name^=retail_" + "]").attr("name");
							$even_quantity_id = $(this).find("input[name^=quantity_" + "]").attr("name");
							$even_spv_id = $(this).find("input[name^=spv_info_" + "]").attr("name");
							$even_fc_id = $(this).find("input[name^=fc_info_" + "]").attr("name");
					    	$even_wi_id = $(this).find("input[name^=wi_info_" + "]").attr("name");
					    	$even_misc1_id = $(this).find("input[name^=misc1_" + "]").attr("name");
					    	
					    	$("#FC_" + $even_fc_id.split("_")[2]).show();
					    	$("#WI_" + $even_wi_id.split("_")[2]).show();
					    	$("#SPV_" + $even_spv_id.split("_")[2]).show();
						}
						
						$(this).find("td:eq(1)").html($option_value.split("-")[2]);
					});
				} else if ($option_value.substring(0, 1) == '2') {
					if ($(".gridTable tbody tr:first-child td:first").html() != $(".gridTable tbody tr:nth-child(2) td:first").html() && $(".gridTable tbody tr").length > 1) {
						$(".gridTable tbody tr:nth-child(odd)").remove();
					}
					
					$(".gridTable tbody tr").each(function(){
						$(this).attr("class", "odd");
						
						if ($(this).find("td:first").attr("name") != "private_brand") {
							$(this).find("td:first").html($option_value.substring(2, $option_value.length));
							$(this).find("td:first").attr("name", "private_brand");
					      	
					      	if ($(this).find("input[name^=private_retail_" + "]").attr("name")) {
								$ext_retail_id = $(this).find("input[name^=private_retail_" + "]").attr("name");
							} else if ($(this).find("input[name^=retail_" + "]").attr("name")) {
								$ext_retail_id = "private_" + $(this).find("input[name^=retail_" + "]").attr("name");
							}
							
							if ($(this).find("input[name^=private_quantity_" + "]").attr("name")) {
								$ext_quantity_id = $(this).find("input[name^=private_quantity_" + "]").attr("name");
							} else if ($(this).find("input[name^=quantity_" + "]").attr("name")) {
								$ext_quantity_id = "private_" + $(this).find("input[name^=quantity_" + "]").attr("name");
							}
							
							if ($(this).find("input[name^=private_spv_info_" + "]").attr("name")) {
								$ext_spv_id = $(this).find("input[name^=private_spv_info_" + "]").attr("name");
							} else if ($(this).find("input[name^=spv_info_" + "]").attr("name")) {
								$ext_spv_id = "private_" + $(this).find("input[name^=spv_info_" + "]").attr("name");
							}
							
							if ($(this).find("input[name^=private_fc_info_" + "]").attr("name")) {
								$ext_fc_id = $(this).find("input[name^=private_fc_info_" + "]").attr("name");
							} else if ($(this).find("input[name^=fc_info_" + "]").attr("name")) {
								$ext_fc_id = "private_" + $(this).find("input[name^=fc_info_" + "]").attr("name");
							}
							
							if ($(this).find("input[name^=private_wi_info_" + "]").attr("name")) {
								$ext_wi_id = $(this).find("input[name^=private_wi_info_" + "]").attr("name");
							} else if ($(this).find("input[name^=wi_info_" + "]").attr("name")) {
								$ext_wi_id = "private_" + $(this).find("input[name^=wi_info_" + "]").attr("name");
							}
							
							if ($(this).find("input[name^=private_misc1_" + "]").attr("name")) {
								$ext_misc1_id = $(this).find("input[name^=private_misc1_" + "]").attr("name");
							} else if ($(this).find("input[name^=misc1_" + "]").attr("name")) {
								$ext_misc1_id = "private_" + $(this).find("input[name^=misc1_" + "]").attr("name");
							}
							
							$("input[name^=retail_"+"]",this).attr("name", $ext_retail_id);
							$("input[name^=quantity_"+"]",this).attr("name", $ext_quantity_id);
							if(typeof($ext_spv_id) != 'undefined') {$("input[name^=spv_info_"+"]",this).attr("name", $ext_spv_id);}
							$("input[name^=fc_info_"+"]",this).attr("name", $ext_fc_id);
							$("input[name^=wi_info_"+"]",this).attr("name", $ext_wi_id);
							$("input[name^=misc1_"+"]",this).attr("name", $ext_misc1_id);
					      	
					      	$("#FC_" + $odd_fc_id.split("_")[2]).hide();
					    	$("#WI_" + $odd_wi_id.split("_")[2]).hide();
					    	$("#SPV_" + $odd_spv_id.split("_")[2]).hide();
						} else {
							$odd_retail_id = $(this).find("input[name^=private_retail_" + "]").attr("name");
							$odd_quantity_id = $(this).find("input[name^=private_quantity_" + "]").attr("name");
							$odd_spv_id = $(this).find("input[name^=private_spv_info_" + "]").attr("name");
							$odd_fc_id = $(this).find("input[name^=private_fc_info_" + "]").attr("name");
					    	$odd_wi_id = $(this).find("input[name^=private_wi_info_" + "]").attr("name");
					    	$odd_misc1_id = $(this).find("input[name^=private_misc1_" + "]").attr("name");
					    	
					    	$("#FC_" + $odd_fc_id.split("_")[3]).hide();
					    	$("#WI_" + $odd_wi_id.split("_")[3]).hide();
					    	$("#SPV_" + $odd_spv_id.split("_")[3]).hide();
						}
						
						$(this).find("td:eq(1)").html($option_value.split("-")[2]);
					});
				}
			}
	);
	
	$(".national_selection").change(
			function(){
				if ($(this).val() != '') {
					$(".gridTable tbody tr").each(function(){
						$(this).find("td:first").html('<a href="/order/showNBrandImg?name=' + $("select[name='national_brand']").val()
								  					  + '&height=600&width=900" title="Sample Image" rel="national-brand" class="thickbox">'
								  					  + $("select[name='national_brand']").val() + '</a>');
						$(this).attr("class", "odd");
						
						if ($(this).find("td:first").attr("name") != "private_brand" && $(".rfid_selection").length >= 1) {
							$(this).find("td:first").removeAttr("name");
							$(this).find("td:first").html($origin_rfid);
						}
					});
				} else if ($(this).val() == 'CUSTOM') {
					$(".gridTable tbody tr").each(function(){
						$(this).find("td:first").html("CUSTOM");
						$(this).attr("class", "even");
						
						if ($(this).find("td:first").attr("name") != "private_brand" && $(".rfid_selection").length >= 1) {
							$(this).find("td:first").removeAttr("name");
							$(this).find("td:first").html($origin_rfid);
						}
					});
				} else {
					$(".gridTable tbody tr").each(function(){
						/*$(this).find("td:first").html("Select above");*/
						$(this).find("td:first").html("");
						$(this).attr("class", "even");
						
						if ($(this).find("td:first").attr("name") != "private_brand" && $(".rfid_selection").length >= 1) {
							$(this).find("td:first").removeAttr("name");
							$(this).find("td:first").html($origin_rfid);
						}
					});
				}
				
				tb_init('a.thickbox, area.thickbox, input.thickbox');
			}
	);
	
	$(".numeric").numeric();
});

function composeJSON() {
	var fc_json = "{'";
	var wi_json = "{'";
	var spv_json = "{'";
	
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
	
	$("input[name^='spv_info_']").each(function(){
		if ($(this).val()) {
			spv_json += $(this).attr("name") + "':'" + $(this).val() + "','";
		}
	});
	
	spv_json = spv_json.substr(0, spv_json.length - 2) + "}";
	
	$("input[name='fc_infos']").val(fc_json);
	$("input[name='wi_infos']").val(wi_json);
	$("input[name='spv_infos']").val(spv_json);
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
