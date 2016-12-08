import {ApellaGen} from 'ui/lib/common';
import gen from 'ember-gen/lib/gen';
import validate from 'ember-gen/validate';
import {i18nValidate} from 'ui/validators/i18n';

const {
  computed,
  get
} = Ember;

export default ApellaGen.extend({
  modelName: 'subject_area',
  auth: true,
  path: 'subject-areas',
  common: {
    validators: {
      title: [i18nValidate([validate.presence(true), validate.length({min:4, max:50})])],
    }
  },
  list: {
    page: {
      title: 'subject_area.menu_label',
    },
    menu: {
      icon: 'school',
      label: 'subject_area.menu_label'
    },
    layout: 'table',
    sortBy: 'title_current:asc',
     row: {
      fields: ['title_current'],
      actions: ['gen:edit', 'remove']
    },
  },
  details: {
    page: {
      title: computed.readOnly('model.title_current')
    }
  }
});
