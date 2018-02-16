define(
  ["jquery", "knockout", "komapping", "kovalidation", "Ability"],
  function($, ko, komapping, kovalidation, Ability) {
    function Character(params) {
      var self = this;
      ko.mapping = komapping;

      ko.mapping.fromJS(params.character(), {
        "copy": ["abilities"],
        "occupation": {
          create: function(options) {
            return ko.observable((options.data)
                                 ? {name: options.data.name,
                                    credit: options.data.credit,
                                    abilities: options.data.abilities}
                                 : {name: "",
                                    credit: {"min": 0, "max": 0},
                                    abilities: {"required": []}})
          }
        },
        "points": {
          create: function(options) {
            var subAbilities = function(category, init) {
              return self.abilities
                .filter(a => a.category[0] == category && a.name != "languages")
                .reduce((acc, a) => acc - parseFloat(a.value()) /
                        (a.proficient() ? 2 : 1),
                        init);
            };

            return {
              investigative: ko.pureComputed(function() {
                return subAbilities("investigative",
                                    options.data.investigative,
                                    + self.occupation().credit.min
                                    + self.abilities.find(a => a.name == "languages").value());
              }),
              general: ko.pureComputed(function() {
                return subAbilities("general",
                                    options.data.general
                                    - self.health() + 1
                                    - self.stability() + 1
                                    - self.sanity() + 4);
              }),
              experience: {
                available: ko.observable(options.data.experience),
                total: ko.pureComputed({
                  read: function() {
                    if (!self.points.available) return 0;
                    return self.points.experience.available()
                      - self.points.investigative() * 3
                      - self.points.general();
                  },
                  write: function(value) {
                    self.points.experience.available(value);
                  }
                })
              }
            };
          }
        }
      }, self);

      self.abilities = self.abilities.map(a => new Ability(a, self.occupation));

      self.investigativeCategories = [];
      self.abilities.forEach(function(ability) {
        if (ability.category[0] == "general") return;
        var category = self.investigativeCategories.find(cat => cat.name == ability.category[1]);
        if (category == undefined) {
          category = {name: ability.category[1], abilities: []};
          self.investigativeCategories.push(category)
        }
        category.abilities.push(ability)
      });

      self.hitThreshold = ko.pureComputed(function() {
        return self.abilities.find(a => a.name == "athletics").value >= 8 ? 4 : 3;
      });

      self.proficiencies = ko.pureComputed(function() {
        return self.abilities.filter(a => a.proficient());
      }).extend({
        validation: {
          validator: function(proficiencies, required) {
            return proficiencies.length == (self.occupation().abilities.options.count
                                            + self.occupation().abilities.required.length);
          },
          message: function () {
            var diff = self.occupation().abilities.options.count
                + self.occupation().abilities.required.length
                - self.abilities.filter(a => a.proficient()).length;
            return "Must choose "
              + Math.abs(diff) + " "
              + ((diff > 0) ? "more" : "fewer")
              + " occupational abilities."
          }
        }
      });
    }

    Character.prototype.submit = function() {
      $.ajax ({
        url: "/toc/character",
        type: "POST",
        data: ko.mapping.toJSON(this),
        contentType: "application/json",
        success: function(result) {
          alert("Success");
        },
        error: function(result) {
          alert(result.responseText);
        }
      });
    };

    return Character;
  }
)
