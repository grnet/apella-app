import DS from 'ember-data';
import ENV from 'ui/config/environment';

const CHOICES = ENV.APP.resource_choices;

export default DS.Model.extend({
  user: DS.belongsTo('user',{label: 'manager.label.user', attrs: { type: 'select', optionLabelAttr: 'username'}}),
  institution: DS.belongsTo('institution', {label: 'institution.label', attrs: {optionLabelAttr: 'title'}}),
  authority: DS.attr({label: 'manager.label.authority_type', type: 'select', choices: CHOICES.AUTHORITIES}),
  authority_full_name: DS.attr({label: 'manager.label.authority_full_name'}),
  manager_role: DS.attr({label: 'manager.label.role', type: 'select', choices: CHOICES.MANAGER_ROLES})
});
