import DS from 'ember-data';
import ENV from 'ui/config/environment';
import {computeDateTimeFormat, computeI18NChoice, prefixSelect} from 'ui/lib/common';

const CHOICES = ENV.APP.resources;

let application_types = prefixSelect(CHOICES.APPLICATION_TYPES, 'user_application.');
let application_states = prefixSelect(CHOICES.APPLICATION_STATES, 'user_application.');

export default DS.Model.extend({
  app_type: DS.attr({type: 'select', choices: application_types, defaultValue: 'tenure'}),
  app_type_verbose: computeI18NChoice('app_type', application_types),
  created_at: DS.attr('date'),
  created_at_format: computeDateTimeFormat('created_at'),
  state: DS.attr({type: 'select', choices: application_states, defaultValue: 'pending'}),
  state_verbose: computeI18NChoice('state', application_states),
  updated_at: DS.attr('date'),
  updated_at_format: computeDateTimeFormat('updated_at'),
  user: DS.belongsTo('user', {formAttrs: {optionLabelAttr: 'full_name_current'}}),
});
