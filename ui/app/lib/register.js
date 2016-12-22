import Ember from 'ember';
import DS from 'ember-data';
import {USER_FIELDS_ALL} from 'ui/utils/common/users';
import gen from 'ember-gen/lib/gen';
import {field} from 'ember-gen';
import ENV from 'ui/config/environment';
import routes from 'ember-gen/lib/routes';

const TEST_REGISTER_DATA = {
  first_name: {el: 'Κώστας', en: 'Costas'},
  last_name: {el: 'Παπαδημητρίου', en: 'Papadimitriou'},
  father_name: {el: 'Γεώργιος', en: 'George'},
  id_passport: '123456789',
  email: 'kpap@grnet.gr',
  mobile_phone_number: '6941111111',
  home_phone_number: '2101111111',
  rank: 'Professor',
  institution: 1,
  department: 1,
  cv_url: 'http://www.cvs.gr/cv-56772',
  fek: 'http://www.fek.gr/fek-145'
};

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

const requiredStringField = function(name, params) {
  params = params || {};
  let isI18n = params && params.formComponent && params.formComponent.startsWith('i18n');
  return field(name, 'string', merge({
    required: true,
    readonly: params.readonly || computed(`model._content.${name}`, function() {
      return !isI18n && get(this, `model._content.${name}`);
    }),
    disabled: reads('readonly')
  }, params));
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

const Register = gen.GenRoutedObject.extend({
  auth: false,
  gens: { success: RegisterSuccess },
  modelName: 'profile',
  args: [':userRole'],
  routeBaseClass: routes.CreateRoute.extend({
    queryParams: {
      initial: { refreshModel: false }
    },
    setupController(controller, model) {
      this._super(...arguments);
      let token = extractToken(window.location);
      if (token) { resetHash(window); };
      set(model, 'registration_token', (token && token.length) ? token : null);
    },
    resetController(controller) {
      set(controller, 'model.registration_token', null);
      set(controller, 'initial', false);
    }
  }),
  component: 'gen-form',
  components: { beforeForm: 'my-intro-component' },
  getModel(params) {
    let userRole = this.paramsFor('auth.register').userRole;
    if (!['professor', 'manager', 'candidate'].includes(userRole)) {
      userRole = 'professor';
    }

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

    let inst = this.store.query('institution', {});
    let dept = this.store.query('department', {});
    return Ember.RSVP.hash({inst, dept}).then((resp) => {
      model.setProperties({
        institution: resp.inst.objectAt(0),
        department: resp.dept.objectAt(0)
      });
      return model;
    });
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

    let f = requiredStringField
    let FS_LOGIN = {
      label: 'register.login.fields',
      fields: [
        f('username'),
        f('password', {formAttrs: { type: 'password'}}),
        f('password2', {formAttrs: { type: 'password'}})
      ],
      layout: {
        flex: [33, 33, 33]
      }
    };

    let FS_ACCOUNT = {
      label: 'register.account.fields',
      fields: [
        f('first_name', {formComponent: 'i18n-input-field'}),
        f('last_name', {formComponent: 'i18n-input-field'}),
        f('father_name', {formComponent: 'i18n-input-field'}),
        f('id_passport'),
        f('email'),
        f('mobile_phone_number'),
        f('home_phone_number')
      ],
      layout: {
        flex: [30, 40, 30, 50, 50, 50, 50]
      }
    };

    let FS_PROFESSOR = {
      fields: [
        f('rank'),
        f('institution', {type: 'model', modelName: 'institution', formAttrs: {}}),
        f('department', {type: 'model', modelName: 'department', formComponent: 'gen-form-field-select', formAttrs: {}}),
        f('cv_url', {
          required: not('model.changeset.cv_url_check'),
          disabled: computed('model.changeset.cv_url_check', function() {
            let check = get(this, 'model.changeset.cv_url_check');
            if (check) { set(this, 'model.changeset.cv_url', ''); };
            return check;
          })
        }),
        f('cv_url_check', {type: 'boolean', required: false, onChange(obj, key, val) { obj.set('cv_url', ''); }}),
        f('cv', {
          type: 'string',
          required: reads('model.changeset.cv_url_check'),
          disabled: computed('model.changeset.cv_url_check', function() {
            let check = get(this, 'model.changeset.cv_url_check');
            set(this, 'model.changeset.cv_file', null);
            return !check;
          })
        }),
        f('fek'),
        f('discipline_in_fek', {type: 'boolean'}),
        f('discipline_text', {
          type: 'text',
          required: computed('model.changeset.discipline_in_fek', function() {
            let check = get(this, 'model.changeset.discipline_in_fek');
            return !check;
          }),
          disabled: computed('model.changeset.discipline_in_fek', function() {
            let check = get(this, 'model.changeset.discipline_in_fek');
            set(this, 'model.changeset.discipline_text', '');
            return check;
          })
        })
      ],
      layout: {
        flex: [25, 40, 35, 100, 30, 70, 60, 40, 100]
      }
    };
    let FS_MANAGER = {}

    let FS_PROFILE = FS_PROFESSOR;
    let FIELDSETS = [FS_ACCOUNT, FS_PROFILE]
    if (!model.get('registration_token')) {
      FIELDSETS.splice(0, 0, FS_LOGIN);
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
      if (token) { return 'register.academic.title'; }
      if (type === 'manager') { return 'register.manager.title'; }
      if (type === 'candidate') { return 'register.candidate.title'; }
      if (type === 'professor') { return 'register.professor.title'; }
      return 'register.title';
    })
  }
});


export {Register, resetHash};
