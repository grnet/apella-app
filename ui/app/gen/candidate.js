import {ApellaGen} from 'ui/lib/common';
import {USER_FIELDSET, USER_FIELDSET_EDIT, USER_VALIDATORS} from 'ui/utils/common/users';
import {field} from 'ember-gen';

const {
  computed,
  get
} = Ember;

export default ApellaGen.extend({
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
      searchFields: ['email', 'username', 'first_name', 'last_name']
    },
    sortBy: 'username:asc',
    search: {
      fields: ['username', 'email']
    },
    label: 'candidate.menu_label',
    row: {
      fields: ['username', 'email', 'full_name_current'],
      actions: ['gen:details', 'gen:edit', 'remove']
    },
  },
  details: {
    fields: ['id', 'username', 'full_name_current'],
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
