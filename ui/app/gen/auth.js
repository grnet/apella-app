import AuthGen from 'ember-gen/lib/auth';
import {USER_FIELDSET, USER_VALIDATORS,
        PROFESSOR_FIELDSET, PROFESSOR_VALIDATORS,
        INSTITUTION_MANAGER_FIELDSET, INSTITUTION_MANGER_VALIDATORS} from 'ui/utils/common/users';

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
    modelName: 'profile',
    menu: { display: true },
    fieldsets: computed('model.role', function(){
      let role = this.get('model').get('role');
      let f = [USER_FIELDSET];
      if (role === 'professor') {
        f.push(PROFESSOR_FIELDSET);
      }
      if (role === 'institutionmanager') {
        f.push(INSTITUTION_MANAGER_FIELDSET);
      }
      console.log("F", f);
      return f;
    }),

    getModel() {
      return get(this, 'store').findRecord('profile', 'me');
    }
  }
})
