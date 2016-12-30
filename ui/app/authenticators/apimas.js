import Ember from 'ember';
import Token from 'ember-simple-auth-token/authenticators/token';
import ENV from 'ui/config/environment';

const {
  merge, computed
} = Ember;

function mergeProfileData(sessionData, profileResponse) {
  let user = profileResponse.user;
  user.user_id = user.id;
  delete user.id;
  delete profileResponse.user;
  merge(sessionData, user);
  merge(sessionData, profileResponse);

  // process unverified users as no-role users
  if (sessionData.hasOwnProperty('is_verified') && sessionData.is_verified === false) {
    sessionData.pending_role = sessionData.role;
    delete sessionData.role;
  }
  return sessionData;
}

export default Token.extend({
  init() {
    this._super();
    this.serverTokenEndpoint = ENV.APP.backend_host + '/auth/login/';
  },

  getUserProfile(token) {
    return $.ajax({
      url: `${ENV.APP.backend_host}/auth/me/`,
      method: 'GET',
      contentType: 'application/json',
      headers: {
        'Authorization': `Token ${token}`
      },
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
        resolve(data);
      });
    }
    return this._super(credentials, headers);
  },

  getResponseData(response) {
    return this.getUserProfile(response.auth_token).then(mergeProfileData.bind(this, response));
  },

})
