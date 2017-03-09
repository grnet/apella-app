import Ember from 'ember';
import DS from 'ember-data';
import USER from 'ui/utils/common/users';
import MANAGER from 'ui/utils/common/manager';
import gen from 'ember-gen/lib/gen';
import {field} from 'ember-gen';
import ENV from 'ui/config/environment';
import routes from 'ember-gen/lib/routes';

const TEST_REGISTER_DATA = {};

const User = Ember.Object.extend({
  save() {
    let url = ENV.APP.backend_host + '/auth/register/';
    let model = this;

    let fields = get(this, 'gen.resource.fields').getEach('key');
    let data = {user: {}};
    fields.push('registration_token');
    fields.forEach((key) => {
      if (key === 'cv') { return; }
      let value = get(model, key);
      if (value !== undefined) {
        if (value instanceof DS.Model) {
          value = value.store.adapterFor(value.constructor.name).urlForModel(value);
        }
        if (USER.FIELDS_ALL.includes(key)) {
          data.user[key] = value;
        } else {
          data[key] = value;
        }
      }
    });
    data['user_role'] = get(model, 'userRole');
    if (data['user_role'] === 'manager') {
      data['user_role'] = 'institutionmanager';
    }

    if (get(model, 'is_foreign') ) {
      data['is_foreign'] = true;
    }

    set(model, 'errors', []);
    let promise = new Ember.RSVP.Promise(function(resolve, reject) {
      Ember.$.ajax({
        method: 'POST',
        url,
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: 'application/json'
      }).then(function(resp) {
        model.setProperties(resp);
        //TODO resolve verification pending from backend
        model.set('emailVerificationPending', true);
        resolve(model);
      }).catch(function(err) {
        if (err && err.status === 400 && err.responseJSON) {
          let errors = Object.keys(err.responseJSON).map((key) => {
            return {attribute: key, message: err.responseJSON[key]};
          });
          if (err.responseJSON.user) {
            Object.keys(err.responseJSON.user).forEach((key) => {
              errors.push({attribute: key, message: err.responseJSON.user[key]});
            })
          }
          set(model, 'errors', errors);
        }
        console.error(err);
        reject(err);
      });
    });
    return promise;
  }
});

const {
  computed: { reads, not },
  get, set, computed,
  merge
} = Ember;

// UTILS

function extractToken(loc) {
  return loc.hash && loc.hash.split("token=")[1];
}

function resetHash(win, replace='') {
  if (win.history.replaceState) {
    win.history.replaceState(null, null, '#' + replace);
  } else {
    win.location.hash = replace;
  }
}

const RegisterSuccess = gen.GenRoutedObject.extend({
  auth: false,
  getModel() {
    let model;
    // we expect register view to have already set the controller model
    // an exception is raised if controllerFor is unable to resolve the controller (route is not yet visited)
    try {
      model = this.controllerFor('auth.register.index').get('registeredModel');
    } catch(err) { console.error(err); model = null; }
    if (!model) { this.transitionTo('auth.login.index'); }
    return model;
  },
  templateName: 'apella-register-success'
});

const RegisterIntro = gen.GenRoutedObject.extend({
  auth: false,
  templateName: 'apella-register-intro',
  menu: {
    display: true,
    label: 'register'
  },
  page: {
    title: 'register',
    breadcrumb: { display: true },
  }
});

const Register = gen.GenRoutedObject.extend({
  auth: false,
  gens: { success: RegisterSuccess},
  modelName: 'profile',
  args: [':userRole'],
  routeBaseClass: routes.CreateRoute.extend({
    queryParams: {
      initial: { refreshModel: false },
      remote_data: { refreshModel: false },
      academic: { refreshModel: false },
      warn_legacy: { refreshModel: false },
    },
    resetController(controller) {
      set(controller, 'model.registration_token', null);
      set(controller, 'initial', false);
      set(controller, 'remote_data', false);
      set(controller, 'academic', false);
    }
  }),
  component: 'gen-form',
  components: { beforeForm: 'register-form-intro' },
  getModel(params) {
    let token = extractToken(window.location);
    if (token) { resetHash(window); };
    if (params.academic && !token) {
      this.transitionTo('auth.register-intro');
    }

    // extract default values from `initial` params
    let defaults = {
      discipline_in_fek: true,
      authority: 'dean',
    };

    let userRole = this.paramsFor('auth.register').userRole;

    if (userRole == 'foreign-professor') {
      defaults['is_foreign'] = true
    }

    if (!['professor', 'manager', 'candidate'].includes(userRole)) {
      userRole = 'professor';
    }
    set(this, 'gen.modelName', userRole);

    try {
      merge(defaults, JSON.parse(atob(params.initial)));
    } catch(err) {}

    merge(defaults, TEST_REGISTER_DATA);
    let remote_data = params.remote_data && JSON.parse(atob(params.remote_data));
    let gen = get(this, 'gen');
    let model = User.create(defaults, {userRole, gen});
    set(model, 'registration_token', (token && token.length) ? token : null);
    set(model, 'is_academic', !!token);
    set(model, 'warn_legacy', params.warn_legacy);
    set(model, 'remote_data', remote_data);
    set(model, 'userRole', userRole);
    return Ember.RSVP.Promise.resolve(model);
  },

  onSubmit(model) {
    this.controllerFor('auth.register.index').set('registeredModel', model);
    if (get(model, 'user.is_active')) {
      if (get(model, 'user.login_method') === 'academic') {
        this.send('shibbolethLogin');
      } else {
        this.transitionTo('auth.login.index');
      }
    } else {
      this.transitionTo('auth.register.success.index');
    }
    return false;
  },

  messages: {
    success: 'user.created'
  },

  fieldsets: computed('model', function() {
    let model = get(this, 'model');
    let type = get(this, 'model.userRole');

    // resolve fieldsets
    let FIELDSETS = [];
    if (type === 'professor') {
      if (get(model, 'is_academic')) {
        FIELDSETS.push(USER.FIELDSET_REGISTER_ACADEMIC);
      } else {
        FIELDSETS.push(USER.FIELDSET_CREATE);
      }
    }
    if (type === 'candidate') {
        FIELDSETS.push(USER.FIELDSET_CREATE);
    }
    if (type === 'manager') {
        FIELDSETS.push(USER.FIELDSET_CREATE);
        FIELDSETS.push(MANAGER.FIELDSET_REGISTER);
        FIELDSETS.push(MANAGER.SUB_FIELDSET_REGISTER);
    }
    return FIELDSETS;
  }),
  validators: computed('model.is_academic', function(){
    let res = USER.VALIDATORS;
    if(get(this, 'model.is_academic')) {
      res['username'] = []
    }
    return res;
  }),
  menu: {
    display: false,
  },
  page: {
    breadcrumb: { display: true },
    title: computed('model.registration_token', 'model.userRole', function() {
      let token = get(this, 'model.registration_token');
      let type = get(this, 'model.userRole');
      if (token) { return 'register.domestic.title'; }
      if (type === 'manager') { return 'register.manager.title'; }
      if (type === 'candidate') { return 'register.candidate.title'; }
      if (type === 'professor') { return 'register.foreign.title'; }
      return 'register.title';
    })
  }
});


export {Register, RegisterIntro, resetHash};
