define(["knockout"], function(ko) {
    return function ViewModel(params) {
        var self = this;
        self.labelPlural = params.labelPlural;
        self.labelSingular = params.labelSingular;
        self.list = params.list;
        self.removeItem = function(index) {
            self.list.splice(index, 1);
        };
        self.addItem = function(data, event) {
            self.list.push({value: ko.observable()});
        };
    };
});
