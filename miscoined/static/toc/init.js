require.config({
  baseUrl: "/static/toc/",
  paths: {
    text: "lib/require.text-2.0.15",
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
  ["knockout", "kovalidation", "ViewModel"],
  function(ko, kovalidation, ViewModel) {
    ko.validation = kovalidation;
    ko.validation.init({
      insertMessages: false,
      decorateInputElement: true
    });

    ko.components.register("list-input", {
      viewModel: { require: "components/list-input" },
      template: { require: "text!components/list-input.html" }
    });

    ko.components.register("ability", {
      viewModel: { require: "components/ability" },
      template: { require: "text!components/ability.html" }
    });

    ko.components.register("character", {
      viewModel: { require: "components/character" },
      template: { require: "text!components/character.html" }
    })


    ko.applyBindings(new ViewModel());
  });
