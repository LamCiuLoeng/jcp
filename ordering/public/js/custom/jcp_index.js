$(document).ready(function(){
	
	$(".numeric").numeric();
    $(".v_is_date").attr("jVal","{valid:function (val) {if(val!=''){return /^[0-9]{4}\\-[0-9]{2}\\-[0-9]{2}$/.test(val) }return true;}, message:'YYYY-MM-DD', styleType:'cover'}");    

	/*
    $(".ajaxSearchField").each(function(){
        var jqObj = $(this);
            jqObj.autocomplete("/order/getAjaxField", {
                    extraParams: {
                       fieldName: jqObj.attr("fieldname")
                    },
                    formatItem: function(item){
                           return item[0]
                    },
                    matchCase : true
            });
    });
    */
    
    
    $("form").submit(function(){
		if($("[name='order_type']:checked").length < 1){
    		$.prompt("Please select the ordering type before you place a order!",{opacity: 0.6,prefix:'cleanred'});
    		return false;
    	}
		if($(":radio:checked").val() == 'order_by_pom') {
			if(!$("[name='poNo']").val()){
    			$.prompt("Please input the JCPenney POM#!",{opacity: 0.6,prefix:'cleanred'});
    			return false;
    		}
			/*if (!$("#pom_customerPO").val()) {
				$.prompt("Please input the Vendor PO#!",{opacity: 0.6,prefix:'cleanred'});
    			return false;
			}*/
		}
		if ($(":radio:checked").val() == 'order_by_sub') {
			/*if (!$("#sub_customerPO").attr('value')) {
				$.prompt("Please input the Vendor PO#!",{opacity: 0.6,prefix:'cleanred'});
    			return false;
			}*/
			if(!$("[name='sub']").val()){
    			$.prompt("Please input the Sub#!",{opacity: 0.6,prefix:'cleanred'});
    			return false;
    		}
			if(!$("[name='lot']").val()){
    			$.prompt("Please input the Lot#!",{opacity: 0.6,prefix:'cleanred'});
    			return false;
    		}
		}
		/*if ($(":radio:checked").val() == 'order_by_manual') {
			if (!$("#man_customerPO").val()) {
				$.prompt("Please input the Vendor PO#!",{opacity: 0.6,prefix:'cleanred'});
    			return false;
			}
		}
		
		if ($(":radio:checked").val() == 'order_for_national') {
			if (!$("#nat_customerPO").val()) {
				$.prompt("Please input the Vendor PO#!",{opacity: 0.6,prefix:'cleanred'});
    			return false;
			}
		}*/
    	
    	return true;
    });
    
});


function getRadioChecked(id){
	$("#"+id).attr("checked",true);
}


/*

var po_search_url = "/order/index";
var sub_search_url = "/order/sub";
var export_url = "/report/export";
var search_url = "/order/search";

function poSearch(){
	var f = $(".tableform");
	
	$(f).append('<input type="hidden" name="criteria" value="' + composeCriteria() + '"/>');
	$(f).attr("action", po_search_url).submit();
}

function subSearch(){
	var f = $(".tableform");
	if (composeCriteria() != false) {
		$(f).append('<input type="hidden" name="criteria" value="' + composeCriteria() + '"/>');
		$(f).attr("action", sub_search_url).submit();
	}
}

function toSearch(){
	var f = $(".tableform");
	
	$(f).append('<input type="hidden" name="criteria" value="' + searchCriteria() + '"/>');
	$(f).attr("action", search_url).submit();
}

function toExport(){
	var f = $(".tableform");
	
	$(f).append('<input type="hidden" name="criteria" value="'+composeCriteria()+'"/>');
	$(f).attr("action",export_url).submit();		
}

function composeCriteria(){
	var criteria = new Array();
	var flag = true;
	
	$(".tableform input[type='text']").each(function(){
		var tmp = $(this);
		if( tmp.val() ){
            criteria.push( $("label[for='"+tmp.attr("id")+"']").text() + " : " + tmp.val() );
			flag = true;
		}else{
			if (tmp.attr("name") == 'sub' || tmp.attr("name") == 'lot') {
				flag = false;
				return false;
			}
		}
	});
	
	$("select").each(function(){
		var tmp = $(this);
		var s = $(":selected",tmp);
		if(s.val()){ 
			criteria.push( $("label[for='"+tmp.attr('id')+"']").text()+" : "+s.text() );
			flag = true;
		}
	});

	if (flag == true) {
		return criteria.join("|");
	} else {
		$.prompt("Please input search criteria!",{opacity: 0.6,prefix:'cleanred',show:'slideDown'});
		return false;
	}
}



function searchCriteria(){
	var criteria = new Array();
	
	$(".tableform input[type='text']").each(function(){
		var tmp = $(this);
		if( tmp.val() ){
            criteria.push( $("label[for='"+tmp.attr("id")+"']").text() + " : " + tmp.val() );
		}
	});
	
	$("select").each(function(){
		var tmp = $(this);
		var s = $(":selected",tmp);
		if(s.val()){ 
			criteria.push( $("label[for='"+tmp.attr('id')+"']").text()+" : "+s.text() );
		}
	});

	return criteria.join("|");
}

*/