import gen from 'ember-gen/lib/gen';
import validate from 'ember-gen/validate';
import {i18nValidate} from 'ui/validators/i18n';
import {field} from 'ember-gen';
import {ApellaGen, i18nField} from 'ui/lib/common';

const {
  computed,
  get
} = Ember;


let FS = {
  list: [
    i18nField('title'),
    'organization',
    'regulatory_framework'
  ],
  common:  ['title', 'organization', 'regulatory_framework']
};


export default ApellaGen.extend({
  order: 1300,
  modelName: 'institution',
  auth: true,
  path: 'institutions',

  common: {
    validators: {
      title: [i18nValidate([validate.presence(true), validate.length({min:3, max:200})])],
      organization: [validate.format({allowBlank: true, type: 'url'})],
      regulatory_framework: [validate.format({allowBlank: true, type: 'url'})],
    }
  },

  abilityStates: {
    owned: computed('role', 'user.institution.id', 'model.id', function() {
      let user_institution = get(this, 'user.institution');
      let user_institution_id = user_institution.split('/').slice(-2)[0];
      return get(this, 'role') === 'institutionmanager' &&
        user_institution_id === get(this, 'model.id');
    }) // we expect server to reply with owned resources
  },

  list: {
    getModel: function(params) {
      let store = get(this, 'store');
      params = params || {};
      // Default ordering
      if(!params.ordering) {
          let locale = get(this, 'i18n.locale');
          params.ordering = `title__${locale}`;
      }
      params['category'] = 'Institution';
      return store.query('institution', params)
    },
    page: {
      title: 'institution.menu_label',
    },
    menu: {
      icon: 'chrome_reader_mode',
      label: 'institution.menu_label'
    },
    sort: {
      active: true,
      serverSide: true,
      fields: ['title']
    },
    filter: {
      active: false,
      serverSide: true,
      search: true,
      searchFields: ['title']
    },
    layout: 'table',
    row: {
      fields: FS.list,
      actions: ['gen:details', 'gen:edit', 'remove'],
      actionsMap: {
        remove: {
          prompt: {
            ok: 'ok',
            cancel: 'cancel',
            title: 'prompt.removeInstitution.title',
            message: 'prompt.removeInstitution.message'
          }
        }
      },
    },
  },
  edit: {
    fields: FS.common,
  },
  details: {
    page: {
      title: computed.readOnly('model.title_current'),
    },
    fields: FS.list,
  }
});
