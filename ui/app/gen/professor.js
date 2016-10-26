import gen from 'ember-gen/lib/gen';
import validate from 'ember-gen/validate';
import {USER_FIELDSET, USER_VALIDATORS} from 'ui/utils/common/users';
import {field} from 'ember-gen';

const PROFESSOR_VALIDATORS = {
  cv_url: [validate.presence(true), validate.format({type:'url'})],
  institution: [validate.presence(true)],
}

let all_validators = Object.assign(PROFESSOR_VALIDATORS, USER_VALIDATORS);

export default gen.CRUDGen.extend({
  modelName: 'professor',
  path: 'professors',
  common: {
    menu: {
      label: 'professor.menu_label',
      icon: 'sentiment_very_dissatisfied'
    },
    validators: all_validators,
    fieldsets: [
      USER_FIELDSET,
      {
        label: 'fieldsets.labels.more_info',
        fields: [
          'institution',
          'department',
          'rank',
          'cv_url',
          'fek',
          'fek_discipline',
          'discipline_free_text',
          'is_foreign',
          'speaks_greek',
       ],
       layout: {
        flex: [50, 50, 100, 50, 50, 100, 50, 50]
       }
      }
    ]
  },
  list: {
    layout: 'table',
    sortBy: 'username:asc',
    search: {
      fields: ['username', 'email']
    },
    page: {
      title: 'professor.menu_label',
    },
    label: 'professor.menu_label',
    fields: ['username', 'email', 'full_name_current', 'rank', ],
    menu: {
      label: 'professor.menu_label',
    },
    row: {
      label: 'professor.menu_label',
      icon: 'person',
    },
  },
  create: {
    page: {
      title: 'professor.create_title'
    },
  },
  details: {
    fields: ['id', 'username', 'first_name_current'],
  }
});
