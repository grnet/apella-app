import gen from 'ember-gen/lib/gen';
import validate from 'ember-gen/validate';

export default gen.CRUDGen.extend({
  modelName: 'department',
  path: 'departments',
  common: {
    menu: {
      icon: 'domain',
      label: 'department.menu_label'
    },
    validators: {
      title: [validate.presence(true), validate.length({min:4, max:50})],
    }
  },
  list: {
    layout: 'table',
    sortBy: 'title:asc',
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
