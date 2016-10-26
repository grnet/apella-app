import gen from 'ember-gen/lib/gen';
import validate from 'ember-gen/validate';
import {i18nValidate} from 'ui/validators/i18n';
import {field} from 'ember-gen';

const {
  computed,
  get
} = Ember;


export default gen.CRUDGen.extend({
  modelName: 'institution',
  path: 'institutions',
  common: {
    validators: {
      title: [i18nValidate([validate.presence(true), validate.length({min:4, max:50})])],
      organization: [validate.format({allowBlank: true, type: 'url'})],
      regulatory_framework: [validate.format({allowBlank: true, type: 'url'})],
    }
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
    fields: ['title_current', 'organization', 'regulatory_framework'],
    row: {
      actions: ['gen:details', 'gen:edit', 'remove']
    },
  },
  create: {
    fields: ['title', 'organization', 'regulatory_framework'],
  },
  edit: {
    fields: ['title', 'organization', 'regulatory_framework'],
  },
  record: {
    menu: {
      label: computed('model.id', function() {
        return get(this, 'model.id');
      })
    }
  }
});
