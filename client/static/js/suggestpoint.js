
$(document).ready(function(){


   $('.search-query').click(function(){
       $('.search-area').fadeIn(); 
       $('.close-btn').fadeIn();
       $('#search_input').focus();
       $.ajax({
            type:'GET',
            url: '/fetch_top_product_type/',
            success: function(data) { 
                var div  = document.getElementById("top_product_type");
                $.each(data.product_type_data, function(index, item) {
                    var a = document.createElement("a");
                    a.textContent = item['product_type_name'];
                    a.setAttribute('href', '/category'+'/'+ item['category__category_slug'] +'/'+item['product_type_slug']+'/');
                    div.appendChild(a);
              })
            },
       });          
   });
   $('.close-btn').click(function(){
       $('.search-area').fadeOut(); 
       document.getElementById('top_product_type').innerHTML = ""; 
   });
  
});
$("#search_input").keyup(function(e){
  e.preventDefault();
  var search_input = $("#search_input").val();
  if(search_input != ''){
        $.ajax({
            type:'GET',
            url: '/search_suggestion/',
            data : { 
                search_query: search_input,
            },
            success: function(data) {
              document.getElementById('search-results').innerHTML = '';
            if(data.category_data != ''){
                var label = document.createElement("div");
                label.innerHTML = "In Category";
                var div  = document.getElementById("search-results");
                div.appendChild(label);
                $.each(data.category_data, function(index, item) {
                    var a = document.createElement("a");
                    a.textContent = item['category_name'];
                    a.setAttribute('href', '/category/'+item['category_slug']+'/');
                    div.appendChild(a);
                }); 
            } 
            if(data.product_type_data != ''){
                var label = document.createElement("div");
                label.innerHTML = "In Product Category";
                var div  = document.getElementById("search-results");
                div.appendChild(label);
                $.each(data.product_type_data, function(index, item) {
                    var a = document.createElement("a");
                    a.textContent = item['product_type_name'];
                    a.setAttribute('href', '/category/'+item['category__category_slug']+'/'+item['product_type_slug']+'/');
                    div.appendChild(a);
                }); 
            }
            if(data.brand_data != ''){
                var label = document.createElement("div");
                label.innerHTML = "In Brand";
                var div  = document.getElementById("search-results");
                div.appendChild(label);
                $.each(data.brand_data, function(index, item) {
                    var a = document.createElement("a");
                    a.textContent = item['brand_name'];
                    a.setAttribute('href', '/'+item['category__category_slug']+'-reviews/'+item['brand_slug']+'/');
                    div.appendChild(a);
                }); 
            }         
           
            },
    })
  }else{
    document.getElementById('search-results').innerHTML = ''

  }
  
});


$(document).on('submit','#expert_suggestion_form',function(e){
    e.preventDefault();
    var delay = 3000;
    var suggestion_category = $("#suggestion_category").val();
    var customer_mo = $("#customer_mo_number").val().length;
    if(suggestion_category != 0 && customer_mo == 10){
        $("#update_alert").addClass("alert alert-danger");
        document.getElementById("customer_help_submit").disabled = true;
        $('#save_loader').addClass('spinner-border spinner-border-sm');
            $.ajax({
                type:'POST',
                url: '/save_expert_help/',
                data:{
                    customer_name:$('#customer_name').val(),
                    customer_email:$('#customer_email').val(),
                    customer_mo_number:$('#customer_mo_number').val(),
                    suggestion_category: suggestion_category,
                    customer_help_note:$('#customer_help_note').val(),
                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
                },
                success:function(data){
                    if(data.saved){
                        setTimeout(function() {
                            delaySuccess(data);
                          }, delay);
                    }
                }

            });
        }else if(suggestion_category == 0){
            $("#update_alert").removeClass("alert alert-success"); 
            $("#update_alert").removeClass("alert alert-warning"); 
            $("#update_alert").html("Please Select Suggestion Category!"); 
            $("#update_alert").addClass("alert alert-danger");
        }else if(customer_mo != 10){
            $("#update_alert").removeClass("alert alert-success"); 
            $("#update_alert").removeClass("alert alert-warning"); 
            $("#update_alert").html("Mobile Number must be of 10 Digit!"); 
            $("#update_alert").addClass("alert alert-danger");
        }else{
            $("#update_alert").removeClass("alert alert-success"); 
            $("#update_alert").removeClass("alert alert-warning"); 
            $("#update_alert").html("Opps! Something went wrong"); 
            $("#update_alert").addClass("alert alert-danger");
        }
});

