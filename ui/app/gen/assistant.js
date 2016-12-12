import {ApellaGen} from 'ui/lib/common';
import gen from 'ember-gen/lib/gen';
import {USER_FIELDSET,
        USER_VALIDATORS,
        ASSISTANT_FIELDSET,
        ASSISTANT_VALIDATORS} from 'ui/utils/common/users';
import {field} from 'ember-gen';

const {
  computed,
  get
} = Ember;

let all_validators = Object.assign({}, USER_VALIDATORS, ASSISTANT_VALIDATORS);

export default ApellaGen.extend({
  modelName: 'assistant',
  resourceName: 'assistants',
  auth: true,
  path: 'assistants',
  common: {
    validators: all_validators,
    fieldsets: [
      USER_FIELDSET,
      ASSISTANT_FIELDSET
    ],

  },
  abilityStates: {
    // resolve ability for position model
    owned: computed('role', function() {
      return get(this, 'role') === 'institutionmanager';
    }) // we expect server to reply with owned resources
  },


  list: {
    page: {
      title: 'assistant.menu_label',
    },
    menu: {
      label: 'assistant.menu_label',
      icon: 'directions_run',

    },
    layout: 'table',
    sortBy: 'username:asc',
    search: {
      fields: ['username', 'email']
    },
    row: {
      fields: ['username', 'email', 'full_name_current', 'institution.title_current', ],
      actions: ['gen:details', 'gen:edit', 'remove']
    },
  },
  details: {
    page: {
      title: computed.readOnly('model.full_name_current')
    }
  }
});
