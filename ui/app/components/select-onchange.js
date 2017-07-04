import DS from 'ember-data';
import Ember from 'ember';
import Select from 'ember-gen/components/gen-form-field-select/component';

const {
  get,
  computed,
  on,
  mixin,
  assert,
} = Ember;

export default Select.extend({

  setUp: on('init', function() {
    let key = get(this, 'fattrs.lookupModel');
    let query = get(this, 'fattrs.changedChoices');
    assert(`lookupModel and changedChoices are required for select-onchange`, key && query);
    mixin(this, {
      relatedQuery: computed('field.modelName', `object.${key}.id`, function() {
        let value = this.get(`object.${key}`);
        return value ? query(this.get('store'), value) : Ember.A();
      })
    })
  })

});
