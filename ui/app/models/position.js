import DS from 'ember-data';
import ENV from 'ui/config/environment';
import {computeI18NChoice, computeDateFormat, computeDateTimeFormat} from 'ui/lib/common';

const {
  computed,
  computed: { readOnly },
  get
} = Ember,
      CHOICES = ENV.APP.resources;

let extra_position_states = [["open", "Open"], ["closed", "Closed"]];
let position_states_expanded = CHOICES.POSITION_STATES.insertAt(2, extra_position_states[0]).insertAt(3, extra_position_states[1]);
// remove state "draft" from position states expanded array
position_states_expanded.splice(0,1);


export default DS.Model.extend({

  // All keys have been sorted alphabetically

  assistant_files: DS.hasMany('apella-file'),
  author: DS.belongsTo('institution-manager'),
  can_apply: computed.equal('currentUserCandidacy.length', 0),
  candidacies: DS.hasMany('candidacy'),
  code: DS.attr({label: 'code.label'}),
  // Use in candidacy select list
  code_and_title: computed('code', 'title', function() {
    return `${this.get('code')} -  ${this.get('title')}`;
  }),
  committee: DS.hasMany('professor'),
  committee_external: DS.hasMany('professor'),
  committee_internal: DS.hasMany('professor'),
  committee_note: DS.belongsTo('apella-file'),
  committee_proposal: DS.belongsTo('apella-file'),
  committee_set_file: DS.belongsTo('apella-file'),

  created_at: DS.attr('date'),
  /*
   * Calculate if a user can apply for a position.
   * If he has not already applied, then can_apply is true.
   * */
  currentUserCandidacy: computed('user_id', 'id', 'candidacies.[]', function() {
    let position_id = get(this, 'id');
    let candidate_id = get(this, 'user_id');
    let promise = get(this, 'store').query('candidacy', {
      position: position_id,
      state: 'posted',
      candidate: candidate_id,
      latest: true
    });
    return DS.PromiseArray.create({promise});
  }),
  department: DS.belongsTo('department', {
    formAttrs: {
      optionLabelAttr: 'title_current'
    }
  }),
  department_dep_number: DS.attr(),
  discipline: DS.attr(),
  description: DS.attr({type:'text'}),
  elected: DS.belongsTo('user', {formAttrs: {optionLabelAttr: 'full_name_current'}}),
  electors: DS.hasMany('professor'),
  electors_meeting_date: DS.attr('date'),
  electors_meeting_date_format: computeDateFormat('electors_meeting_date'),
  electors_meeting_proposal: DS.belongsTo('apella-file'),
  electors_meeting_to_set_committee_date: DS.attr('date'),
  electors_meeting_to_set_committee_date_format: computeDateFormat('electors_meeting_to_set_committee_date'),
  electors_regular_external: DS.hasMany('professor'),
  electors_regular_internal: DS.hasMany('professor'),
  electors_set_file: DS.belongsTo('apella-file'),
  electors_sub_external: DS.hasMany('professor'),
  electors_sub_internal: DS.hasMany('professor'),
  ends_at: DS.attr('date', {utc: true}),
  ends_at_format: computeDateFormat('ends_at'),
  failed_election_decision: DS.belongsTo('apella-file'),
  fek: DS.attr({label: 'position.fek.label', displayComponent: 'url-display'}),
  fek_posted_at: DS.attr('date'),
  fek_posted_at_format: computeDateFormat('fek_posted_at'),
  institution: readOnly('department.institution'),
  is_closed: computed('ends_at', 'state', function() {
    let now = posted = get(this, 'state') === 'posted',
      end = moment(get(this, 'ends_at')).endOf('day');
    return end.isBefore() && posted;
  }),
  is_latest: computed('code', 'id', function() {
    return get(this, 'code').replace('APP','') === get(this, 'id');
  }),
  is_open: computed('starts_at', 'ends_at', function() {
    let now = moment(),
      start = moment(get(this, 'starts_at')).startOf('day'),
      end = moment(get(this, 'ends_at')).endOf('day');
    return now.isBetween(start, end);
  }),
  // is_posted is true for the positions that are not yet open
  is_posted: computed('state', 'is_closed', 'is_open', function(){
    return get(this, 'state') === 'posted' && !(get(this, 'is_open') || get(this, 'is_closed'));
  }),
  nomination_act: DS.belongsTo('apella-file'),
  nomination_act_fek: DS.attr({displayComponent: 'url-display'}),
  nomination_proceedings: DS.belongsTo('apella-file'),
  old_code: DS.attr(),
  participation: DS.attr(),
  participation_current: computed('participation', 'i18n.locale', function(){
    return this.get('i18n').t(this.get('participation'));
  }),
  past_positions: DS.hasMany('position'),
  proceedings_cover_letter: DS.belongsTo('apella-file'),
  revocation_decision: DS.belongsTo('apella-file'),
  second_best: DS.belongsTo('user', {formAttrs: {optionLabelAttr: 'full_name_current'}}),
  // Use in currentUserCandidacy
  session: Ember.inject.service(),
  starts_at: DS.attr('date'),
  starts_at_format: computeDateFormat('starts_at'),
  state: DS.attr({type: 'select', choices: CHOICES.POSITION_STATES, defaultValue: 'posted'}),
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
  }),
  state_expanded: DS.attr({type: 'select', choices: position_states_expanded}),
  state_verbose: computeI18NChoice('state', CHOICES.POSITION_STATES),
  subject: DS.belongsTo('subject', {
    formComponent: 'select-onchange',
    formAttrs: {
      lookupModel: 'subject_area',
      changedChoices: function(store, value) {
        return store.query('subject', {area: get(value, 'id')});
      },
      optionLabelAttr: 'title_current',
    }
  }),
  subject_area: DS.belongsTo('subject-area', {
    formAttrs: {
      optionLabelAttr: 'title_current'
    }
  }),
  title: DS.attr(),
  updated_at: DS.attr('date'),
  updated_at_format: computeDateTimeFormat('updated_at'),
  // Use in currentUserCandidacy
  user_id: computed.alias('session.session.authenticated.user_id'),
});
