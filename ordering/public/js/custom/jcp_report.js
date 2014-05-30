$(document).ready(function(){
    var dateFormat = 'yy-mm-dd';
    
    $(".datePicker").datepicker({firstDay: 1 , dateFormat: dateFormat});
    $(".v_is_date").attr("jVal",
                         "{valid:function (val) {if(val!=''){return /^[0-9]{4}\\-[0-9]{2}\\-[0-9]{2}$/.test(val) }return true;}, message:'YYYY-MM-DD', styleType:'cover'}");    
});

var export_url = "/report/export";

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