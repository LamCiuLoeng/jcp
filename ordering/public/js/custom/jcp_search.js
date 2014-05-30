$(document).ready(function(){
    var dateFormat = 'yy-mm-dd';
    
    $(".datePicker").datepicker({firstDay: 1 , dateFormat: dateFormat});
    $(".v_is_date").attr("jVal",
                         "{valid:function (val) {if(val!=''){return /^[0-9]{4}\\-[0-9]{2}\\-[0-9]{2}$/.test(val) }return true;}, message:'YYYY-MM-DD', styleType:'cover'}");    
});

var search_url = "/order/search";

function toSearch(){
	var f = $(".tableform");
	
	$(f).append('<input type="hidden" name="criteria" value="' + searchCriteria() + '"/>');
	$(f).attr("action", search_url).submit();
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