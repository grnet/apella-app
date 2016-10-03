import gen from 'ember-gen/lib/gen';

export default gen.CRUDGen.extend({
  modelName: 'department',
  common: {
    menu: {
      icon: 'domain',
      label: 'department.menu_label'
    }
  }
});
