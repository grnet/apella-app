import DS from 'ember-data';
import ENV from 'ui/config/environment';
import {computeI18N, computeI18NChoice} from 'ui/lib/common';
import get_label from '../utils/common/label_list_item';

const { computed, get } = Ember,
      CHOICES = ENV.APP.resource_choices;


export default DS.Model.extend({
  user_id: DS.attr(),
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

  role_verbose: computeI18NChoice('role', CHOICES.USER_ROLES),
  first_name_current: computeI18N('first_name'),
  last_name_current: computeI18N('last_name'),
  father_name_current: computeI18N('father_name'),
  full_name_current: computeI18N('first_name_current')
});
