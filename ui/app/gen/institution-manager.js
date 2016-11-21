import gen from 'ember-gen/lib/gen';
import {USER_FIELDSET,
        USER_VALIDATORS,
        INSTITUTION_MANAGER_FIELDSET,
        INSTITUTION_MANAGER_VALIDATORS} from 'ui/utils/common/users';
import {field} from 'ember-gen';

const {
  computed,
  get
} = Ember;

export default gen.CRUDGen.extend({
  modelName: 'institution-manager',
  path: 'managers',
  common: {
    validators: USER_VALIDATORS,
    fieldsets: [
      USER_FIELDSET,
      INSTITUTION_MANAGER_FIELDSET,
    ]
  },
  list: {
    page: {
      title: 'manager.menu_label',
    },
    menu: {
      label: 'manager.menu_label',
      icon: 'sentiment very satisfied'
    },
    layout: 'table',
    sortBy: 'username:asc',
    search: {
      fields: ['username', 'email']
    },
    row: {
      fields: ['username', 'email', 'full_name_current', 'institution.title_current', ],
      actions: ['gen:details', 'gen:edit', 'remove']
    },
  },
  details: {
    fields: ['id', 'username', 'last_name'],
  },
  record: {
    menu: {
      label: computed('model.id', function() {
        return get(this, 'model.id');
      })
    }
  }
});
