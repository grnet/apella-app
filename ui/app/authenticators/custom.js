import Token from 'ember-simple-auth-token/authenticators/token';
import ENV from 'ui/config/environment';


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
      response['role'] = res.user.role || '';
      return response;
    });
  },

})
