import Ember from 'ember';
import Token from 'ember-simple-auth-token/authenticators/token';
import ENV from 'ui/config/environment';

const {
  merge
} = Ember;

export default Token.extend({
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
