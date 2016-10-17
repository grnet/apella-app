import gen from 'ember-gen/lib/gen';

export default gen.CRUDGen.extend({
  modelName: 'subject',
  path: 'subjects',
  common: {
    menu: {
      icon: 'local_library',
      label: 'subject.menu_label'
    }
  },
  list: {
    tableLayout: true,
    selectable: true,
    fields: ['title', 'area.title'],
    page: {
      title: 'subject.menu_label',
    }
  },
  create: {
    page: {
      title: 'subject.create_title',
    }
  }
});
