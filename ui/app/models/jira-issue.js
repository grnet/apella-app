import DS from 'ember-data';
import ENV from 'ui/config/environment';
import {computeI18NChoice, computeDateTimeFormat, prefixSelect} from 'ui/lib/common';

const {
  computed,
  get
} = Ember,
  CHOICES = ENV.APP.resources;

let issue_types = prefixSelect(CHOICES.JIRA_ISSUE_TYPES, 'jira.');
let states = prefixSelect(CHOICES.JIRA_ISSUE_STATES, 'jira.');

export default DS.Model.extend({
  code: DS.attr(),
  user: DS.belongsTo('user', {formAttrs: {optionLabelAttr: 'full_name_current'}}),
  reporter: DS.belongsTo('user', {formAttrs: {optionLabelAttr: 'full_name_current'}}),
  reporter_id_if_not_user: computed('user.id', 'reporter.id', function(){
    if (get(this, 'user.id') == get(this, 'reporter.id')) {
      return '-';
    } else {
      return get(this, 'reporter.id');
    }
  }),
  title: DS.attr(),
  description: DS.attr({type:'text'}),
  state: DS.attr({type: 'select', choices: states, defaultValue: 'open'}),
  state_verbose: computeI18NChoice('state', states),
  issue_type: DS.attr({type: 'select', choices: issue_types, defaultValue: 'complaint'}),
  issue_type_verbose: computeI18NChoice('issue_type', issue_types),
  resolution: DS.attr({type: 'select', choices: CHOICES.JIRA_ISSUE_RESOLUTION}),
  resolution_verbose: computeI18NChoice('resolution', CHOICES.JIRA_ISSUE_RESOLUTION),
  created_at: DS.attr('date'),
  created_at_format: computeDateTimeFormat('created_at'),
  updated_at: DS.attr('date'),
  updated_at_format: computeDateTimeFormat('updated_at'),
});
