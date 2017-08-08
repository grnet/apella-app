import DS from 'ember-data';
import ENV from 'ui/config/environment';
import {booleanFormat, computeI18N, computeI18NChoice} from 'ui/lib/common';

const { computed, get } = Ember,
      CHOICES = ENV.APP.resources;


export default DS.Model.extend({
  user_id: DS.attr(),
  old_user_id: DS.attr(),
  username: DS.attr(),
  password: DS.attr({formAttrs: {type: 'password'}}),
  email: DS.attr(),
  first_name: DS.attr({formComponent: 'i18n-input-field'}),
  last_name: DS.attr({formComponent: 'i18n-input-field'}),
  father_name: DS.attr({formComponent: 'i18n-input-field'}),
  // role is used to check user group
  role: DS.attr({type: 'select', choices: CHOICES.USER_ROLES}),
  id_passport: DS.attr(),
  mobile_phone_number: DS.attr(),
  home_phone_number: DS.attr(),
  is_stuff: DS.attr({type: 'boolean', defaultValue: false}),
  is_active: DS.attr({type: 'boolean', defaultValue: false}),
  email_verified: DS.attr({type: 'boolean', defaultValue: false}),
  can_set_academic: DS.attr({type: 'boolean'}),
  can_upgrade_role: DS.attr({type: 'boolean'}),

  role_verbose: computeI18NChoice('role', CHOICES.USER_ROLES),
  first_name_current: computeI18N('first_name'),
  last_name_current: computeI18N('last_name'),
  father_name_current: computeI18N('father_name'),
  login_method: DS.attr('string'),

  has_accepted_terms: DS.attr({type: 'boolean', defaultValue: false }),
  has_accepted_terms_verbose: booleanFormat('has_accepted_terms'),

  shibboleth_idp: DS.attr(),
  shibboleth_schac_home_organization: DS.attr(),

  full_name_current: computed('first_name_current', 'last_name_current', function(){
    return `${this.get('first_name_current')} ${this.get('last_name_current')}`;
  }),

  status_verbose: computed('is_active', 'email_verified', 'i18n.locale', function() {
    if (!get(this, 'email_verified')) {
      return get(this, 'i18n').t('email_pending_verification');
    } else {
      if (get(this, 'is_active')) {
        return get(this, 'i18n').t('active');
      } else {
        return get(this, 'i18n').t('inactive');
      }
    }
  }),

  jira_issues: DS.hasMany('jira_issue', {
    async: true,
    inverse: 'user'
  }),


});

