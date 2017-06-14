import {ApellaGen, i18nField} from 'ui/lib/common';
import {i18nValidate} from 'ui/validators/i18n';
import validate from 'ember-gen/validate';
import gen from 'ember-gen/lib/gen';
import USER from 'ui/utils/common/users';
import {field} from 'ember-gen';
import {disable_field, departmentInstitutionFilterField} from 'ui/utils/common/fields';
import {rejectUser, verifyUser} from 'ui/utils/common/actions';
import { fs_viewed_by_others } from 'ui/utils/common/assistant';

const {
  computed,
  computed: { reads },
  get
} = Ember;

let fs = fs_viewed_by_others;

export default ApellaGen.extend({
  order: 400,
  name: 'institution-users',
  modelName: 'assistant',
  resourceName: 'assistants',
  auth: true,
  path: 'institution-users',
  session: Ember.inject.service(),

  abilityStates: {
    // resolve ability for position model
    owned: computed('role', function() {
      return get(this, 'role') === 'institutionmanager';
    }) // we expect server to reply with owned resources
  },


  list: {
    page: {
      title: 'institution_users.label',
    },
    menu: {
      label: 'institution_users.label',
      icon: 'perm contact calendar',
      display: computed('role', function() {
        let role = get(this, 'role');
        let forbittenRoles = ['professor', 'candidate', 'assistant'];
        return (forbittenRoles.includes(role) ? false : true);
      })
    },
    getModel: function(params) {
      params = params || {};
      params.is_secretary = false;
      return this.store.query('assistant', params);
    },
    filter: {
      active: true,
      meta: {
        fields: computed('user.role', function() {
          let role = get(this, 'user.role');
          if (role === 'institutionmanager') {
            return ['is_verified', 'is_rejected'];
          }
          else {
            return [
              field('institution', {
                query: function(select, store, field, params) {
                  let locale = get(select, 'i18n.locale'),
                    ordering_param = `title__${locale}`;
                  params = params || {};
                  params.ordering = ordering_param;
                  params.category = 'Institution';

                  return store.query('institution', params);
                }
              }),
              departmentInstitutionFilterField('departments'),
              'is_verified', 'is_rejected'
            ];
          }
        })
      },
      serverSide: true,
      search: true,
      searchPlaceholder: 'search.placeholder.assistants'
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
      USER.FIELDSET_DETAILS_VERIFIABLE,
      fs.permissions_details,
      fs.get_department_fieldset(true)
    ]
  },
  create: {
    processModel: function(model) {
      model.set('is_secretary', false);
      return model;
    },
    onSubmit(model) {
      this.transitionTo('institution-users.record.index', model)
    },
    fieldsets: [
      USER.FIELDSET_CREATE,
      fs.permissions_modifiable,
      fs.get_department_fieldset(false)
    ],
    validators: USER.VALIDATORS
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
