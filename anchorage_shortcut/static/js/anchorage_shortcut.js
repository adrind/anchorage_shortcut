$(document).ready(function() {
  var $inputField = $('#q');
  var template = Hogan.compile($('#autocomplete').text());
  var client = algoliasearch('VAPPYHPR6T', '4d3aeef86379e027844484707898c797');
  var prefix = window.location.origin === 'http://localhost:8000' ? '' : 'prod_';
  var stepIndex = client.initIndex(prefix+'step_index');
  var stepFaqIndex = client.initIndex(prefix+'step_faq_index');
  var taskListFaqIndex = client.initIndex(prefix+'task_list_faq_index');
  var roadmapType = window.location.pathname.split('/') && window.location.pathname.split('/')[1];

  var registerIndex = function (index, name, data) {
      return {
          source: function (query, cb) {
              index.search({query: query, filters: 'roadmap:'+roadmapType}, function (err, content) {
                  if (err) {
                      cb(err);
                      return;
                  }
                  cb(content.hits);
              });

          },
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

  $inputField.typeahead(
      { hint: true },
      registerIndex(stepIndex, 'step', {url: 'url', title: 'title'}),
      registerIndex(stepFaqIndex, 'step_faq', {url: 'page_url', title: 'question'}),
      registerIndex(taskListFaqIndex, 'task_list_faq', {url: 'page_url', title: 'question'})
  );

  $('.twitter-typeahead').on('typeahead:selected', function(event, selection) {
        document.location.pathname = selection.url;
  });
});
