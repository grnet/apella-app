import Ember from 'ember';
import fetch from "ember-network/fetch";
import ENV from 'ui/config/environment';

const {
  computed,
  get, set, inject, getOwner
} = Ember;

const PasswordModel = Ember.Object.extend({
  session: inject.service('session'),
  save() {
    let {new_password, re_new_password, current_password} = this.getProperties('new_password', 're_new_password', 'current_password');

    let url = ENV.APP.backend_host + '/auth/password/';
    let token = get(this, 'session.session.authenticated.auth_token');
    set(this, 'errors', []);

    return fetch(url, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': `Token ${token}`
      },
      body: JSON.stringify({new_password, re_new_password, current_password})
    }).then((resp) => {
      if (200 <= resp.status && 300 > resp.status) {
        this.setProperties({new_password: '', re_new_password: '', current_password: ''});
        return this;
      }
      return resp.json().then((json) => {
        if (!json.detail) {
          let errors = [];
          Object.keys(json).forEach((key) => {
            errors.push({attribute: key, message: json[key]});
          })
          set(this, 'errors', errors);
          throw json;
        } else {
          let err = new Error(resp.statusText)
          err.detail = json.detail;
          throw err;
        }
      })
    })
  }
});

export default Ember.Component.extend({
  tagName: '',

  model: computed(function() {
    return PasswordModel.create({container: getOwner(this)})
  }),

  modelMeta: {
    fields: [
      ['current_password', {type: 'string', formAttrs: { type: 'password' }}],
      ['new_password', {type: 'string', formAttrs: { type: 'password' }}],
      ['re_new_password', {type: 'string', formAttrs: { type: 'password' }}]
    ]
  },

  cancel() {},

  actions: {
    onSubmit() { this.cancel(); } // close overlay
  }
})

