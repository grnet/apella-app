import gen from 'ember-gen/lib/gen';

export default gen.CRUDGen.extend({
  modelName: 'subject_area',
  common: {
    menu: {
      icon: 'school',
    }
  },
});