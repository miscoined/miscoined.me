define(['jquery', 'knockout'], function($, ko) {
  return function ViewModel(characterName) {
    var self = this;

    self.occupations = ko.observableArray();

    $.ajax({
      url: "/toc/api/occupations",
      type: "GET",
      contentType: "application/json"
    }).done(function(data) {
      self.occupations(data);
    });

    self.character = ko.observable();
    $.ajax({
      url: "/toc/api/character" + (characterName ? '/' + characterName : ''),
      type: "GET",
      contentType: "application/json",
    }).done(function(data) {
      self.character(data);
    });

  };
});
