import validate from 'ember-gen/validate';
import gen from 'ember-gen/lib/gen';

export default gen.CRUDGen.extend({
  modelName: 'position',
  common: {
    menu: {
      icon: 'business_center',
    },
    validators: {
      title: [validate.presence(true), validate.length({min:4, max:50})],
      description: [validate.presence(true), validate.length({max:300})],
    },
    fieldsets: [{
      label: 'fieldsets.labels.basic_info',
      fields: ['title', 'state', 'description', 'discipline', 'department', 'subject_area', 'subject'],
      layout: {
        flex: [50, 50, 100, 50, 50, 50, 50]
      }
    }, {
      label: 'position.fek_section.title',
      fields: ['fek', 'fek_posted_at'],
      layout: {
        flex: [50, 50]
      },
    }, {
      label: 'fieldsets.labels.details',
      fields: ['electors', 'committee', 'assistants', 'elected'],
      layout: {
        flex: [50, 50, 50, 50]
      }

    }],
  }
});
