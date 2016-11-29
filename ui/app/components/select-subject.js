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

  relatedQuery: computed('field.modelName', 'object.subject_area', function() {

    let srcField = get(this, 'object.subject_area');
    let model = get(this, 'field.modelName');

    if (!srcField || !srcField.get('id')) {
      return DS.PromiseArray.create({promise: Ember.RSVP.resolve([])});
    }

    let srcField_id = get(srcField, 'id');

    let promise = this.get('store').findAll(model).then(function(items) {
      return Ember.RSVP.all(items.getEach('area')).then(() => {
        return items.filterBy('area.id', srcField_id);
      });
    });

    return DS.PromiseArray.create({promise});

  }),

});
