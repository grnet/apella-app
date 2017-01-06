import Ember from 'ember';
import validate from 'ember-gen/validate';
import {i18nValidate} from 'ui/validators/i18n';
import {field} from 'ember-gen';
import {disable_field} from 'ui/utils/common/fields';
import {fileField} from 'ui/lib/common';

const { assign, computed, get, set } = Ember;

const FILE_FIELDS = [
  'publications',
  'id_passport_file',
  'diplomas',
  'cv',
  'application_form'
];

const USER_FIELDS_ALL = [
  'user_id',
  'username',
  'password',
  'email',
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
  'password',
  'email',
  'first_name',
  'last_name',
  'father_name',
  'id_passport',
  'mobile_phone_number',
  'home_phone_number'
]

const USER_FIELDS_EDIT = [
  field('username', { readonly: true }),
  field('email', { readonly: true }),
  'first_name',
  'last_name',
  'father_name',
  'id_passport',
  'mobile_phone_number',
  'home_phone_number'
];
const USER_FIELDS_EDIT_ACADEMIC = USER_FIELDS_EDIT.slice(1);

const USER_FIELDS_REGISTER = [
  field('username', { readonly: false }),
  'password',
  field('password2', { type: 'string', formAttrs: { type: 'password' }}),
  field('email', { readonly: false }),
  'first_name',
  'last_name',
  'father_name',
  'id_passport',
  'mobile_phone_number',
  'home_phone_number'
];
const USER_FIELDS_REGISTER_ACADEMIC = USER_FIELDS_REGISTER.slice(3);

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

const PROFESSOR_FILES_FIELDS = [
  fileField('cv', 'professor', 'cv', {})
];

const CANDIDATE_FILES_FIELDS = [
  fileField('id_passport_file', 'candidate', 'id_passport', {
  }),
  fileField('application_form', 'candidate', 'application_form', {
  }),
  fileField('cv', 'candidate', 'cv', {
  }),
  fileField('diplomas', 'candidate', 'diploma', {}, {
    multiple: true
  }),
  fileField('publications', 'candidate', 'publication', {}, {
    multiple: true
  }),
]

const PROFESSOR_FIELDS = [
  'institution',
  'department',
  'rank',
  field('cv_url', {
    hint: 'cv_url.hint',
  }),
  'fek',
  field('discipline_text', {
    type: 'text',
    required: computed('model.changeset.discipline_in_fek', function() {
      let check = get(this, 'model.changeset.discipline_in_fek');
      return !check;
    }),
    disabled: computed('model.changeset.discipline_in_fek', function() {
      let check = get(this, 'model.changeset.discipline_in_fek');
      if (check) { Ember.run.once(this, () => set(this, 'model.changeset.discipline_text', '')) };
      return check;
    })
  }),
  field('discipline_in_fek',{
    hint: 'discipline_in_fek.hint',
  }),
  'is_foreign',
  'speaks_greek',
];

const PROFESSOR_FIELDS_REGISTER = PROFESSOR_FIELDS.concat();

const PROFESSOR_FIELDS_REGISTER_REQUIRED = [
  'institution', 'department', 'rank', 'fek'
];

const INSTITUTION_MANGER_FIELDS = [
  'institution',
  'authority',
  'authority_full_name',
  'manager_role',
]

const INSTITUTION_SUB_MANAGER_FIELDS = [
  'sub_first_name',
  'sub_last_name',
  'sub_father_name',
  'sub_email',
  'sub_mobile_phone_number',
  'sub_home_phone_number'
]

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
        flex: [100, 50, 50, 50, 50, 50, 50]
  }
}

const USER_FIELDSET_EDIT_ACADEMIC = Ember.assign({}, USER_FIELDSET_EDIT, {
  fields: USER_FIELDS_EDIT_ACADEMIC
});

const USER_FIELDSET_REGISTER_ACADEMIC = Ember.assign({}, USER_FIELDSET_EDIT, {
  fields: USER_FIELDS_REGISTER_ACADEMIC,
  required: USER_FIELDS_REGISTER_REQUIRED_ACADEMIC
});

const USER_FIELDSET_REGISTER = Ember.assign({}, USER_FIELDSET_EDIT, {
  fields: USER_FIELDS_REGISTER,
  required: USER_FIELDS_REGISTER_REQUIRED
});

const USER_FIELDSET_DETAILS = {
  label: 'fieldsets.labels.user_info',
  fields: [
    'username',
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

const PROFESSOR_FIELDSET = {
  label: 'fieldsets.labels.more_info',
  fields: PROFESSOR_FIELDS,
  layout: {
    flex: [50, 50, 100, 50, 50, 100, 100, 100, 50, 50]
   }
}

const PROFESSOR_FILES_FIELDSET = {
  label: 'fieldsets.labels.files',
  fields: PROFESSOR_FILES_FIELDS
};

const CANDIDATE_FILES_FIELDSET = {
  label: 'fieldsets.labels.files',
  fields: CANDIDATE_FILES_FIELDS 
}

const PROFESSOR_FIELDSET_REGISTER = Ember.assign({}, PROFESSOR_FIELDSET, {
  label: Ember.computed('model.is_academic', function() {
    let academic = this.get('model.is_academic');
    if (academic) { return 'fieldsets.labels.user_info.academic'; }
    return 'fieldsets.labels.more_info';
  }),
  required: PROFESSOR_FIELDS_REGISTER_REQUIRED,
  fields: PROFESSOR_FIELDS_REGISTER
});

const INST_MANAGER_FIELDSET_MAIN = {
  label: 'fieldsets.labels.more_info',
  fields: INSTITUTION_MANGER_FIELDS,
  layout: {
    flex: [50, 50, 50, 50]
   }
}

const INST_MANAGER_FIELDSET_SUB = {
  label: 'manager.label.sub_fieldset',
  fields: INSTITUTION_SUB_MANAGER_FIELDS,
  layout: {
    flex: [50, 50, 50, 50, 50, 50]
   }
}

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

const PROFESSOR_VALIDATORS = {
  cv_url: [validate.format({allowBlank: true, type:'url'})],
  institution: [validate.presence(true)],
}

const INSTITUTION_MANAGER_VALIDATORS = {
  sub_first_name: [i18nValidate([validate.presence(true), validate.length({min:3, max:200})])],
  sub_last_name: [i18nValidate([validate.presence(true), validate.length({min:3, max:200})])],
  sub_father_name: [i18nValidate([validate.presence(true), validate.length({min:3, max:200})])],
  sub_mobile_phone_number: [validate.format({ type: 'phone' })],
  sub_home_phone_number: [validate.format({ type: 'phone' })],
  sub_email: [validate.format({ type: 'email' })],
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
        USER_FIELDSET_REGISTER, USER_FIELDSET_REGISTER_ACADEMIC, PROFESSOR_FIELDSET_REGISTER,
        USER_FIELDSET_DETAILS, USER_FIELDSET_DETAILS_ACADEMIC, USER_FIELDSET_EDIT_ACADEMIC,
        PROFESSOR_FIELDSET, PROFESSOR_VALIDATORS, PROFESSOR_FILES_FIELDSET,
        CANDIDATE_FILES_FIELDSET,
        INST_MANAGER_FIELDSET_MAIN, INST_MANAGER_FIELDSET_SUB,
        INSTITUTION_MANAGER_VALIDATORS, USER_FIELDS_ALL};
