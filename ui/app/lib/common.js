import Ember from 'ember';
import {CRUDGen} from 'ember-gen/lib/gen';
import ENV from 'ui/config/environment';
import {field} from 'ember-gen/lib/util';

const {
  get,
  computed: { reads },
  computed,
  merge
} = Ember;

const ApellaGen = CRUDGen.extend({
  auth: true,
  resourceName: reads('path'),
  list: {
    sort: {
      serverSide: true,
      active: true
    },
    paginate: {
      limits: [10, 40, 100],
      serverSide: true,
      active: true
    }
  }
});

// a `field` wrapper which automatically sets sortKey/dataKey and formComponent for 
// i18n fields.
function i18nField(key, attrs) {
  attrs = attrs || {};
  return field(`${key}_current`, merge({ 
    _services: ['i18n'],
    sortKey: computed('i18n.locale', function() {
      let locale = get(this, 'i18n.locale');
      return `${key}.${locale}`;
    }),
    dataKey: key,
    formComponent: 'i18n-input-field'
  }, attrs));
}

// a `field` wrapper for computed properties related fields
function computedField(key, dependency, attrs) {
  attrs = attrs || {};
  return field(key, merge({
    sortKey: dependency,
    dataKey: dependency,
    readonly: true
  }, attrs));
}

export {
  ApellaGen, i18nField, computedField
};

