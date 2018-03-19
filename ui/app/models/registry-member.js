import Professor from 'ui/models/professor';
import DS from 'ember-data';


/*
 * Hacky manipulation of registry-member model:
 *
 * When a new registry-member is created we need to send only `registry_id`
 * and `professor_id`.
 * When registy-members are fetched we keep only professor related data
 * as if we had a `professor` model.
 * There is no update action for registry-members.
 *
 * */

export default Professor.extend({
  registry_id: DS.attr(),
  professor_id: DS.attr(),

  __api__: {
    serialize(snapshot, options) {
      let registry_id = snapshot.registry_id;
      let professor_id = snapshot.professor_id;
      return {
        registry_id,
        professor_id
      }
    },

    normalize: function(hash, serializer) {
      // keep only id, professor and nested user information
      let id = hash.id;
      var user_tmp = hash['professor'].user;
      hash = hash['professor'];

      let user_info = user_tmp;
      Object.keys(user_info).forEach(function(key){
        if (key == 'id') {
          hash['user_id'] = user_info['id']
        } else {
          hash[key] = user_info[key]
        }
      });

      hash.cv_in_url = false;
      if (hash.cv_url && hash.cv_url.length > 0) {
        hash.cv_in_url = true;
      }
      delete hash['user'];
      hash['id'] = id;
      return hash;
    },
  },

});
