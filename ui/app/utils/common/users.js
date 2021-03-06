import Ember from 'ember';
import validate from 'ember-gen/validate';
import {i18nValidate} from 'ui/validators/i18n';
import {mustAcceptTerms} from 'ui/validators/custom';
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

function samePassword({field, checkLen}) {
  return (key, value, old, changes, content) => {
    if (changes.password && value && value.length > (checkLen || 3)) {
      if (value != changes.password) {
        return 'passwords.do.not.match'
      }
    }
    return true;
  }
};

const FILE_FIELDS = [
  'publications',
  'id_passport_file',
  'diplomas',
  'cv',
  'cv_professor',
  'pubs_note'
];

const FIELDS_ALL = [
  'user_id',
  'email',
  'username',
  'password',
  'first_name',
  'last_name',
  'father_name',
  'role',
  'id_passport',
  'home_phone_number',
  'mobile_phone_number',
  'shibboleth_idp',
  'shibboleth_schac_home_organization',
  'has_accepted_terms',
];

const VALIDATORS = {
  username: [validate.presence(true), validate.length({min:3, max:50})],
  first_name: [i18nValidate([validate.presence(true), validate.length({min:3, max:200})])],
  last_name: [i18nValidate([validate.presence(true), validate.length({min:3, max:200})])],
  father_name: [i18nValidate([validate.presence(true), validate.length({min:3, max:200})])],
  mobile_phone_number: [validate.presence(true), validate.number({ integer: true }), validate.length({min:10, max:20})],
  home_phone_number: [validate.presence(true), validate.number({ integer: true }), validate.length({min:10, max:20})],
  email: [validate.format({ type: 'email' })],
  id_passport: [validate.presence(true)],
};

const VALIDATORS_CREATE = Ember.assign({}, VALIDATORS, {
  has_accepted_terms: [mustAcceptTerms()],
});


const FIELDSET_CREATE = {
  label: 'fieldsets.labels.user_info',
  fields: [
    'username',
    'email',
    field('password', {
      required: true,
      validators: [
        validate.length({min: 6}),
      ],
      type: 'string',
      formAttrs: { type: 'password' }
    }),
    field('password2', {
      required: true,
      validators: [
        validate.length({min: 6}),
        samePassword({field: 'password', checkLen: 5})
      ],
      type: 'string',
      formAttrs: { type: 'password' }
    }),
    'first_name',
    'last_name',
    'father_name',
    'id_passport',
    'home_phone_number',
    'mobile_phone_number',
    'has_accepted_terms'
  ],
  layout: {
    flex: [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 100]
  }
};

const FIELDSET_EDIT_VERIFIABLE = {
  label: 'fieldsets.labels.user_info',
  fields: [
    field('username', { disabled: true }),
    field('status_verbose', { disabled: true}),
    field('user_id', {disabled: true}),
    field('email', { disabled: true }),
    'first_name',
    'last_name',
    'father_name',
    'id_passport',
    'home_phone_number',
    'mobile_phone_number',
  ],
  layout: {
    flex: [50, 50, 50, 50, 50, 50, 50, 50, 50, 50]
  }
}

const FIELDSET_DETAILS_VERIFIABLE = {
  label: 'fieldsets.labels.user_info',
  fields: [
    field('username', {disabled: true}),
    field('status_verbose', {disabled: true}),
    field('user_id', {disabled: true}),
    'email',
    'full_name_current',
    'father_name_current',
    'id_passport',
    'home_phone_number',
    'mobile_phone_number',
  ],
  layout: {
    flex: [50, 50, 50, 50, 50, 50, 50, 25, 25]
  }
};

const FIELDSET_EDIT_NON_VERIFIABLE = {
  label: 'fieldsets.labels.user_info',
  fields: [
    field('username', { disabled: true }),
    field('user_id', {disabled: true}),
    field('email', { disabled: true }),
    'first_name',
    'last_name',
    'father_name',
    'id_passport',
    'home_phone_number',
    'mobile_phone_number',
  ],
  layout: {
    flex: [100, 50, 50, 50, 50, 50, 50, 50, 50]
  }
};

const FIELDSET_DETAILS_NON_VERIFIABLE = {
  label: 'fieldsets.labels.user_info',
  fields: [
    field('username', {disabled: true}),
    field('user_id', {disabled: true}),
    'email',
    'full_name_current',
    'father_name_current',
    'id_passport',
    'home_phone_number',
    'mobile_phone_number',
  ],
  layout: {
    flex: [100, 50, 50, 50, 50, 50, 25, 25]
  }
};

const FIELDSET_DETAILS_NON_VERIFIABLE_LESS_FIELDS = {
  label: 'fieldsets.labels.user_info',
  fields: [
    field('username', {disabled: true}),
    field('user_id', {disabled: true}),
    'email',
    'full_name_current',
    'father_name_current',
    'home_phone_number',
    'mobile_phone_number',
  ],
  layout: {
    flex: [100, 50, 50, 50, 50, 50, 50, 50]
  }
};

const FIELDSET_EDIT_USER = {
  label: 'fieldsets.labels.user_info',
  fields: [
    field('username', { disabled: true }),
    field('id', {disabled: true}),
    'email',
    'first_name',
    'last_name',
    'father_name',
    'id_passport',
    'home_phone_number',
    'mobile_phone_number',
  ],
  layout: {
    flex: [100, 50, 50, 50, 50, 50, 50, 50, 50]
  }
}

