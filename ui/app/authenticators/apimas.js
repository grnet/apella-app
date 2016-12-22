import Ember from 'ember';
import Token from 'ember-simple-auth-token/authenticators/token';
import ENV from 'ui/config/environment';

const {
  merge, computed
} = Ember;

export default Token.extend({
  init() {
    this._super();
    this.serverTokenEndpoint = ENV.APP.backend_host + '/auth/login/';
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
    let token = response.auth_token;

    return $.ajax({
      url: `${ENV.APP.backend_host}/auth/me/`,
      method: 'GET',
      contentType: 'application/json',
      headers: {
        'Authorization': `Token ${token}`
      },
    }).then(function(res){
      let user = res.user;
      user.user_id = user.id;
      delete user.id;
      delete res.user;
      merge(response, user);
      merge(response, res);
      return response;
    });
  },

})
