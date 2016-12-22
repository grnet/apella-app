import DS from 'ember-data';
import ENV from 'ui/config/environment';
import {computeI18N, computeI18NChoice, computeDateFormat, computeDateTimeFormat} from 'ui/lib/common';
import get_label from '../utils/common/label_list_item';


const { computed, get } = Ember,
      CHOICES = ENV.APP.resources;


export default DS.Model.extend({
  title: DS.attr(),
  description: DS.attr({type:'text'}),
  discipline: DS.attr(),
  department_dep_number: DS.attr(),
  author: DS.belongsTo('institution-manager'),

  department: DS.belongsTo('department', {
    formAttrs: {
      optionLabelAttr: 'title_current'
    }
  }),
  subject_area: DS.belongsTo('subject-area', {
    formAttrs: {
      optionLabelAttr: 'title_current'
    }
  }),
  subject: DS.belongsTo('subject', {
    formComponent: 'select-onchange',
    formAttrs: {
      lookupModel: 'subject_area',
      changedChoices: function(store, value) {
        return store.query('subject', {area: get(value, 'id')})
      },
      optionLabelAttr: 'title_current',
    }
  }),
  fek: DS.attr(),
  fek_posted_at: DS.attr('date'),
  fek_posted_at_format: computeDateFormat('fek_posted_at'),
  assistants: DS.hasMany('assistant'),
  electors: DS.hasMany('professor'),
  committee: DS.hasMany('professor'),
  elected: DS.belongsTo('user', {formAttrs: {optionLabelAttr: 'username'}}),
  state: DS.attr({type: 'select', choices: CHOICES.POSITION_STATES, defaultValue: 'posted'}),
  state_verbose: computeI18NChoice('state', CHOICES.POSITION_STATES),
  starts_at: DS.attr('date'),
  starts_at_format: computeDateFormat('starts_at'),
  ends_at: DS.attr('date'),
  ends_at_format: computeDateFormat('ends_at'),
  created_at: DS.attr('date'),
  updated_at: DS.attr('date'),
  updated_at_format: computeDateTimeFormat('updated_at'),
  code: DS.attr({label: 'code.label'}),
  // Use in candidacy select list
  code_and_title: computed('code', 'title', function() {
    return `${this.get('code')} -  ${this.get('title')}`;
  }),

  candidacies: DS.hasMany('candidacy'),

  participation: DS.attr(),
  participation_current: computed('participation', 'i18n.locale', function(){
    return this.get('i18n').t(this.get('participation'));
  }),

  past_positions: DS.hasMany('position'),

  is_latest: computed('code', 'id', function() {
    return get(this, 'code').replace('APP','') === get(this, 'id');
  }),

  is_open: computed('starts_at', 'ends_at', function() {
    let now = moment(),
      start = get(this, 'starts_at'),
      end = get(this, 'ends_at');

    return (now.isBetween(start, end) || now.isSame(start) || now.isSame(end));
  }),

  is_closed: computed('ends_at', function() {
    let now = moment(),
      end = get(this, 'ends_at');
    return now.isAfter(end);
  }),

  /*
   * If a position is in state "posted" we display a state depending on the
   * ability to accept candidacies at the current time. These states are:
   * posted: before the posted position starts to accept candidacies
   * open: when the posted position accepts candidacies
   * closed: after the last day that a posted position can accept candidacies
   */

  state_calc_verbose: computed('is_open', 'is_closed', 'state', 'i18n.locale', function() {
    if(get(this, 'state') === 'posted') {
      if(get(this, 'is_closed')) {
        return get(this, 'i18n').t('closed');
      }
      else if(get(this, 'is_open')) {
        return get(this, 'i18n').t('open');
      }
      else {
        return get(this, 'state_verbose');
      }
    }
    else {
      return get(this, 'state_verbose');
    }
  })
});
