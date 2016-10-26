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
    sortBy: 'title_current:asc',
    fields: FS.list,
    search: {
      fields: FS.list
    },
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
