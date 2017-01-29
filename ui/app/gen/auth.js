import gen from 'ember-gen/lib/gen';
import routes from 'ember-gen/lib/routes';
import {field} from 'ember-gen';
import AuthGen from 'ember-gen/lib/auth';
import {USER_FIELDSET, USER_FIELDSET_EDIT, USER_FIELDSET_EDIT_ACADEMIC,
        USER_VALIDATORS, PROFESSOR_FIELDSET, PROFESSOR_VALIDATORS,
        PROFESSOR_FILES_FIELDSET, CANDIDATE_FILES_FIELDSET, USER_FIELDSET_DETAILS
       } from 'ui/utils/common/users';
import MANAGER from 'ui/utils/common/manager';
import ASSISTANT from 'ui/utils/common/assistant';
import {disable_field} from 'ui/utils/common/fields';
import ENV from 'ui/config/environment';
import {Register, RegisterIntro, resetHash} from 'ui/lib/register';
import fetch from "ember-network/fetch";

const {
  computed: { reads, not, equal },
  get, set, computed,
  merge
} = Ember;


// user can apply for position
function isVerifiable(role) {
  return role === 'candidate' || role === 'professor' || role === 'institutionmanager';
}

function extractError(loc) {
  return loc.hash && loc.hash.split("error=")[1];
}

function extractActivate(loc) {
  return loc.hash && loc.hash.split("activate=")[1];
}

function extractReset(loc) {
  return loc.hash && loc.hash.split("reset=")[1];
}

function extractToken(loc) {
  let token = loc.hash && loc.hash.split("token=")[1];
  if (token) { resetHash(window) };
  return token;
}


let fields_with_user_id = Ember.copy(USER_FIELDSET_DETAILS.fields);
let fields_with_id = Ember.copy(USER_FIELDSET_DETAILS.fields);
fields_with_user_id.unshiftObject(field('user_id', {disabled: true}));
fields_with_id.unshiftObject(field('id', {disabled: true}));

const USER_FIELDSET_USER_ID = {
  label: USER_FIELDSET_DETAILS.label,
  fields: fields_with_user_id,
  layout: {
    flex: [50, 50, 50, 50, 50, 50, 25, 25]
  }
}

const USER_FIELDSET_ID = {
  label: USER_FIELDSET_DETAILS.label,
  fields: fields_with_id,
  layout: {
    flex: [50, 50, 50, 50, 50, 50, 25, 25]
  }
}


const PROFILE_FIELDSETS = function(view) {
  return computed('model.role', function(){
    let f = [];
    let role = this.get('model').get('role');
    let is_academic = get(this, 'model.login_method') === 'academic';
    let _USER_FIELDSET;

    if (view === 'details') {
      _USER_FIELDSET = USER_FIELDSET_USER_ID
    }

    if (view === 'edit') {
      _USER_FIELDSET = USER_FIELDSET_EDIT;
      if (is_academic) {
        _USER_FIELDSET = USER_FIELDSET_EDIT_ACADEMIC;
      }
    }

    if (role === 'assistant') {
      if (view === 'edit') {
        f.push(ASSISTANT.FIELDSET)
      }
      if (view === 'details') {
        f.push(ASSISTANT.FIELDSET_DETAILS)
      }
    }

    if (role == 'helpdeskadmin') {
      f.push(USER_FIELDSET_ID);
    }
    if (role == 'helpdeskuser') {
      f.push(USER_FIELDSET_ID);
    }

    if (role === 'professor') {
      f.push(_USER_FIELDSET);
      f.push(PROFESSOR_FIELDSET);
      f.push(PROFESSOR_FILES_FIELDSET);
    }

    if (role === 'candidate') {
      f.push(_USER_FIELDSET);
      f.push(CANDIDATE_FILES_FIELDSET);
    }

    if (role === 'institutionmanager') {
      f.push(_USER_FIELDSET);
      f.push(MANAGER.FIELDSET);
      if (view === 'edit') {
        f.push(MANAGER.SUB_FIELDSET);
      }
      if (view === 'details') {
        f.push(MANAGER.SUB_FIELDSET_DETAILS);
      }

    }
    return f;
  });
};

