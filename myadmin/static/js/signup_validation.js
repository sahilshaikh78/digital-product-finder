$(function() {
    

        $("#name_error").hide();
        $("#email_error").hide();
        $("#password_error").hide();
        $("#register_btn").prop('disabled', true);
        var name_err = false;
        var email_error = false;
        var password_error = false;

        $("#name").keyup(function(){
            check_name();
        });
       $("#email").keyup(function(){
            check_email();
        });
        $("#password").keyup(function(){
            check_password();
        });

        function check_name(){
            var pattern = /^[a-zA-Z]*$/;
            var name = $("#name").val();
            if(pattern.test(name) && name !== ''){
                $("#name_error").hide();
                $("#name").css("border","2px solid green");
                $("#register_btn").prop('disabled', false);

            }else{
                $("#name_error").html("<i class='fas fa-exclamation-circle'></i> Should contain only Characters");
                $("#name_error").show();
                $("#name").css("border","2px solid red");
                name_err = true;
                $("#register_btn").prop('disabled', true);

            }
        }
      function check_email(){
            var pattern = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
            var email = $("#email").val();
            if(pattern.test(email) && email !== ''){
                $.ajax({
                    type:'POST',
                    url: '/email_check/',
                    data : { 
                        email: $('#email').val(),
                        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
                    },
                    success: function(data) {
                        if (data.is_taken) {
                            $("#email_error").html("<i class='fas fa-exclamation-circle'></i> Email Already Exists! Please Try other Email");
                            $("#email_error").show();
                            email_error = true;
                            $("#register_btn").prop('disabled', true);

                        }else{
                            $("#email_error").hide();
                            $("#email").css("border","2px solid green");
                            email_error = false;
                            $("#register_btn").prop('disabled', false);

                        }
                    },
                });
                $("#email_error").hide();
                $("#email").css("border","2px solid green");
                $("#register_btn").prop('disabled', false);
            }else{
                $("#email_error").html("<i class='fas fa-exclamation-circle'></i> Invalid Email");
                $("#email_error").show();
                $("#email").css("border","2px solid red");
                email_error = true;
                $("#register_btn").prop('disabled', true);

            }
        }
        
        function check_password(){
            var password_len = $("#password").val().length;
            if(password_len < 6){
                $("#password_error").html("<i class='fas fa-exclamation-circle'></i> Atleast 6 Characters");
                $("#password_error").show();
                $("#password").css("border","2px solid red");
                password_error = true;
                $("#register_btn").prop('disabled', true);

            }else{
                $("#password_error").hide();
                $("#password").css("border","2px solid green");
                $("#register_btn").prop('disabled', false);

            }
        }

        $("#signup_form").submit(function(){
             name_err = false;
             email_error = false;
             password_error = false;

            check_name();
            check_email();
            check_password();

            if(name_err === false && email_err === false && password_err === false){
                return true;
            }else{
                return false;
            }
        });
});