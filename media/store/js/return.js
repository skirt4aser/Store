/**
 * Created with PyCharm.
 * User: Ars
 * Date: 03.04.13
 * Time: 23:29
 * To change this template use File | Settings | File Templates.
 */

(function($) {

    var len;

    var methods = {
        init : function(options){
            if ($('#failure').text()!=''){
                alert($('#failure').text());
            }
            len = options.product_len;
            for (var i=0;i<len;i++){
                var total = $('#id_productofpurchase_set-'+i+'-return_amount').val() * parseInt($('#acceptance_price_'+i).text());
                $('#total_product-'+i).text(total);
            }
            calc();
            $('table input').on('focusout',function(){
                var pk = this.id;
                pk = pk.substring(25, pk.indexOf('-return'));
                var total = $('#id_productofpurchase_set-'+pk+'-return_amount').val() * parseInt($('#acceptance_price_'+pk).text());
                $('#total_product-'+pk).text(total);
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
        for (var i=0;i<len;i++){
            main_total += parseInt($('#total_product-'+i).text());
        }
        $('#total').text(main_total);
    }

    $.fn.return_ = function( method ) {
        if ( methods[method] ) {
            return methods[method].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Метод ' +  method + ' не существует в return.js' );
        }
    };

}(jQuery));

