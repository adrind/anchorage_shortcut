var INPUT_NAME = 'choice_rules-NUM-value-name';

var availableChoices = {};
var selectedChoices = {};

function removeButtonHtml(dataId, val) {
    return '<button class="selected-choice button bicolor icon icon-cross" data-id="'+dataId+'">'+val+'</span>'
};

function addButtonHtml($parent, dataId, val, icon) {
    var html = '<button class="button bicolor choice-btn icon icon-'+icon+'" data-id="'+ dataId +'">'+ val +'</button>';
    $parent.append(html);
    return $('button[data-id="'+dataId+'"]');
};

function choiceRemovedCallback(evt) {
    var $el = $(evt.target),
        $container = $el.closest('.choice-list-container'),
        prefixId = $container.attr('id'),
        $newChoiceButtons = $container('.new-choice-button-group'),
        val = $el.data('id'),
        inputId = '#'+$container.attr('name'),
        inputVal = $(inputId).val(),
        selectedChoicesStr = inputVal.split(','),
        index = selectedChoicesStr.indexOf(String(val));

    selectedChoicesStr.splice(index, 1);
    var name = $(evt.target).text();

    $(inputId).val(selectedChoicesStr.join(','));
    $container.find('button[data-id="'+val+'"]').remove();
    var $newBtn = addButtonHtml($newChoiceButtons, val, name, 'plus');

    $newBtn.click(choiceSelectedCallback);
    return false;
};

function choiceSelectedCallback(evt) {
    var $container = $(evt.target).closest('.choice-list-container');
    var $selectedChoices = $container.find('.selected-choice-container');
    var val = $(evt.target).data('id');
    var name = $(evt.target).text();
    var inputId = '#'+$container.attr('name');
    var inputVal = $(inputId).val() === 'NEW' ? val : inputVal+','+ val;
    $(inputId).val(inputVal);

    $container.find('button[data-id="'+val+'"]').remove();
    var $newBtn = addButtonHtml($selectedChoices, val, name, 'cross');
    $newBtn.click(choiceRemovedCallback);
    return false;
};

function initializeChoices(prefix) {
    var count = 0;
    var prefixId = '#' + prefix + '-container';
    var $selectedChoiceBtns = $(prefixId + ' .selected-choice-container').find('button');
    var selectedChoicesForPrefix = [];

    $selectedChoiceBtns.each(function (i, choice) {
        selectedChoicesForPrefix.push($(choice).data('id'));
    });

    $('#choice_list-list').find('input').each(function (i, input) {
       var $input = $(input);
       if($input.attr('id').match(/value-label/)) {
           availableChoices[count] = $input.val();
           if(selectedChoicesForPrefix.indexOf(count) == -1) {
               var $container = $(prefixId + ' .new-choice-button-group');
               addButtonHtml($container, count, $input.val(), 'plus');
           }
           count++;
       }
    });

    $(prefixId + ' .choice-btn').each(function (i, btn) {
       $(btn).click(choiceSelectedCallback);
    });

    $(prefixId + ' .selected-choice').each(function (i, btn) {
       var $btn = $(btn);
       var id = $btn.data('id');
       $btn.text(availableChoices[id]);

       $btn.click(choiceRemovedCallback)
    });

    $(prefixId + ' .selected-choice-input').each(function (i, input) {
      var $input = $(input);
      var $container = $input.closest('.choice-list-container');
      var label = $container.siblings('label').attr('for');
      var index = label.split('-')[1];
      var inputName = INPUT_NAME.replace('NUM', index);
      $input.attr('name', inputName);
      $input.attr('id', inputName);
      $container.attr('name', inputName);
    });
}
