import {ApellaGen} from 'ui/lib/common';
import gen from 'ember-gen/lib/gen';
import {USER_FIELDSET,
        USER_FIELDSET_DETAILS,
        USER_FIELDSET_EDIT,
        USER_VALIDATORS,
        PROFESSOR_FIELDSET,
        PROFESSOR_VALIDATORS} from 'ui/utils/common/users';
import {field} from 'ember-gen';

const {
  computed,
  get
} = Ember;

let all_validators = Object.assign(PROFESSOR_VALIDATORS, USER_VALIDATORS);

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
      icon: 'sentiment_very_dissatisfied'
    },
    layout: 'table',
    sortBy: 'username:asc',
    search: {
      fields: ['username', 'email']
    },
    row: {
      fields: ['username', 'email', 'full_name_current', 'rank', ],
      actions: ['gen:details', 'gen:edit', 'remove']
    },
  },
  details: {
    page: {
      title: computed.readOnly('model.full_name_current')
    },
    fieldsets: [
      USER_FIELDSET_DETAILS,
      PROFESSOR_FIELDSET,
    ]

  },
  edit: {
    fieldsets: [
      USER_FIELDSET_EDIT,
      PROFESSOR_FIELDSET,
    ]
  },
  create: {
    fieldsets: [
      USER_FIELDSET,
      PROFESSOR_FIELDSET,
    ]
  }



});
