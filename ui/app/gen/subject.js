import gen from 'ember-gen/lib/gen';

export default gen.CRUDGen.extend({
  modelName: 'subject',
  common: {
    menu: {
      icon: 'local_library',
      label: 'subject.menu_label'
    }
  },
  list: {
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
