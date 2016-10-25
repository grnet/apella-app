import Ember from 'ember';
import validate from 'ember-gen/validate';
import {i18nValidate} from 'ui/validators/i18n';

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



const USER_FIELDSET = {
  label: 'fieldsets.labels.user_info',
  fields: USER_FIELDS,
  layout: {
        flex: [100, 50, 50, 50, 50, 100, 50, 50, 50, 50]
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
}



const normalizeUser = function(hash, serializer) {
  let user_info = hash['user'];
  Object.keys(user_info).forEach(function(key){
    if (key!= 'id') {
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


export {normalizeUser, serializeUser,
        USER_FIELDS, USER_FIELDSET, USER_VALIDATORS};
