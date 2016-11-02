import DS from 'ember-data';
import ENV from 'ui/config/environment';
import User from 'ui/models/user';
import {normalizeUser, serializeUser, normalizeUserErrors} from 'ui/utils/common/users';

const CHOICES = ENV.APP.resource_choices;

export default User.extend({
  __api__: {
    normalizeErrors: normalizeUserErrors,
    normalize: normalizeUser,
    serialize: serializeUser
  },
  institution: DS.belongsTo('institution', {label: 'institution.label', attrs: {optionLabelAttr: 'title_current'}}),
  authority: DS.attr({label: 'manager.label.authority_type', type: 'select', choices: CHOICES.AUTHORITIES}),
  authority_full_name: DS.attr({label: 'manager.label.authority_full_name'}),
  manager_role: DS.attr({label: 'manager.label.role', type: 'select', choices: CHOICES.MANAGER_ROLES})
});
