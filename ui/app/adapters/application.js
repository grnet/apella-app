import BaseAdapter from 'ember-gen-apimas/adapters/application';

export default BaseAdapter.extend({
  urlForQuery(query, modelName) {
     /*
      * For urls in form: modelName/id/relatedModel we use a flag like "history"
      * or "registry_members" and we tranform properly the request.
      *
      * Use to get resources history:
      * store.query(modelName, {id:id, history:true} will result in the call
      * /<modelName>/<id>/history
      */
     if (query.history) {
       Ember.assert('Both query history and query id must be set', query.history && query.id)
       let id = query.id;
       delete query['id'];
       delete query['history'];
       return this.buildURL(modelName, id) + 'history';
     }
      /*
      * Use to get registry members:
      * store.query(modelName, {id:id, registry_members:true} will result in the call
      * /registry/<id>/members
      */
     else if (query.registry_members) {
       Ember.assert('Both registry_members flag and registry id must be set', query.registry_members && query.id);
       let id = query.id,
         modelName = 'registry';
       delete query['id'];
       delete query['registry_members'];
       return this.buildURL(modelName, id) + 'members';
     }
     return this._super(...arguments)
   }
});
