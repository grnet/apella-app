import gen from 'ember-gen/lib/gen';
import {USER_FIELDSET, USER_VALIDATORS,
        PROFESSOR_FIELDSET, PROFESSOR_VALIDATORS,
        INSTITUTION_MANAGER_FIELDSET, INSTITUTION_MANGER_VALIDATORS} from 'ui/utils/common/users';
let {
  computed, get
} = Ember;



const redirect = {
        routeMixin: {
          beforeModel() {
           this.transitionTo('profile.record.edit', 'me');
          }
        },
      },
      noBreadcrumb = {
        page: {breadcrumb: false}
      },
      { merge } = Ember;


export default gen.CRUDGen.extend({
  modelName: 'profile',
  common: {
    fieldsets: computed('model.role', function(){
      let role = this.get('model').get('role');
      let f = [USER_FIELDSET];
      if (role=='professor') {
        f.push(PROFESSOR_FIELDSET);
      }
      if (role=='institutionmanager') {
        f.push(INSTITUTION_MANAGER_FIELDSET);
      }

      return f;
    })
  },
  list: merge(redirect, {menu: {label: 'profile.label', icon: 'pets'}}),
  create: redirect,
  details: redirect,
  edit: merge(noBreadcrumb, {
    actions: []
  }),
  record: noBreadcrumb

});
