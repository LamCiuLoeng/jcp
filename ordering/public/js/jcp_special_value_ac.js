$(document).ready(function(){

    $(".ajaxSearchField").each(function(){
        var jqObj = $(this);

            //jqObj.autocomplete("/pls/getAjaxField", {
            jqObj.autocomplete("/order/getAjaxField", {
                    extraParams: {
                       fieldName: jqObj.attr("name")
                    },
                    formatItem: function(item){
                           return item[0]
                    },
                    matchCase : true
            });

    });

});
