import {ApellaGen} from 'ui/lib/common';
import gen from 'ember-gen/lib/gen';
import {field} from 'ember-gen';
import _ from 'lodash/lodash'
import Users  from 'ui/gen/user';

let {
  computed, get
} = Ember;

export default ApellaGen.extend({
  order: 1000,
  modelName: 'registry',
  auth: true,
  path: 'registries',

  abilityStates: {
    // resolve ability for position model
    owned: computed('role', function() {
      return get(this, 'role') === 'institutionmanager';
    }) // we expect server to reply with owned resources
  },

  common: {
    fieldsets: [{
      label: 'registry.main_section.title',
      fields: [field('type', {label: 'common.type_label'}),
        field('department', {
          displayAttr: 'title_current',
          query: function(table, store, field, params) {
            params = params || {};
            let role = get(field, 'session.session.authenticated.role');
            if (role == 'institutionmanager' || role == 'assistant') {
              let user_institution = get(field, 'session.session.authenticated.institution');
              let id = user_institution.split('/').slice(-2)[0];
              params.institution = id;
            }
            return store.query('department', params);
          }
        })
      ],
      layout: {
        flex: [30, 70]
      }
    },{
      label: 'registry.members_section.title',
      fields: [field('members', { label: null,
        modelMeta: {
          filter: {
            active: false,
            search: true,
            searchFields: ['last_name_current']
          },
          sort: {
            active: true,
            sortBy: 'last_name_current'
          },
          paginate: {
            active: true
          },
          row: {
            fields: ['id', 'last_name_current', 'first_name_current', 'email', 'institution.title_current', 'department.title_current', 'rank']
          }
        }
      })]
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
