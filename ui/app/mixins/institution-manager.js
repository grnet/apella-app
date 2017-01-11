import Ember from 'ember';
import DS from 'ember-data';
import ENV from 'ui/config/environment';
import {computeI18N, computeI18NChoice} from 'ui/lib/common';

const CHOICES = ENV.APP.resources;

export default Ember.Mixin.create({
  institution: DS.belongsTo('institution', {label: 'institution.label', formAttrs: {optionLabelAttr: 'title_current'}}),
  authority: DS.attr({
    label: 'manager.label.authority_type',
    type: 'select',
    choices: CHOICES.AUTHORITIES,
    translate: true,
  }),
  authority_full_name: DS.attr({label: 'manager.label.authority_full_name'}),
  manager_role: DS.attr({label: 'manager.label.role', type: 'select', choices: CHOICES.MANAGER_ROLES, translate:true}),
  manager_role_verbose: computeI18NChoice('manager_role', CHOICES.USER_ROLES),
  sub_first_name: DS.attr({label: 'first_name.label', formComponent: 'i18n-input-field'}),
  sub_last_name: DS.attr({label: 'last_name.label', formComponent: 'i18n-input-field'}),
  sub_father_name: DS.attr({label: 'father_name.label', formComponent: 'i18n-input-field'}),
  sub_email: DS.attr({label: 'email.label'}),
  sub_mobile_phone_number: DS.attr({label: 'mobile_phone_number.label'}),
  sub_home_phone_number: DS.attr({label: 'home_phone_number.label'}),
  sub_first_name_current: computeI18N('sub_first_name'),
  sub_last_name_current: computeI18N('sub_last_name'),
  sub_father_name_current: computeI18N('sub_father_name'),
});
