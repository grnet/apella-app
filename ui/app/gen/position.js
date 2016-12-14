import {field} from 'ember-gen';
import {disable_field} from 'ui/utils/common/fields';
import {ApellaGen} from 'ui/lib/common';
import validate from 'ember-gen/validate';
import gen from 'ember-gen/lib/gen';
import {afterToday, beforeToday, afterDays} from 'ui/validators/dates';
import moment from 'moment';


const {
  computed,
  get,
  merge
} = Ember;


let actions = {
  goToDetails: {
    label: 'details.label',
    icon: 'remove red eye',
    action(route, model) {
      route.transitionTo('candidacy.record.index', model);
    }
  }
};

const candidaciesField = field('candidacies', {
    valueQuery: function(store, params, model, value) {
      let position_id = model.get('id');
      // no use of params for now
      let query = {position: position_id};
      return store.query('candidacy', query);
    },
    label: null,
    modelMeta: {
      row: {
        fields: ['id',
          field('candidate.last_name_current', {label: 'last_name.label'}),
          field('candidate.first_name_current', {label: 'first_name.label'}),
          field('candidate.father_name_current', {label: 'father_name.label'}),
          field('submitted_at_format', {label: 'submitted_at.label'}),
          field('updated_at_format', {label: 'updated_at.label'})
        ],
        actions: ['goToDetails'],
        actionsMap: {
          goToDetails: actions.goToDetails
        }
      },
      sortBy: ['id'],
      }
    }
  );

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
      ends_at: [afterDays({on:'starts_at', days:30})],
      fek: [validate.format({type:'url'}),
            validate.format({regex: /^(https:\/\/|http:\/\/)/i,
                             message: 'It should start with http or https'})],
      department_dep_number: [validate.presence(true), validate.number({integer: true})]

    }
  },
  create: {
    onSubmit(model) {
      this.transitionTo('position.record.index', model);
    },
    fieldsets: [{
      label: 'fieldsets.labels.basic_info',
      fields: ['title', 'department', 'description',
        'discipline','subject_area', 'subject'],
      layout: {
        flex: [50, 50, 100, 100, 50, 50]
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
  edit: {
    fieldsets: [{
      label: 'fieldsets.labels.basic_info',
      fields: [disable_field('code'), disable_field('state'), 'title',
        'department', 'description', 'discipline','subject_area', 'subject'],
      layout: {
        flex: [50, 50, 50, 50, 100, 100, 50, 50]
      }
    }, {
      label: 'fieldsets.labels.details',
      fields: ['fek', 'fek_posted_at', 'starts_at', 'ends_at'],
      layout: {
        flex: [50, 50, 50, 50]
      },
    }],
  },
  details: {
    page: {
      title: computed.readOnly('model.code')
    },
    fieldsets: [{
      label: 'fieldsets.labels.basic_info',
      fields: [disable_field('code'), disable_field('state_verbose'), 'title',
        field('department.title_current', {label: 'department.label'}),
        'description', 'discipline', field('subject_area.title_current',{label: 'subject_area.label'}),
        field('subject.title_current', {label: 'subject.label'})],
      layout: {
        flex: [50, 50, 50, 50, 100, 100, 50, 50]
      }
    }, {
      label: 'fieldsets.labels.details',
      fields: ['fek', field('fek_posted_at_format', {label: 'fek_posted_at.label'}),
        field('starts_at_format', {label: 'starts_at.label'}),
        field('ends_at_format', {label: 'ends_at.label'})],
      layout: {
        flex: [50, 50, 50, 50]
      }
    }, {
      label: 'candidacy.menu_label',
      fields: [candidaciesField]
    }],
  }
});
