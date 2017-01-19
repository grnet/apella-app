import Ember from 'ember';
import validate from 'ember-gen/validate';
import {i18nValidate} from 'ui/validators/i18n';
import {field} from 'ember-gen';
import {disable_field} from 'ui/utils/common/fields';
import {fileField} from 'ui/lib/common';

const {
  assign,
  computed,
  get,
  set,
  computed: { or }
} = Ember;

const VALIDATORS = {
  sub_first_name: [i18nValidate([validate.presence(true), validate.length({min:3, max:200})])],
  sub_last_name: [i18nValidate([validate.presence(true), validate.length({min:3, max:200})])],
  sub_father_name: [i18nValidate([validate.presence(true), validate.length({min:3, max:200})])],
  sub_mobile_phone_number: [validate.format({ type: 'phone' })],
  sub_home_phone_number: [validate.format({ type: 'phone' })],
  sub_email: [validate.format({ type: 'email' })],
}

const FIELDS = [
  field('institution', {displayAttr: 'title_current'}),
  'authority',
  'authority_full_name',
];

const FIELDS_REGISTER = FIELDS.concat();

const SUB_FIELDS = [
  'sub_first_name',
  'sub_last_name',
  'sub_father_name',
  'sub_email',
  'sub_mobile_phone_number',
  'sub_home_phone_number'
];

const SUB_FIELDS_REGISTER = SUB_FIELDS.concat();

const FIELDSET = {
  label: 'fieldsets.labels.more_info',
  fields: FIELDS,
  layout: {
    flex: [50, 50, 50, 50]
   }
};

const FIELDSET_REGISTER = {
  label: 'fieldsets.labels.more_info',
  fields: FIELDS_REGISTER,
  layout: {
    flex: [50, 50, 100]
   }
};

const SUB_FIELDSET = {
  label: 'manager.label.sub_fieldset',
  fields: SUB_FIELDS,
  layout: {
    flex: [33, 33, 33, 50, 50]
   }
};

const SUB_FIELDSET_DETAILS = {
  label: 'manager.label.sub_fieldset',
  fields: [
    'sub_full_name_current',
    'sub_email',
    'sub_father_name_current',
    'sub_mobile_phone_number',
    'sub_home_phone_number'
  ],
  layout: {
    flex: [50, 50, 50, 25, 25]
   }
};


const SUB_FIELDSET_REGISTER = {
  label: 'manager.label.sub_fieldset',
  fields: SUB_FIELDS_REGISTER,
  layout: {
    flex: [33, 33, 33, 50, 50]
   }
};

export {
  FIELDSET,
  FIELDSET_REGISTER,
  SUB_FIELDSET,
  SUB_FIELDSET_DETAILS,
  SUB_FIELDSET_REGISTER,
  VALIDATORS
}
