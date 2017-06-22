
function initializeChoices() {
    $('#choice_list-list').find('input').each(function (i, input) {
       var $input = $(input);
       if($input.attr('id').match(/value-label/)) {
            $('#button-group').append('<button class="button bicolor choice-btn" id="'+ i +'">'+ $input.val() +'</button>');
       }
    });

    $('.choice-btn').each(function (i, btn) {
       $(btn).click()
    });
}
