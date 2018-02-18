define(
  ["jquery", "knockout", "komapping", "kovalidation"],
  function($, ko, komapping, kovalidation) {
    return function Ability(ability, occupation) {
      var self = this;

      ko.mapping.fromJS(ability, {
        "copy": ["name", "investigative", "category"],
        "languages": {
          create: function(options) {
            return {name: ko.observable(options.data)};
          }
        },
        "district knowledges": {
          create: function(options) {
            return {name: options.data.name, value: ko.observable(options.data.value)};
          }
        }
      }, self);

      self.jsonName = 'ability-' + self.name.replace(/\s+/g, '');

      self.proficientRequired = ko.pureComputed(function() {
        return occupation() && occupation().abilities.required.indexOf(self.name) != -1;
      });

      self.proficientOption = ko.pureComputed(function() {
        return occupation()
          && occupation().abilities.options
          && occupation().abilities.options.allowed.includes(self.name);
      });

      self.proficient = ko.pureComputed({
        read: function() {
          return self.proficientRequired() ||
            self.proficientOption && self.proficientChecked();
        },
        write: function(isChecked) {
          self.proficientChecked(isChecked);
        }
      });

      self.proficientChecked = ko.observable(false);

      if (self.name == 'credit rating') {
        self.min = ko.pureComputed(function() {
          return occupation().credit.min;
        });
        self.max = ko.pureComputed(function() {
          return occupation().credit.max;
        });
        self.cost = ko.pureComputed(function() {
          return Math.max(parseInt(self.value()) - self.min(), 0);
        });
      } else if (self.name == 'languages') {
        self.proficientLanguage = ko.observable();
        self.addLanguage = function() {
          self.languages.push({name: ko.observable()});
        };
        self.removeLanguage = function(index) {
          self.languages.splice(index, 1);
        };
        self.isProficient = function(language) {
          return self.proficientLanguage() == language || self.proficient();
        }
        self.value = ko.pureComputed(function() {
          return self.languages().length;
        });
        self.cost = ko.pureComputed(function() {
          return self.languages().reduce(
            (acc, l) => acc + self.isProficient(l.name) ? 0.5 : 1, 0);
        });
      } else {
        self.cost = ko.pureComputed(function() {
          return parseInt(self.value()) / (self.proficient() ? 2 : 1);
        });
      }

    }
  });
