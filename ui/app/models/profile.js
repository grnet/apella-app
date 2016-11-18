import DS from 'ember-data';
import User from 'ui/models/user';
import professorFields from 'ui/mixins/professor';
import {normalizeUser, serializeUser, normalizeUserErrors} from 'ui/utils/common/users';
import institutionManagerFields from 'ui/mixins/institution-manager';

const { get } = Ember;

export default User.extend(professorFields, institutionManagerFields, {
  __api__: {
    namespace: 'auth',
    path: 'me',
    // always return my profile endpoint
    buildURL: function(adapter, url, id, snap, rtype, query) {
      let host = get(adapter, 'host'),
          namespace = get(this, 'namespace'),
          path = get(this, 'path');

      return this.urlJoin(host, namespace, path) + '/';
    },
    normalizeErrors: normalizeUserErrors,
    normalize: normalizeUser,
    serialize: serializeUser
  },
});
