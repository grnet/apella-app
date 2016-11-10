import DS from 'ember-data';

const { get } = Ember;

export default DS.Model.extend({
  __api__: {
    namespace: 'auth',
    path: 'me',
    // always return my profile endpoint
    buildURL: function(adapter, url, id, snap, rtype, query) {
      let host = get(adapter, 'host'),
          namespace = get(this, 'namespace'),
          path = get(this, 'path');

      return this.urlJoin(host, namespace, path) + '/';
    }
  },
  username: DS.attr(),
  email: DS.attr()
});
