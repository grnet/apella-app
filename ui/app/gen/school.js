import gen from 'ember-gen/lib/gen';

export default gen.CRUDGen.extend({
  modelName: 'school',
  common: {
    menu: {
      icon: 'account_balance',
      label: 'school.menu_label'
    }
  },
  list: {
    page: {
      title: 'school.menu_label',
    }
  },
  create: {
    page: {
      title: 'school.create_title'
    },
  },
});
