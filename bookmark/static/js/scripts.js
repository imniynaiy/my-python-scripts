// This file contains the JavaScript code using jQuery to handle user interactions, such as clicking on folder links and toggling the is_archived and is_personal fields.

$(document).ready(function() {
    // Event delegation for toggling is_archived
    $('#links-table-body tr').on('change', '.toggle-archived', function() {
        const linkId = $(this).closest('tr').data('link-id');
        const isArchived = $(this).is(':checked');
        updateLinkStatus(linkId, { is_archived: isArchived });
    });

    // Event delegation for toggling is_personal
    $('#links-table-body tr').on('change', '.toggle-personal', function() {
        const linkId = $(this).closest('tr').data('link-id');
        const isPersonal = $(this).is(':checked');
        updateLinkStatus(linkId, { is_personal: isPersonal });
    });

    // Function to update link status
    function updateLinkStatus(linkId, data) {
        $.ajax({
            url: `/api/link/${linkId}`,
            type: 'PUT',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function() {
                console.log('Link status updated successfully');
            },
            error: function() {
                console.error('Error updating link status');
            }
        });
    }
});