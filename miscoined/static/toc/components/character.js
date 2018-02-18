define(
  ["jquery", "knockout", "komapping", "kovalidation", "Ability"],
  function($, ko, komapping, kovalidation, Ability) {
    function Character(params) {
      var self = this;
      ko.mapping = komapping;

      ko.mapping.fromJS(params.character(), {
        "copy": ["abilities", "points"],
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
        }
      }, self);

      self.abilities = self.abilities.map(a => new Ability(a, self.occupation));

      var sumAbilities = function(filter) {
        return self.abilities
          .filter(filter)
          .reduce((acc, a) => acc + a.cost(), 0);
      };

      self.points.investigative = ko.observable(self.points.investigative);
      self.points.investigativeTotal = ko.pureComputed(function() {
        return self.points.investigative()
          - sumAbilities(a => a.category[0] == "investigative");
      });

      self.points.general = ko.observable(self.points.general);
      self.points.generalTotal = ko.pureComputed(function() {
        return self.points.general()
          - sumAbilities(a => a.category[0] == "general")
          - self.health() + 1
          - self.stability() + 1
          - self.sanity() + 4;
      });

      self.points.experience = ko.observable(self.points.experience);
      self.points.experienceTotal = ko.pureComputed(function () {
        return self.points.experience()
          - (self.points.investigative() - self.points.investigativeTotal()) * 3
          - (self.points.general() - self.points.generalTotal());
      });

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
      }).then(function(result) {alert("Success");},
              function(result) {alert(result.responseText);});
    };

    return Character;
  }
)
