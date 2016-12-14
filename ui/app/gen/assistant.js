import {ApellaGen} from 'ui/lib/common';
import gen from 'ember-gen/lib/gen';
import {USER_FIELDSET,
        USER_VALIDATORS,
        ASSISTANT_FIELDSET,
        ASSISTANT_FIELDSET_MANAGER,
        ASSISTANT_FIELDSET_EDIT_MANAGER,
        ASSISTANT_FIELDSET_EDIT_ASSISTANT,
        ASSISTANT_FIELDSET_EDIT_MANAGER_READONLY,
        ASSISTANT_VALIDATORS_EDIT_MANAGER,
        ASSISTANT_VALIDATORS} from 'ui/utils/common/users';
import {field} from 'ember-gen';

const {
  computed,
  computed: { reads },
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
      fields: computed('role', function(){
        if (get(this, 'role') === 'institutionmanager') {
          return ['username', 'email', 'full_name_current',
                  'can_create_positions_verbose',
                  'can_create_registries_verbose'];
        }
        return ['username', 'email', 'full_name_current', 'institution.title_current', ]
      }),
      actions: ['gen:details', 'gen:edit', 'remove']
    },
  },
  details: {
    page: {
      title: computed.readOnly('model.full_name_current')
    }
  },
  create: {
    processModel: function(model) {
      let role = reads('session.session.authenticated.role');
      if (role === 'institutionmanager') {
        let institution = reads('session.session.authenticated.institution');
        get(this, 'store').findRecord('inst', institution).then((inst) => {
          model.set('institution', inst)
        })
      }
      return model;
    },
    fieldsets: computed('role', function() {
      if (get(this, 'role') === 'institutionmanager') {
        return  [
          USER_FIELDSET,
          ASSISTANT_FIELDSET_MANAGER
        ]
      } else {
        return [
          USER_FIELDSET,
          ASSISTANT_FIELDSET
        ]
      }
    })
  },
  edit: {
    validators: computed('role', function(){
      let role = get(this, 'role')
      if (role === 'institutionmanager') {
        return ASSISTANT_VALIDATORS_EDIT_MANAGER
      }
    }),
    fieldsets: computed('role', function() {
      let role = get(this, 'role')
      if (role === 'institutionmanager') {
        return  [
          ASSISTANT_FIELDSET_EDIT_MANAGER,
          ASSISTANT_FIELDSET_EDIT_MANAGER_READONLY
        ]
      }
      if (role === 'assistant') {
        return [
          ASSISTANT_FIELDSET_EDIT_ASSISTANT
        ]
      }
    })
  }
});