const FIELDSET_DETAILS_USER = {
  label: 'fieldsets.labels.user_info',
  fields: [
    field('username', {disabled: true}),
    field('id', {disabled: true}),
    'email',
    'full_name_current',
    'father_name_current',
    'id_passport',
    'home_phone_number',
    'mobile_phone_number',
  ],
  layout: {
    flex: [100, 50, 50, 50, 50, 50, 25, 25]
  }
}

const FIELDSET_EDIT_ACADEMIC = {
  label: 'fieldsets.labels.user_info',
  fields: [
    field('status_verbose', { disabled: true}),
    field('user_id', {disabled: true}),
    field('email', { disabled: true }),
    'first_name',
    'last_name',
    'father_name',
    'id_passport',
    'home_phone_number',
    'mobile_phone_number'
  ],
  layout: {
    flex: [50, 50, 50, 50, 50, 50, 50, 50, 50, 50]
  }
}

const FIELDSET_DETAILS_ACADEMIC = {
  label: 'fieldsets.labels.user_info',
  fields: [
    field('status_verbose', {disabled: true}),
    field('user_id', {disabled: true}),
    'email',
    'full_name_current',
    'father_name_current',
    'id_passport',
    'home_phone_number',
    'mobile_phone_number',
  ],
  layout: {
    flex: [50, 50, 50, 50, 50, 50, 50, 25, 25]
  }
}


const FIELDSET_REGISTER_ACADEMIC = {
  label: 'fieldsets.labels.user_info',
  fields:  [
    field('email', { disabled: false }),
    'first_name',
    'last_name',
    'father_name',
    'id_passport',
    'home_phone_number',
    'mobile_phone_number',
    'has_accepted_terms'
  ],
  layout: {
    flex: [100, 50, 50, 50, 50, 50, 50, 100]
  }
};

const normalizeUser = function(hash, serializer) {
  let user_info = hash['user'];
  // for users with nested user object, we need to flatten nested user object.
  // All properties get flatten as they are, except from user.id that is
  // flattened as user_id
  Object.keys(user_info).forEach(function(key){
    if (key == 'id') {
      hash['user_id'] = user_info['id']
    } else {
      hash[key] = user_info[key]
    }
  });

  // handle client-side only attribute
  hash.cv_in_url = false;
  if (hash.cv_url && hash.cv_url.length > 0) {
    hash.cv_in_url = true;
  }
  delete hash['user'];
  // if the flattened user properties do not contain id, then user_id is
  // assigned to it.
  // This is the case for helpdesk users
  if (!hash.hasOwnProperty('id')){
    hash['id'] = hash['user_id']
  }
  return hash;
}


const serializeUser = function(json) {
  let user_info = {};

  for (let filefield of FILE_FIELDS) {
    if (filefield in json) {
      delete json[filefield];
    }
  }

  for (let field of FIELDS_ALL) {
    if (field in json) {
      if (field=='user_id') {
        user_info['id'] = json['user_id']
      } else {
        user_info[field] = json[field];
      }
      delete json[field];
    }
  }
  if (Object.keys(user_info).length) {
    json['user'] = user_info;
  }

  if (json.hasOwnProperty('cv_in_url') && !json['cv_in_url']){
      json['cv_url'] ='';
  }

  return json;
}

const normalizeUserErrors = function(errors) {
  return errors.map((e) => {
    // remove '/user/' nesting
    e.source.pointer = e.source.pointer.replace('/user/', '/');
    return e;
  });
}
/*
  FIELDSET_CREATE: Used for the creation of all types of users and the
    registration of non academin users
  FIELDSET_REGISTER_ACADEMIC: Used for the creation of an academin user .Does
    not contains 'username' field.
  FIELDSET_*_VERIFIABLE: Used for candidate, professor, institution-manager,
    assistants. Appart from common user fields, contains 'user_id' and
    'status_verbose' fields
  FIELDSET_*_VERIFABLE: Used for helpdesk. Like VERIFIABLE fields, but it does
    not contain 'status_verbose' field
  FIELDSET_DETAILS_NON_VERIFIABLE_LESS_FIELDS: Used for users with role ministry
  FIELDSET_*_USER: For plain users. Contains 'id' field and does not contain
  'status_verbose' field.
  FIELDSET_*_ACADEMIC: For academin users. Verifiable users that do not have
   'username' field.
*/

export {normalizeUser, serializeUser, normalizeUserErrors,
        FILE_FIELDS,
        FIELDS_ALL,
        VALIDATORS,

        FIELDSET_CREATE,
        VALIDATORS_CREATE,

        FIELDSET_EDIT_VERIFIABLE,
        FIELDSET_DETAILS_VERIFIABLE,

        FIELDSET_EDIT_NON_VERIFIABLE,
        FIELDSET_DETAILS_NON_VERIFIABLE,
        FIELDSET_DETAILS_NON_VERIFIABLE_LESS_FIELDS,

        FIELDSET_EDIT_USER,
        FIELDSET_DETAILS_USER,

        FIELDSET_EDIT_ACADEMIC,
        FIELDSET_DETAILS_ACADEMIC,

        FIELDSET_REGISTER_ACADEMIC,
};
