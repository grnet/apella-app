import Ember from 'ember';
import {CRUDGen} from 'ember-gen/lib/gen';
import ENV from 'ui/config/environment';
import {field} from 'ember-gen/lib/util';
import moment from 'moment';
import validate from 'ember-gen/validate';


const {
  get,
  computed: { reads },
  computed,
  merge
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
  let hook, lastArg = args[args.length - 1];
  if (typeof lastArg === 'function') { hook = args.pop(); }
  let choicesValues = choices.map((key) => key[0]);

  return computed(key, 'i18n.locale', ...args, function() {
    let i18n = get(this, 'i18n');
    let value = get(this, key);
    let i18nKey = choices[choicesValues.indexOf(value)][1];
    return value && i18nKey && i18n.t(i18nKey);
  });
}

function computeDateFormat(key) {
  return computed(key, function() {
    let date = get(this, key)
    return moment(date).format(DATE_FORMAT);
  });
};

function computeDateTimeFormat(key) {
  return computed(key, function() {
    let date = get(this, key)
    return moment(date).format(DATE_TIME_FORMAT);
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

export {
  ApellaGen, i18nField, computedField, computeI18N, computeI18NChoice,
  booleanFormat, computeDateFormat, computeDateTimeFormat, urlValidator
};

