import Ember from 'ember';

const USER_FIELDS = [
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

const normalizeUser = function(hash, serializer) {
  let user_info = hash['user'];
  Object.keys(user_info).forEach(function(key){
    hash[key] = user_info[key];
  });
  delete hash['user'];
  return hash;
}


const serializeUser = function(json) {
  let user_info = {};
  for (let field of USER_FIELDS) {
    if (field in json) {
      user_info[field] = json[field];
      delete json[field];
    }
  }
  if (Object.keys(user_info).length) {
    json['user'] = user_info;
  }
  return json;
}


export {normalizeUser, serializeUser};
