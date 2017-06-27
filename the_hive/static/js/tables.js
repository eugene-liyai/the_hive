$(document).ready(function() {

    $('.hidden-row-style').css('padding', '0');

    $('#stats_table').DataTable();

    $('select.form-control.input-sm').change(function(){
         var x = $(this).val();
         if (x === '10') {
             $('ul.nav.sidebar-nav').css('height', '750px');
         }else if (x === '25') {
             $('ul.nav.sidebar-nav').css('height', '950px');
         }else if (x === '50') {
             $('ul.nav.sidebar-nav').css('height', '1850px');
         }else if (x === '100'){
             $('ul.nav.sidebar-nav').css('height', '3700px');
         }
    });

    $('.checkbox_select').click(function () {
        var parent = $(this).parent().closest('tr');
        if ( $(this).is(':checked') ) {
            parent.css('background-color', '#eeeed4');
            parent.addClass('selected-row');
        } else {
            parent.css('background-color', '');
            parent.removeClass('selected-row');
        }
    });

    $('#summary-btn').click(function () {
        var allSelected = $('.selected-row');
        var rate = $(this).attr('data-rate');
        var totalDuration = $('#total-duration');
        var sumTotal = $('#sum-total');
        var sum = 0;
        if (allSelected.length > 0){
            for(var i=0; i < allSelected.length; i++){
                sum = sum + Number($(allSelected[i]).find( "td.duration" ).text());
            }
            $(totalDuration).html("<b>"+sum+"</b>");
            $(sumTotal).html("<b>"+sum * Number(rate)+"</b>");
        }else{
            $(totalDuration).html("<b>No jobs selected</b>");
            $(sumTotal).html("<b>No jobs selected</b>");
        }
    });

    $('#user_jobs_table').DataTable();
});
