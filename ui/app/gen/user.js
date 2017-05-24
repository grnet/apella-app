import {field} from 'ember-gen';
import {ApellaGen} from 'ui/lib/common';
import gen from 'ember-gen/lib/gen';
import validate from 'ember-gen/validate';
import USER from 'ui/utils/common/users';
import {deactivateUser, activateUser} from 'ui/utils/common/actions';

const {
  computed,
  get
} = Ember;

export default ApellaGen.extend({
  order: 700,
  modelName: 'user',
  auth: true,
  path: 'users',
  common: {
    validators: USER.VALIDATORS,
  },
  list: {
    page: {
      title: 'user.menu_label',
    },
    menu: {
      icon: 'account_box',
      label: 'user.menu_label'
    },
    filter: {
      active: true,
      meta: {
        fields: ['role', 'is_active', field('has_accepted_terms', {label: 'has_accepted_terms.filter.label'})]
      },
      serverSide: true,
      search: true,
      searchFields: ['id', 'email', 'username', 'first_name', 'last_name']
    },
    sort: {
      active: true,
      serverSide: true,
      fields: ['id', 'username', 'email']
    },
    row: {
      fields: [field('id', {label: 'user_id.label'}), field('old_user_id'), 'has_accepted_terms_verbose', field('status_verbose', {label: 'state.label'}), 'username', 'email', 'full_name_current', 'role_verbose', 'login_method'],
      actions: ['gen:details', 'gen:edit', 'remove', 'activateUser', 'deactivateUser'],
      actionsMap: {
        deactivateUser: deactivateUser,
        activateUser: activateUser,
      }

    },
  },
  details: {
    page: {
      title: computed.readOnly('model.full_name_current')
    },
    fieldsets: [
      USER.FIELDSET_DETAILS_USER
    ]
  },
  edit: {
    fieldsets: [
      USER.FIELDSET_EDIT_USER,
    ]
  },
  create: {
    fieldsets: [
      USER.FIELDSET_CREATE,
    ]
  }
});
