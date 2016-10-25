import gen from 'ember-gen/lib/gen';
import {USER_FIELDSET, USER_VALIDATORS} from 'ui/utils/common/users';
import {field} from 'ember-gen';


export default gen.CRUDGen.extend({
  modelName: 'institution-manager',
  path: 'managers',
  common: {
    menu: {
      label: 'manager.menu_label',
      icon: 'sentiment very satisfied'
    },
    validators: USER_VALIDATORS,
    fieldsets: [
      USER_FIELDSET,
      {
        label: 'fieldsets.labels.more_info',
        fields: [
          'institution',
          'authority',
          'authority_full_name',
          'manager_role',
       ],
       layout: {
        flex: [50, 50, 50, 50]
       }
      }
    ]
  },
  list: {
    layout: 'table',
    sortBy: 'username:asc',
    search: {
      fields: ['username', 'email']
    },
    page: {
      title: 'manager.menu_label',
    },
    label: 'manager.menu_label',
    fields: ['username', 'email', 'full_name_current', 'institution.title_current', ],
    menu: {
      label: 'manager.menu_label',
    },
    row: {
      label: 'manager.menu_label',
      icon: 'person',
    },
  },
  create: {
    page: {
      title: 'manager.create_title'
    },
  },
  details: {
    fields: ['id', 'username', 'last_name'],
  }
});
