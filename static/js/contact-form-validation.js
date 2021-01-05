// Wait for the DOM to be ready
$(function() {
    // Initialize form validation on the registration form.
    // It has the name attribute "registration"
    $("form[name='contact']").validate({
      // Specify validation rules
      rules: {
        // The key name on the left side is the name attribute
        // of an input field. Validation rules are defined
        // on the right side
        name: "required",
        email: {
          required: true,
          // Specify that email should be validated
          // by the built-in "email" rule
          email: true
        },
        mobile: "required",
        msg: "required",
      },
      // Specify validation error messages
      messages: {
        name: "Please enter your name",
        email: "Please enter your email",
        mobile: "Please enter your mobile",

        /*name:{
            required: "Please enter your Name",
            lettersonly: "Please Enter the Valid Name"

        } ,
        email:{
            required: "Please enter your Email",
            email: "Please Enter the Valid Email"

        } ,
        mobile:{
            required: "Please enter your Mobile Number",
            digits: "Please Enter the Valid Mobile Number",
            maxlength: "Mobile Number Must be of 10 Digit"
        } ,*/
        msg: "Please enter your Message"
      },
      // Make sure the form is submitted to the destination defined
      // in the "action" attribute of the form when valid
      submitHandler: function(form) {
      
        form.submit();
      }
    });
  });