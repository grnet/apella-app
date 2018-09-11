import RegistryMember from 'ui/models/registry-member';

export default RegistryMember.extend({
  __api__: {
    pathForType(){ return 'registry-members'},

    normalize: function(hash, serializer) {
      // keep only id, professor and nested user information
      let id = hash['professor'].id;
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
