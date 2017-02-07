import Ember from 'ember';
import DS from 'ember-data';
import ENV from 'ui/config/environment';
import {booleanFormat, computeI18NChoice} from 'ui/lib/common';

const {
  get, set, computed, on
} = Ember,
      CHOICES = ENV.APP.resources;

export default Ember.Mixin.create({
  institution: DS.belongsTo('institution', {
    autocomplete: true,
    formAttrs: {optionLabelAttr: 'title_current'}
  }),
  institution_freetext: DS.attr(),
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
  rank_verbose: computeI18NChoice('rank', CHOICES.RANKS),
  is_foreign: DS.attr({type: 'boolean', defaultValue: false, displayComponent: 'boolean-display' }),
  is_foreign_descr: computed('is_foreign', 'locale.i18n', function() {
    let is_foreign = get(this, 'is_foreign');
    return is_foreign ? get(this, 'i18n').t('professor_foreign') : get(this, 'i18n').t('professor_domestic');
  }),
  speaks_greek: DS.attr({type: 'boolean', defaultValue: true, displayComponent: 'boolean-display' }),
  speaks_greek_verbose: booleanFormat('speaks_greek'),
  cv_url: DS.attr({displayComponent: 'url-display'}),
  cv_in_url: DS.attr({type: 'boolean', displayComponent: 'boolean-display'}),
  cv: DS.belongsTo('apella-file'),
  cv_professor: DS.belongsTo('apella-file'),
  diplomas: DS.hasMany('apella-file'),
  publications: DS.hasMany('apella-file'),
  fek: DS.attr(),
  discipline_text: DS.attr(),
  discipline_in_fek: DS.attr({type: 'boolean', defaultValue: true, displayComponent: 'boolean-display'}),
  discipline_in_fek_verbose: booleanFormat('discipline_in_fek'),
  active_elections: DS.attr('number'),

  institution_global: computed('is_foreign', 'institution.title_current', 'institution_freetext', function(){
    if (get(this, 'is_foreign')) {
      return get(this, 'institution_freetext')
    } else {
      return get(this, 'institution.title_current')
    }
  }),

  user_id: DS.attr()
});
