import gen from 'ember-gen/lib/gen';
import validate from 'ember-gen/validate';

export default gen.CRUDGen.extend({
  modelName: 'candidacy',
  common: {
  validators: {
    candidate: [
      validate.presence(true),
    ],
    position: [
      validate.presence(true),
      validate.format({type: 'url'}),
    ],
    cv: [
      validate.presence(true),
      validate.length({max: 200})
    ],
    diploma: [
      validate.presence(true),
      validate.length({max: 200})
    ],
    publication: [
      validate.presence(true),
      validate.length({max: 200})
    ],
    additionalFiles: [
      validate.presence(true),
      validate.length({max: 200})
    ]
  }
  },
  create: {
    page: {
      title: 'candidacy.page_title'
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
