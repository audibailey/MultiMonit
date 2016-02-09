$(document).ready(function() {
    var max_fields      = 10; //maximum input boxes allowed
    var wrapper         = $(".input_fields_wrap"); //Fields wrapper
    var add_button      = $(".add_field_button"); //Add button ID

    var x = 1; //initlal text box count
    $(add_button).click(function(e){ //on add input button click
        e.preventDefault();
        if(x < max_fields){ //max input box allowed
            x++; //text box increment
            $(wrapper).append('<div class="input-control modern text" style="width: 100%"><input type="text" name="monitxml' + x +'"><span class="label">Monit HTTP XML URL:</span> <span class="informer">Example: http://example.com:2812/_status?format=xml</span><span class="placeholder">Monit XML URL</span><button class="button remove_field"><span class="mif-cross"></span></button></div>'); //add input box
        }
    });

    $(wrapper).on("click",".remove_field", function(e){ //user click on remove text
        e.preventDefault(); $(this).parent('div').remove(); x--;
    })
});