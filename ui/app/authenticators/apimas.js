import Ember from 'ember';
import Token from 'ember-simple-auth-token/authenticators/token';
import ENV from 'ui/config/environment';
import {FILE_FIELDS} from 'ui/utils/common/users';

const {
  merge, computed, get, set, inject
} = Ember;

function mergeProfileData(sessionData, profileResponse) {
  let user = profileResponse.user;
  user.user_id = user.id;
  delete user.id;
  delete profileResponse.user;
  if (profileResponse.departments && profileResponse.departments.length) { 
    profileResponse.departments.forEach((dep, i) => {
      profileResponse.departments[i] = dep.split('/').slice(-2)[0];
    });
  }
  merge(sessionData, user);
  merge(sessionData, profileResponse);
  for (let key of FILE_FIELDS) {
    delete sessionData[key];
  }

  // process unverified users as no-role users
  if (sessionData.hasOwnProperty('is_verified') && sessionData.is_verified === false) {
    sessionData.pending_role = sessionData.role;
    delete sessionData.role;
  }
  if (sessionData.login_method === 'academic') {
    sessionData.username = sessionData.email;
  }
  return sessionData;
}

export default Token.extend({

  init() {
    this._super();
    this.serverTokenEndpoint = ENV.APP.backend_host + '/auth/login/';
  },

  gen: inject.service(),

  getUserProfile(token) {
    return $.ajax({
      url: `${ENV.APP.backend_host}/auth/me/`,
      method: 'GET',
      contentType: 'application/json',
      headers: {
        'Authorization': `Token ${token}`,
        'Accept': 'application/json'
      },
    }).then((user) => {
      if (user && user.user && user.user.can_set_academic) {
        let gen = get(this, 'gen');
        gen.get('gens').forEach((gen) => {
          let name = get(gen, 'routeName');
          if (!name.startsWith('auth')) {
            set(gen, 'hasPermission', false);
            set(gen, 'menuDisplay', false);
          }
        });
      }
      return user;
    });
  },

  restore(data) {
    return this.getUserProfile(data.auth_token).then(mergeProfileData.bind(this, data));
  },

  authenticate(credentials, headers) {
    // handle direct token authentication
    if (credentials && credentials.auth_token && credentials.user) {
      return new Ember.RSVP.Promise((resolve, reject) => {
        let data = {
          auth_token: credentials.auth_token,
          user_id: credentials.user.id
        };
        merge(data, credentials.user);
        mergeProfileData(data, credentials);
        resolve(data);
      });
    }
    return this._super(credentials, headers);
  },

  getResponseData(response) {
    return this.getUserProfile(response.auth_token).then(mergeProfileData.bind(this, response));
  },

})
