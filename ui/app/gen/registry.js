import {
  ApellaGen, i18nField, i18nUserSortField, get_registry_members, fileField
} from 'ui/lib/common';
import {disable_field} from 'ui/utils/common/fields';
import gen from 'ember-gen/lib/gen';
import {field} from 'ember-gen';
import _ from 'lodash/lodash'
import Users  from 'ui/gen/user';
import {goToDetails} from 'ui/utils/common/actions';

let {
  computed, get, assign
} = Ember;


// Fieldsets for quickDetailsView of professors
let fs_user = {
  label: 'user_data',
  fields: [
    'user_id',
    i18nField('last_name', {label: 'last_name.label'}),
    i18nField('first_name', {label: 'first_name.label'}),
    i18nField('father_name', {label: 'father_name.label'}),
  ],
  layout: {
    flex: [100, 33, 33, 33]
  }
};

let fs_contact = {
  label: 'contact',
  fields: [
    'email',
    'home_phone_number',
    'mobile_phone_number'
  ]
};

let fs_prof_domestic = {
  label: 'professor_profile',
  fields: [
    'is_foreign_descr',
    field('institution_global', {label: 'institution.label'}),
    i18nField('department.title', {label: 'department.label'}),
    'cv_url',
    fileField('cv_professor', 'professor', 'cv_professor',
      { readonly: true, label: 'cv.label' }),
    'rank',
    'fek',
    'discipline_text',
    field('discipline_in_fek_verbose', { label: 'discipline_in_fek.label' })
  ],
  layout: {
    flex: [100, 50, 50, 100, 100, 50, 50, 50, 50]
  }
};

let fs_prof_foreign = {
  label: 'professor_profile',
  fields: [
    'is_foreign_descr',
    field('institution_global', {label: 'institution.label'}),
    'cv_url',
    fileField('cv_professor', 'professor', 'cv_professor',
      { readonly: true, label: 'cv.label' }),
    'rank',
    'discipline_text',
    field('speaks_greek_verbose', {label: 'speaks_greek.label'})
  ],
  layout: {
    flex: [100, 100, 100, 100, 50, 50, 100]
  }
};


let fields_members_table = [
    field('user_id', {type: 'string', dataKey: 'user__id'}),
    i18nUserSortField('last_name', {label: 'last_name.label'}),
    i18nField('first_name', {label: 'first_name.label'}),
    'is_foreign_descr',
    field('institution_global', {label: 'institution.label'}),
    i18nField('department.title', {label: 'department.label'}),
    'rank',
    'discipline_text'
];

function peak_fs_professors() {
  let professor = get(this, 'model'),
    is_foreign = professor.get('is_foreign'),
    head = [fs_user, fs_contact];
  if(is_foreign) {
    return head.concat(fs_prof_foreign);
  }
  else {
    return head.concat(fs_prof_domestic);
  }
};

// serverSide is a boolean value that is used for filtering, sorting, searching
function membersAllModelMeta(serverSide, hideQuickView) {
   let sortFields = (serverSide ? ['user_id', 'last_name'] : ['user_id', 'last_name_current', 'first_name_current']),
    searchFields = (serverSide ? ['last_name_current', 'discipline_text'] : ['last_name.el', 'last_name.en', 'discipline_text']);
  return {
    row: {
      fields: fields_members_table,
      actions: ['view_details'],
      actionsMap: {
        view_details: {
          icon: 'open_in_new',
          detailsMeta: {
            fieldsets: computed('model', peak_fs_professors)
          },
          action: function() {},
          /*
           * Display the quickDetails button when:
           * The user is the institution manager or an assistant of
           * institution X and the registry belongs to institution X
           *
           * TODO: Calculate this once per table-field and not per row.
           */
          hidden: computed ('role', function() {
            let role = get(this, 'role'),
              hidden = true;
            if(hideQuickView === true) {
              return true;
            }
            // false for edit and create view
            else if( hideQuickView === false) {
              return false;
            }
            // undefined for details view
            else {
              if(role === 'institutionmanager' || role === 'assistant') {
                let controller = Ui.__container__.lookup('controller:registry.record.index'),
                  registry = controller.get('model'),
                  registry_institution = get(registry, 'institution'),
                  registry_institution_id = get(registry_institution, 'id').split('/').slice(-2)[0],
                  user_institution = get(this, 'session.session.authenticated.institution'),
                  user_institution_id = user_institution.split('/').slice(-2)[0];
                if(registry_institution_id === user_institution_id) {
                  hidden = false;
                }
              }
              return hidden;
            }
          }),
          label: 'view.user.details',
          confirm: true,
          prompt: {
            title: computed('model.user_id', function() {
              return get(this, 'model.full_name_current');
            }),
            cancel: 'close',
            contentComponent: 'member-quick-view'
          }
        }
      }
    },
    paginate: {
      active: true,
      serverSide: serverSide,
      limits: [10, 20, 30]
    },
    filter: {
      search: true,
      searchPlaceholder: 'search.placeholder_members',
      serverSide: serverSide,
      active: true,
      searchFields: searchFields,
      meta: {
        fields: [
          field('user_id', {type: 'string'}),
          field('institution', {
            type: 'model',
            autocomplete: true,
            displayAttr: 'title_current',
            modelName: 'institution',
          }),
          field('rank')
        ]
      }
    },
    sort: {
      serverSide: serverSide,
      active: true,
      fields: sortFields
    }
  };
};

