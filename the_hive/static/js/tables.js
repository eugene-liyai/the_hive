$(document).ready(function() {
    $('#user_jobs_table').DataTable();

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
});
