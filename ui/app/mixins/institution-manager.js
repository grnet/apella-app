import Ember from 'ember';
import DS from 'ember-data';
import ENV from 'ui/config/environment';

const CHOICES = ENV.APP.resource_choices;

export default Ember.Mixin.create({
  institution: DS.belongsTo('institution', {label: 'institution.label', formAttrs: {optionLabelAttr: 'title_current'}}),
  authority: DS.attr({label: 'manager.label.authority_type', type: 'select', choices: CHOICES.AUTHORITIES}),
  authority_full_name: DS.attr({label: 'manager.label.authority_full_name'}),
  manager_role: DS.attr({label: 'manager.label.role', type: 'select', choices: CHOICES.MANAGER_ROLES})
});
