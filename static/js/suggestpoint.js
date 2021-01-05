
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
                    a.setAttribute('href', item['product_type_slug']);
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
                    a.setAttribute('href', '/category/'+item['category_slug']);
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
                    a.setAttribute('href', '/category/'+item['category__category_slug']+'/'+item['product_type_slug']);
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
                    a.setAttribute('href', '/'+item['category__category_slug']+'-reviews/'+item['brand_slug']);
                    div.appendChild(a);
                }); 
            }         
           
            },
    })
  }else{
    document.getElementById('search-results').innerHTML = ''

  }
  
});
