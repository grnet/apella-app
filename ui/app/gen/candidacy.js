import gen from 'ember-gen/lib/gen';
import validate from 'ember-gen/validate';

const mandatory = [validate.presence(true)],
      max_chars = validate.length({max: 200}),
      mandatory_with_max_chars = [mandatory, max_chars];


export default gen.CRUDGen.extend({
  modelName: 'candidacy',
  common: {
    menu: {
      icon: 'assignment',
      label: 'candidacy.menu_label'
    },
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
    page: {
      title: 'candidacy.menu_label',
    }
  },
  create: {
    page: {
      title: 'candidacy.create_title'
    },
    fieldsets: [
    {
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
  },
});
