import DS from 'ember-data';
import User from 'ui/models/user';
import professorFields from 'ui/mixins/professor';
import {normalizeUser, serializeUser, normalizeUserErrors} from 'ui/utils/common/users';
import institutionManagerFields from 'ui/mixins/institution-manager';
import assistantFields from 'ui/mixins/assistant';
import candidateFields from 'ui/mixins/candidate';
import {VerifiedUserMixin} from 'ui/lib/common';

const { get } = Ember;

const inherits = [
  candidateFields,
  professorFields,
  institutionManagerFields,
  assistantFields,
  VerifiedUserMixin
];

export default User.extend(...inherits, {
  userAdapter() {
    return get(this, 'store').adapterFor(get(this, 'role'));
  },

  userURL() {
    let id = get(this, 'user_id');
    let adapter = this.userAdapter();
    return adapter.buildURL(get(this, 'role'), id, 'findRecord');
  },

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
