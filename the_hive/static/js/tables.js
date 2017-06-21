$(document).ready(function() {
    $('#user_jobs_table').DataTable();

    $('.hidden-row-style').css('padding', '0');

    $('#stats_table').DataTable();


    $.fn.deleteJob = function(job_id) {
        $.ajax({
            url: '/admin/delete_job/'+job_id,
            type: 'GET'
        });
    }
});
