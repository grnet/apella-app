import gen from 'ember-gen/lib/gen';

export default gen.CRUDGen.extend({
  modelName: 'subject',
  common: {
    menu: {
      icon: 'local_library'
    }
  }
});
