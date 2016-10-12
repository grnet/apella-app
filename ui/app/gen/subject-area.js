import gen from 'ember-gen/lib/gen';

export default gen.CRUDGen.extend({
  modelName: 'subject_area',
  common: {
    menu: {
      icon: 'school',
      label: 'subject_area.menu_label'
    }
  },
  list: {
    tableLayout: true,
    selectable: true,
    page: {
      title: 'subject_area.menu_label',
    }
  },
  create: {
    page: {
      title: 'subject_area.create_title',
    }
  }
});
