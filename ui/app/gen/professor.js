import {ApellaGen, emptyArrayResult, filterSelectSortTitles} from 'ui/lib/common';
import gen from 'ember-gen/lib/gen';
import USER from 'ui/utils/common/users';
import PROFESSOR from 'ui/utils/common/professor';
import {field} from 'ember-gen';
import {rejectUser, verifyUser, requestProfileChanges} from 'ui/utils/common/actions';

const {
  computed,
  get
} = Ember;

let all_validators = Object.assign(PROFESSOR.VALIDATORS, USER.VALIDATORS);

export default ApellaGen.extend({
  order: 600,
  modelName: 'professor',
  auth: true,
  path: 'professors',
  common: {
    validators: all_validators,
  },
  list: {
    getModel(params) {
      params = params || {};
      let role = get(this, 'user.role'),
        roles_see_only_verified = ['institutionmanager', 'assistant'];
      if(roles_see_only_verified.includes(role)) {
        params.is_verified = true;
      }
      else {
        /*
         * "no_verification_request" changes the value of "is_verified",
         * "is_rejected" and "verification_pending" parameters.
         *
         * These are also filters. So, if a user selects the
         * "no_verification_request" and one of the other filters at the same
         * time the list that he/she sees is empty.
         */
        if(params.no_verification_request) {
          if(params.is_verified || params.verification_pending || params.is_rejected) {
            let store = this.store;
            return emptyArrayResult(store, 'professor');
          }
          else {
            params.is_verified = false;
            params.verification_pending = false;
            params.is_rejected = false;
          }
        }
      }
      return this.store.query('professor', params);
    },
    page: {
      title: computed('role', function() {
        let role = get(this, 'role'),
          roles_see_only_verified = ['institutionmanager', 'assistant'];

        if(roles_see_only_verified.includes(role)) {
          return 'professor.menu_label_alt'
        }
        else {
          return 'professor.menu_label';
        }
      })
    },
    menu: {
      label: computed('role', function() {
        let role = get(this, 'role'),
          roles_see_only_verified = ['institutionmanager', 'assistant'];

        if(roles_see_only_verified.includes(role)) {
          return 'professor.menu_label_alt'
        }
        else {
          return 'professor.menu_label';
        }
      }),
      icon: 'people'
    },
    filter: {
      active: true,
      meta: {
        fields: computed('role', function() {
          let role = get(this, 'user.role'),
            roles_see_only_verified = ['institutionmanager', 'assistant'],
            fields = undefined;
          if(roles_see_only_verified.includes(role)) {
            fields = [
              filterSelectSortTitles('institution'),
              'rank',
              'is_foreign',
            ];
          }
          else {
            fields = [
              filterSelectSortTitles('institution'),
              'rank',
              'is_foreign',
              'is_verified',
              'is_rejected',
              'verification_pending',
              field('no_verification_request', { type: 'boolean' })
            ];
          }
          return fields;
        })
      },
      serverSide: true,
      search: true,
      searchPlaceholder: 'search.placeholder.professors',
      searchFields: ['user_id', 'email', 'username', 'first_name', 'last_name']
    },
    sort: {
      active: true,
      serverSide: true,
      sortBy: 'username',
      fields: [
        'user_id',
        'username',
        'email',
      ]
    },
    row: {
        fields: computed('role', function() {
          let role = get(this, 'role'),
            roles_see_only_verified = ['institutionmanager', 'assistant'],
            fields = undefined;
          if(roles_see_only_verified.includes(role)) {
            fields = [
              'user_id',
              'old_user_id',
              'full_name_current',
              field('email', {dataKey: 'user__email'}),
              field('institution_global', {label: 'institution.label'}),
              'rank_verbose',
            ];
          }
          else {
            fields = [
              'user_id',
              'old_user_id',
              field('username', {dataKey: 'user__username'}),
              'full_name_current',
              field('email', {dataKey: 'user__email'}),
              field('status_verbose', {label: 'state.label'}),
              field('institution_global', {label: 'institution.label'}),
              'rank_verbose'
            ];
          }
          return fields;
        }),
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
    fieldsets: computed('role', function(){
      let role = get(this, 'role');
      let f = [
        USER.FIELDSET_DETAILS_VERIFIABLE,
        PROFESSOR.FIELDSET,
      ]
      if (role === 'helpdeskadmin' || role === 'helpdeskuser' || role === 'ministry') {
        f.push(PROFESSOR.FILES_FIELDSET);
      }
      return f;
    })
  },
  edit: {
    fieldsets: [
      USER.FIELDSET_EDIT_VERIFIABLE,
      PROFESSOR.FIELDSET,
    ]
  },
  create: {
    fieldsets: [
      USER.FIELDSET_CREATE,
      PROFESSOR.FIELDSET,
    ]
  }

});
