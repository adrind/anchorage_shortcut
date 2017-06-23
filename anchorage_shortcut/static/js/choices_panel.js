var currentOptions = {};

var INPUT_NAME = 'choice_rules-NUM-value-name';

function removeButtonHtml(dataId, val) {
    return '<button class="selected-choice button bicolor icon icon-cross" data-id="'+dataId+'">'+val+'</span>'
};

function addButtonHtml(parentId, dataId, val, icon) {
    var html = '<button class="button bicolor choice-btn icon icon-'+icon+'" data-id="'+ dataId +'">'+ val +'</button>';
    $(parentId).append(html);
    return $('button[data-id="'+dataId+'"]');
};

function choiceRemovedCallback(evt) {
    var $container = $(evt.target).closest('.choice-list-container');
    var val = $(evt.target).data('id');
    var inputId = '#'+$container.attr('name');
    var inputVal = $(inputId).val();
    var selectedChoices = inputVal.split(',');
    var index = selectedChoices.indexOf(String(val));
    selectedChoices.splice(index, 1);

    $(inputId).val(selectedChoices.join(','));
    $('button[data-id="'+val+'"]').remove();
    var $newBtn = addButtonHtml('#button-group', val, currentOptions[val], 'plus');

    $newBtn.click(choiceSelectedCallback);
    return false;
};

function choiceSelectedCallback(evt) {
    var $container = $(evt.target).closest('.choice-list-container');
    var val = $(evt.target).data('id');
    var inputId = '#'+$container.attr('name');
    var inputVal = $(inputId).val();
    if(inputVal) {
        $(inputId).val(inputVal+','+val);
    } else {
        $(inputId).val(val);
    }

    $('button[data-id="'+val+'"]').remove();
    var $newBtn = addButtonHtml('.selected-choice-container', val, currentOptions[val], 'cross');
    $newBtn.click(choiceRemovedCallback);
    return false;
};

function initializeChoices() {
    var count = 0;
    var $selectedChoiceBtns = $('.selected-choice-container').find('button');
    var selectedChoices = [];

    $selectedChoiceBtns.each(function (i, choice) {
        selectedChoices.push($(choice).data('id'));
    });

    $('#choice_list-list').find('input').each(function (i, input) {
       var $input = $(input);
       if($input.attr('id').match(/value-label/)) {
           currentOptions[count] = $input.val();
           if(selectedChoices.indexOf(count) == -1) {
               addButtonHtml('#button-group', count, $input.val(), 'plus');
           }
           count++;
       }
    });

    $('.choice-btn').each(function (i, btn) {
       $(btn).click(choiceSelectedCallback);
    });

    $('.selected-choice').each(function (i, btn) {
       var $btn = $(btn);
       var id = $btn.data('id');
       $btn.text(currentOptions[id]);

       $btn.click(choiceRemovedCallback)
    });

    $('.selected-choice-input').each(function (i, input) {
      var $input = $(input);
      var $container = $input.closest('.choice-list-container');
      var label = $container.siblings('label').attr('for');
      var index = label.split('-')[1];
      var inputName = INPUT_NAME.replace('NUM', index);
      $input.attr('name', inputName);
      $input.attr('id', inputName);
      $container.attr('name', inputName);
    })

}
