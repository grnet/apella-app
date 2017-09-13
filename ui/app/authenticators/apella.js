import Ember from 'ember';
import ApimasAuthenticator from 'ember-gen-apimas/authenticators/apimas';
import {FILE_FIELDS} from 'ui/utils/common/users';

const {
  merge, computed, get, set, inject
} = Ember;

export default ApimasAuthenticator.extend({
  processProfileData(data, profile) {
    let user = profile.user;
    user.user_id = user.id.toString();
    delete user.id;
    delete profile.user;
    if (profile.departments && profile.departments.length) {
      profile.departments.forEach((dep, i) => {
        profile.departments[i] = dep.split('/').slice(-2)[0];
      });
    }
    merge(data, user);
    merge(data, profile);
    for (let key of FILE_FIELDS) {
      delete data[key];
    }
    if(data.id) {
      data.id = data.id.toString();
    }

    // process unverified users as no-role users
    if (data.hasOwnProperty('is_verified') && data.is_verified === false) {
      data.pending_role = data.role;
      data.role = 'unverified-user';
    }
    if (data.login_method === 'academic') {
      data.username = data.email;
    }
    return data;
  }
})
