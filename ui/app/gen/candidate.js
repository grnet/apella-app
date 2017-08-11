import {ApellaGen, emptyArrayResult} from 'ui/lib/common';
import USER from 'ui/utils/common/users';
import CANDIDATE from 'ui/utils/common/candidate';
import {field} from 'ember-gen';
import {rejectUser, verifyUser, requestProfileChanges, createIssue} from 'ui/utils/common/actions';

const {
  computed,
  get
} = Ember;


export default ApellaGen.extend({
  order: 500,
  modelName: 'candidate',
  path: 'candidates',
  common: {
    validators: USER.VALIDATORS,
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
          return emptyArrayResult(store, 'candidate');
        }
        else {
          params.is_verified = false;
          params.verification_pending = false;
          params.is_rejected = false;
        }
      }
      return this.store.query('candidate', params);
    },
    page: {
      title: 'candidate.menu_label',
    },
    menu: {
      label: 'candidate.menu_label',
      icon: 'people_outline'
    },
    filter: {
      active: true,
      meta: {
        fields: ['is_verified', 'is_rejected', 'verification_pending',
          field('no_verification_request', { type: 'boolean' })]
      },
      serverSide: true,
      search: true,
      searchPlaceholder: 'search.placeholder.candidates'
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
    label: 'candidate.menu_label',
    row: {
      fields: [
        'user_id',
        field('status_verbose', {label: 'state.label'}),
        field('username', {dataKey: 'user__username'}),
        field('email', {dataKey: 'user__email'}),
        'full_name_current'
      ],
      actions: ['gen:details', 'gen:edit', 'remove', 'verifyUser', 'rejectUser', 'requestProfileChanges', 'createIssue'],
      actionsMap: {
        verifyUser: verifyUser,
        rejectUser: rejectUser,
        requestProfileChanges: requestProfileChanges,
        createIssue: createIssue
      }
    },
  },
  details: {
    page: {
      title: computed.reads('model.full_name_current')
    },
    fieldsets: [
      USER.FIELDSET_DETAILS_VERIFIABLE,
      CANDIDATE.FILES_FIELDSET
    ]
  },
  edit: {
    fieldsets: [
      USER.FIELDSET_EDIT_VERIFIABLE,
    ]
  },
  create: {
    fieldsets: [
      USER.FIELDSET_CREATE,
    ]
  }
});
