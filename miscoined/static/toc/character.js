define(["jquery", "knockout", "komapping", "kovalidation"], function($, ko, komapping, kovalidation) {

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
        };

        ko.mapping.fromJS(ability, mapping, self);

        self.jsonName = 'ability-' + self.name.replace(/\s+/g, '');

        self.proficientRequired = ko.pureComputed(function() {
            return character.occupation().abilities.required.indexOf(self.name) != -1;
        });

        self.proficientOption = ko.pureComputed(function() {
            return character.occupation().abilities.options
                && character.occupation().abilities.options.allowed.includes(self.name);
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

        self.proficientChecked = ko.observable(false).extend({
            validation: {
                validator: function(isChecked) {
                    return (
                        character == undefined ||
                            !isChecked ||
                            character.occupation().abilities.options &&
                            character.abilities().filter(a => a.proficientChecked()).length ==
                            character.occupation().abilities.options.count);
                }
            }
        });

        if (self.name == 'credit rating') {
            self.min = ko.pureComputed(function() {
                return character.occupation().credit.max;
            });
            self.max = ko.pureComputed(function() {
                return character.occupation().credit.min;
            })
        }

        if (self.name == 'languages') {
            self.value = ko.pureComputed(function() {
                return self.languages().reduce(
                    (acc, l) => acc + self.isProficient(l.name) ? 0.5 : 1, 0);
            });
            self.addLanguage = function() {
                self.languages.push({name: ko.observable()});
            };
            self.removeLanguage = function(index) {
                self.languages.splice(index, 1);
            };
            self.isProficient = function(language) {
                return self.proficientLanguage() == language || self.proficientChecked();
            }
            self.proficientLanguage = ko.observable();
        }

    }

    function Character() {
        var self = this;
        ko.mapping = komapping;

        var mapping = {
            'occupation': {
                create: function(options) {
                    return ko.observable({name: options.data.name,
                                          credit: options.data.credit,
                                          abilities: options.data.abilities})
                }
            },
            "points": {
                create: function(options) {
                    var subAbilities = function(category, init) {
                        return self.abilities().filter(a => a.category[0] == category)
                            .reduce((acc, a) => acc - parseInt(a.value()) /
                                    (a.proficientChecked() ? 2 : 1),
                                    init);
                    };

                    return {
                        investigative: ko.pureComputed(function() {
                            return subAbilities("investigative",
                                                options.data.investigative,
                                                + self.occupation().credit.min);
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
                                        - self.points.investigative()
                                        - self.points.general();
                                },
                                write: function(value) {
                                    self.points.experience.available(value);
                                }
                            })
                        }
                    };
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

        self.hitThreshold = ko.pureComputed(function() {
            return self.abilities().find(a => a.name == "athletics").value >= 8 ? 4 : 3;
        })

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
    return character;
});
