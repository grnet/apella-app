import {ApellaGen, i18nField} from 'ui/lib/common';
import {i18nValidate} from 'ui/validators/i18n';
import validate from 'ember-gen/validate';
import gen from 'ember-gen/lib/gen';
import {USER_FIELDSET, USER_FIELDSET_DETAILS,
        USER_VALIDATORS} from 'ui/utils/common/users';
import {field} from 'ember-gen';
import {disable_field} from 'ui/utils/common/fields';
import {rejectUser, verifyUser} from 'ui/utils/common/actions';

const {
  computed,
  computed: { reads },
  get
} = Ember;

// Permissions for create/edit view [common]
const FS_PERMISSIONS_MODIFIABLE = {
  label: 'fieldsets.labels.more_info',
  fields: [
    field('is_secretary_verbose', { disabled:  true, label: 'is_secretary.label' }),
    'can_create_registries',
    'can_create_positions'
  ],
  layout: {
    flex: [33, 33, 33]
  }
};

const FS_PERMISSIONS_DETAILS = {
  label: 'fieldsets.labels.more_info',
  fields: [
    'institution.title_current',
    'is_secretary',
    'can_create_registries_verbose',
    'can_create_positions_verbose'
  ],
  layout: {
    flex: [100, 33, 33, 33]
   }
};

const FS_NAMES = {
  label: 'fieldsets.labels.user_info',
  text: 'fieldsets.text.manager_can_edit',
  fields: [
  disable_field('username'),
    'first_name',
    'last_name',
    'father_name',
    'id_passport',
  ],
  layout: {
    flex: [100, 50, 50, 50, 50]
  }
};

const FS_CONTACT = {
  label: 'contact',
  text: 'fieldsets.text.assistant_can_edit',
  fields: [
    disable_field('email'),
    disable_field('mobile_phone_number'),
    disable_field('home_phone_number')
  ],
  layout: {
    flex: [100, 50, 50]
  }
};

function get_department_fieldset(hide_remove_btn) {
  return {
    label: 'department.menu_label',
    text: 'fieldsets.text.manager_can_edit',
    fields: [field('departments', {
      label: null,
      modelName: 'department',
      query: function(table, store, field, params) {
        let institution = get(field, 'user.institution'),
          institution_id = institution.split('/').slice(-2)[0],
          locale = get(table, 'i18n.locale');
        params = params || {};
        params.institution = institution_id;
        params.ordering = params.ordering || `title__${locale}`;
        return store.query('department', params);
      },
      modelMeta: {
        row: {
          fields: [i18nField('title', {label: 'department.label'})],
          actionsMap: function(hide_remove_btn) {
            return { remove: { hidden: hide_remove_btn }};
          }
        },
        paginate: {
          active: true,
          serverSide: true,
          limits: [10, 20, 30]
        },
        filter: {
          search: false,
          serverSide: true,
          active: true,
          searchFields: [],
          meta: {
            fields: [
              field('department', {
                type: 'model',
                autocomplete: true,
                displayAttr: 'title_current',
                modelName: 'department',
                query: function(select, store, field, params) {
                  let locale = select.get('i18n.locale');
                  return store.findRecord('profile', 'me').then(function(me) {
                    return me.get('institution').then(function(institution) {
                      let institution_id = institution.get('id');
                      params = params || {};
                      params.ordering = `title__${locale}`;
                      params.institution = institution_id;
                      return store.query('department', params);
                    })
                  })
                },
              })
            ]
          }
        },
        sort: {
          serverSide: true,
          active: true,
          fields: ['id', 'title_current']
        }
      },
      displayComponent: 'gen-display-field-table',
    })]
  };
};

const EDIT_VALIDATORS = {
  first_name: [i18nValidate([validate.presence(true), validate.length({min:3, max:200})])],
  last_name: [i18nValidate([validate.presence(true), validate.length({min:3, max:200})])],
  father_name: [i18nValidate([validate.presence(true), validate.length({min:3, max:200})])],
  id_passport: [validate.presence(true)],
}

let all_validators = Object.assign({}, USER_VALIDATORS);

export default ApellaGen.extend({
  order: 400,
  name: 'institution-users',
  modelName: 'assistant',
  resourceName: 'assistants',
  auth: true,
  path: 'institution-users',
  session: Ember.inject.service(),

  common: {
    validators: all_validators,
    fieldsets: [
      USER_FIELDSET,
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
      FS_PERMISSIONS_DETAILS,
      get_department_fieldset(true)
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
      USER_FIELDSET,
      FS_PERMISSIONS_MODIFIABLE,
      get_department_fieldset(false)
    ]
  },
  edit: {
    validators: EDIT_VALIDATORS,
    fieldsets: [
      FS_NAMES,
      FS_PERMISSIONS_MODIFIABLE,
      FS_CONTACT,
      get_department_fieldset(false)
    ]
  }
});
