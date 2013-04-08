/**
 * Created with PyCharm.
 * User: Ars
 * Date: 02.04.13
 * Time: 1:30
 * To change this template use File | Settings | File Templates.
 */

(function($) {

    var len;
    var issued;

    var methods = {
        init : function(options){
            len = options.product_len;
            issued = options.issued;
            for (var i=0;i<len;i++){
                var total = $('#id_productofpurchase_set-'+i+'-acceptance_amount').val() * $('#id_productofpurchase_set-'+i+'-acceptance_price').val();
                $('#total_product-'+i).text(total);
            }
            calc();
            $('input:not(#id_costs,#id_cash)').on('focusout',function(){
                var pk = this.id;
                pk = pk.substring(25, pk.indexOf('-acceptance'));
                var total = $('#id_productofpurchase_set-'+pk+'-acceptance_amount').val() * $('#id_productofpurchase_set-'+pk+'-acceptance_price').val();
                $('#total_product-'+pk).text(total);

                calc();
            });
            $('#id_costs, #id_cash').on('focusout',function(){
                calc();
            });
            $('#create').on('click',function(){
                var info = false;
                $('tbody input').each(function(){
                    if ($(this).val()==''){
                        info = true;
                    }
                });
                if (info==true){
                    alert('Заполните все поля в таблице');
                }else{
                    $('#create_submit').click();
                }
            });
        }
    };

    function calc(){
        var main_total = 0;
        var main_total_purchase = 0;
        for (var i=0;i<len;i++){
            main_total += parseInt($('#total_product-'+i).text());
            main_total_purchase += parseInt($('#purchase_sum_'+i).text());
        }
//        var balance = main_total_purchase - main_total - $('#id_costs').val();
        var balance = parseInt(issued) - main_total - $('#id_costs').val();
        var debt = $('#id_cash').val()-balance;
        $('#total').text(main_total);
        $('#balance').text(balance);
        $('#debt').text(debt);
    }

    $.fn.acceptance = function( method ) {
        if ( methods[method] ) {
            return methods[method].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Метод ' +  method + ' не существует в acceptance.js' );
        }
    };

}(jQuery));

