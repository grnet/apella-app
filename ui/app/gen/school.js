import gen from 'ember-gen/lib/gen';
import {field} from 'ember-gen';
import validate from 'ember-gen/validate';
import {i18nValidate} from 'ui/validators/i18n';

const {
  computed,
  get
} = Ember;

export default gen.CRUDGen.extend({
  modelName: 'school',
  path: 'schools',
  common: {
    validators: {
      title: [i18nValidate([validate.presence(true), validate.length({min:4, max:50})])]
    }
  },
  list: {
    page: {
      title: 'school.menu_label',
    },
    menu: {
      icon: 'account_balance',
      label: 'school.menu_label'
    },
    layout: 'table',
    row: {
      fields: ['title_current', field('institution.title_current', {label: 'institution.label', type: 'text'})],
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
