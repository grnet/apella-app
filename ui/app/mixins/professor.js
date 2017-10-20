import Ember from 'ember';
import DS from 'ember-data';
import ENV from 'ui/config/environment';
import {booleanFormat, computeI18NChoice, computeDateFormat} from 'ui/lib/common';

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

  user_id: DS.attr(),

  leave_starts_at: DS.attr('date'),
  leave_starts_at_format: computeDateFormat('leave_starts_at'),
  leave_ends_at: DS.attr('date'),
  leave_ends_at_format: computeDateFormat('leave_ends_at'),
  leave_file: DS.belongsTo('apella-file'),
   //leave is upcoming if
   //- the professor is domestic
   //- there is an leave_ends_at date
   //- leave_ends_at date has not passed
  leave_upcoming: computed('is_foreign', 'leave_ends_at', function() {
    let is_domestic = !get(this, 'is_foreign');
    let end = moment(get(this, 'leave_ends_at')).endOf('day');
    return end && is_domestic && end.isAfter();
  }),
  // the professor is on leave if leave_upcoming is true and
  // now is between leave end date and leave start date
  on_leave: computed('leave_upcoming', 'leave_starts_at', function() {
    let start = moment(get(this, 'leave_starts_at')).startOf('day');
    let leave_upcoming = get(this, 'leave_upcoming');
    return leave_upcoming && start.isBefore();
  }),
  on_leave_verbose: booleanFormat('on_leave'),
  is_disabled: DS.attr({type: 'boolean', displayComponent: 'boolean-display'}),
  disabled_at: DS.attr('date'),
  disabled_at_format: computeDateFormat('disabled_at'),
  disabled_by_helpdesk: DS.attr({type: 'boolean'}),
  disabled_by: computed('is_disabled', 'disabled_by_helpdesk', 'i18n.locale', function() {
    let is_disabled = get(this, 'is_disabled'),
      disabled_by_helpdesk = get(this, 'disabled_by_helpdesk'),
      disabled_by = '-';
    if(is_disabled) {
      disabled_by =  (disabled_by_helpdesk ? 'helpdesk' : 'user');
    }
    return get(this, 'i18n').t(disabled_by);
  }),

  leave_verbose: computed('on_leave', 'leave_upcoming', 'i18n.locale', function() {
    if (get(this, 'on_leave')) {
      return get(this, 'i18n').t('leave.current');
    } else if (get(this, 'leave_upcoming')) {
      return get(this, 'i18n').t('leave.upcoming');
    } else {
      return '-'
    }
  })

});
