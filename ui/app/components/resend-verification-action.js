import Ember from 'ember';
import fetch from "ember-network/fetch";
import ENV from 'ui/config/environment';

const {
  computed,
  get, set
} = Ember;

const VerificationModel = Ember.Object.extend({
  save() {
    let email = get(this, 'email');
    let url = ENV.APP.backend_host + '/auth/register/';
    return fetch(url, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({resend_verification: email})
    }).then((resp) => {
      set(this, 'email', undefined);
      if (200 < resp.status && 300 > resp.status) {
        return this;
      }
      return resp.json().then((json) => {
        let err = new Error(resp.statusText)
        err.detail = json.detail;
        throw err;
      })
    })
  }
});

export default Ember.Component.extend({
  tagName: '',
  model: computed(function() {
    return VerificationModel.create()
  })
})
