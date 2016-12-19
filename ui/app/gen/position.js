import {field} from 'ember-gen';
import {disable_field} from 'ui/utils/common/fields';
import {ApellaGen, urlValidator} from 'ui/lib/common';
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
    action(route, model, aaa) {
      // TMP
      let resource = model.get('_internalModel.modelName'),
        dest_route = `${resource}.record.index`;
      route.transitionTo(dest_route, model);
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
    }
  });

const assistantsField = field('assistants', {
  label: null,
  modelMeta: {
    row: {
      fields: ['id',
        field('last_name_current', {label: 'last_name.label'}),
        field('first_name_current', {label: 'first_name.label'}),
        field('email', {label: 'email.label'}),
      ],
      actions: ['goToDetails'],
      actionsMap: {
        goToDetails: actions.goToDetails
      }
    },
  }
});


const committeeField = field('committee', {
  label: null,

  modelMeta: {
    row: {
      fields: ['id',
        field('last_name_current', {label: 'last_name.label'}),
        field('first_name_current', {label: 'first_name.label'}),
        field('email', {label: 'email.label'}),
      ],
      actions: ['goToDetails'],
      actionsMap: {
        goToDetails: actions.goToDetails
      }
    },
  }
});

const historyField = field('past_positions', {
    valueQuery: function(store, params, model, value) {
      let id = model.get('id');
      let query = {id: id, history: true};
      return store.query('position', query);
    },
    label: null,
    modelMeta: {
      row: {
        fields: ['id', 'code', 'state_verbose',
          field('starts_at_format', {label: 'starts_at.label'}),
          field('ends_at_format', {label: 'ends_at.label'})
        ],
        actions: ['goToDetails'],
        actionsMap: {
          goToDetails: actions.goToDetails
        }
      },
    }
  });



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
    participates: computed('role', 'session.session.authenticated.id', 'model.electors.[]', 'model.committee.[]', function() {
      let role = get(this, 'role');
      let professorId = this.get('session.session.authenticated.id').toString();
      let electors = get(this, 'model.electors').getEach('id');
      let committee = get(this, 'model.committee').getEach('id');
      let participations = electors.concat(committee)
      return role === 'professor' && participations.includes(professorId)
    }),
    before_open: computed('role', 'model.starts_at', function(){
      return moment(new Date()).isBefore(moment(get(this, 'model.starts_at')));
    })
  },

  common: {
    validators: {
      title: [validate.presence(true), validate.length({min:4, max:200})],
      description: [validate.presence(true), validate.length({max:300})],
      starts_at: [afterToday()],
      fek_posted_at: [beforeToday()],
      ends_at: [afterDays({on:'starts_at', days:30})],
      fek: urlValidator,
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
    }, {
      label: 'assistants.label',
      text: 'assistants_on_position_explain',
      fields: [assistantsField]
    }],
  },
  list: {
    sort: {
      active: true,
      fields: ['code', 'title'],
      serverSide: true
    },
    filter: {
      active: true,
      meta: {
        fields: ['state', 'department']
      },
      serverSide: true,
      search: true,
    },
    page: {
      title: 'position.menu_label',
    },
    menu: {
      icon: 'business_center',
      label: 'position.menu_label'
    },
    layout: 'table',
    row: {
      fields: ['code', 'title', field('state_verbose', {sortKey: 'state'}), field('department.title_current', {label: 'department.label'})],
      actions: ['gen:details','applyCandidacy', 'gen:edit', 'remove', 'cancelPosition' ],
      actionsMap: {
        applyCandidacy: {
          label: 'applyCandidacy',
          icon: 'playlist add',
          permissions: [{'resource': 'candidacies', 'action': 'create'}],
          action(route, model){
            console.log(get(model, 'code'))
          }
        },
        cancelPosition: {
          label: 'cancelPosition',
          icon: 'pan_tool',
          action(route, model) {
            model.set('state', 'cancelled');
            model.save().then((value) => {
              return value;
            }, (reason) => {
              model.rollbackAttributes();
              return reason.errors;
            });
          },
          permissions: [{action: 'edit'}],
          hidden: computed('model.code', 'model.state', function(){
            let starts_at = get(get(this, 'model'), 'starts_at')
            let state = get(get(this, 'model'), 'state');
            let before_open = moment(new Date()).isBefore(moment(starts_at));
            return !(before_open && (state == 'posted'))
          }),
          confirm: true,
          prompt: {
            ok: 'cancelPosition',
            cancel: 'cancel',
            message: 'prompt.cancelPosition.message',
            title: 'prompt.cancelPosition.title',
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
      label: 'committee.label',
      fields: [committeeField]
    },{
      label: 'fieldsets.labels.basic_info',
      fields: ['code', 'state_verbose', 'title',
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
    },
    {
      label: 'candidacy.menu_label',
      fields: [candidaciesField]
    },
    {
      label: 'assistants.label',
      text: 'assistants_on_position_explain',
      fields: [assistantsField]
    },
    {
      label: 'position.history.title',
      fields: [historyField]
    }]
  }
});
