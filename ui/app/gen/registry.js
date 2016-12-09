import {ApellaGen} from 'ui/lib/common';
import gen from 'ember-gen/lib/gen';
import {field} from 'ember-gen';
import _ from 'lodash/lodash'
import Users  from 'ui/gen/user';

let {
  computed, get
} = Ember;

export default ApellaGen.extend({
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
      fields: [field('type', {label: 'common.type_label'}), field('department', {displayAttr: 'title_current'})],
      layout: {
        flex: [30, 70]
      }
    },{
      label: 'registry.members_section.title',
      fields: [field('members', { label: null,
        modelMeta: { search: { fields: ['id', 'last_name_current', 'first_name_current', 'email'] }, sortBy: ['last_name_current'], row: { fields: ['id', 'last_name_current', 'first_name_current', 'email', 'institution.title_current', 'department.title_current', 'rank'] } } })]
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
