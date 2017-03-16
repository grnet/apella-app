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

  modelValueHint: computed('field.label', 'isLoading', 'modelValue', 'notFound', function() {
    let model = get(this, 'modelValue');
    let notFound = get(this, 'notFound');
    let isLoading = get(this, 'isLoading');

    if (notFound && !isLoading) { return 'user.not.found.error'; }

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
    set(this, 'notFound', false);
    if (!val) {
      set(this, 'isLoading', false);
      return this.sendAction('onChange', null);
    }
    store.findRecord(model, val).then((record) => {
      set(this, 'modelValue', record);
      this.sendAction('onChange', record);
    }).catch(() => {
      set(this, 'notFound', true);
      set(this, 'modelValue', null);
      this.sendAction('onChange', null);
    }).finally(() => {
      set(this, 'isLoading', false);
    });
  },

  actions: {
    handleChange(value) {
      set(this, 'customValue', value);
      if (!value) {
        set(this, 'modelValue', null);
      }
      Ember.run.debounce(this, 'setValue', value, 1000);
    }
  }
});
