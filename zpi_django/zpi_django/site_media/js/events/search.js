$(function() {
  $("#drugs").autocomplete({
    source: "/autocomplete/",
    minLength: 2,
  });
});
