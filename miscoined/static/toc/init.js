require.config({
  baseUrl: "/static/toc/",
  paths: {
    text: "lib/requirejs-text/text",
    jquery: "lib/jquery/dist/jquery.min",
    knockout: "lib/knockout/build/output/knockout-latest",
    komapping: "lib/knockout-mapping/dist/knockout.mapping.min",
    kovalidation: "lib/knockout.validation/dist/knockout.validation.min"
  },
  shim: {
    komapping: {
      deps: ["knockout"],
      exports: "komapping"
    },
    kovalidation: {
      deps: ["knockout"],
      exports: "kovalidation"
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
    });

    ko.applyBindings(new ViewModel());
  });
