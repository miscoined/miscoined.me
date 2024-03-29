define(
  ["jquery", "knockout", "komapping", "kovalidation", "Ability"],
  function($, ko, komapping, kovalidation, Ability) {
    function Character(params) {
      var self = this;
      ko.mapping = komapping;

      ko.mapping.fromJS(params.character(),
                        {"copy": ["abilities",
                                  "points.investigative",
                                  "points.general",
                                  "points.experience"]},
                        self);

      self.occupation = ko.pureComputed(function () {
        var occ = params.occupations().find(o => o.name == self.occupationName());
        if (occ) return occ;
        return {name: "",
                credit: {min: 0, max: 0},
                abilities: {required: [], options: {allowed: [], count: 0}}};
      });

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
      self.points.investigativeTotalDisplay = ko.pureComputed(function() {
        return Math.max(self.points.investigativeTotal(), 0);
      })

      self.points.general = ko.observable(self.points.general);
      self.points.generalTotal = ko.pureComputed(function() {
        return self.points.general()
          - sumAbilities(a => a.category[0] == "general")
          - self.health() + 1
          - self.stability() + 1
          - self.sanity() + 4;
      });
      self.points.generalTotalDisplay = ko.pureComputed(function() {
        return Math.max(self.points.generalTotal(), 0);
      })

      self.points.experience = ko.observable(self.points.experience);
      self.points.experienceTotal = ko.pureComputed(function () {
        return parseInt(self.points.experience())
          + Math.min(0, self.points.generalTotal())
          + Math.min(0, self.points.investigativeTotal() * 3);
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
        url: "/toc/api/character",
        type: "POST",
        data: ko.mapping.toJSON(this),
        contentType: "application/json"
      }).then(function(result) {
          window.location.replace("/toc/character/" + result.name);
      }, function(result) {
          alert(result.responseText);
      });
    };

    return Character;
  }
);
