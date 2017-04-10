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
      return this.store.query('professor', params);
    },
    page: {
      title: 'professor.menu_label',
    },
    menu: {
      label: 'professor.menu_label',
      icon: 'people',
      display: computed('role', function() {
        let role = get(this, 'role');
        let forbiddenRoles = ['institutionmanager', 'assistant'];
        return (forbiddenRoles.includes(role) ? false : true);
      })
    },
    filter: {
      active: true,
      meta: {
        fields: [
          filterSelectSortTitles('institution'),
          'rank',
          'is_foreign',
          'is_verified',
          'is_rejected',
          'verification_pending',
          field('no_verification_request', { type: 'boolean' })
        ]
      },
      serverSide: true,
      search: true,
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
      fields: [
        'user_id',
        'old_user_id',
        field('status_verbose', {label: 'state.label'}),
        field('institution_global', {label: 'institution.label'}),
        field('username', {dataKey: 'user__username'}),
        field('email', {dataKey: 'user__email'}),
        'full_name_current', 'rank_verbose'
      ],
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
