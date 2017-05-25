import Ember from 'ember';

const {
  set,
  computed,
  computed: { reads },
} = Ember;

export default Ember.Component.extend({
  classNames: ['layout-wrap', 'layout-row'],
  choices: reads('fattrs.choices'),
  actions: {

    handleChange(choice, newVal){
      let value = this.get('value') || Ember.A();

      if (newVal) {
        value.pushObject(choice);
      } else {
        value.removeObject(choice);
      }


      debugger;
      this.onChange(value);
    },

  }

});
