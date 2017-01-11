import gen from 'ember-gen/lib/gen';
import routes from 'ember-gen/lib/routes';
import {field} from 'ember-gen';
import AuthGen from 'ember-gen/lib/auth';
import {USER_FIELDSET, USER_FIELDSET_EDIT, USER_VALIDATORS,
        PROFESSOR_FIELDSET, PROFESSOR_VALIDATORS, PROFESSOR_FILES_FIELDSET,
        INST_MANAGER_FIELDSET_MAIN, INST_MANAGER_FIELDSET_SUB,
        INSTITUTION_MANAGER_VALIDATORS, CANDIDATE_FILES_FIELDSET,
        USER_FIELDSET_DETAILS
       } from 'ui/utils/common/users';
import {disable_field} from 'ui/utils/common/fields';
import ENV from 'ui/config/environment';
import {Register, RegisterIntro, resetHash} from 'ui/lib/register';
import fetch from "ember-network/fetch";

const {
  computed: { reads, not, equal },
  get, set, computed,
  merge
} = Ember;

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

const PROFILE_ASSISTANT_FIELDSET = {
  label: 'fieldsets.labels.user_info',
  text: 'fieldsets.text.assistant_profile',
  fields: [
    field('username', { readonly: true }),
    'email',
    'mobile_phone_number',
    'home_phone_number',
    disable_field('first_name'),
    disable_field('last_name'),
    disable_field('father_name'),
    disable_field('id_passport'),
    disable_field('institution'),
    disable_field('can_create_positions_verbose'),
    disable_field('can_create_registries_verbose'),
  ],
  layout: {
        flex: [100, 50, 50, 50, 50, 50, 50, 50, 50, 50, 25, 25]
  }
}

const PROFILE_FIELDSETS = function(view) { 
  return computed('model.role', function(){
    let f = [];
    let role = this.get('model').get('role');
    if (role === 'assistant') {
      f.push(PROFILE_ASSISTANT_FIELDSET)
      return f;
    }
    f.push(USER_FIELDSET_DETAILS);

    if (role === 'professor') {
      f.push(PROFESSOR_FIELDSET);
      f.push(PROFESSOR_FILES_FIELDSET);
    }
    if (role === 'candidate') {
      f.push(CANDIDATE_FILES_FIELDSET);
    }
    if (role === 'institutionmanager') {
      f.push(INST_MANAGER_FIELDSET_MAIN, INST_MANAGER_FIELDSET_SUB);
    }
    return f;
  });
};

// GENS
//
const ProfileDetailsView = gen.GenRoutedObject.extend({
  routeBaseClass: routes.DetailsRoute,
  fieldsets: PROFILE_FIELDSETS('details'),
  component: 'gen-details',
  actions: ['change_password'],
  actionsMap: {
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
    display: computed('role', function(){
      let role = get(this, 'role');
      let allowedRoles = ['professor', 'candidate'];
      return (allowedRoles.includes(role) ? true : false);
    }),
    icon: 'access_alarm',
    label: 'userInterest.menu_label'
  },
  page: {
    title: 'userInterest.menu_label',
    breadcrumb: { display: true }
  }
});

export default AuthGen.extend({
  order: 1,
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
            headers: {'Content-Type': 'application/json'},
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
          headers: { 'Authorization': `Token ${token}` }
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
            return session.authenticate('authenticator:apimas', user);
          });
        })
      },

      beforeModel(transition) {
        let activate = extractActivate(window.location);
        if (activate) {
          return this.handleActivate(activate);
        }
        let token = extractToken(window.location);
        if (token) {
          return this.handleTokenLogin(token);
        }
        return this._super(transition);
      },

      setupController(controller, model) {
        this._super(controller, model);
        let error = extractError(window.location);
        if (error === "user.not.found") {
          controller.set('userNotFound', true);
        }
        if (error === "user.exists") {
          controller.set('userExists', true);
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
        let reset = extractReset(window.location);
        if (reset) { controller.set('resetToken', reset); }

        resetHash(window);
      },
      resetController(controller) {
        controller.set('userNotFound', false);
        controller.set('userExists', false);
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
      label: 'profile.menu_label',
    },
    onSubmit: function() {},

    validators: computed('model.role', function(){
      let role = this.get('model').get('role');
      let f = Object.assign({}, USER_VALIDATORS);
      if (role === 'professor') {
        f = Object.assign(f, PROFESSOR_VALIDATORS);
      }
      if (role === 'institutionmanager') {
        f = Object.assign(f, INSTITUTION_MANAGER_VALIDATORS);
      }
      return f;
    }),
    fieldsets: PROFILE_FIELDSETS('edit'),

    extraActions: computed('model.is_verified', 'model.verification_pending', function() {
      let isVerified = get(this, 'user.is_verified');
      let verificationPending = get(this, 'user.verification_pending');
      if (!isVerified) {
        return [{
          label: 'request.profile.verification',
          icon: 'check_circle',
          primary: true,
          action: function(route, form) {
            let model = get(form, 'model');
            set(model, 'verification_request', new Date());
            form.submit().then((model_or_err) => {
              set(model, 'verification_request', null);
              if (model_or_err && get(form, 'changeset.isValid') && !model_or_err.isAdapterError) {
                route.get('messageService').setSuccess('verification.request.submitted');
                route.transitionTo('auth.profile.details');
              }
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
        let verificationPending = get(user, 'verification_pending');
        if (verificationPending || isVerified) {
          this.transitionTo('auth.profile.details');
        }
        return user;
      });
    }
  }
})
