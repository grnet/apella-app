import gen from 'ember-gen/lib/gen';

export default gen.CRUDGen.extend({
  modelName: 'institution',
  common: {
    menu: {
      icon: 'location_city',
      label: 'institution.menu_label'
    }
  },
});
