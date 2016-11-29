/* jshint node: true */
var choices = require('../../resources/www/common');
var holidays = require('../../resources/www/holidays');
const PERMISSIONS = require('../../resources/permissions');

PERMISSIONS['positions']['destroy'] = {'institutionmanager': { '*': { 'superuser': '4.5.6' } } };

module.exports = function(environment) {
  var ENV = {
    modulePrefix: 'ui',
    environment: environment,
    rootURL: '/apella/ui/',
    locationType: 'auto',
    i18n : {
      defaultLocale: 'el',
      locales: ['el', 'en']
    },
    EmberENV: {
      FEATURES: {
        // Here you can enable experimental features on an ember canary build
        // e.g. 'with-controller': true
      },
      EXTEND_PROTOTYPES: {
        // Prevent Ember Data from overriding Date.parse.
        Date: false
      }
    },

    APP: {
      backend_host: 'http://127.0.0.1:8000/apella/api',
      resource_choices: choices,
      resource_holidays: holidays,
      date_format: 'DD , MMMM YYYY',
      // Here you can pass flags/options to your application instance
      // when it is created
    },
  };

  ENV['ember-gen'] = {
    permissions: PERMISSIONS
  },

  ENV['ember-simple-auth'] = {
    authenticationRoute: 'auth.index',
    authorizer: 'authorizer:token',
  };

  ENV['ember-simple-auth-token'] = {
    serverTokenEndpoint: ENV.APP.backend_host + '/auth/login/',
    identificationField: 'username',
    passwordField: 'password',
    tokenPropertyName: 'auth_token',
    authorizationPrefix: 'Token ',
    authorizationHeaderName: 'Authorization',
    headers: {},
  };

  if (environment === 'development') {
    ENV['ember-cli-mirage'] = {
        enabled: false
    }
    // ENV.APP.LOG_RESOLVER = true;
    // ENV.APP.LOG_ACTIVE_GENERATION = true;
    // ENV.APP.LOG_TRANSITIONS = true;
    // ENV.APP.LOG_TRANSITIONS_INTERNAL = true;
    // ENV.APP.LOG_VIEW_LOOKUPS = true;
  }

  if (environment === 'test') {
    // Testem prefers this...
    ENV.locationType = 'none';

    // keep test console output quieter
    ENV.APP.LOG_ACTIVE_GENERATION = false;
    ENV.APP.LOG_VIEW_LOOKUPS = false;

    ENV.APP.rootElement = '#ember-testing';
  }

  if (environment === 'production') {

  }

  return ENV;
};
