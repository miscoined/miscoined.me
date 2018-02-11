ko.validation.init({
    insertMessages: false,
    decorateInputElement: true
});

function Ability(ability) {
    var self = this;

    var mapping = {
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
    }

    ko.mapping.fromJS(ability, mapping, self);

    self.jsonName = 'ability-' + self.name.replace(/\s+/g, '');

    self.proficientRequired = ko.pureComputed(function() {
        return character.occupation().abilities.required.indexOf(self.name) != -1;
    });

    self.proficientOption = ko.pureComputed(function() {
        return character.occupation().abilities.options.allowed.includes(self.name);
    });

    self.proficientChecked = ko.observable(false).extend({
        validation: {
            validator: function(isChecked) {
                return (
                    character == undefined ||
                        self.proficientRequired() ||
                        !isChecked ||
                        character.abilities().filter(
                            a => !a.proficientRequired() && a.proficientChecked()).length ==
                        character.occupation().abilities.options.count);
            }
        }
    });

    if (self.name == 'languages') {
        self.value.subscribe(function(value) {
            var diff = Math.abs(value - self.languages().length);
            if (value > self.languages().length) {
                var newLanguages = ko.utils.arrayMap(new Array(diff), function(i) {
                    return {name: ko.observable()};
                });
                self.languages.push.apply(self.languages, newLanguages);
            } else if (value < self.languages().length) {
                self.languages.splice(self.languages().length - diff, diff);
            }
        });
    } else if (self.name == 'credit rating') {
        self.valueConstrained = ko.pureComputed(function() {
            return Math.min(Math.max(self.value(), character.occupation().credit.min),
                            character.occupation().credit.max);
        });
    }
}

function Character() {
    var self = this;

    var mapping = {
        'occupation': {
            create: function(options) {
                return ko.observable({name: options.data.name,
                                      credit: options.data.credit,
                                      abilities: options.data.abilities})
            }
        },
        'abilities': {
            create: function(options) {
                return new Ability(options.data);
            }
        }
    };

    $.ajax({
        url: "/toc/api/character",
        type: "GET",
        contentType: "application/json",
        async: false,
        success: function(data) {
            ko.mapping.fromJS(data, mapping, self);
        }
    });

    $.ajax({
        url: "/toc/api/occupations",
        type: "GET",
        contentType: "application/json",
        async: false,
        success: function(data) {
            self.occupations = data;
        }
    });

    self.occupation.subscribe(function(occupation) {
        self.abilities().forEach(function(ability) {
            ability.proficientChecked(occupation.abilities.required.includes(ability.name));
        });
    });

    self.investigativeCategories = [];
    self.abilities().forEach(function(ability) {
        if (ability.category[0] == "general") return;
        var category = self.investigativeCategories.find(cat => cat.name == ability.category[1]);
        if (category == undefined) {
            category = {name: ability.category[1], abilities: []};
            self.investigativeCategories.push(category)
        }
        category.abilities.push(ability)
    });

    self.proficiencies = ko.pureComputed(function() {
        return self.abilities().filter(a => a.proficientChecked());
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

var character = new Character();
ko.applyBindings(character);
