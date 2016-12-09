import DS from 'ember-data';
import Ember from 'ember';
import Select from 'ember-gen/components/gen-form-field-select/component';

const {
  get,
  computed,
} = Ember;

export default Select.extend({

  relatedQuery: computed('field.modelName', 'object.institution', 'fattrs.lookupField', function() {
    let srcField = get(this, 'object.institution');
    let model = get(this, 'field.modelName');
    let query = {};

    if (!srcField || !srcField.get('id')) {
      return DS.PromiseArray.create({promise: Ember.RSVP.resolve([])});
    }

    query[get(this, 'fattrs.lookupField')] = get(srcField, 'id');
    return get(this, 'store').query(model, query);
  }),
});
