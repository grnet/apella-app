import DS from 'ember-data';
import DRFAdapter from 'ember-django-adapter/adapters/drf';
import ENV from 'ui/config/environment';
import {apiFor, urlJoin} from 'ui/adapters/util';
import DataAdapterMixin from 'ember-simple-auth/mixins/data-adapter-mixin';


export default DRFAdapter.extend(DataAdapterMixin,{


	host: ENV.APP.backend_host,
	contentType: 'application/json',
	dataType: 'json',
  authorizer: 'authorizer:token',

  pathForType: function(type) {
    return apiFor(type, this).pathForType(this, type);
  },

	buildURL: function(modelName, id, snapshot, requestType, query) {
		var url = this._super(modelName, id, snapshot, requestType, query);
    return apiFor(modelName, this).buildURL(this, url, id, snapshot, requestType, query);
	},

  urlForModel: function(model) {
    let name = model.constructor.modelName;
    let id = model.get('id');
    return this.buildURL(name, id, {}, 'findRecord');
  },

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
      return this.buildURL(modelName, id)+'history';
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
      return this.buildURL(modelName, id)+'members';
    }
    return this._super(...arguments)
  },

  action: function(model, action, method='POST') {
    let actionURL = this.urlForModel(model) + action + '/';
    return this.ajax(actionURL, method);
  }
});