function membersField(modelMetaSide, selectModelMetaSide, hideQuickView) {
  return field('members', {
    refreshValueQuery: modelMetaSide,
    valueQuery: function(store, params, model, value) {
      // If the model has no id we are in create view
      if(model.get('id')) {
        // Default ordering (if other is not set)
        if(!params.ordering) {
          let locale = model.get('i18n.locale');
          params.ordering = `user__last_name__${locale}`;
        }
          return get_registry_members(model, store, params);
      }
      else {
        return value ? value : [];
      }
    },
    query: function(table, store, field, params) {
      // Default ordering (if other is not set)
      if(!params.ordering) {
        let locale = get(table, 'i18n.locale');
        params.ordering = `user__last_name__${locale}`;
      }
        return store.query('professor', params);
    },
    // a list-like gen config
    label: null,
    modelMeta: membersAllModelMeta(modelMetaSide, hideQuickView),
    selectModelMeta: membersAllModelMeta(selectModelMetaSide, hideQuickView),
    modelName: 'professor',
    displayComponent: 'gen-display-field-table'
  });
}


export default ApellaGen.extend({
  modelName: 'registry',
  auth: true,
  path: 'registries',

  abilityStates: {
    /*
     * Permission rule "owned" executes for institutionmanager
     * An institutionmanager ownes the registries of his institution.
     */
    owned: computed('model.institution.id', 'user.institution.id', function() {
      let registry_institution_id =  this.get('model.institution.id'),
        user_institution_id = get(this, 'user.institution').split('/').slice(-2)[0];
      return registry_institution_id === user_institution_id;
    }),
    /*
     * Permission rule "can_create" executes for assistants
     * An assistant can create a registry for his own institution, if the
     * institution manager has gave him the permission:
     * user.can_create = true
     */
    can_create: computed('user.can_create_registries', 'model.institution.id', 'user.institution.id', function() {
        let registry_institution_id =  this.get('model.institution.id'),
          user_institution_id = get(this, 'user.institution').split('/').slice(-2)[0];
          can_create_registries  = get(this, 'user.can_create_registries');
        return (registry_institution_id === user_institution_id) && can_create_registries;
    })
  },

  create: {
    onSubmit(model) {
      this.transitionTo('registry.record.index', model);
    },
    fieldsets: [{
      label: 'registry.main_section.title',
      fields: [
        field('department', {
          displayAttr: 'title_current',
          query: function(table, store, field, params) {
            // on load sort by title
            let locale = get(table, 'i18n.locale');
            let ordering_param = {
              ordering: `title__${locale}`
            };
            let query;
            let role = get(field, 'session.session.authenticated.role');
            if (role == 'institutionmanager' || role == 'assistant') {
              let user_institution = get(field, 'session.session.authenticated.institution');
              let id = user_institution.split('/').slice(-2)[0];
              query = assign({}, { institution: id }, ordering_param);
            } else {
              query = ordering_param;
            }
            return store.query('department', query);
          }
        }),
        field('type', {label: 'type.label'}),

      ],
      layout: {
        flex: [70, 30]
      }
    },{
      label: 'registry.members_section.title',
      fields: [membersField(false, true, false)]
    }]
  },

  list: {
    menu: {
      icon: 'view list',
      label: 'registry.menu_label'
    },
    page: {
      title: 'registry.menu_label'
    },
    layout: 'table',
    paginate: {
      active: true,
      serverSide: true,
      limits: [10, 20, 30]
    },
    filter: {
      search: false,
      serverSide: true,
      active: true,
      meta: {
        fields: [
          field('institution',
            {
              label: 'institution.label',
              type: 'model',
              displayAttr: 'title_current',
              modelName: 'institution',
              dataKey: 'department.institution',
              query: function(select, store, field, params) {
                let locale = select.get('i18n.locale');
                params = params || {};
                params.ordering = `title_${locale}`;
                params.category = 'Institution';
                return store.query('institution', params);
              }
            }),
          'type',
          field('id', {type: 'string'}),
        ]
      }
    },
    sort: {
      serverSide: true,
      active: true,
      fields: ['id', 'type_verbose']
    },
    row: {
      fields: [
        'id',
        i18nField('institution.title', {label: 'institution.label'}),
        i18nField('department.title', {label: 'department.label', type: 'text'}),
        field('type_verbose', {label: 'type.label', type: 'text', dataKey: 'type'})
      ],
      actions: ['gen:details', 'gen:edit', 'remove']
    }
  },

  details: {
    page: {
      title: computed('model.institution.title_current', function() {
        let institution_title = get(this, 'model.institution.title_current'),
          registry_id = get(this, 'model.id');
        return `${institution_title} (${registry_id})`;
      })
    },
    fieldsets: [{
      label: 'registry.main_section.title',
      fields: [
        i18nField('institution.title'),
        i18nField('department.title'),
        'type'
      ],
      layout: {
        flex: [100, 50, 50]
      }
    },{
      label: 'registry.members_section.title',
      fields: [membersField(true, true)]
    }]
  },
  edit: {
    /*
     * Load the institution before the getModel returns the model registry.
     * Use in the abilityState "owned".
     */
    getModel: function(params, model) {
      return model.get('department').then(function(department) {
        return department.get('institution').then(function(institution) {
          return model;
        })
      })
    },
    fieldsets: [{
      label: 'registry.main_section.title',
      fields: [
          field('institution',
            {
              label: 'institution.label',
              type: 'model',
              displayAttr: 'title_current',
              modelName: 'institution',
              dataKey: 'department.institution',
              disabled: true
            }),
        disable_field('department', { displayAttr: 'title_current' }),
        disable_field('type')
      ],
      layout: {
        flex: [50, 50, 50]
      }
    },{
      label: 'registry.members_section.title',
      fields: [membersField(false, true, false)]
    }]
  }
});
