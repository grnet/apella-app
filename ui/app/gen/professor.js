import {ApellaGen} from 'ui/lib/common';
import gen from 'ember-gen/lib/gen';
import {USER_FIELDSET,
        USER_FIELDSET_DETAILS_VERIFIABLE,
        USER_FIELDSET_EDIT_VERIFIABLE,
        USER_VALIDATORS} from 'ui/utils/common/users';
import PROFESSOR from 'ui/utils/common/professor';
import {field} from 'ember-gen';
import {rejectUser, verifyUser, requestProfileChanges} from 'ui/utils/common/actions';

const {
  computed,
  get
} = Ember;

let all_validators = Object.assign(PROFESSOR.VALIDATORS, USER_VALIDATORS);

export default ApellaGen.extend({
  order: 600,
  modelName: 'professor',
  auth: true,
  path: 'professors',
  common: {
    validators: all_validators,
  },
  list: {
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
    layout: 'table',
    filter: {
      active: true,
      meta: {
        fields: ['institution', 'rank', 'is_foreign', 'is_verified', 'is_rejected', 'verification_pending']
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
        USER_FIELDSET_DETAILS_VERIFIABLE,
        PROFESSOR.FIELDSET,
      ]
      if (role === 'helpdeskadmin' || role === 'helpdeskuser' ) {
        f.push(PROFESSOR.FILES_FIELDSET);
      }
      return f;
    })
  },
  edit: {
    fieldsets: [
      USER_FIELDSET_EDIT_VERIFIABLE,
      PROFESSOR.FIELDSET,
    ]
  },
  create: {
    fieldsets: [
      USER_FIELDSET,
      PROFESSOR.FIELDSET,
    ]
  }

});
