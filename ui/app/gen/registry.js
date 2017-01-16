import {
  ApellaGen, i18nField, i18nUserSortField, i18nUserSortAttr, get_registry_members
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


// serverSide is a boolean value that is used for filtering, sorting, searching
function membersAllModelMeta(serverSide) {
  console.log('serverSide', serverSide)
     // TMP: user__last_name__el
    let sortFields = (serverSide ? ['user_id', 'last_name_current'] : ['user_id', 'user__last_name__el']);

  return {
    row: {
      fields: [
        field('user_id', {type: 'string', dataKey: 'user__id'}),
        i18nUserSortField('last_name', {label: 'last_name.label'}),
        i18nField('first_name', {label: 'first_name.label'}),
        'is_foreign_descr',
        i18nField('institution.title', {label: 'institution.label'}),
        i18nField('department.title', {label: 'department.label'}),
        'rank',
        'discipline_text'
      ],
      actions: ['goToDetails'],
      actionsMap: {
        goToDetails: goToDetails
      }
    },
    paginate: {
      active: true,
      serverSide: serverSide,
      limits: [5, 10, 15]
    },
    filter: {
      search: true,
      searchPlaceholder: 'search.placeholder_last_name',
      serverSide: serverSide,
      active: true,
      meta: {
        fields: [field('user_id', {type: 'string'})]
      }
    },
    sort: {
      serverSide: serverSide,
      active: true,
      /*fields: ['user_id', computed('i18n.locale', function() {
        console.log('LOCALE', get(this, 'i18n.locale'))
        let a = ['user__last_name__el', {_services: ['i18n']}];
        return 'user__last_name__el';
      })]*/
      fields: sortFields
    }
  };
};

function membersField(modelMetaSide, selectModelMetaSide) {
  return field('members', {
    valueQuery: function(store, params, model, value) {

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
    // resolve ability for position model
    owned: computed('role', function() {
      return get(this, 'role') === 'institutionmanager';
    }), // we expect server to reply with owned resources
    can_create: computed('user.can_create_registries', function() {
      return get(this, 'user.can_create_registries');
    })
  },

  create: {
    onSubmit(model) {
      this.transitionTo('registry.record.index', model);
    },
    fieldsets: [{
      label: 'registry.main_section.title',
      fields: [field('type', {label: 'type.label'}),
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
        })
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
    layout: 'table',
    page: {
      title: 'registry.menu_label'
    },
    filter: {
      search: false,
      serverSide: true,
      active: true,
      meta: {
        fields: [field('id', {type: 'string'}), 'type', 'institution']
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
      fields: ['type',
        i18nField('department.title'),
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
        disable_field('type'),
        disable_field('department', {displayAttr: 'title_current'}),
      ],
      layout: {
        flex: [30, 70]
      }
    },{
      label: 'registry.members_section.title',
      fields: [membersField(true, true)]
    }]
  }
});
