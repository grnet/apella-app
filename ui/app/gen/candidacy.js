import {field} from 'ember-gen';
import gen from 'ember-gen/lib/gen';
import validate from 'ember-gen/validate';
import _ from 'lodash/lodash'

const presence = validate.presence(true),
      max_chars = validate.length({max: 200}),
      mandatory = [validate.presence(true)],
      mandatory_with_max_chars = [presence, max_chars],
      {
        get, computed
      } =Ember,
      CANDIDACY_POSTED_ID = '2',
      POSITION_POSTED_ID = '2';

let FS = {
  list:  ['position.code', 'position.department.school.institution.title_current',
          'position.department.title_current',
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
  edit: {
    position_fields: ['position.code_and_title', 'position.title', 'position.department.school.institution.title_current', 'position.department.title_current', 'position.discipline','position.fek', 'position.fek_posted_at_format', 'position.starts_at_format', 'position.ends_at_format' ],
    position_layout: {
      flex: [30, 30, 30, 30, 30, 30, 30, 30, 30 ]
    }
  }

}

export default gen.CRUDGen.extend({
  modelName: 'candidacy',
  path: 'candidacies',
  common: {
    validators: {
      candidate: mandatory,
      position: mandatory,
//      cv: mandatory_with_max_chars,
//      diploma: mandatory_with_max_chars,
//      publication: mandatory_with_max_chars,
//      additionalFiles: mandatory_with_max_chars,
    }
  },
  list: {
    getModel: function(params) {
      // TODO replace with session's user group
      let userGroup = 'admin';
      if (userGroup == 'admin') {
        return this.store.findAll('candidacy');
      } else {
      // TODO replace with session's user
        let userId = '2';
        return this.store.query('candidacy', {
          'state': CANDIDACY_POSTED_ID,
          'candidate': userId,
        });
      }
    },
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
    fieldsets: FS.create,
   },
  details: {
  },
  record: {
    menu: {
      label: computed('model.id', function() {
        return get(this, 'model.id');
      })
    },
  },
  edit: {
    fieldsets: computed('model.position.state', function() {
      let candidacy_fields = ['selfEvaluation', 'additionalFiles', 'othersCanView'];
      let disable_field = function(el){
        return field(el, {
          attrs: {
            readonly: true,
            disabled: true,
          }
        })
      }
      if (this.get('model.position.state') != POSITION_POSTED_ID) {
        candidacy_fields = _.map(candidacy_fields, disable_field);
      };

      return [{
        label: 'candidacy.position_section.title',
        text: 'candidacy.position_section.subtitle',
        fields: _.map(FS.edit.position_fields, disable_field),
        layout: FS.edit.position_layout
      },
      {
        label: 'candidacy.candidate_section.title',
        text: 'candidacy.candidate_section.subtitle',
        fields: [disable_field('candidate.full_name_current'), 'cv', 'diploma', 'publication'],
        layout: {
          flex: [50, 50, 50, 50]
        },
      },
        {
          label: 'candidacy.candidacy_section.title',
          fields: candidacy_fields,
          layout: {
            flex: [50, 50, 50, 50]
          }
        }
      ];
    }),
  },
});
