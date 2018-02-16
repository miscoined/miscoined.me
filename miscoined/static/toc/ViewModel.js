define(['jquery', 'knockout'], function($, ko) {
  return function ViewModel() {
    var self = this;

    self.occupations = ko.observableArray();
    self.character = ko.observable();

    $.ajax({
      url: "/toc/api/occupations",
      type: "GET",
      contentType: "application/json"
    }).done(function(data) {
      self.occupations(data);
    });

    $.ajax({
      url: "/toc/api/character",
      type: "GET",
      contentType: "application/json",
    }).done(function(data) {
      self.character(data);
    });

  };
});
