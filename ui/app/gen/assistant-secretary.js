import {ApellaGen, i18nField} from 'ui/lib/common';
import {i18nValidate} from 'ui/validators/i18n';
import validate from 'ember-gen/validate';
import gen from 'ember-gen/lib/gen';
import {USER_FIELDSET, USER_FIELDSET_DETAILS,
        USER_VALIDATORS} from 'ui/utils/common/users';
import {field} from 'ember-gen';
import {disable_field} from 'ui/utils/common/fields';
import {rejectUser, verifyUser} from 'ui/utils/common/actions';
import { fs_viewed_by_others } from 'ui/utils/common/assistant';

const {
  computed,
  computed: { reads },
  get
} = Ember;

let fs = fs_viewed_by_others;

export default ApellaGen.extend({
  order: 350,
  name: 'secretaries',
  modelName: 'assistant',
  resourceName: 'assistants',
  path: 'secretaries',
  auth: true,
  session: Ember.inject.service(),

  abilityStates: {
    // resolve ability for position model
    owned: computed('role', function() {
      return get(this, 'role') === 'institutionmanager';
    }) // we expect server to reply with owned resources
  },

  list: {
    page: {
      title: 'secretaries.label',
    },
    menu: {
      label: 'secretaries.label',
      icon: 'assignment ind',
      display: computed('role', function() {
        let role = get(this, 'role');
        let forbittenRoles = ['professor', 'candidate', 'assistant'];
        return (forbittenRoles.includes(role) ? false : true);
      })
    },
    getModel: function(params) {
      params = params || {};
      params.is_secretary = true;
      return this.store.query('assistant', params);
    },
    layout: 'table',
    filter: {
      active: true,
      meta: {
        fields: ['is_verified', 'is_rejected', 'verification_pending']
      },
      serverSide: true,
      search: true,
      searchFields: ['id', 'email', 'username', 'first_name', 'last_name']
    },
    sort: {
      active: true,
      serverSide: true,
      fields: [
        'user_id',
        'username',
        'email',
      ]
    },
    search: {
      fields: ['username', 'email']
    },
    row: {
      fields: computed('role', function(){
        if (get(this, 'role') === 'institutionmanager') {
          return [
            field('status_verbose', {label: 'state.label'}),
            field('username', {dataKey: 'user__username'}),
            field('email', {dataKey: 'user__email'}),
            'full_name_current',
            'can_create_positions_verbose',
            'can_create_registries_verbose',
          ];
        }
        return [
          'user_id',
          field('status_verbose', {label: 'state.label'}),
          field('username', {dataKey: 'user__username'}),
          field('email', {dataKey: 'user__email'}),
          'full_name_current', 'institution.title_current',
        ]
      }),
      actions: ['gen:details', 'gen:edit', 'remove', 'verifyUser', 'rejectUser'],
      actionsMap: {
        verifyUser: verifyUser,
        rejectUser: rejectUser,
      }

    },
  },
  details: {
    page: {
      title: computed.readOnly('model.full_name_current')
    },
    fieldsets: [
      USER_FIELDSET_DETAILS,
      fs.permissions_details,
      fs.get_department_fieldset(true)
    ]
  },
  create: {
    processModel: function(model) {
      model.set('is_secretary', true);
      return model;
    },
    onSubmit(model) {
      this.transitionTo('secretaries.record.index', model)
    },
    fieldsets: [
      USER_FIELDSET,
      fs.permissions_modifiable,
      fs.get_department_fieldset(false)
    ],
    validators: USER_VALIDATORS
  },
  edit: {
    fieldsets: [
      fs.names,
      fs.permissions_modifiable,
      fs.contact,
      fs.get_department_fieldset(false)
    ],
    validators: fs.edit_validators
  }
});
