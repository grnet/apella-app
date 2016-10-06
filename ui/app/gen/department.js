import gen from 'ember-gen/lib/gen';

export default gen.CRUDGen.extend({
  modelName: 'department',
  common: {
    menu: {
      icon: 'domain',
      label: 'department.menu_label'
    }
  },
  list: {
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
