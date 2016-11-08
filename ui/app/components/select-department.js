import DS from 'ember-data';
import Ember from 'ember';
import Select from 'ember-gen/components/gen-form-field-select/component';

const {
  get,
  set,
  computed,
  observer
} = Ember;

export default Select.extend({

  relatedQuery: computed('field.relModel', 'object.institution', function() {

    let srcField = get(this, 'object.institution');
    let model = get(this, 'field.relModel');

    if (!srcField || !srcField.get('id')) {
      return DS.PromiseArray.create({promise: Ember.RSVP.resolve([])});
    }

    let srcField_id = get(srcField, 'id');

    let promise = this.get('store').findAll(model).then(function(items) {
      return Ember.RSVP.all(items.getEach('institution')).then(() => {
        return items.filterBy('institution.id', srcField_id);
      });
    });

    return DS.PromiseArray.create({promise});

  }),

  observeSubjectArea: observer('object.institution.[]', function(){
      set(this, 'value', null);
  }),

});
