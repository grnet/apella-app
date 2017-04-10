import {
  ApellaGen, i18nField, i18nUserSortField, get_registry_members,
  fileField, preloadRelations, filterSelectSortTitles
} from 'ui/lib/common';
import {disable_field} from 'ui/utils/common/fields';
import gen from 'ember-gen/lib/gen';
import {field} from 'ember-gen';
import _ from 'lodash/lodash'
import Users  from 'ui/gen/user';
import {goToDetails} from 'ui/utils/common/actions';
import {
  fs_user, fs_contact, fs_prof_domestic, fs_prof_foreign, peak_fs_professors
} from 'ui/lib/professors_quick_details';

let {
  computed, get, assign
} = Ember;

let fields_members_table = [
    field('user_id', {type: 'string', dataKey: 'user__id'}),
    'old_user_id',
    i18nUserSortField('last_name', {label: 'last_name.label'}),
    i18nField('first_name', {label: 'first_name.label'}),
    field('institution_global', {label: 'institution.label'}),
    i18nField('department.title', {label: 'department.label'}),
    'discipline_text'
];

// serverSide is a boolean value that is used for filtering, sorting, searching
function membersAllModelMeta(serverSide, hideQuickView) {
   let sortFields = (serverSide ? ['user_id', 'last_name'] : ['user_id', 'last_name_current', 'first_name_current']),
    searchFields = (serverSide ? ['last_name_current', 'discipline_text', 'old_user_id'] : ['last_name.el', 'last_name.en', 'discipline_text', 'old_user_id']);


   // For now, hide client side functionality
  let display = serverSide;

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
                let controller = this.container.lookup('controller:registry.record.index'),
                  registry = controller.get('model'),
                  registry_institution = get(registry, 'institution'),
                  registry_institution_id = get(registry_institution, 'id').split('/').slice(-2)[0],
                  user_institution = get(this, 'session.session.authenticated.institution'),
                  user_institution_id = user_institution.split('/').slice(-2)[0];
                if(registry_institution_id === user_institution_id) {
                  hidden = false;
                }
              }
              else if (role === 'ministry') {
                hidden = false;
              }
              return hidden;
            }
          }),
          label: 'view.professor.details',
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
      active: display,
      serverSide: serverSide,
      limits: [10, 20, 30]
    },
    filter: {
      search: true,
      searchPlaceholder: 'search.placeholder_members',
      serverSide: serverSide,
      active: display,
      searchFields: searchFields,
      meta: {
        fields: [
          field('user_id', {type: 'string'}),
          filterSelectSortTitles('institution'),
          field('rank')
        ]
      }
    },
    sort: {
      serverSide: serverSide,
      active: display,
      fields: sortFields
    }
  };
};

function membersField(modelMetaSide, selectModelMetaSide, hideQuickView, lessFields) {

  return field('members', {
    formComponent: 'apella-members-edit-field',
    refreshValueQuery: modelMetaSide,
    valueQuery: function(store, params, model, value) {

      // If the model has no id we are in create view
      // if(model.get('id') && modelMetaSide) {
      if (model.get('id')) {
        // Default ordering (if other is not set)
        if (!params.ordering) {
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
      params.is_verified = true;
      params.create_registry = true;
      return store.query('professor', params);
    },
    // a list-like gen config
    label: null,
    modelMeta: membersAllModelMeta(modelMetaSide, hideQuickView),
    selectModelMeta: membersAllModelMeta(selectModelMetaSide, hideQuickView),
    modelName: 'professor',
    displayComponent: 'gen-display-field-table',
    dialog: {
      cancel: null,
      add: 'add'
    }
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
     * An can create a registry if the institution manager has given him
     * the permission: user.can_create = true
     */

    can_create: computed('user.can_create_registries', function() {
      return get(this, 'user.can_create_registries');
    }),

    /*
     * Permission rule "can_create_owned" executes for assistants
     * An assistant can_create_owned a registry for his own department, if the
     * institution manager has gave him the permission:
     * user.can_create = true
     */
    can_create_owned: computed('can_create', 'model.department.id', 'user.departments', function() {
        let registry_department =  get(this, 'model.department.id'),
          user_departments = get(this, 'user.departments'),
          can_create  = get(this, 'can_create');
        let owns = user_departments.includes(registry_department);
        return owns && can_create;
    })
  },

  create: {
    onSubmit(model) {
      this.transitionTo('registry.record.edit.index', model);
    },
    fieldsets: [{
      label: 'registry.main_section.title',
      fields: [
        field('department', {
          displayAttr: 'title_current',
          query: function(table, store, field, params) {

            // If the logged in user is an assistant, department field is a
            // select list  with the assistant's departments
            let role = get(field, 'session.session.authenticated.role');
            if (role == 'assistant') {
              let deps = get(field, 'session.session.authenticated.departments');
              let promises = deps.map((id) => {
                return store.findRecord('department', id);
              })

              var promise = Ember.RSVP.all(promises).then((res) => {
                return res;
              }, (error) => {
                return [];
              });

              return DS.PromiseArray.create({
                promise : promise
              })
            }

            // on load sort by title
            let locale = get(table, 'i18n.locale');
            let ordering_param = {
              ordering: `title__${locale}`
            };
            let query;
            // If the logged in user is an institutionmanager, department field
            // is a select list with all the deparments that belong to the
            // institutionmanager's institution
            if (role == 'institutionmanager') {
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
    }, {
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
              autocomplete: true,
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
        field('type_verbose', {label: 'type.label', type: 'text', dataKey: 'type'}),
        'members_count'
      ],
      actions: ['gen:details', 'gen:edit', 'remove']
    }
  },

  details: {
    getModel: function(params, model) {
      return preloadRelations(model, 'department', 'department.institution');
    },
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
        'type',
        'members_count'
      ],
      layout: {
        flex: [50, 50, 50, 50]
      }
    }, {
      label: 'registry_set_decision_file',
      fields: [
      fileField('registry_set_decision_file', 'registry', 'registry_set_decision_file',
        { readonly: true, label: null })
      ]
    }, {
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
      return preloadRelations(model, 'department', 'members', 'department.institution');
    },
    onSubmit(model) {
      this.refresh();
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
        disable_field('type'),
        disable_field('members_count')
      ],
      layout: {
        flex: [50, 50, 50, 50]
      }
    }, {
      label: 'registry_set_decision_file',
      fields: [
      fileField('registry_set_decision_file', 'registry', 'registry_set_decision_file',
        { label: null }, { replace: true, preventDelete: true })
      ]
    }, {
      label: 'registry.members_section.title',
      fields: [membersField(true, true, false)]
    }]
  }
});
