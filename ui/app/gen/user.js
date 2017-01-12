import {field} from 'ember-gen';
import {ApellaGen} from 'ui/lib/common';
import gen from 'ember-gen/lib/gen';
import validate from 'ember-gen/validate';
import {USER_FIELDSET, USER_FIELDSET_EDIT,
        USER_FIELDSET_DETAILS,
        USER_VALIDATORS} from 'ui/utils/common/users';

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
    validators: USER_VALIDATORS,
    fieldsets: [
      USER_FIELDSET
    ]
  },
  list: {
    page: {
      title: 'user.menu_label',
    },
    menu: {
      icon: 'face',
      label: 'user.menu_label'
    },
    layout: 'table',
    filter: {
      active: true,
      meta: {
        fields: ['role', 'is_active']
      },
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
    row: {
      fields: [field('id', {label: 'user_id.label'}), 'username', 'email', 'full_name_current', 'role_verbose'],
      actions: ['gen:details', 'gen:edit', 'remove']
    },
  },
  details: {
    page: {
      title: computed.readOnly('model.full_name_current')
    },
    fieldsets: [
      USER_FIELDSET_DETAILS
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
