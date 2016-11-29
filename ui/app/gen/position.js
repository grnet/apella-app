import {ApellaGen} from 'ui/lib/common';
import validate from 'ember-gen/validate';
import gen from 'ember-gen/lib/gen';
import {afterToday, beforeToday, notHoliday, afterDays} from 'ui/validators/dates';

const {
  computed,
  get
} = Ember;

export default ApellaGen.extend({
  modelName: 'position',
  auth: true,
  path: 'positions',

  abilityStates: {
    owned: computed('model', 'role', function() { return true; })
  },

  common: {
    validators: {
      title: [validate.presence(true), validate.length({min:4, max:50})],
      description: [validate.presence(true), validate.length({max:300})],
      starts_at: [afterToday()],
      fek_posted_at: [beforeToday()],
      ends_at: [notHoliday(), afterDays({on:'starts_at', days:30})],
      fek: [validate.format({type: 'url'})],
      department_dep_number: [validate.presence(true), validate.number({integer: true})]

    },
    fieldsets: [{
      label: 'fieldsets.labels.basic_info',
      fields: [
        'title', 'author', ['state', {disabled: true}], 'description',
        'discipline', 'department', 'subject_area', 'subject',
        ['department_dep_number', {disabled: true}]
      ],
      layout: {
        flex: [100, 50, 50, 100, 50, 50, 50, 50, 50]
      }
    }, {
      label: 'fieldsets.labels.details',
      fields: ['fek', 'fek_posted_at', 'starts_at', 'ends_at'],
      layout: {
        flex: [50, 50, 50, 50]
      },
    }],
  },
  create: {
    fieldsets: [{
      label: 'fieldsets.labels.basic_info',
      fields: ['title', 'author',
        ['state', {
          attrs: {
            readonly: true,
          }
        }],
        'description', 'discipline', 'department', 'subject_area', 'subject', 'department_dep_number'],
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
    },
    menu: {
      icon: 'business_center',
      label: 'position.menu_label'
    },
    layout: 'table',
    row: {
      fields: ['code', 'title', 'state_verbose'],
      actions: ['gen:details','applyCandidacy', 'gen:edit', 'remove' ],
      actionsMap: {
        applyCandidacy: {
          label: 'position.button.apply',
          action(item){
            // TBA...
          }
        }
      }
    }
  },
  details: {
    page: {
      title: computed.readOnly('model.code')
    }
  }
});
