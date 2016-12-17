import Ember from 'ember';
import DS from 'ember-data';
import ENV from 'ui/config/environment';

const { get } = Ember,
      CHOICES = ENV.APP.resources;

export default Ember.Mixin.create({
  institution: DS.belongsTo('institution', {formAttrs: {optionLabelAttr: 'title_current'}}),
  department: DS.belongsTo('department', {
    formComponent: 'select-onchange',
    formAttrs: {
      lookupModel: 'institution',
      changedChoices: function(store, value) {
        return store.query('department', {institution: get(value, 'id')})
      },
      optionLabelAttr: 'title_current',
    }
  }),
  rank: DS.attr({type: 'select', choices: CHOICES.RANKS, defaultValue:'Assistant Professor'}),
  is_foreign: DS.attr({type: 'boolean', defaultValue: false }),
  speaks_greek: DS.attr({type: 'boolean', defaultValue: true }),
  cv_url: DS.attr(),
  cv: DS.attr(),
  fek: DS.attr(),
  discipline_text: DS.attr(),
  discipline_in_fek: DS.attr({type: 'boolean', defaultValue: true})

});
