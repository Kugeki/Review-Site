function format_data(data) {
    var result = '';
    for (var i = 0; i < data.length; i++) {
        result += '<div class="review">' +
            '    <div class="card-panel">' +
            '        <div class="row">' +
            '            <div class="col s5">' +
            '                <p>' + data[i].person.first_name + '</p>' +
            '                <a href=\"' + data[i].person.account + '\" target="_blank"><i class="material-icons">account_circle</i></a>' +
            '            </div>' +
            '            <div class="col s2">' +
            '                <p>' + data[i].rating + ' stars</p>' +
            '            </div>' +
            '            <div class="col s5">' +
            '                <p>' + data[i].blogger.first_name + '</p>' +
            '                <a href=\"' + data[i].blogger.account + '\" target="_blank"><i class="material-icons">account_circle</i></a>' +
            '            </div>' +
            '        </div>' +
            '        <p>' + data[i].content + '</p>' +
            '    </div>' +
            '</div>';

    }
    return result;
}

function show_reviews(data) {
    $('.reviews').html(format_data(data["reviews"]));
}


// Функции для сортировки и поиска

function get_sort_value() {
    var value = $('select[name=sort]').val()

    if (value == 1) {
        return '';
    }
    if (value == 2) {
        return "-rating";
    }
    if (value == 3) {
        return "rating";
    }
}

function get_search_value() {
    var input = $('#review_search');
    return input[0].value;
}

$('#review_search').on('input', function () {
    var input = $('#review_search');
    var url = input.attr("src");
    $.ajax({
        url: url,
        data: {
            'inputRequest': "search sort",
            'searchValue': get_search_value(),
            'sortValue': get_sort_value(),
        },
        dataType: 'json',
        success: function (data) {
            console.log(data);

            $('.reviews').html(format_data(data["reviews"]));
        }
    });
});

$('#sort').on('change', function () {
    $.ajax({
        url: $('#review_search').attr("src"),
        data: {
            'inputRequest': "search sort",
            'searchValue': get_search_value(),
            'sortValue': get_sort_value(),
        },
        dataType: 'json',
        success: function (data) {
            $('.reviews').html(format_data(data["reviews"]));
        }
    });
});


$(document).ready(function () {
    $('.modal').modal({
        dismissible: false
    });

    $('select').formSelect();
});

$('#post-form').on('submit', function (e) {
    e.preventDefault();

    var review = {};
    review.person = {}
    review.person.first_name = $('#pers_first_name').val();
    review.person.last_name = $('#pers_last_name').val();
    review.person.account = $('#pers_account').val();
    review.blogger = {};
    review.blogger.first_name = $('#blog_first_name').val();
    review.blogger.last_name = $('#blog_last_name').val();
    review.blogger.account = $('#blog_account').val();
    review.rating = Number($('#review_rating').val());
    review.content = $('#review_content').val();

    var data = review;
    var csrf_token = $('#post-form [name="csrfmiddlewaretoken"]').val();
    data["csrfmiddlewaretoken"] = csrf_token;

    var url = $('#post-form').attr("action");
    console.log(data);

    $.ajax({
        url: url,
        type: 'POST',
        dataType: 'json',
        data: JSON.stringify(data),
        cache: true,
        success: function (data) {

            console.log("OK");
            $.ajax({
                url: $('#review_search').attr("src"),
                data: {
                    'inputRequest': "search sort",
                    'searchValue': get_search_value(),
                    'sortValue': get_sort_value(),
                },
                dataType: 'json',
                success: function (data) {
                    $('.reviews').html(format_data(data["reviews"]));
                }
            });

        },
        error: function () {
            console.log("Error");
        }
    })


});