// GENS
//
const ProfileDetailsView = gen.GenRoutedObject.extend({
  partials: { bottom: 'profile-details-actions' },
  routeBaseClass: routes.DetailsRoute,
  fieldsets: PROFILE_FIELDSETS('details'),
  component: 'gen-details',
  actions: ['change_password'],
  actionsMap: {
    'sync_candidacies': {
      label: 'sync.candidacies',
      raised: true,
      action: function(route, profile) {
        let messages = get(route, 'messageService');
        let [url, adapter] = [profile.roleURL(), profile.userAdapter()];
        adapter.ajax(url + 'sync_candidacies/', 'POST').then(() => {
          messages.setSuccess('sync.candidacies.success');
        }).catch(() => {
          messages.setError('sync.candidacies.error');
        });
      },
      primary: true,
      hidden: computed('model.is_verified', 'model.role', function() {
        let verified = get(this, 'model.is_verified');
        let role = get(this, 'model.role');
        if (isVerifiable(role)) { return !verified; }
        return true;
      }),
      confirm: true,
      prompt: {
        title: 'sync_candidacies',
        message: 'sync_candidacies.confirm',
        ok: 'ok',
        cancel: 'cancel'
      }
    },
    'change_password': {
      raised: false,
      label: 'password.change',
      confirm: true,
      action: function() {},
      hidden: computed('model.login_method', function() {
        return get(this, 'model.login_method') !== 'password';
      }),
      prompt: {
        title: 'password.change',
        contentComponent: 'change-password',
        noControls: true
      }
    }
  },
  getModel() {
    return get(this, 'store').findRecord('profile', 'me');
  }
});

const PositionInterest = gen.GenRoutedObject.extend({
  modelName: 'user-interest',
  path: 'my-interests',
  getModel() {
    let user_id = get(this, 'session.session.authenticated.user_id');
    return this.store.queryRecord('user-interest', {user:user_id });
  },
  templateName: 'user-interests',
  routeBaseClass: routes.EditRoute,
  session: Ember.inject.service(),
  role: reads('session.session.authenticated.role'),

  menu: {
    order: 150,
    display: computed('role', function(){
      let role = get(this, 'role');
      let allowedRoles = ['professor', 'candidate'];
      return (allowedRoles.includes(role) ? true : false);
    }),
    icon: 'notifications',
    label: 'userInterest.menu_label'
  },
  page: {
    title: 'userInterest.menu_label',
    breadcrumb: { display: true }
  }
});

