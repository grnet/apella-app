import {field} from 'ember-gen';
import gen from 'ember-gen/lib/gen';
import validate from 'ember-gen/validate';

const presence = validate.presence(true),
      max_chars = validate.length({max: 200}),
      mandatory = [validate.presence(true)],
      mandatory_with_max_chars = [presence, max_chars],
      {
        get, computed
      } =Ember;

let FS = {
  list:  ['position.code', 'position.department.school.institution.title_current',
          'position.department.title',
          'position.state_verbose'],
  create: [{
    label: 'candidacy.position_section.title',
    text: 'candidacy.position_section.subtitle',
    fields: ['position'],
    layout: {
      flex: [50]
    },
  },
  {
    label: 'candidacy.candidate_section.title',
    text: 'candidacy.candidate_section.subtitle',
    fields: ['candidate', 'cv', 'diploma', 'publication'],
    layout: {
      flex: [50, 50, 50, 50]
    },
  },
    {
      label: 'candidacy.candidacy_section.title',
      fields: ['selfEvaluation', 'additionalFiles', 'othersCanView'],
      layout: {
        flex: [50, 50, 50, 50]
      }
    }
  ],
  edit: [{
    label: 'candidacy.position_section.title',
    text: 'candidacy.position_section.subtitle',
    fields: [field('position', {
        hint: 'candidacy.edit.position.hint',
        attrs: {
          optionLabelAttr: 'code_and_title',
          readonly: true,
        }
    })],
    layout: {
      flex: [50]
    },
  },
  {
    label: 'candidacy.candidate_section.title',
    text: 'candidacy.candidate_section.subtitle',
    fields: ['candidate', 'cv', 'diploma', 'publication'],
    layout: {
      flex: [50, 50, 50, 50]
    },
  },
    {
      label: 'candidacy.candidacy_section.title',
      fields: ['selfEvaluation', 'additionalFiles', 'othersCanView'],
      layout: {
        flex: [50, 50, 50, 50]
      }
    }
  ],

}

export default gen.CRUDGen.extend({
  modelName: 'candidacy',
  path: 'candidacies',
  common: {
    validators: {
      candidate: mandatory,
      position: mandatory,
      cv: mandatory_with_max_chars,
      diploma: mandatory_with_max_chars,
      publication: mandatory_with_max_chars,
      additionalFiles: mandatory_with_max_chars,
    }
  },
  list: {
    layout: 'table',
    sortBy: 'position.code:asc',
    fields: FS.list,
    search: {
      fields: FS.list,
    },
    page: {
      title: 'candidacy.menu_label',
    },
    menu: {
      label: 'candidacy.menu_label',
      icon: 'assignment'
    },
    row: {
      actions: ['gen:details', 'gen:edit', 'remove']
    }
  },
  create: {
    page: {
      title: 'common.create_label'
    },
    menu: {
      label: 'common.button.create_label',
      icon: 'library add'
    },
    fieldsets: FS.create,
   },
  details: {
    menu: {
      label: 'common.button.details_label',
      icon: 'remove red eye'
    }
  },
  record: {
    menu: {
      label: computed('model.id', function() {
        return get(this, 'model.id');
      })
    },
  },
  edit: {
    page: {
      title: 'common.edit_label'
    },
    menu: {
      label: 'common.button.edit_label',
      icon: 'border color'
    },
    fieldsets: FS.edit,
  },
});
