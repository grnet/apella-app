import DS from 'ember-data';

export default DS.Model.extend({

  name: Ember.computed.alias('title'),
  title: DS.attr(),
  __api__: {
    path: 'subject_areas',
  }
});