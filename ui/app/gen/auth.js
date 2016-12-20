import gen from 'ember-gen/lib/gen';
import routes from 'ember-gen/lib/routes';
import AuthGen from 'ember-gen/lib/auth';
import {USER_FIELDSET, USER_FIELDSET_EDIT, USER_VALIDATORS,
        PROFESSOR_FIELDSET, PROFESSOR_VALIDATORS,
        INST_MANAGER_FIELDSET_MAIN, INST_MANAGER_FIELDSET_SUB,
        INSTITUTION_MANAGER_VALIDATORS} from 'ui/utils/common/users';
import {field} from 'ember-gen';
import {disable_field} from 'ui/utils/common/fields';

const {
  computed: { reads },
  get, computed
} = Ember;

const PROFILE_ASSISTANT_FIELDSET = {
  label: 'fieldsets.labels.more_info',
  fields: [
    field('username', { readonly: true }),
    'password',
    'email',
    'mobile_phone_number',
    'home_phone_number',
    disable_field('first_name'),
    disable_field('last_name'),
    disable_field('father_name'),
    disable_field('id_passport'),
    disable_field('can_create_positions'),
    disable_field('can_create_registries'),
    disable_field('institution.title_current'),
  ],
  layout: {
        flex: [100, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50]
  }
}

export default AuthGen.extend({
  order: 1,

  login: {
    config: {
      authenticator: 'apimas'
    }
  },

  profile: {
    gens: {
      position_interest: gen.GenRoutedObject.extend({
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
          title: 'my.interests',
          breadcrumb: { display: true }
        }
      })
    },
    modelName: 'profile',
    menu: {
      display: true,
      label: 'profile.menu_label',
    },
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
    fieldsets: computed('model.role', function(){
      let f = [];
      let role = this.get('model').get('role');
      if (role === 'assistant') {
        f.push(PROFILE_ASSISTANT_FIELDSET)
        return f;
      }
      f.push(USER_FIELDSET_EDIT);

      if (role === 'professor') {
        f.push(PROFESSOR_FIELDSET);
      }
      if (role === 'institutionmanager') {
        f.push(INST_MANAGER_FIELDSET_MAIN, INST_MANAGER_FIELDSET_SUB);
      }
      return f;
    }),

    getModel() {
      return get(this, 'store').findRecord('profile', 'me');
    }
  }
})
