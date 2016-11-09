import gen from 'ember-gen/lib/gen';
import validate from 'ember-gen/validate';
import {i18nValidate} from 'ui/validators/i18n';
import {field} from 'ember-gen';

const {
  computed,
  get
} = Ember;


let FS = {
  list: ['title_current', 'category_verbose', 'organization', 'regulatory_framework'],
};


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
    fields: FS.list,
    row: {
      actions: ['gen:details', 'gen:edit', 'remove']
    },
  },
  record: {
    menu: {
      label: computed('model.id', function() {
        return get(this, 'model.id');
      })
    }
  }
});
