import {ApellaGen} from 'ui/lib/common';
import gen from 'ember-gen/lib/gen';
import {USER_FIELDSET,
        USER_FIELDSET_DETAILS_VERIFIABLE,
        USER_FIELDSET_EDIT_VERIFIABLE,
        USER_VALIDATORS,
        INST_MANAGER_FIELDSET_DETAILS_MAIN,
        INST_MANAGER_FIELDSET_DETAILS_SUB,
        INST_MANAGER_FIELDSET_MAIN,
        INST_MANAGER_FIELDSET_SUB} from 'ui/utils/common/users';
import MANAGER from 'ui/utils/common/manager'
import {field} from 'ember-gen';
import {rejectUser, verifyUser, requestProfileChanges} from 'ui/utils/common/actions';

const {
  computed,
  get
} = Ember;

let all_validators = Object.assign({}, USER_VALIDATORS, MANAGER.VALIDATORS);

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
      icon: 'supervisor_account',
      display: computed('role', function() {
        let role = get(this, 'role');
        let permittedRoles = ['helpdeskadmin', 'helpdeskuser'];
        return (permittedRoles.includes(role) ? true : false);
      })
    },
    getModel: function(params) {
      params = params || {};
      params['manager_role'] = 'institutionmanager';
      return this.store.query('institution-manager', params);
    },
    layout: 'table',
    filter: {
      active: true,
      serverSide: true,
      meta: {
        fields: [field('institution', {autocomplete: true}), 'is_verified', 'is_rejected', 'verification_pending']
      },
      search: true,
      searchFields: ['user_id', 'email', 'username', 'first_name', 'last_name']
    },
    sort: {
      active: true,
      serverSide: true,
      fields: [
        'user_id',
        'username',
        'email',
      ]
    },
    row: {
      fields: ['user_id', field('status_verbose', {label: 'state.label'}),
              field('username', {dataKey: 'user__username'}),
              field('email', {dataKey: 'user__email'}),
              'full_name_current', 'institution.title_current'],
      actions: ['gen:details', 'gen:edit', 'remove', 'verifyUser', 'rejectUser', 'requestProfileChanges'],
      actionsMap: {
        verifyUser: verifyUser,
        rejectUser: rejectUser,
        requestProfileChanges: requestProfileChanges,
      }
    },
  },
  details: {
    page: {
      title: computed.readOnly('model.full_name_current')
    },
    fieldsets: [
      USER_FIELDSET_DETAILS_VERIFIABLE,
      MANAGER.FIELDSET,
      MANAGER.SUB_FIELDSET_DETAILS
    ]

  },
  edit: {
    fieldsets: [
      USER_FIELDSET_EDIT_VERIFIABLE,
      MANAGER.FIELDSET,
      MANAGER.SUB_FIELDSET
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
