$(document).ready(function() {
    // Modal handling
    $('.clickable').click(function(e) {
        e.preventDefault();
        var url = $(this).data('url');
        var title = $(this).closest('tr').find('td:nth-child(2)').text();
        
        $('#detailModal .modal-title').text('Details: ' + title);
        $('#detailModal .modal-body').html('<div class="text-center"><i class="glyphicon glyphicon-refresh"></i> Loading...</div>');
        $('#detailModal').modal('show');
        
        $.ajax({
            url: url,
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: function(response) {
                $('#detailModal .modal-body').html(response);
            },
            error: function(xhr, status, error) {
                var errorMsg = 'An error occurred while loading the details.';
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMsg = xhr.responseJSON.error;
                }
                $('#detailModal .modal-body').html(
                    '<div class="alert alert-danger">' +
                    '<i class="glyphicon glyphicon-exclamation-sign"></i> ' +
                    errorMsg + '</div>'
                );
                console.error('Modal error:', error);
            }
        });
    });

});
