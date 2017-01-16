import {ApellaGen} from 'ui/lib/common';
import {USER_FIELDSET, USER_FIELDSET_EDIT, USER_VALIDATORS} from 'ui/utils/common/users';
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
      serverSide: true,
      search: true,
      searchFields: ['id', 'email', 'username', 'first_name', 'last_name']
    },
    sort: {
      active: true,
      sortBy: 'id',
      serverSide: true,
      fields: ['id', 'username']
    },
    label: 'candidate.menu_label',
    row: {
      fields: computed('role', function() {
        let role = get(this, 'role');
        let fs = ['user_id', 'username', 'email', 'full_name_current'];
        if (role === ('helpdeskadmin' || 'helpdeskuser') ) {
          fs.splice(1, 0, field('status_verbose', {label: 'state.label'}));
        }
        return fs;
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
    fields: ['user_id', 'username', 'full_name_current'],
    page: {
      title: computed.reads('model.full_name_current')
    }
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
