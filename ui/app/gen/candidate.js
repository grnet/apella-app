import {ApellaGen} from 'ui/lib/common';
import {USER_FIELDSET, USER_FIELDSET_DETAILS,
        CANDIDATE_FILES_FIELDSET,
        USER_FIELDSET_EDIT, USER_VALIDATORS} from 'ui/utils/common/users';
import {field} from 'ember-gen';
import {rejectUser, verifyUser, requestProfileChanges} from 'ui/utils/common/actions';

const {
  computed,
  get
} = Ember;


export default ApellaGen.extend({
  order: 500,
  modelName: 'candidate',
  path: 'candidates',
  common: {
    validators: USER_VALIDATORS,
  },
  list: {
    page: {
      title: 'candidate.menu_label',
    },
    menu: {
      label: 'candidate.menu_label',
      icon: 'people_outline'
    },
    layout: 'table',
    filter: {
      active: true,
      meta: {
        fields: ['is_verified', 'is_rejected', 'verification_pending']
      },
      serverSide: true,
      search: true,
      searchFields: ['id', 'email', 'username', 'first_name', 'last_name']
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
      title: computed.reads('model.full_name_current')
    },
    fieldsets: [
      USER_FIELDSET_DETAILS,
      CANDIDATE_FILES_FIELDSET
    ]

  },
  edit: {
    fieldsets: [
      USER_FIELDSET_EDIT,
    ]
  },
  create: {
    fieldsets: [
      USER_FIELDSET,
    ]
  }
});
