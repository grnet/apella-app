import gen from 'ember-gen/lib/gen';
import validate from 'ember-gen/validate';
import {i18nValidate} from 'ui/validators/i18n';

let FS = {
  list : ['title_current', 'area.title_current']
}


export default gen.CRUDGen.extend({
  modelName: 'subject',
  path: 'subjects',
  common: {
    menu: {
      icon: 'local_library',
      label: 'subject.menu_label'
    },
    validators: {
      title: [i18nValidate([validate.presence(true), validate.length({min:4, max:50})])],
    }
  },
  list: {
    layout: 'table',
    sortBy: 'title_current:asc',
    fields: FS.list,
    search: {
      fields: FS.list
    },
    page: {
      title: 'subject.menu_label',
    }
  },
  create: {
    page: {
      title: 'subject.create_title',
    }
  }
});
