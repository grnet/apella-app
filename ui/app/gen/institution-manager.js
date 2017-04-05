import {ApellaGen, emptyArrayResult} from 'ui/lib/common';
import gen from 'ember-gen/lib/gen';
import USER from 'ui/utils/common/users';
import MANAGER from 'ui/utils/common/manager'
import {field} from 'ember-gen';
import {rejectUser, verifyUser, requestProfileChanges} from 'ui/utils/common/actions';

const {
  computed,
  get
} = Ember;

let all_validators = Object.assign({}, USER.VALIDATORS, MANAGER.VALIDATORS);

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
    getModel(params) {
      params = params || {};
      params['manager_role'] = 'institutionmanager';
      /*
       * "no_verification_request" changes the value of "is_verified",
       * "is_rejected" and "verification_pending" parameters.
       *
       * These are also filters. So, if a user selects the
       * "no_verification_request" and one of the other filters at the same
       * time the list that he/she sees is empty.
       */

      if(params.no_verification_request) {
        delete params.no_verification_request;
        if(params.is_verified || params.verification_pending || params.is_rejected) {
          let store = this.store;
          return emptyArrayResult(store, 'institution-manager');
        }
        else {
          params.is_verified = false;
          params.verification_pending = false;
          params.is_rejected = false;
        }
      }
      return this.store.query('institution-manager', params);
    },
    page: {
      title: 'manager.menu_label',
    },
    menu: {
      label: 'manager.menu_label',
      icon: 'supervisor_account',
      display: computed('role', function() {
        let role = get(this, 'role');
        let permittedRoles = ['helpdeskadmin', 'helpdeskuser', 'ministry'];
        return (permittedRoles.includes(role) ? true : false);
      })
    },
    filter: {
      active: true,
      serverSide: true,
      meta: {
        fields: [field('institution', {autocomplete: true}), 'is_verified', 'is_rejected', 'verification_pending', field('no_verification_request', { type: 'boolean' })]
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
      USER.FIELDSET_DETAILS_VERIFIABLE,
      MANAGER.FIELDSET,
      MANAGER.SUB_FIELDSET_DETAILS
    ]

  },
  edit: {
    fieldsets: [
      USER.FIELDSET_EDIT_VERIFIABLE,
      MANAGER.FIELDSET,
      MANAGER.SUB_FIELDSET
    ]
  },
  create: {
    fieldsets: [
      USER.FIELDSET_CREATE,
      MANAGER.FIELDSET,
      MANAGER.FIELDSET_SUB
    ]
  }

});
