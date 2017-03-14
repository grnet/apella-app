import SelectField from 'ember-gen/components/gen-form-field-select/component';


const { set, get, computed, observer } = Ember;

// Once user writes down an id value, resolve the model from the store and 
// send the record using onChange action in order for underlying form object 
// to be updated with the record field (as the field is probably a belongsTo 
// property).
export default SelectField.extend({
  modelValue: null,

  // set initial value id
  customValue: computed('value.id', function() {
    let value = get(this, 'value');
    if (value && value.id) {
      set(this, 'customValue', value.id);
    }
  }),

  modelValueHint: computed('field.label', 'isLoading', function() {
    let model = get(this, 'modelValue');
    let isLoading = get(this, 'isLoading');

    if (!model && !isLoading) { return 'value.not.set'; }

    let valueLabel = 'loading...';
    if (!isLoading && model) {
      valueLabel = get(model, get(this, 'fattrs.optionLabelAttr'));
    }
    return valueLabel;
  }),

  setValue(val) {
    let model = get(this, 'field.modelName');
    let store = get(this, 'store');
    set(this, 'isLoading', true);
    if (!val) { 
      set(this, 'isLoading', false);
      return this.sendAction('onChange', null);
    }
    store.findRecord(model, val).then((record) => {
      set(this, 'modelValue', record);
      this.sendAction('onChange', record);
    }).catch(() => {
      set(this, 'modelValue', null);
      this.sendAction('onChange', null);
    }).finally(() => {
      set(this, 'isLoading', false);
    });
  },

  actions: {
    handleChange(value) {
      set(this, 'customValue', value);
      Ember.run.debounce(this, 'setValue', value, 1000);
    }
  }
});
