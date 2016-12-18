import gen from 'ember-gen/lib/gen';
import validate from 'ember-gen/validate';
import {i18nValidate} from 'ui/validators/i18n';
import {field} from 'ember-gen';
import {ApellaGen, i18nField, computedField} from 'ui/lib/common';

const {
  computed,
  get
} = Ember;


let FS = {
  list: [
    i18nField('title'),
    computedField('category_verbose', 'category'),
    'organization',
    'regulatory_framework'
  ]
};


export default ApellaGen.extend({
  modelName: 'institution',
  auth: true,
  path: 'institutions',

  common: {
    validators: {
      title: [i18nValidate([validate.presence(true), validate.length({min:4, max:200})])],
      organization: [validate.format({allowBlank: true, type: 'url'})],
      regulatory_framework: [validate.format({allowBlank: true, type: 'url'})],
    }
  },

  abilityStates: {
    owned: computed('role', function() {
      return get(this, 'role') === 'institutionmanager';
    }) // we expect server to reply with owned resources
  },

  list: {
    page: {
      title: 'institution.menu_label',
    },
    menu: {
      icon: 'location_city',
      label: 'institution.menu_label'
    },
    sort: {
      active: true,
      serverSide: true,
      fields: ['title']
    },
    layout: 'table',
    row: {
      fields: FS.list,
      actions: ['gen:details', 'gen:edit', 'remove']
    },
  },

  details: {
    page: {
      title: computed.readOnly('model.title_current'),
    },
    fieldsets: [{
        layout: {
          flex: [100, 20, 40, 40]
        },
        fields: ['title_current', 'category_verbose', 'organization', 'regulatory_framework']
    }]
  }
});
