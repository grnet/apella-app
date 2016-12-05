import {field} from 'ember-gen';
import {disable_field} from 'ui/utils/common/fields';
import {ApellaGen} from 'ui/lib/common';
import validate from 'ember-gen/validate';
import gen from 'ember-gen/lib/gen';
import {afterToday, beforeToday, notHoliday, afterDays} from 'ui/validators/dates';
import moment from 'moment';


const {
  computed,
  get
} = Ember;

export default ApellaGen.extend({
  modelName: 'position',
  auth: true,
  path: 'positions',

  abilityStates: {
    owned: computed('role', function() { 
      return get(this, 'role') === 'institutionmanager';
    }), // we expect server to reply with owned resources
    'open': computed('model.state', 'model.ends_at', function() {
      return get(this, 'model.state') === 'open' && moment(get(this, 'model.ends_at')).isBefore(new Date());
    }),
    closed: computed('model.starts_at', function() {
      return moment(get(this, 'model.starts_at')).isBefore(moment(new Date()));
    }),
    electing: computed('model.state', 'closed', function() {
      return get(this, 'model.state') === 'posted' && get(this, 'closed');
    }),
    participates: computed('role', 'user.id', 'model.electors.[]', function() {
      let role = get(this, 'role');
      let userId = get(this, 'user.id');
      let electors = get(this, 'model.electors').getEach('id');
      return role === 'professor' && electors.includes(userId);
    })
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
        'title', 'author', disable_field('state'), 'description',
        'discipline', 'department', 'subject_area', 'subject',
        disable_field('department_dep_number')
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
      fields: ['department', disable_field('department_dep_number'), 'title',
        disable_field('state'), 'description', 'discipline','subject_area',
        'subject', 'author'],
      layout: {
        flex: [50, 50, 50, 50, 50, 100, 100, 50, 50]
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
      fields: ['code', 'title', 'state_verbose', field('department.title_current', {label: 'department.label'})],
      actions: ['gen:details','applyCandidacy', 'gen:edit', 'remove' ],
      actionsMap: {
        applyCandidacy: {
          label: 'applyCandidacy',
          icon: 'playlist add',
          permissions: [{'resource': 'candidacies', 'action': 'create'}],
          action(route, model){
            console.log(get(model, 'code'))
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
