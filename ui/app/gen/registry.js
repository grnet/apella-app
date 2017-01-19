import {
  ApellaGen, i18nField, i18nUserSortField, get_registry_members
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


let memberQuickDetailsFieldsets = [
  {
    label: null,
    fields: [
      field('user_id', {type: 'string', dataKey: 'user__id'}),
      i18nUserSortField('last_name', {label: 'last_name.label'}),
      i18nField('first_name', {label: 'first_name.label'}),
      'is_foreign_descr',
      field('institution_global', {label: 'institution.label'}),
      i18nField('department.title', {label: 'department.label'}),
      'rank',
      'discipline_text'
    ],
    layout: {
      flex: [100, 100, 100, 100, 100, 100, 100, 100, 100]
    }
  }
];

// serverSide is a boolean value that is used for filtering, sorting, searching
function membersAllModelMeta(serverSide) {
   let sortFields = (serverSide ? ['user_id', 'last_name_current'] : ['user_id', 'last_name_el', 'last_name_en']);
  /*
   * For now, hide the client side filtering, searching, ordering because these
   * functionalities are not yet developed.
   * TODO: Remove this code when client side functionalities are developed
   */
  let display = serverSide;
  return {
    row: {
      fields: [
        field('user_id', {type: 'string', dataKey: 'user__id'}),
        i18nUserSortField('last_name', {label: 'last_name.label'}),
        i18nField('first_name', {label: 'first_name.label'}),
        i18nField('department.title', {label: 'department.label'}),
      ],
      actions: ['view_details'],
      actionsMap: {
        view_details: {
          icon: 'open_in_new',
          detailsMeta: {
            fieldsets: memberQuickDetailsFieldsets
          },
          action: function() {},
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
      limits: [5, 10, 15]
    },
    filter: {
      search: display,
      searchPlaceholder: 'search.placeholder_last_name',
      serverSide: serverSide,
      active: display,
      meta: {
        fields: [field('user_id', {type: 'string'})]
      }
    },
    sort: {
      serverSide: serverSide,
      active: display,
      fields: sortFields
    }
  };
};

function membersField(modelMetaSide, selectModelMetaSide) {
  return field('members', {
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
    modelMeta: membersAllModelMeta(modelMetaSide),
    selectModelMeta: membersAllModelMeta(selectModelMetaSide),
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
        user_institution_id = get(this, 'user.institution').split('/').filter(v => v!=="").get('lastObject');
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
          user_institution_id = get(this, 'user.institution').split('/').filter(v => v!=="").get('lastObject'),
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
        flex: [30, 70]
      }
    },{
      label: 'registry.members_section.title',
      fields: [membersField(false, true)]
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
      limits: [5, 15, 20]
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
      fields: ['id', 'type_verbose', 'institution.title_current', 'department.title_current']
    },
    row: {
      fields: [
        'id',
        field('institution.title_current', {label: 'institution.label', type: 'text'}),
        field('department.title_current', {label: 'department.label', type: 'text'}),
        field('type_verbose', {label: 'type.label', type: 'text'})
      ],
      actions: ['gen:details', 'gen:edit', 'remove']
    }
  },

  details: {
    page: {
      title: computed.readOnly('model.id')
    },
    fieldsets: [{
      label: 'registry.main_section.title',
      fields: [
        i18nField('department.title'),
        'type'
      ],
      layout: {
        flex: [30, 70]
      }
    },{
      label: 'registry.members_section.title',
      fields: [membersField(true, true)]
    }]
  },
  edit: {
    fieldsets: [{
      label: 'registry.main_section.title',
      fields: [
        disable_field('department', {displayAttr: 'title_current'}),
        disable_field('type')
      ],
      layout: {
        flex: [30, 70]
      }
    },{
      label: 'registry.members_section.title',
      fields: [membersField(false, true)]
    }]
  }
});
