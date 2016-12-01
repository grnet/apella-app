import gen from 'ember-gen/lib/gen';
import validate from 'ember-gen/validate';
import {i18nValidate} from 'ui/validators/i18n';
import {field} from 'ember-gen';
import {ApellaGen} from 'ui/lib/common';

const {
  computed,
  get
} = Ember;


let FS = {
  list: [
    field('title_current', {dataKey: 'title'}), 
    field('category_verbose', {dataKey: 'category'}), 
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
      title: [i18nValidate([validate.presence(true), validate.length({min:4, max:50})])],
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
    sortBy: 'organization:asc',
    layout: 'table',
    paginate: {
      limit: [10, 15, 30]
    },
    row: {
      fields: FS.list,
      actions: ['gen:details', 'gen:edit', 'remove']
    },
  },

  details: {
    page: {
      title: computed.readOnly('model.title_current')
    }
  }
});
