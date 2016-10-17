import gen from 'ember-gen/lib/gen';

export default gen.CRUDGen.extend({
  modelName: 'department',
  path: 'departments',
  common: {
    menu: {
      icon: 'domain',
      label: 'department.menu_label'
    }
  },
  list: {
    tableLayout: true,
    selectable: true,
    fields: ['title', 'school.title'],
    page: {
      title: 'department.menu_label',
    }
  },
  create: {
    page: {
      title: 'department.create_title'
    },
  }
});
