import gen from 'ember-gen/lib/gen';
import validate from 'ember-gen/validate';
import {i18nValidate} from 'ui/validators/i18n';

const {
  computed,
  get
} = Ember;

let FS = {
  list : ['title_current', 'area.title_current']
}


export default gen.CRUDGen.extend({
  modelName: 'subject',
  path: 'subjects',
  common: {
    preloadModels: ['subject-area'],
    validators: {
      title: [i18nValidate([validate.presence(true), validate.length({min:4, max:50})])],
    }
  },
  list: {
    page: {
      title: 'subject.menu_label',
    },
    menu: {
      icon: 'local_library',
      label: 'subject.menu_label'
    },
    layout: 'table',
    paginate: {
      limit: [10, 15]
    },
    sortBy: 'title_current:asc',
    search: {
      fields: FS.list
    },
    row: {
      fields: FS.list,
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
