import gen from 'ember-gen/lib/gen';

export default gen.CRUDGen.extend({
  modelName: 'institution',
  list: {
    row: {
      icon: 'location_city',
    }
  },
});
