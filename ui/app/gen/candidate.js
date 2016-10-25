import gen from 'ember-gen/lib/gen';
import {USER_FIELDSET, USER_VALIDATORS} from 'ui/utils/common/users';
import {field} from 'ember-gen';


export default gen.CRUDGen.extend({
  modelName: 'candidate',
  path: 'candidates',
  common: {
    menu: {
      label: 'candidate.menu_label',
      icon: 'sentiment_dissatisfied'
    },
    validators: USER_VALIDATORS,
    fieldsets: [
      USER_FIELDSET,
    ]
  },
  list: {
    layout: 'table',
    sortBy: 'username:asc',
    search: {
      fields: ['username', 'email']
    },
    page: {
      title: 'candidate.menu_label',
    },
    label: 'candidate.menu_label',
    fields: ['username', 'email', 'full_name_current' ],
    menu: {
      label: 'candidate.menu_label',
    },
    row: {
      label: 'candidate.menu_label',
      icon: 'person',
    },
  },
  create: {
    page: {
      title: 'candidate.create_title'
    },
  },
  details: {
    fields: ['id', 'username', 'full_name_current'],
  }
});