function delaySuccess(data) {
    $('#save_loader').removeClass('spinner-border spinner-border-sm');
    document.getElementById("customer_help_submit").disabled = false;
    alert("Inquiery Saved Successfully! We will contact you soon");
    location.reload();
}

//find out items from localstorage
if(localStorage.getItem('compare') == null){
    var compare = {};
    document.getElementById('compareButton').style.display = 'none';
}else{
    compare = JSON.parse(localStorage.getItem('compare'));
    if(Object.keys(compare).length == 1){
        document.getElementById('pop_compare').innerHTML = 'Select 1 more company to compare';    
    }else{
        document.getElementById('pop_compare').innerHTML = 'Compare 2 Company';    

    }
    $('#compareButton').slideDown([3000][5000]);
    document.getElementById('compareButton').style.display = 'block';
}

//when brand compare click add or remove brand to comparsion
$('.compare').click(function(){
    var br_id = this.id.toString();
    if(compare[br_id] == undefined){
        brand_name = document.getElementById('namebr' + br_id).innerHTML;
        category = document.getElementById('cat_for_compare').innerHTML.toLowerCase();
        compare[br_id] = [1,brand_name,category];
    }
    if(Object.keys(compare).length == 1){
        localStorage.setItem('compare',JSON.stringify(compare));
        document.getElementById('pop_compare').innerHTML = 'Select 1 more company to compare';    
      }else if(Object.keys(compare).length == 2){
        localStorage.setItem('compare',JSON.stringify(compare));
        document.getElementById('pop_compare').innerHTML = 'Compare 2 Company';    
      }else{
        alert('Oops! You can only compare any 2 Companies! Please remove one to add a new company to compare.')
    }
    if(localStorage.getItem('compare') == null){
        $('#compareButton').slideDown([3000][5000]);
        document.getElementById('compareButton').style.display = 'block';
    }else{
        document.getElementById('compareButton').style.display = 'block';
    }
    updateCompareBox(compare);

});

//add compare popover
$('#pop_compare').popover();
updateCompareBox(compare);
function updateCompareBox(compare){
    var pop_str = "";
    pop_str = pop_str + "<p><b>Compare Products</b><p>";
    var i = 0;
    var brand1, brand2, category = 0;
    for(var item in compare){
        pop_str = pop_str + "<b>"+ compare[item][1] + "</b><br/>";
        i = i+1;
        if(i == 1){
            pop_str = pop_str + "Vs.<br/>";
            brand1 = compare[item][1].toLowerCase();
            category = compare[item][2].toLowerCase();
        }else{
            brand2 = compare[item][1].toLowerCase();
        }
    }
    if(Object.keys(compare).length == 2){
        pop_str = pop_str + '<a href="/'+ category +'-comparison/'+ brand1 + '-vs-' + brand2 + '/" class="btn master_btn">Compare Now!</a>';
    }
    pop_str = pop_str + "<div><button class='btn btn-primary' onclick='clearCompare()' id='clearCart'>Clear</button></div>"
        document.getElementById('pop_compare').setAttribute('data-content', pop_str);

}

function clearCompare(){
    compare = JSON.parse(localStorage.getItem('compare'));
    localStorage.clear();
    compare={};
    document.getElementById('pop_compare').style.display = 'none';
    updateCompareBox(compare);
    location.reload();

}