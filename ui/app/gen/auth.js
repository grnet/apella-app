import gen from 'ember-gen/lib/gen';
import routes from 'ember-gen/lib/routes';
import AuthGen from 'ember-gen/lib/auth';
import {USER_FIELDSET, USER_VALIDATORS,
        PROFESSOR_FIELDSET, PROFESSOR_VALIDATORS,
        INST_MANAGER_FIELDSET_MAIN, INST_MANAGER_FIELDSET_SUB,
        INSTITUTION_MANGER_VALIDATORS} from 'ui/utils/common/users';

const {
  get, computed
} = Ember;

export default AuthGen.extend({
  login: {
    config: {
      authenticator: 'custom'
    }
  },

  profile: {
    gens: {
      position_interest: gen.GenRoutedObject.extend({
        modelName: 'profile',
        path: 'my-interests',
        getModel(profile) {
          return this.store.findRecord('profile', 'me');
        },
        templateName: 'user-interests',
        routeBaseClass: routes.EditRoute,
        menu: { 
          display: true,
          icon: 'access_alarm',
          label: 'user.positions.interests'
        },
        page: {
          title: 'my.interests',
          breadcrumb: { display: true }
        }
      })
    },
    actions: ['gen:position_interest'],
    modelName: 'profile',
    menu: { display: true },
    fieldsets: computed('model.role', function(){
      let role = this.get('model').get('role');
      let f = [USER_FIELDSET];
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
