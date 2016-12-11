import Ember from 'ember';
import validate from 'ember-gen/validate';
import {i18nValidate} from 'ui/validators/i18n';
import {field} from 'ember-gen';

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

const PROFESSOR_FIELDS = [
  'institution',
  'department',
  'rank',
  field('cv_url', {
    hint: 'cv_url.hint',
  }),
  'cv',
  'fek',
  'discipline_text',
  field('discipline_in_fek',{
    hint: 'discipline_in_fek.hint',
  }),
  'is_foreign',
  'speaks_greek',
]

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
        flex: [100, 50, 50, 50, 50, 100, 50, 50, 50, 50]
  }
}

const PROFESSOR_FIELDSET = {
  label: 'fieldsets.labels.more_info',
  fields: PROFESSOR_FIELDS,
  layout: {
    flex: [50, 50, 100, 50, 50, 100, 100, 100, 50, 50]
   }
}

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
  username: [validate.presence(true), validate.length({min:4, max:50})],
  first_name: [i18nValidate([validate.presence(true), validate.length({min:4, max:200})])],
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
  sub_first_name: [i18nValidate([validate.presence(true), validate.length({min:4, max:200})])],
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
        USER_FIELDS, USER_FIELDSET, USER_VALIDATORS,
        PROFESSOR_FIELDSET, PROFESSOR_VALIDATORS,
        INST_MANAGER_FIELDSET_MAIN, INST_MANAGER_FIELDSET_SUB,
        INSTITUTION_MANAGER_VALIDATORS};
