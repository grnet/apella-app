import gen from 'ember-gen/lib/gen';
import validate from 'ember-gen/validate';
import {USER_FIELDSET, USER_VALIDATORS} from 'ui/utils/common/users';

export default gen.CRUDGen.extend({
  modelName: 'user',
  path: 'users',
  common: {
    menu: {
      icon: 'face',
      label: 'user.menu_label'
    },
    validators: USER_VALIDATORS,
    fieldsets: [
      USER_FIELDSET
    ]
  },
  list: {
    layout: 'table',
    search: {
      fields: ['username', 'email', 'full_name_current','role_verbose']
    },
    sortBy: 'username:asc',
    fields: ['username', 'email', 'full_name_current', 'role_verbose'],
    page: {
      title: 'user.menu_label',
    }
  },
  create: {
    page: {
      title: 'user.create_title',
    }
  }
});
