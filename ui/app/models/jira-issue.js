import DS from 'ember-data';
import ENV from 'ui/config/environment';
import {prefixSelect} from 'ui/lib/common';

const {
  computed,
  get
} = Ember,
  CHOICES = ENV.APP.resources;

let issue_types = prefixSelect(CHOICES.JIRA_ISSUE_TYPES, 'jira.');

export default DS.Model.extend({
  code: DS.attr(),
  user: DS.belongsTo('user', {formAttrs: {optionLabelAttr: 'full_name_current'}}),
  reporter: DS.belongsTo('user', {formAttrs: {optionLabelAttr: 'full_name_current'}}),
  title: DS.attr(),
  description: DS.attr({type:'text'}),
  state: DS.attr({type: 'select', choices: CHOICES.JIRA_ISSUE_STATES, defaultValue: 'open'}),
  issue_type: DS.attr({type: 'select', choices: issue_types, defaultValue: 'complaint'}),
  resolution: DS.attr({type: 'select', choices: CHOICES.JIRA_ISSUE_RESOLUTION, defaultValue: 'fixed'}),
  created_at: DS.attr('date'),
  updated_at: DS.attr('date'),
});
