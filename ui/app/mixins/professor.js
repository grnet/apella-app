import Ember from 'ember';
import DS from 'ember-data';
import ENV from 'ui/config/environment';

const {
  get, computed
} = Ember,
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
  rank: DS.attr({type: 'select', choices: CHOICES.RANKS, defaultValue:'Assistant Professor', translate: true}),
  is_foreign: DS.attr({type: 'boolean', defaultValue: false }),
  is_foreign_descr: computed('is_foreign', 'locale.i18n', function() {
    let is_foreign = get(this, 'is_foreign');
    return is_foreign ? get(this, 'i18n').t('professor_foreign') : get(this, 'i18n').t('professor_domestic');
  }),
  speaks_greek: DS.attr({type: 'boolean', defaultValue: true }),
  cv_url: DS.attr(),
  cv: DS.belongsTo('apella-file'),
  cv_professor: DS.belongsTo('apella-file'),
  diplomas: DS.hasMany('apella-file'),
  publications: DS.hasMany('apella-file'),
  fek: DS.attr(),
  discipline_text: DS.attr(),
  discipline_in_fek: DS.attr({type: 'boolean', defaultValue: true}),
  active_elections: DS.attr('number')
});
