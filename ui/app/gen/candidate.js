import {ApellaGen} from 'ui/lib/common';
import {USER_FIELDSET, USER_FIELDSET_EDIT, USER_VALIDATORS} from 'ui/utils/common/users';
import {field} from 'ember-gen';

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
      icon: 'sentiment_dissatisfied'
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
      fields: ['user_id', 'username', 'email', 'full_name_current'],
      actions: ['gen:details', 'gen:edit', 'remove']
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
