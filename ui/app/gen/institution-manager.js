import {ApellaGen} from 'ui/lib/common';
import gen from 'ember-gen/lib/gen';
import {USER_FIELDSET,
        USER_FIELDSET_DETAILS,
        USER_FIELDSET_EDIT,
        USER_VALIDATORS,
        INST_MANAGER_FIELDSET_DETAILS_MAIN,
        INST_MANAGER_FIELDSET_DETAILS_SUB,
        INST_MANAGER_FIELDSET_MAIN,
        INST_MANAGER_FIELDSET_SUB,
        INSTITUTION_MANAGER_VALIDATORS} from 'ui/utils/common/users';
import {field} from 'ember-gen';

const {
  computed,
  get
} = Ember;

let all_validators = Object.assign({}, USER_VALIDATORS, INSTITUTION_MANAGER_VALIDATORS);

export default ApellaGen.extend({
  order: 300,
  modelName: 'institution-manager',
  resourceName: 'institution-managers',
  auth: true,
  path: 'managers',
  common: {
    validators: all_validators,
  },
  list: {
    page: {
      title: 'manager.menu_label',
    },
    menu: {
      label: 'manager.menu_label',
      icon: 'sentiment very satisfied',
      display: computed('role', function() {
        let role = get(this, 'role');
        let permittedRoles = ['helpdeskadmin'];
        return (permittedRoles.includes(role) ? true : false);
      })
    },
    layout: 'table',
    sortBy: 'username:asc',
    search: {
      fields: ['username', 'email']
    },
    row: {
      fields: ['username', 'email', 'full_name_current', 'institution.title_current', 'manager_role_verbose'],
      actions: ['gen:details', 'gen:edit', 'remove']
    },
  },
  details: {
    page: {
      title: computed.readOnly('model.full_name_current')
    },
    fieldsets: [
      USER_FIELDSET_DETAILS,
      INST_MANAGER_FIELDSET_DETAILS_MAIN,
      INST_MANAGER_FIELDSET_DETAILS_SUB
    ]

  },
  edit: {
    fieldsets: [
      USER_FIELDSET_EDIT,
      INST_MANAGER_FIELDSET_MAIN,
      INST_MANAGER_FIELDSET_SUB
    ]
  },
  create: {
    fieldsets: [
      USER_FIELDSET,
      INST_MANAGER_FIELDSET_MAIN,
      INST_MANAGER_FIELDSET_SUB
    ]
  }

});
