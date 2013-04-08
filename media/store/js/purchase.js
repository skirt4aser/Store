/**
 * Created with PyCharm.
 * User: Ars
 * Date: 24.03.13
 * Time: 16:27
 * To change this template use File | Settings | File Templates.
 */

(function($) {

    var methods = {
        init : function(){
//            Сохраняем Закуп
            $('#create').on('click',function(){
                if (document.location.pathname=='/purchase/'){
                    alert('Добавьте товар для создания закупа');
                }else if($('#id_issued').val()==''){
                    alert('Поле выдано должно быть заполнено');
                }else{
                    var pk = document.location.pathname;
                    pk = pk.substring(10,pk.length-1);
                    $.post('/ajax/purchase/save/',{
                        csrfmiddlewaretoken :   $('input[name=csrfmiddlewaretoken]').val(),
                        id_purchase         :   pk,
                        id_supplier         :   $('#id_supplier :selected').val(),
                        id_purchaser        :   $('#id_purchaser :selected').val(),
                        id_warehouse        :   $('#id_warehouse :selected').val(),
                        date_purchase       :   $('#id_date_purchase').val(),
                        comment             :   $('#id_comment').val(),
                        issued              :   $('#id_issued').val()
                    },function(text,status){
                        if (status=='success'){
                            if (text=='ok'){
                                window.location.href = "/purchases/page/1/";
                            }else{
                                alert(text);
                            }
                        }
                    },'html');
                }
            });
//            Вытаскиваем цену товара
            $('#id_product').on('change',function(){
                $.post('/ajax/purchase/get_product_price/',{
                    csrfmiddlewaretoken :   $('input[name=csrfmiddlewaretoken]').val(),
                    id_product          :   $('#id_product :selected').val()
                },function(price,status){
                    if (status=='success'){
                        $('#id_purchase_price').val(price);
                    }
                },'html');
            });
//            Удаление товара
            $('.delete').on('click',function(){
                return confirm('Вы точно хотите удалить данный товар из закупа?');
            });
//            Меняем текст кнопки для удобства
            var path = document.location.pathname;
            if (path.indexOf('purchase')!=-1 && path.indexOf('product')!=-1){
                $('#add_product').text('Изменить товар');
            }
//            Удаление закупа
            $('#delete_purchase').on('click',function(){
                return confirm('Вы точно хотите удалить данный закуп?');
            });
        }
    };

    $.fn.purchase = function( method ) {
        if ( methods[method] ) {
            return methods[method].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Метод ' +  method + ' не существует в purchase.js' );
        }
    };

}(jQuery));

