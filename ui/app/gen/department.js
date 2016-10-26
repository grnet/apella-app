import gen from 'ember-gen/lib/gen';
import {field} from 'ember-gen';
import validate from 'ember-gen/validate';
import {i18nValidate} from 'ui/validators/i18n';

const {
  get,
  computed
} = Ember;

export default gen.CRUDGen.extend({
  modelName: 'department',
  path: 'departments',
  common: {
    validators: {
      title: [i18nValidate([validate.presence(true), validate.length({min:4, max:50})])],
    }
  },
  list: {
    menu: {
      icon: 'domain',
      label: 'department.menu_label'
    },
    page: {
      title: 'department.menu_label',
    },
    layout: 'table',
    sortBy: 'title_current:asc',
    fields: ['title_current', field('school.title_current', {label: 'school.label', type: 'text'})],
    row: {
      actions: ['gen:details', 'gen:edit', 'remove']
    }
  },
  record: {
    menu: {
      label: computed('model.id', function() {
        return get(this, 'model.id');
      })
    }
  }
});
