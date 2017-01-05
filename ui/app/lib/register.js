import Ember from 'ember';
import DS from 'ember-data';
import {
  USER_FIELDS_ALL,
  USER_FIELDSET_REGISTER,
  USER_FIELDSET_REGISTER_ACADEMIC,
  PROFESSOR_FIELDSET_REGISTER
} from 'ui/utils/common/users';
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
        if (USER_FIELDS_ALL.includes(key)) {
          data.user[key] = value;
        } else {
          data[key] = value;
        }
      }
    });
    data['user_role'] = get(model, 'userRole');

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
      academic: { refreshModel: false }
    },
    resetController(controller) {
      set(controller, 'model.registration_token', null);
      set(controller, 'initial', false);
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

    let userRole = this.paramsFor('auth.register').userRole;
    if (!['professor', 'manager', 'candidate'].includes(userRole)) {
      userRole = 'professor';
    }
    set(this, 'gen.modelName', userRole);

    // extract default values from `initial` params
    let defaults = {
      discipline_in_fek: true
    };
    try {
      merge(defaults, JSON.parse(atob(params.initial)));
    } catch(err) {}

    merge(defaults, TEST_REGISTER_DATA);
    let gen = get(this, 'gen');
    let model = User.create(defaults, {userRole, gen});
    set(model, 'registration_token', (token && token.length) ? token : null);
    set(model, 'is_academic', !!token);
    return Ember.RSVP.Promise.resolve(model);
  },

  onSubmit(model) {
    this.controllerFor('auth.register.index').set('registeredModel', model);
    this.transitionTo('auth.register.success.index');
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
        FIELDSETS.push(USER_FIELDSET_REGISTER_ACADEMIC);
      } else {
        FIELDSETS.push(USER_FIELDSET_REGISTER);
      }
      FIELDSETS.push(PROFESSOR_FIELDSET_REGISTER);
    }
    if (type === 'candidate') {
        FIELDSETS.push(USER_FIELDSET_REGISTER);
    }
    if (type === 'manager') {
        FIELDSETS.push(USER_FIELDSET_REGISTER);
    }
    return FIELDSETS;
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
