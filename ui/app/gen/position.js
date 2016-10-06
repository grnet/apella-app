import validate from 'ember-gen/validate';
import gen from 'ember-gen/lib/gen';
import {afterToday, beforeToday} from 'ui/validators/dates';

export default gen.CRUDGen.extend({
  modelName: 'position',
  common: {
    menu: {
      icon: 'business_center',
      label: 'position.menu_label'
    },
    validators: {
      title: [validate.presence(true), validate.length({min:4, max:50})],
      description: [validate.presence(true), validate.length({max:300})],
      starts_at: [afterToday()],
      fek_posted_at: [beforeToday()],
      fek: [validate.format({type: 'url'})]
    },
    fieldsets: [{
      label: 'fieldsets.labels.basic_info',
      fields: ['title', 'author',
              ['state', {
                attrs: {
                  readonly: true,
                }
              }],
              'description', 'discipline', 'department', 'subject_area', 'subject'],
      layout: {
        flex: [100, 50, 50, 100, 50, 50, 50, 50]
      }
    }, {
      label: 'fieldsets.labels.details',
      fields: ['fek', 'fek_posted_at', 'starts_at', 'ends_at'],
      layout: {
        flex: [50, 50, 50, 50]
      },
    }],
  },
  list: {
    page: {
      title: 'position.menu_label',
    }
  },
  create: {
    page: {
      title: 'position.create_title'
    },
  },


});
