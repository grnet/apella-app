import {ApellaGen} from 'ui/lib/common';
import gen from 'ember-gen/lib/gen';
import validate from 'ember-gen/validate';
import {USER_FIELDSET, USER_VALIDATORS} from 'ui/utils/common/users';

const {
  computed,
  get
} = Ember;

export default ApellaGen.extend({
  modelName: 'user',
  auth: true,
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
    paginate: {
      limit: [10, 15]
    },
    search: {
      fields: ['username', 'email', 'full_name_current','role_verbose']
    },
    sortBy: 'username:asc',
    row: {
      fields: ['username', 'email', 'full_name_current', 'role_verbose'],
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
