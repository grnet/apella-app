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

const ASSISTANT_FIELDSET_MANAGER = {
  label: 'fieldsets.labels.more_info',
  fields: ['can_create_registries', 'can_create_positions'],
  layout: {
    flex: [50, 50]
  }
}

const ASSISTANT_FIELDSET = {
  label: 'fieldsets.labels.more_info',
  fields: ['institution', 'can_create_registries', 'can_create_positions'],
  layout: {
    flex: [100, 50, 50]
   }
}

const ASSISTANT_FIELDSET_DETAILS = {
  label: 'fieldsets.labels.more_info',
  fields: ['institution.title_current', 'can_create_registries_verbose', 'can_create_positions_verbose'],
  layout: {
    flex: [100, 50, 50]
   }
}


const ASSISTANT_FIELDSET_EDIT_MANAGER = {
  label: 'fieldsets.labels.user_info',
  text: 'fieldsets.text.manager_can_edit',
  fields: [
    field('username', { readonly: true }),
    'can_create_positions',
    'can_create_registries',
    'first_name',
    'last_name',
    'father_name',
    'id_passport'
  ],
  layout: {
    flex: [50,25,25, 50, 50, 50, 50]
  }
}

const ASSISTANT_FIELDSET_EDIT_MANAGER_READONLY = {
  label: 'fieldsets.labels.user_info',
  text: 'fieldsets.text.assistant_can_edit',
  fields: [
    field('email', { readonly: true }),
    field('mobile_phone_number', { readonly: true }),
    field('home_phone_number', { readonly: true })
  ],
  layout: {
    flex: [100, 50, 50]
  }
}

const ASSISTANT_DEPARTMENT_FIELDSET = {
  label: 'department.menu_label',
  fields: [field('department', {
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
        fields: [i18nField('title', {label: 'department.label'})]
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
}

const ASSISTANT_VALIDATORS_EDIT_MANAGER = {
  first_name: [i18nValidate([validate.presence(true), validate.length({min:3, max:200})])],
  last_name: [i18nValidate([validate.presence(true), validate.length({min:3, max:200})])],
  father_name: [i18nValidate([validate.presence(true), validate.length({min:3, max:200})])],
  id_passport: [validate.presence(true)],
}

let all_validators = Object.assign({}, USER_VALIDATORS);

export default ApellaGen.extend({
  order: 400,
  modelName: 'assistant',
  resourceName: 'assistants',
  auth: true,
  path: 'assistants',
  session: Ember.inject.service(),

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
      icon: 'person_add',
      display: computed('role', function() {
        let role = get(this, 'role');
        let forbittenRoles = ['professor', 'candidate', 'assistant'];
        return (forbittenRoles.includes(role) ? false : true);
      })
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
      ASSISTANT_FIELDSET_DETAILS,
      ASSISTANT_DEPARTMENT_FIELDSET
    ]
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
    onSubmit(model) {
      this.transitionTo('assistant.record.index', model)
    },
    fieldsets: computed('role', function() {
      if (get(this, 'role') === 'institutionmanager') {
        return  [
          USER_FIELDSET,
          ASSISTANT_FIELDSET_MANAGER,
          ASSISTANT_DEPARTMENT_FIELDSET
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
          ASSISTANT_FIELDSET_EDIT_MANAGER_READONLY,
          ASSISTANT_DEPARTMENT_FIELDSET
        ]
      }
    })
  }
});
