import gen from 'ember-gen/lib/gen';
import {field} from 'ember-gen';

export default gen.CRUDGen.extend({
  modelName: 'registry',
  path: 'registries',

  common: {
    menu: {
      icon: 'view list',
      label: 'registry.menu_label'
    }
  },
  list: {
    layout: 'table',
    sortBy: 'institution.title:asc',
    page: {
     title: 'registry.menu_label'
    },
    fields: [
      field('institution.title', {label: "institution.label", type: 'text'}),
      field('department.title', {label: 'department.label', type: 'text'}),
      field('type_verbose', {label: 'general.type_label', type: 'text'})
    ],
    row: {
      actions: ['details', 'edit', 'remove']
    }
  },
  create: {
    page: {
      title: 'general.create_label'
    },
    fieldsets: [{
      label: 'registry.main_section.title',
      fields: [field('type', {label: 'general.type_label'}), 'department'],
      layout: {
        flex: [30, 70]
      }
    },{
      label: 'registry.members_section.title',
      fields: ['members']
    }]
  }
});
