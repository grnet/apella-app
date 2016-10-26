import gen from 'ember-gen/lib/gen';
import {USER_FIELDSET, USER_VALIDATORS} from 'ui/utils/common/users';
import {field} from 'ember-gen';

const {
  computed,
  get
} = Ember;

export default gen.CRUDGen.extend({
  modelName: 'candidate',
  path: 'candidates',
  common: {
    validators: USER_VALIDATORS,
    fieldsets: [
      USER_FIELDSET,
    ]
  },
  list: {
    page: {
      title: 'candidate.menu_label',
    },
    menu: {
      label: 'candidate.menu_label',
      icon: 'sentiment_dissatisfied'
    },
    layout: 'table',
    sortBy: 'username:asc',
    search: {
      fields: ['username', 'email']
    },
    label: 'candidate.menu_label',
    fields: ['username', 'email', 'full_name_current' ],
    row: {
      actions: ['gen:details', 'gen:edit', 'remove']
    },
  },
  details: {
    fields: ['id', 'username', 'full_name_current'],
  },
  record: {
    menu: {
      label: computed('model.id', function() {
        return get(this, 'model.id');
      })
    }
  }
});
