import DS from 'ember-data';
import ENV from 'ui/config/environment';
import {computeDateTimeFormat, computeI18NChoice, prefixSelect} from 'ui/lib/common';

const {
  computed,
  get
} = Ember,
  CHOICES = ENV.APP.resources;



let application_types = prefixSelect(CHOICES.APPLICATION_TYPES, 'user_application.');
let application_states = prefixSelect(CHOICES.APPLICATION_STATES, 'user_application.');

export default DS.Model.extend({
  app_type: DS.attr({type: 'select', choices: application_types, defaultValue: 'tenure'}),
  app_type_verbose: computeI18NChoice('app_type', application_types),
  can_accept_candidacies: DS.attr(),
  cannot_create_position: DS.attr(),
  created_at: DS.attr('date'),
  created_at_format: computeDateTimeFormat('created_at'),
  department: DS.belongsTo('department', {formAttrs: {optionLabelAttr: 'title_current'}}),
  position_id: DS.attr(),
  position_id_format: computed('position_id', function(){
    let position_id = get(this, 'position_id');
    return position_id > 0 ? position_id: '-';
  }),
  position_state: DS.attr(),
  state: DS.attr({type: 'select', choices: application_states, defaultValue: 'pending'}),
  state_verbose: computeI18NChoice('state', application_states),
  updated_at: DS.attr('date'),
  updated_at_format: computeDateTimeFormat('updated_at'),
  user: DS.belongsTo('user', {formAttrs: {optionLabelAttr: 'full_name_current'}}),
});
