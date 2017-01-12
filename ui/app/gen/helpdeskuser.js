import {ApellaGen} from 'ui/lib/common';
import {USER_FIELDSET, USER_FIELDSET_EDIT, USER_VALIDATORS} from 'ui/utils/common/users';
import {field} from 'ember-gen';

const {
  computed,
  get
} = Ember;

export default ApellaGen.extend({
  order: 500,
  modelName: 'helpdeskuser',
  path: 'helpdeskusers',
  common: {
    validators: USER_VALIDATORS,
  },
  list: {
    page: {
      title: 'helpdeskuser.menu_label',
    },
    menu: {
      label: 'helpdeskuser.menu_label',
      icon: 'sentiment_dissatisfied'
    },
    layout: 'table',
    row: {
      fields: ['username', 'email', 'full_name_current'],
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
