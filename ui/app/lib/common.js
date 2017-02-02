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
  assign
} = Ember;

const ApellaGen = CRUDGen.extend({
  auth: true,
  _metaMixin: {
    session: Ember.inject.service(),
    role: reads('session.session.authenticated.role')
  },
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

// a `field` wrapper for computed properties related fields
function computedField(key, dependency, attrs) {
  attrs = attrs || {};
  return field(key, merge({
    sortKey: dependency,
    dataKey: dependency,
    readonly: true
  }, attrs));
}

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
    message: 'It should start with http or https'})
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
    return '-';
  }),
});

function fileField(key, path, kind, attrs, formAttrs) {
  return field(key, assign({}, {
    type: 'file',
    formComponent: 'apella-file-field',
    displayComponent: 'apella-file-field',
    displayAttrs: assign({hideLabel: true}, { path, kind }, formAttrs || {}),
    formAttrs: assign({}, { path, kind }, formAttrs || {})
  }, attrs || {}));
}

function get_registry_members(registry, store, params) {
  let registry_id = registry.get('id'),
    query = assign({}, params, { id: registry_id, registry_members: true});

  return store.query('professor', query);
};

export {
  ApellaGen, i18nField, computedField, computeI18N, computeI18NChoice,
  booleanFormat, computeDateFormat, computeDateTimeFormat, urlValidator,
  VerifiedUserMixin, fileField, i18nUserSortField, get_registry_members
};

