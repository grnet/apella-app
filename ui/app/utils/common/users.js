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

const FILE_FIELDS = [
  'publications',
  'id_passport_file',
  'diplomas',
  'cv',
  'cv_professor'
];

const USER_FIELDS_ALL = [
  'user_id',
  'email',
  'username',
  'password',
  'first_name',
  'last_name',
  'father_name',
  'role',
  'id_passport',
  'mobile_phone_number',
  'home_phone_number'
]

const USER_FIELDS = [
  'username',
  'email',
  'password',
  'first_name',
  'last_name',
  'father_name',
  'id_passport',
  'mobile_phone_number',
  'home_phone_number'
]

const USER_FIELDS_EDIT = [
  field('username', { disabled: true }),
  field('email', { disabled: true }),
  'first_name',
  'last_name',
  'father_name',
  'id_passport',
  'mobile_phone_number',
  'home_phone_number'
];
const USER_FIELDS_EDIT_ACADEMIC = USER_FIELDS_EDIT.slice(1);

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

const USER_FIELDS_REGISTER = [
  field('username', {
    disabled: false,
    validators: [validate.length({min: 4})]
  }),
  field('email', { disabled: false }),
  field('password', {
    required: true,
    type: 'string',
    validators: [validate.length({min: 6})],
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
  'mobile_phone_number',
  'home_phone_number'
];

const USER_FIELDS_REGISTER_ACADEMIC = [
  field('email', { disabled: false }),
  'first_name',
  'last_name',
  'father_name',
  'id_passport',
  'mobile_phone_number',
  'home_phone_number'
];

const USER_FIELDS_REGISTER_REQUIRED = [
  'username',
  'password',
  'password2',
  'email',
  'first_name',
  'last_name',
  'father_name',
  'id_passport',
  'mobile_phone_number',
  'home_phone_number'
];
const USER_FIELDS_REGISTER_REQUIRED_ACADEMIC = USER_FIELDS_REGISTER_REQUIRED.slice(3);


const USER_FIELDSET = {
  label: 'fieldsets.labels.user_info',
  fields: USER_FIELDS,
  layout: {
        flex: [100, 50, 50, 50, 50, 50, 50, 50, 50, 50]
  }
}

const USER_FIELDSET_EDIT = {
  label: 'fieldsets.labels.user_info',
  fields: USER_FIELDS_EDIT,
  layout: {
    flex: [50, 50, 50, 50, 33, 33, 33, 50]
  }
}

const USER_FIELDSET_EDIT_ACADEMIC = Ember.assign({}, USER_FIELDSET_EDIT, {
  fields: USER_FIELDS_EDIT_ACADEMIC,
  layout: {
    flex: [100, 33, 33, 33, 33, 33, 33]
  }
});

const USER_FIELDSET_REGISTER_ACADEMIC = Ember.assign({}, USER_FIELDSET_EDIT, {
  fields: USER_FIELDS_REGISTER_ACADEMIC,
  required: USER_FIELDS_REGISTER_REQUIRED_ACADEMIC,
  layout: {
    flex: [100, 33, 33, 33, 33, 33, 33, 33, 33]
  }
});

const USER_FIELDSET_REGISTER = Ember.assign({}, USER_FIELDSET_EDIT, {
  fields: USER_FIELDS_REGISTER,
  required: USER_FIELDS_REGISTER_REQUIRED,
  layout: {
    flex: [50, 50, 50, 50, 33, 33, 33, 33, 33, 33]
  }
});

const USER_FIELDSET_DETAILS = {
  label: 'fieldsets.labels.user_info',
  fields: [
    field('username', {disabled: true}),
    'email',
    'full_name_current',
    'father_name_current',
    'id_passport',
    'mobile_phone_number',
    'home_phone_number',
  ],
  layout: {
    flex: [50, 50, 50, 50, 50, 25, 25]
  }
}


const USER_FIELDSET_DETAILS_ACADEMIC = Ember.assign({}, USER_FIELDSET_DETAILS, {
  fields: USER_FIELDSET_DETAILS.fields.slice(1)
});

const USER_VALIDATORS = {
  username: [validate.presence(true), validate.length({min:3, max:50})],
  first_name: [i18nValidate([validate.presence(true), validate.length({min:3, max:200})])],
  last_name: [i18nValidate([validate.presence(true), validate.length({min:3, max:200})])],
  father_name: [i18nValidate([validate.presence(true), validate.length({min:3, max:200})])],
  mobile_phone_number: [validate.format({ type: 'phone' })],
  home_phone_number: [validate.format({ type: 'phone' })],
  email: [validate.format({ type: 'email' })],
  id_passport: [validate.presence(true)],
}

const normalizeUser = function(hash, serializer) {
  let user_info = hash['user'];
  Object.keys(user_info).forEach(function(key){
    if (key!= 'id' || !hash['id']) {
      hash[key] = user_info[key];
    } else {
      hash['user_id'] = user_info['id'];
    }
  });

  // handle client-side only attribute
  hash.cv_in_url = false;
  if (hash.cv_url && hash.cv_url.length > 0) {
    hash.cv_in_url = true;
  }
  delete hash['user'];
  return hash;
}


const serializeUser = function(json) {
  let user_info = {};

  for (let filefield of FILE_FIELDS) {
    if (filefield in json) {
      delete json[filefield];
    }
  }

  for (let field of USER_FIELDS_ALL) {
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
  return json;
}

const normalizeUserErrors = function(errors) {
  return errors.map((e) => {
    // remove '/user/' nesting
    e.source.pointer = e.source.pointer.replace('/user/', '/');
    return e;
  });
}


export {normalizeUser, serializeUser, normalizeUserErrors,
        USER_FIELDS, USER_FIELDSET, USER_FIELDSET_EDIT, USER_VALIDATORS,
        USER_FIELDSET_DETAILS,
        USER_FIELDSET_REGISTER, USER_FIELDSET_REGISTER_ACADEMIC,
        USER_FIELDSET_DETAILS, USER_FIELDSET_DETAILS_ACADEMIC, USER_FIELDSET_EDIT_ACADEMIC,
        USER_FIELDS_ALL, FILE_FIELDS};
