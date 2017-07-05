var INPUT_NAME = 'choice_rules-NUM-value-name',
    CHOICE_LIST_NAME = '#choice_list-list';

/*
 *  Adds HTML for a select/remove choice button.
 *  @param {jQuery selector} $parent - the element to append the HTML to
 *  @param {string} dataId - the id of the choice
 *  @param {string} val - the human readable text of the choice
 *  @param {string} icon - plus | cross
 */
function addButtonHtml($parent, dataId, val, icon) {
    var html = '<button class="button bicolor choice-btn icon icon-'+icon+'" data-id="'+ dataId +'">'+ val +'</button>';
    $parent.append(html);
    return $('button[data-id="'+dataId+'"]');
};

/*
 * The method called after a 'remove choice' button is selected.
 * @param {Event} evt - jQuery event object
 */
function choiceRemovedCallback(evt) {
    var $el = $(evt.target),
        $container = $el.closest('.choice-list-container'),
        prefixId = $container.attr('id'),
        $newChoiceButtons = $container.find('.new-choice-button-group'),
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

/*
 * The method called after an 'add choice' button is selected.
 * @param {Event} evt - jQuery event object
 */
function choiceSelectedCallback(evt) {
    var $container = $(evt.target).closest('.choice-list-container');
    var $selectedChoices = $container.find('.selected-choice-container');
    var val = $(evt.target).data('id');
    var name = $(evt.target).text();
    var inputId = '#'+$container.attr('name');
    var inputVal = $(inputId).val() === 'NEW' ? val : $(inputId).val() +','+ val;
    $(inputId).val(inputVal);

    $container.find('button[data-id="'+val+'"]').remove();
    var $newBtn = addButtonHtml($selectedChoices, val, name, 'cross');
    $newBtn.click(choiceRemovedCallback);
    return false;
};

/*
 * The method that gets called each time an admin panel is created.
 * @param {string} prefix - the id of the admin panel
 */
function initializeChoices(prefix) {
    var PREFIX_ID = '#' + prefix + '-container';
    var count = 0;
    var $selectedChoiceBtns = $(PREFIX_ID + ' .selected-choice-container').find('button');
    var selectedChoices = [];
    var availableChoices = {};

    $selectedChoiceBtns.each(function (i, choice) {
        selectedChoices.push($(choice).data('id'));
    });

    //Create a button for each choice from the list of available choices
    //If that choice has been selected, don't add it as an option to select
    $(CHOICE_LIST_NAME).find('input').each(function (i, choiceInput) {
       var $choiceInput = $(choiceInput);
       if($choiceInput.attr('id').match(/value-label/)) {
           availableChoices[count] = $choiceInput.val();
           if(selectedChoices.indexOf(count) == -1) {
               var $container = $(PREFIX_ID + ' .new-choice-button-group');
               addButtonHtml($container, count, $choiceInput.val(), 'plus');
           }
           count++;
       }
    });

    $(PREFIX_ID + ' .choice-btn').each(function (i, btn) {
       $(btn).click(choiceSelectedCallback);
    });

    $(PREFIX_ID + ' .selected-choice').each(function (i, btn) {
       var $btn = $(btn);
       var id = $btn.data('id');
       $btn.text(availableChoices[id]);

       $btn.click(choiceRemovedCallback)
    });

    $(PREFIX_ID + ' .selected-choice-input').each(function (i, input) {
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
