import {field} from 'ember-gen';
import {disable_field} from 'ui/utils/common/fields';
import {ApellaGen, urlValidator} from 'ui/lib/common';
import validate from 'ember-gen/validate';
import gen from 'ember-gen/lib/gen';
import {afterToday, beforeToday, afterDays} from 'ui/validators/dates';
import moment from 'moment';


const {
  computed,
  computed: { reads },
  get,
  merge,
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
          field('updated_at_format', {label: 'updated_at.label'})
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
    owned: computed('user.user_id', 'model.author', 'role', 'model.assistants.[]', function() {
      let id = get(this, 'user.id').toString();

      let is_attached_assistant = false;
      let is_institutionmanager = get(this, 'role') === 'institutionmanager';
      let is_author = this.get('model.author.user_id') == get(this, 'user.user_id');

      if (this.get('model.assistants')) {
        if (this.get('model.assistants').getEach('id')) {
          let res = this.get('model.assistants').getEach('id');
          if (res.includes(id)) {
            is_attached_assistant = true;
          }
        }
      }

      return is_author || is_attached_assistant || is_institutionmanager;
    }), // we expect server to reply with owned resources
    'open': computed('model.state', 'model.ends_at', 'owned', function() {
      return get(this, 'model.state') === 'open' &&
        moment(get(this, 'model.ends_at')).isBefore(new Date()) &&
        get(this, 'owned');
    }),
    closed: computed('model.starts_at', 'owned', function() {
      return moment(get(this, 'model.starts_at')).isBefore(moment(new Date())) && get(this, 'owned');
    }),
    electing: computed('model.state', 'closed', 'owned', function() {
      return get(this, 'model.state') === 'posted' && get(this, 'closed') && get(this, 'owned');
    }),
    before_open: computed('owned', 'model.starts_at', function(){
      return moment(new Date()).isBefore(moment(get(this, 'model.starts_at'))) && get(this, 'owned');
    }),
    can_create: computed('user.can_create_positions', function() {
      return get(this, 'user.can_create_positions');
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
          icon: 'highlight_off',
          action(route, model) {
            model.set('state', 'cancelled');
            model.save().then((value) => {
              return value;
            }, (reason) => {
              model.rollbackAttributes();
              window.alert(reason)
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
