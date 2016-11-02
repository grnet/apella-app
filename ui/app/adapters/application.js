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

  action: function(model, action, method='POST') {
    let actionURL = this.urlForModel(model) + action + '/';
    return this.ajax(actionURL, method);
  }
});
