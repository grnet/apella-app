import Ember from 'ember';

const {
  computed: {reads}
} = Ember;


export default Ember.Component.extend({
  classNames: ['layout-row', 'layout-wrap'],
  choices: reads('fattrs.choices'),

  actions: {
    handleChange(choice, newVal){
      let value = this.get('value') || Ember.A();
      if (newVal) {
        value.addObject(choice);
      } else {
        value.removeObject(choice);
      }
      this.onChange(value);
    },
  }
});