export default AuthGen.extend({
  order: 100,
  routeMixins: [{
      actions: {
        shibbolethLogin() {
          window.location = ENV.APP.shibboleth_login_url + '?login=1'
        },
        shibbolethRegister() {
          window.location = ENV.APP.shibboleth_login_url + '?register=1'
        }
      }
  }],

  gens: {
    register: Register,
    'register-intro': RegisterIntro
  },

  login: {
    extraActions: [
      {
        label: 'password.forgot',
        confirm: true,
        action: function() {},
        prompt: {
          title: 'password.forgot',
          contentComponent: 'forgot-password',
          noControls: true
        }
      }
    ],
    config: {
      authenticator: 'apimas'
    },
    templateName: 'apella-login',
    routeMixins: [{
      handleActivate(activate) {
        let [uid, token] = activate.split("|");
        if (uid && token) {
          let url = ENV.APP.backend_host + '/auth/activate/';
          let data = {uid, token};
          return fetch(url, {
            method: 'POST',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
          }).then((resp) => {
            let err, msg;
            if (resp.status === 204) {
              msg = 'user.email_verification.success';
            } else {
              err = 'user.email_verification.error';
              resp.json().then((json) => {
                if (!json.detail) { return; }
                this.get('messageService').setError(json.detail);
              });
              resetHash(window, "error=user.email_verification.error");
            }
            if (msg) { this.get('messageService').setSuccess(msg); }
            if (err) { this.get('messageService').setError(err); }
          });
        }
      },

      handleTokenLogin(token) {
        if (get(this, 'session.isAutneticated')) {
          resetHash();
          return;
        }
        let url = ENV.APP.backend_host + '/auth/me/';
        return fetch(url, {
          headers: { 
            'Accept': 'application/json',
            'Authorization': `Token ${token}`
          }
        }).then((resp) => {
          if (resp.status !== 200) {
            return resp.json().then((json) => {
              this.get('messageService').setError('login.failed');
            });
          }
          return resp.json().then((user) => {
            let session = get(this, 'session');
            user.auth_token = token;
            resetHash(window);
            this.get('messageService').setSuccess('login.success');
            return session.authenticate('authenticator:apimas', user);
          });
        })
      },

      beforeModel(transition) {
        let activate = extractActivate(window.location);
        if (activate) {
          return this.handleActivate(decodeURI(activate)).finally(() => {
            return this.transitionTo('index');
          });
        }
        let token = extractToken(window.location);
        if (token) {
          return this.handleTokenLogin(decodeURI(token));
        }
        return this._super(transition);
      },

      setupController(controller, model) {
        this._super(controller, model);
        let error = extractError(window.location);
        error = decodeURI(error);

        if (error === "user.not.found") {
          controller.set('userNotFound', true);
        }
        if (error === "user.exists") {
          controller.set('userExists', true);
        }
        if (error === "migration.error") {
          controller.set('migrationError', true);
        }
        if (error === "user.not.email_verified") {
          controller.set('userNotEmailVerified', true);
        }
        if (error === "user.not.verified") {
          controller.set('userNotVerified', true);
        }
        if (error === "user.email_verification.error") {
          controller.set('userEmailVerificationFailed', true);
        }
        if (error === "user.not.active") {
          controller.set('userNotActive', true);
        }
        if (error === "no.affiliation") {
          controller.set('noAffiliation', true);
        }
        let reset = extractReset(window.location);
        if (reset) { controller.set('resetToken', decodeURI(reset)); }

        resetHash(window);
      },
      resetController(controller) {
        controller.set('userNotFound', false);
        controller.set('userExists', false);
        controller.set('migrationError', false);
        controller.set('userNotVerified', false);
        controller.set('userVerificationFailed', false);
        controller.set('userNotActive', false);
      }
    }]
  },

  profile: {
    page: {
       title: 'profile.menu_label',
    },
    gens: {
      position_interest: PositionInterest,
      details: ProfileDetailsView
    },
    modelName: 'profile',
    menu: {
      display: true,
      icon: 'portrait',
      label: 'profile.menu_label',
    },
    onSubmit: function() {},
    components: { beforeForm: 'profile-form-intro' },

    validators: computed('model.role', function(){
      let role = this.get('model').get('role');
      let f = Object.assign({}, USER_VALIDATORS);
      if (role === 'professor') {
        f = Object.assign(f, PROFESSOR_VALIDATORS);
      }
      if (role === 'institutionmanager') {
        f = Object.assign(f, MANAGER.VALIDATORS);
      }
      return f;
    }),
    fieldsets: PROFILE_FIELDSETS('edit'),

    extraActions: computed('model.role', 'model.is_verified', 'model.verification_pending', function() {
      let isVerified = get(this, 'user.is_verified');
      let verificationPending = get(this, 'user.verification_pending');
      let role = get(this, 'model.role');

      if (!isVerifiable(role)) { return []; }

      if (!isVerified) {
        return [{
          label: 'request.profile.verification',
          icon: 'check_circle',
          primary: true,
          action: function(route, form) {
            let model = get(form, 'model');
            let messages = get(route, 'messageService');
            let url = model.roleURL();
            let token = get(this, 'user.auth_token');
            form.submit().then((model_or_err) => {
              if (model_or_err && !get(form, 'changeset.isValid') || model_or_err.isAdapterError) {
                return;
              }
              return fetch(url + 'request_verification/', {
                method: 'POST',
                headers: {
                  'Accept': 'application/json',
                  'Authorization': `Token ${token}`
                },
              }).then((resp) => {
                if (resp.status === 200) {
                  model.reload();
                  messages.setSuccess('request.verification.success');
                  route.transitionTo('auth.profile.details');
                } else {
                  throw new Error(res);
                }
              }).catch((err) => {
                messages.setError('request.verification.error');
              });
            });
          },
          confirm: true,
          prompt: {
            title: 'request.profile.verification',
            message: 'request.profile.verification.message',
            ok: 'submit',
            cancel: 'cancel'
          }
        }]
      }
      return [];
    }),

    getModel() {
      return get(this, 'store').findRecord('profile', 'me').then((user) => {
        let isVerified = get(user, 'is_verified');
        let role = get(user, 'role');
        let verificationPending = get(user, 'verification_pending');
        if (isVerifiable(role) && (verificationPending || isVerified)) {
          this.transitionTo('auth.profile.details');
        }
        return user;
      });
    }
  }
})
