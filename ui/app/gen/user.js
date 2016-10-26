import gen from 'ember-gen/lib/gen';
import validate from 'ember-gen/validate';
import {USER_FIELDSET, USER_VALIDATORS} from 'ui/utils/common/users';

const {
  computed,
  get
} = Ember;

export default gen.CRUDGen.extend({
  modelName: 'user',
  path: 'users',
  common: {
    validators: USER_VALIDATORS,
    fieldsets: [
      USER_FIELDSET
    ]
  },
  list: {
    page: {
      title: 'user.menu_label',
    },
    menu: {
      icon: 'face',
      label: 'user.menu_label'
    },
    layout: 'table',
    search: {
      fields: ['username', 'email', 'full_name_current','role_verbose']
    },
    sortBy: 'username:asc',
    fields: ['username', 'email', 'full_name_current', 'role_verbose'],
    row: {
      actions: ['gen:details', 'gen:edit', 'remove']
    },
  },
  record: {
    menu: {
      label: computed('model.id', function() {
        return get(this, 'model.id');
      })
    }
  }
});
