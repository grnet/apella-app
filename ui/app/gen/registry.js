import {
  ApellaGen, i18nField, i18nUserSortField, i18nUserSortAttr, get_registry_members
} from 'ui/lib/common';
import gen from 'ember-gen/lib/gen';
import {field} from 'ember-gen';
import _ from 'lodash/lodash'
import Users  from 'ui/gen/user';
import {goToDetails} from 'ui/utils/common/actions';

let {
  computed, get, assign
} = Ember;


const membersField = field('members', {
  valueQuery: function(store, params, model, value) {
    return get_registry_members(model, store, params);
  },
  query: function(table, store, field, params) {
    let locale = get(table, 'i18n.locale'),
      default_ordering_param = {
        ordering: 'user__id'
      },
      query = (params.ordering ? params : assign({}, params, default_ordering_param));
    return store.query('professor', query);
  },
  // a list-like gen config
  label: null,
  modelMeta: {
    row: {
      fields: [
        field('user_id', {type: 'string'}),
//        field('last_name_current', {label: 'last_name.label', dataKey: 'user__last_name_current'}),
        i18nUserSortField('last_name', {label: 'TEST'}),
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
      serverSide: true,
      limits: [5, 10, 15]
    },
    filter: {
      search: true,
      searchPlaceholder: 'search.placeholder_last_name',
      serverSide: true,
      active: true,
      meta: {
        fields: [field('user_id', {type: 'string'})]
      }
    },
    sort: {
      serverSide: true,
      active: true,
      fields: ['user_id', computed('i18n.locale', function() {
        console.log('LOCALE', get(this, 'i18n.locale'))
        return 'user__last_name__el';
      })]
    },
  },
  modelName: 'professor',
  displayComponent: 'gen-display-field-table'
});


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

  common: {
    fieldsets: [{
      label: 'registry.main_section.title',
      fields: [field('type', {label: 'common.type_label'}),
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
      fields: [membersField]
    }]
  },

  create: {
    onSubmit(model) {
      this.transitionTo('registry.record.index', model);
    }
  },

  list: {
    menu: {
      icon: 'view list',
      label: 'registry.menu_label'
    },
    layout: 'table',
    sortBy: 'institution.title:asc',
    page: {
     title: 'registry.menu_label'
    },
    filter: {
      active: true,
      meta: {
        fields: ['type', 'department']
      },
      serverSide: true,
      search: false,
    },

    row: {
      fields: [
        field('institution.title_current', {label: 'institution.label', type: 'text'}),
        field('department.title_current', {label: 'department.label', type: 'text'}),
        field('type_verbose', {label: 'common.type_label', type: 'text'})
      ],
      actions: ['gen:details', 'gen:edit', 'remove']
    }
  },
  details: {
    page: {
      title: computed.readOnly('model.id')
    }
  }
});
