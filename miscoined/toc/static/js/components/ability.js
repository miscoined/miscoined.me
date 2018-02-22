define(["jquery", "knockout"], function($, ko) {
    function AbilityViewModel(params) {
      this.occupation = params.occupation;
      this.ability = params.ability;
    };

    AbilityViewModel.prototype.districtSum = function() {
      return this.ability.districts().reduce((acc, d) => acc - parseFloat(d.value()), 0);
    }

  return AbilityViewModel;
  }
);
