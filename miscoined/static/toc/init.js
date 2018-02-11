require.config({
    baseUrl: "/static/toc/",
    paths: {
        jquery: "lib/jquery-3.3.1-min",
        knockout: "lib/knockout-3.4.2-min",
        komapping: "lib/knockout.mapping-2.4.1-min",
        kovalidation: "lib/knockout.validation-2.0.3-min"
    },
    shim: {
        komapping: {
            deps: ["knockout"],
            exports: "komapping"
        },
        kovalidation: {
            deps: ["knockout"],
            exports: "komapping"
        }
    }
});

require(
    ["knockout", "kovalidation", "character"],
    function(ko, kovalidation, character) {
        ko.validation = kovalidation;
        ko.validation.init({
            insertMessages: false,
            decorateInputElement: true
        });

        ko.applyBindings(character);
    });
