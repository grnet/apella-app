import Ember from 'ember';
import DS from 'ember-data';
import {CRUDGen} from 'ember-gen/lib/gen';
import ENV from 'ui/config/environment';
import {field} from 'ember-gen/lib/util';
import moment from 'moment';
import validate from 'ember-gen/validate';
import _ from 'lodash/lodash';


const {
  get,
  computed: { reads },
  computed,
  merge,
  assign,
  assert,
  inject
} = Ember;

// A route mixin which should apply for all authenticated routes. Handles
// cross app things such as non accepted terms.
const UserConstraintsRouteMixin = {
  messageService: inject.service('messages'),
  beforeModel(transition) {
    let session = get(this, 'session');
    if (get(session, 'isAuthenticated')) {
      let profile = get(session, 'session.authenticated');
      let set_academic = get(profile, 'can_set_academic');
      let has_accepted_terms = get(profile, 'has_accepted_terms');
      let isProfile = get(transition, 'targetName') === 'auth.profile';
      let isContact = get(transition, 'targetName').includes('jira-issue');
      if ((set_academic || !has_accepted_terms) && !isProfile && !isContact) {
        transition.abort();
        return this.transitionTo('auth.profile');
      }
    }
    return this._super(transition);
  }
}

const ApellaGen = CRUDGen.extend({
  auth: true,
  _metaMixin: {
    session: Ember.inject.service(),
    role: reads('session.session.authenticated.role')
  },
  routeMixins: [UserConstraintsRouteMixin],
  resourceName: reads('path'),
  list: {
    layout: 'table',
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

const DATE_FORMAT = ENV.APP.date_format,
      DATE_TIME_FORMAT = ENV.APP.date_time_format;

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
    filterKey: reads('sortKey'),
    dataKey: key,
    formComponent: 'i18n-input-field'
  }, attrs));
}

function i18nUserSortField(key, attrs) {
  attrs = attrs || {};
  return field(`${key}_current`, merge({
    _services: ['i18n'],
    sortKey: computed('i18n.locale', function() {
      let locale = get(this, 'i18n.locale'),
        dataKey = `user__${key}__${locale}`;
      return dataKey;
    }),
    formComponent: 'i18n-input-field'
  }, attrs));
};

function computeI18N(key, ...args) {
  let hook, lastArg = args[args.length - 1];
  if (typeof lastArg === 'function') { hook = args.pop(); }
  return computed(key, 'i18n.locale', ...args, function() {
    let activeLang = get(this, 'i18n.locale');
    let value = get(this, key);
    if (hook) { return hook.apply(this, [value, activeLang]); }
    return value && value[activeLang];
  });
}

function computeI18NChoice(key, choices, ...args) {
  /*
   * This is very hacky. It's used to create a model for the substitute
   * institution manager *only in the UI*. We cannot add this as a role in
   * resources/common.json because that file is used in the backend, too.
   */
  if(key === 'role') {
    let flat_choices = _.flatten(choices),
      substitute_institution_manager = ['sub_institution_manager', 'Substitute Institution Manager'];
    if(!flat_choices.includes('sub_institution_manager')) {
      choices.pushObject(substitute_institution_manager)
    }
  }
  let hook, lastArg = args[args.length - 1];
  if (typeof lastArg === 'function') { hook = args.pop(); }
  let choicesValues = choices.map((key) => key[0]);

  return computed(key, 'i18n.locale', ...args, function() {
    let i18n = get(this, 'i18n');
    let value = get(this, key);
    let i18nKey = '';
    if (choicesValues.indexOf(value)>=0) {
      i18nKey = choices[choicesValues.indexOf(value)][1];
    }
    return value && i18nKey && i18n.t(i18nKey);
  });
}

function computeDateFormat(key) {
  return computed(key, function() {
    let date = get(this, key)
    return date ? moment(date).format(DATE_FORMAT) : '-';
  });
};

function computeDateTimeFormat(key) {
  return computed(key, function() {
    let date = get(this, key)
    return date ? moment(date).format(DATE_TIME_FORMAT) : '';
  });
};


function booleanFormat(key) {
  return computed(key, function(){
    let value = get(this, key);
    return value? '✓':'-';
  })
}

const urlValidator = [
  validate.format({type:'url'}),
  validate.format({
    regex: /^(https:\/\/|http:\/\/)/i,
    message: 'urlStarts.message'})
]

const VerifiedUserMixin = Ember.Mixin.create({
  is_verified: DS.attr('boolean'),
  verified_at: DS.attr('date'),
  verification_request: DS.attr('date'),
  verification_pending: DS.attr('boolean'),
  is_rejected: DS.attr('boolean'),
  rejected_reason: DS.attr('string'),
  changes_request: DS.attr('date'),
  status_verbose: computed('is_verified', 'is_rejected', 'verification_pending',  'i18n.locale', function() {
    if (get(this, 'is_rejected')) {
      return get(this, 'i18n').t('rejected');
    }
    if (get(this, 'is_verified')) {
      return get(this, 'i18n').t('verified');
    }
    if (get(this, 'verification_pending')) {
      return get(this, 'i18n').t('pending_verification');
    }
    return get(this, 'i18n').t('not_requested_verification');
  }),
});

