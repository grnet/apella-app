import Ember from 'ember';
import fetch from "ember-network/fetch";
import ENV from 'ui/config/environment';

const {
  computed,
  get, set,
  inject,
  computed: { reads }
} = Ember;

const VerificationModel = Ember.Object.extend({
  save() {
    let email = get(this, 'email');
    let url = ENV.APP.backend_host + '/auth/register/';
    return fetch(url, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
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
  session: inject.service('session'),
  isAuthenticated: reads('session.isAuthenticated'),
  verificationModel: computed(function() {
    let model = get(this, 'model');
    let init = {};
    if (model && get(model, 'email')) {
      init = {email: get(model, 'email')};
    };
    return VerificationModel.create(init);
  })
})
