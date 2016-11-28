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
        modelMeta: { search: { fields: ['username'] }, sortBy: ['username'], row: { fields: ['id', 'username', 'email'] } } })]
    }]
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
  record: {
    menu: {
      label: computed('model.id', function() {
        return get(this, 'model.id');
      })
    },
  }
});