function fileField(key, path, kind, attrs, formAttrs) {
  return field(key, assign({}, {
    type: 'file',
    formComponent: 'apella-file-field',
    displayComponent: 'apella-file-field',
    displayAttrs: assign({hideLabel: true}, { path, kind }, formAttrs || {}),
    sortBy: 'filename',
    formAttrs: assign({}, { path, kind }, formAttrs || {})
  }, attrs || {}));
}


function get_registry_members(registry, store, params) {
  let registry_id = registry.get('id'),
      query = assign({}, params, {registry_id: registry_id});
  let members = store.query('registry-member', query);
  return preloadRelations(members, 'department', 'institution');
}

function get_registry_members_for_position(registry, store, params) {
  let registry_id = registry.get('id'),
      query = assign({}, params, {registry_id: registry_id});
  let members = store.query('registry-member-position', query);
  return preloadRelations(members, 'department', 'institution');
}


// Helper to resolve model relations along with store query entries.
//
// Given a store.query result modify query promise in order to resolve
// after nested per per record relations are also resolved. After each
// nested relation is resolved the initial query result can be used in
// views, such as a list view, and be sure that all used nested relational
// data are preloaded and immediatelly accessible in templates.
function preloadRelations(model, ...keys) {

  let PromiseFactory = DS.PromiseArray.create.bind(DS.PromiseArray);

  if (!model.then) {
    if (model instanceof Array) {
      model = DS.PromiseArray.create({promise: Ember.RSVP.Promise.resolve(model)});
    } else {
      model = DS.PromiseObject.create({promise: Ember.RSVP.Promise.resolve(model)});
    }
  }

  if (model instanceof DS.PromiseObject) {
    PromiseFactory = DS.PromiseObject.create.bind(DS.PromiseObject);
  }

  let promise = model.then((arr) => {
    let resolved = arr;
    if (!(arr instanceof Array) && !(arr instanceof DS.AdapterPopulatedRecordArray)) {
      arr = [arr];
    }
    let promises = {};
    let nestedKeys = [];
    let rootKeys = [];

    keys.forEach((key) => {
      let refs = [];
      let isNested = key.indexOf('.') > -1;
      let attr = key;
      if (isNested) {
        let parts = key.split('.');
        attr = parts.slice(0, -1).join('.');
        key = parts[parts.length - 1];
        if (!nestedKeys[attr]) { nestedKeys[attr] = []; }
        nestedKeys[attr].push(key);
        return;
      }
      rootKeys.push(key);

      arr.map((entry) => {
        assert(`cannot preload '${key}' relationship. ${attr} not preloaded?`, entry);
        assert(`${entry} is not a DS.Model`, entry.belongsTo);

        let rel = entry.relationshipFor(key);
        let ref;
        if (rel.kind === 'belongsTo') {
          ref = entry.belongsTo(key).link();
        } else {
          ref = entry.hasMany(key).link();
        }
        if (!promises[key]) { promises[key] = []; }
        if (!ref) { promises[key].push(get(entry, key)); }
        if (ref && refs.indexOf(ref) === -1) {
          promises[key].push(get(entry, key));
          refs.push(ref);
        }
      });
    });

    return Ember.RSVP.Promise.all(rootKeys.map((key) => {
      if (!promises[key]) { return Ember.RSVP.Promise.resolve(); }
      return Ember.RSVP.Promise.all(promises[key]).then((resolved) =>  {
        if (nestedKeys[key] && nestedKeys[key].length) {
          return preloadRelations(Ember.RSVP.Promise.resolve(resolved), ...nestedKeys[key]).then(() => {
            return model;
          });
        } else {
          return model;
        }
      }, (error) => {
        return model;
      });
    })).then(() => { return resolved });
  });

  return PromiseFactory({promise});
};


function emptyArrayResult(store, modelName) {
  let type = store.modelFor(modelName);
  let emptyResult = DS.AdapterPopulatedRecordArray.create({type});
  let promise = Ember.RSVP.resolve(emptyResult);

  return DS.PromiseArray.create({promise});
}

function prefixSelect(arr, prefix) {
  arr.map(function(el) {
    return el[1] = `${prefix}${el[1]}`;
  });
  return arr;
}


/*
 * Select filter with the items in the list sorted by title in
 * current language.
 */

function filterSelectSortTitles(modelName, dataKey) {
  return field(modelName, {
    query: function(select, store, field, params) {
      let locale = get(select, 'i18n.locale'),
        ordering_param = `title__${locale}`;
      params = params || {};
      params.ordering = ordering_param;

      return store.query(modelName, params);
    },
    autocomplete: true,
    dataKey: dataKey || modelName
  })
};

export {
  ApellaGen, i18nField, computeI18N, computeI18NChoice,
  booleanFormat, computeDateFormat, computeDateTimeFormat, urlValidator,
  VerifiedUserMixin, fileField, i18nUserSortField, get_registry_members,
  get_registry_members_for_position,
  preloadRelations, emptyArrayResult,
  prefixSelect, filterSelectSortTitles, UserConstraintsRouteMixin
};
