jQuery(document).ready(function ($) {
    (function ($) {
        $(function () {
            var selectField = $('#id_project');
            var selectFieldUser = $('#id_project_module');

            selectField.change(function () {
                // alert('JIIIIIIIIIIIIIIIIIIII')
                moduleFun()
                assignUser()
                
            });
            selectFieldUser.change(function () {
                if($(this).val() !=''){
                    assignUser()
                }
            });
            function moduleFun(){
                var serializedData = $('#bug_form').serialize();
                $.ajax(
                    {
                        type:"POST",
                        url: "/portal/assignProjectModels",
                        data: serializedData,
                        success: function( data ) 
                        {
                            $('#id_project_module').html(' ')
                            let html_data = '';
                            html_data += `<option value="">---------------</option>`
                            if(data.module){
                                var module =data.module;
                          
                                module.forEach(function (pm) {
                                    html_data += `<option value="${pm.id}">${pm.project_module}</option>`
                                    
                                });
                                console.log(html_data)
                                $("#id_project_module").html(html_data);  
                            }
                          
                        }
                     })
            }
            function assignUser(){
                var serializedData = $('#bug_form').serialize();
                $.ajax(
                    {
                        type:"POST",
                        url: "/portal/assignProjectModels",
                        data: serializedData,
                        success: function( data ) 
                        {
                            $('#id_assign_user').html(' ')
                            let html_data_user = '';
                            html_data_user += `<option value="">---------------</option>`
                            if(data.select_user){
                                var user =data.select_user;
                        
                                user.forEach(function (user) {
                                    html_data_user += `<option value="${user.id}">${user.username}</option>`
                                    
                                });
                                $("#id_assign_user").html(html_data_user);  
                            }
                        
                        }
                    })
            }
        });
    })(django.jQuery);
});