import Ember from 'ember';
import validate from 'ember-gen/validate';
import {i18nValidate} from 'ui/validators/i18n';
import {field} from 'ember-gen';
import {disable_field} from 'ui/utils/common/fields';
import {fileField} from 'ui/lib/common';
import {i18nField} from 'ui/lib/common';

const {
  assign,
  computed,
  get,
  set,
  computed: { or }
} = Ember;

// Fieldsets for assistants profile

const FIELDSET = {
  label: 'fieldsets.labels.user_info',
  text: 'fieldsets.text.assistant_profile',
  fields: [
    disable_field('user_id'),
    disable_field('username'),
    disable_field('email'),
    'mobile_phone_number',
    'home_phone_number',
    disable_field('first_name'),
    disable_field('last_name'),
    disable_field('father_name'),
    disable_field('id_passport'),
  ],
  layout: {
    flex: [50, 50, 50, 50, 50, 50, 50, 50, 50, 50]
  }
};

const FIELDSET_PERMISSIONS_INFO = {
  label: 'fieldsets.labels.more_info',
  fields: [
    field('institution', {displayAttr: 'title_current', disabled: true}),
    field('is_secretary_verbose', { disabled: true, label: 'is_secretary.label' }),
    disable_field('can_create_positions_verbose'),
    disable_field('can_create_registries_verbose'),
    field('departments', {
      disabled: true,
      label: 'department.menu_label',
      modelName: 'department',
      modelMeta: {
        row: {
          fields: [i18nField('title', { label: 'title.label' })],
          actionsMap: { remove: { hidden: true } }
        }
      },
      displayComponent: 'gen-display-field-table'
    })
  ],
  layout: {
    flex: [100, 33, 33, 33, 100]
  }
};

const FIELDSET_DETAILS = {
  label: 'fieldsets.labels.user_info',
  fields: [
    'user_id',
    'username',
    'email',
    'mobile_phone_number',
    'home_phone_number',
    'first_name_current',
    'last_name_current',
    'father_name_current',
    'id_passport',
    field('institution', {displayAttr: 'title_current'}),
    field('is_secretary_verbose', {label: 'is_secretary.label'}),
    'can_create_positions_verbose',
    'can_create_registries_verbose',
  ],
  layout: {
        flex: [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 33, 33, 33]
  }
};

/*
 * Fieldsets that are used when displaying assistants' data to managers or
 * helpdesk users/admins
 */
let fs_viewed_by_others = {
  permissions_modifiable: {
    label: 'fieldsets.labels.more_info',
    fields: [
      field('is_secretary_verbose', { disabled:  true, label: 'is_secretary.label' }),
      'can_create_registries',
      'can_create_positions'
    ],
    layout: {
      flex: [33, 33, 33]
    }
  },
  permissions_details: {
    label: 'fieldsets.labels.more_info',
    fields: [
      'institution.title_current',
      field('is_secretary_verbose', {label: 'is_secretary.label'}),
      'can_create_registries_verbose',
      'can_create_positions_verbose'],
    layout: {
      flex: [100, 33, 33, 33]
    }
  },
  names: {
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
  },
  contact: {
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
  },
  get_department_fieldset: function(hide_remove_btn) {
    return {
      label: 'department.menu_label',
      text: 'fieldsets.text.manager_can_edit',
      fields: [field('departments', {
        label: null,
        required: true,
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
                  dataKey: 'id',
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
  },
  edit_validators: {
    first_name: [i18nValidate([validate.presence(true), validate.length({min:3, max:200})])],
    last_name: [i18nValidate([validate.presence(true), validate.length({min:3, max:200})])],
    father_name: [i18nValidate([validate.presence(true), validate.length({min:3, max:200})])],
    id_passport: [validate.presence(true)],
  }
};

export {
  FIELDSET,
  FIELDSET_DETAILS,
  FIELDSET_PERMISSIONS_INFO,
  fs_viewed_by_others
}
