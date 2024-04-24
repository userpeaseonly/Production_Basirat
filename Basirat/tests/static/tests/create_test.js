$(document).ready(function () {
    const form = document.getElementById('create-test-form');
    $(document).on('submit', '#create-test-form', function (e) {
        e.preventDefault();
        const name = $('#name').val();
        const title = $('#title').val();
        const description = $('#description').val();
        const duration = $('#duration').val();
        const is_active = $('#is_active').is(':checked');
        const start_date = $('#start_date').val();
        const end_date = $('#end_date').val();
        const groups = $('#groups').val();  // Get selected group values


        $.ajax({
            type: 'POST',
            url: create_test_url,
            data: {
                // name: name,
                title: title,
                description: description,
                duration: duration,
                is_active: is_active,
                start_date: start_date,
                end_date: end_date,
                groups: groups,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (response) {
                alert('Test created successfully!');
                window.location.href = edit_test_url;
            },
            error: function (xhr, errmsg, err) {
                alert('Error creating test!');
            }
        });
    });
});