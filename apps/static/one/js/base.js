jQuery(document).ready(function ($) {
    (function ($) {
        $(function () {
            var selectField = $('#id_project');

            selectField.change(function () {
    
                var serializedData = $('#projectmodule_form').serialize();
                $.ajax(
                    {
                        type:"POST",
                        url: "/portal/assignProjectUser",
                        data: serializedData,
                        success: function( data ) 
                        {
                            $('#id_assign_module_user').html(' ')
                            let html_data = '';
                            let user =data.user;
                            html_data += `<option value="">---------------</option>`
                      
                         
                            user.forEach(function (user) {
                                
                                    html_data += `<option value="${user.assign}" ${user.select}>${user.username}</option>`
                                
                            });
                            $("#id_assign_module_user").html(html_data);
                        }
                     })
            });
            if($('#id_project').val()){
                // alert($('#id').val())
                var serializedData = $('#projectmodule_form').serialize();
                $.ajax(
                    {
                        type:"POST",
                        url: "/portal/assignProjectUser",
                        data: serializedData,
                        success: function( data ) 
                        {
                            $('#id_assign_module_user').html(' ')
                            let html_data = '';
                            let user =data.user;
                
                 
                            user.forEach(function (user) {
                     
                                    html_data += `<option value="${user.assign}" ${user.select}>${user.username}</option>`
                                
                            });
                            $("#id_assign_module_user").html(html_data);
                        }
                     })
            }
          
        });
    })(django.jQuery);
});