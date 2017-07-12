$(document).ready(function() {
  var $inputField = $('#q');
  var template = Hogan.compile($('#autocomplete').text());
  var client = algoliasearch('VAPPYHPR6T', '4d3aeef86379e027844484707898c797');
  var stepIndex = client.initIndex('step_index');
  var stepFaqIndex = client.initIndex('step_faq_index');
  var taskListFaqIndex = client.initIndex('task_list_faq_index');

  var registerIndex = function (index, name, data) {
      return {
          source: index.ttAdapter(),
          displayKey: name,
          templates: {
              suggestion: function (hit) {
                  return template.render({
                      url: hit[data.url],
                      title: hit._highlightResult[data.title].value
                  })
              }
          }
      }
  };

  $('.search-terms a').click(function(e) {
    $inputField.val($(this).text()).change().focus();
  });
  $inputField.typeahead(
      { hint: false },
      registerIndex(stepIndex, 'step', {url: 'url', title: 'title'}),
      registerIndex(stepFaqIndex, 'step_faq', {url: 'page_url', title: 'question'}),
      registerIndex(taskListFaqIndex, 'task_list_faq', {url: 'page_url', title: 'question'})
  );
});
