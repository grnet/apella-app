import {field} from 'ember-gen';
import {ApellaGen, preloadRelations} from 'ui/lib/common';
import _ from 'lodash/lodash';
import {cancelCandidacy, goToPosition} from 'ui/utils/common/actions';
import {fileField} from 'ui/lib/common';
import moment from 'moment';

const {
  set, get, computed, computed: { alias },
  getOwner
} = Ember;

let POSITION_FIELDS = [
    field('position', {
      disabled: true,
      displayAttr: 'title'
    }),
    field('position.old_code', { disabled: true}),
    field('position.department.institution.title_current', { disabled: true }),
    field('position.department.title_current', { disabled:true }),
    field('position.discipline', { disabled: true }),
    field('position.fek', {disabled: true, displayComponent: 'url-display'}),
    field('position.fek_posted_at_format', { disabled: true}),
    field('position.starts_at_format', { disabled: true }),
    field('position.ends_at_format', { disabled: true}),
    field('position.state_calc_verbose', {disabled: true}) ];

let POSITION_FIELDSET =  {
      label: 'candidacy.position_section.title',
      text: 'candidacy.position_section.subtitle',
      fields: POSITION_FIELDS,
      layout: {
        flex: [60, 30, 30, 30, 30, 30, 30, 30, 30, 30 ]
      },
      flex: 100
};

let CANDIDATE_FIELDSET =  {
      label: 'candidacy.candidate_section.title',
      text: computed('role', function(){
        let role = get(this, 'role');
        if (role === 'professor' || role === 'candidate') {
          return 'candidacy.candidate_section.subtitle_candidate';
        }
        return 'candidacy.candidate_section.subtitle';
      }),
      fields: [
        field('candidate', {
          disabled: true,
          displayAttr: 'full_name_current',
        }),
        fileField('cv', 'candidate', 'cv', {
          readonly: true,
        }),
        fileField('diplomas', 'candidate', 'diplomas', {
          readonly: true
        }),
        fileField('publications', 'candidate', 'publications', {
          readonly: true
        })],
      layout: {
        flex: [100, 100, 100, 100]
      },
      flex: 100,
};

let CANDIDACY_FIELDSET =  {
    label: 'candidacy.candidacy_section.title',
    fields: computed('model.position.position_type', function(){
      let election = get(this, 'model.position.position_type') === 'election';

      let res = [
        fileField('self_evaluation_report', 'candidacy', 'self_evaluation_report', {
          hint: 'five_before_electors_meeting',
          readonly: computed('model.position.is_open', 'model.position.electors_meeting_date', function() {
            let electors_at = moment(get(this, 'model.position.electors_meeting_date')).startOf('days');
            let after_deadline = false;
            if (electors_at) {
              let limit_day = electors_at.subtract(5, 'days'),
                today = moment().startOf('days');
              after_deadline = today.isAfter(limit_day);
            }
            return after_deadline;
          })
        }, {
          replace: true
        }),
        fileField('attachment_files', 'candidacy', 'attachment_files', {
          hint: 'one_before_electors_meeting',
          readonly: computed('model.position.is_open', 'model.position.electors_meeting_date', function() {
            let electors_at = moment(get(this, 'model.position.electors_meeting_date')).startOf('days');
            let after_deadline = false;
            if (electors_at) {
              let today = moment().startOf('days'),
                limit_day = electors_at.subtract(1, 'days');
              after_deadline = today.isAfter(limit_day);
            }
            return after_deadline;
          })
        }, {
          multiple: true
        })
      ];
      if (election) {
        res.pushObject(
          field('othersCanView', {
            disabled: computed('model.position.is_open', function(){
              return !get(this, 'model.position.is_open');
            })
          })
        )
      }
      return res;
    }),
    flex: 100,
};

let CANDIDACY_FIELDSET_DETAILS =  {
    label: 'candidacy.candidacy_section.title',
    fields: computed('model.position.position_type', function(){
      let election = get(this, 'model.position.position_type') === 'election';
      let res = [
        fileField('self_evaluation_report', 'candidacy', 'self_evaluation_report', {
          readonly: true,
          hint: 'five_before_electors_meeting',
        }, { replace: true}),
       fileField('attachment_files', 'candidacy', 'attachment_files', {
          readonly: true,
          sortBy: 'filename',
          hint: 'one_before_electors_meeting',
        }, { replace: true, multiple: true})
      ];
      if (election) {
        res.pushObject('othersCanView');
      }
      return res;
    }),
    flex: 100,
    layout: {
      flex: [100, 100, 100]
    }
};


let FS = {
  common: [
    POSITION_FIELDSET,
    CANDIDATE_FIELDSET,
  ],
  list: [
    field('position.code', {dataKey: 'position__id'}),
    'position.title',
    'position.department.institution.title_current',
    'position.department.title_current',
    'position.state_calc_verbose',
    field('state_verbose', {label: 'candidacy.state'})
  ],
  list_with_user_id: [
    field('position.code', {dataKey: 'position__id'}),
    field('id', {label: 'candidacy.id'}),
    field('candidate.id', {label: 'candidate.user_id.label'}),
    field('candidate.full_name_current', {label: 'full_name'}),
    'position.title',
    'position.department.institution.title_current',
    'position.department.title_current',
    'position.state_calc_verbose',
    field('state_verbose', {label: 'candidacy.state'})
  ],

  create_helpdeskadmin: [
    POSITION_FIELDSET,
    {
      label: 'fieldsets.labels.candidate',
      text: 'candidate.select.id',
      fields: [field('candidate', {
        formComponent: 'select-model-id-field',
        query: function(table, store, field, params) {
          let promises = [
            store.query('user', {role: 'professor'}),
            store.query('user', {role: 'candidate'}),
          ];

          var promise = Ember.RSVP.all(promises).then(function(arrays) {
            var mergedArray = Ember.A();
            arrays.forEach(function (records) {
              mergedArray.pushObjects(records.toArray());
            });
            return mergedArray.uniqBy('id');
          });

          return DS.PromiseArray.create({
            promise: promise,
          });
        }
      })],
      layout: {
        flex: [50]
      }
    },
  ],
};


export default ApellaGen.extend({
  order: 900,
  modelName: 'candidacy',
  path: 'candidacies',
  session: Ember.inject.service(),

  abilityStates: {
    // resolve ability for position model
    positionAbility: computed('model.position.id', 'role', 'user', 'model', function() {
      let ability = getOwner(this).lookup('ability:positions');
      let props = this.getProperties('role', 'user');
      props.model = get(this, 'model.position');
      ability.setProperties(props);
      return ability;
    }),
    position_open: alias('model.position.is_open'),
    others_can_view: alias('model.othersCanView'),

    owned: computed('role', 'user.user_id', 'model.candidate.id', function() {
      let is_institutionmanager = get(this, 'role') === 'institutionmanager';
      let is_candidate_owning = get(this, 'user.user_id') === get(this, 'model.candidate.id');
      return is_institutionmanager || is_candidate_owning;
    }),

    owned_open: computed('owned', 'position_open', 'model.state', function() {
      let position_open = get(this, 'position_open');
      let candidacy_not_cancelled = get(this, 'model.state') !== 'cancelled';
      return get(this, 'owned') && position_open && candidacy_not_cancelled;
    }),

    owned_by_assistant: computed('user.departments', 'model.position_department', function() {
      let assistant_departments = get(this, 'user.departments') || [];
      // TODO: Extract department using a better way
      let position_department = this.get('model.position_department').split('/').slice(-2)[0];
      return assistant_departments.indexOf(position_department) > -1;
    }),

    five_before_electors_meeting: computed('model.state', 'position_open', 'model.position.electors_meeting_date', 'owned', function() {
      let electors_at = get(this, 'model.position.electors_meeting_date');
      let candidacy_not_cancelled = get(this, 'model.state') !== 'cancelled';
      let position_open = get(this, 'position_open');
      let owned = get(this, 'owned');
      let before_deadline = true;
      if (electors_at) {
        before_deadline =  moment().add(5, 'days').isBefore(electors_at);
      }
      return candidacy_not_cancelled && (position_open || before_deadline) && owned;
    }),

    one_before_electors_meeting: computed('model.state', 'position_open', 'model.position.electors_meeting_date', 'owned', function() {
      let electors_at = moment(get(this, 'model.position.electors_meeting_date')).startOf('days');
      let candidacy_not_cancelled = get(this, 'model.state') !== 'cancelled';
      let before_deadline = true;
      let owned = get(this, 'owned');
      let today = moment().startOf('days');
      if (electors_at) {
        before_deadline =  today.isBefore(electors_at);
      }
      return candidacy_not_cancelled && before_deadline && owned;
    }),

    participates: computed('user.id', 'model.position.electors', 'model.position.committee', function() {
      let professor_id = get(this, 'user.id'),
        position = get(this, 'model.position'),
        electors, committee, participations;

      if(get(position, 'electors')) {
        electors = position.get('electors').getEach('id'),
        committee = position.get('committee').getEach('id');
        participations = _.union(electors, committee);

        if(participations.includes(professor_id)) {
          return true;
        }
      }
      return false;
    }),
    is_dep_candidacy: computed('', function() {
      return false;
    })
  },

  common: {
    preloadModels: [],
    fieldsets: FS.common,
    validators: {
    }
  },
  list: {
    actions: [],

    getModel: function(params) {
      let role = get(this, 'session.session.authenticated.role');
      if (role === 'candidate' || role === 'professor') {
        let user_id = get(this, 'session.session.authenticated.user_id');
        params = params || {};
        params.candidate = user_id;
      }
      let model = this.store.query('candidacy', params);
      return preloadRelations(model, 'position', 'candidate', 'position.department', 'position.department.insitution');
    },
    sort: {
      active: true,
      fields: ['position.code', 'position.title', 'candidate.id'],
      serverSide: true
    },
    filter: {
      active: true,
      meta: {
        fields: ['state']
      },
      serverSide: true,
      search: true,
      searchPlaceholder: computed('role', function() {
        let role = get(this, 'role');
        if(role === 'candidate') {
          return 'search.placeholder.candidacies_by_candidate';
        }
        else {
          return 'search.placeholder.candidacies_by_helpdesk';
        }
      })
    },
    page: {
      title: 'candidacy.menu_label',
    },
    menu: {
      label: computed('role', function() {
        let role = get(this, 'role');
        if (role === 'professor' || role === 'candidate'){
          return 'my_candidacy.menu_label';
        }
        else {
          return 'candidacy.menu_label';
        }
      }),
      icon: 'event_note',
      display: computed('role', function() {
        let role = get(this, 'role');
        let forbiddenRoles = ['institutionmanager', 'assistant'];
        return (forbiddenRoles.includes(role) ? false : true);
      })
    },
    row: {
      fields: computed('role', function() {
        let role = get(this, 'role');
        let fs = FS.list_with_user_id;
        if (role === 'candidate' || role === 'professor' ) {
          fs = FS.list;
        }
        return fs;
      }),

      actions: ['gen:details', 'goToPosition', 'gen:edit', 'cancelCandidacy'],
      actionsMap: {
        cancelCandidacy: cancelCandidacy,
        goToPosition: goToPosition,
      }
    }
  },
  create: {
    fieldsets: computed('model.position', 'role', function(){
      if (get(this, 'role') === 'helpdeskadmin') {
        return FS.create_helpdeskadmin;
      } else {
        return FS.common;
      }
    }),
    onSubmit(model) {
      let role = get(this, 'session.session.authenticated.role');
      if (role === 'helpdeskadmin') {
        this.transitionTo('candidacy.record.index', model);
      } else {
        this.transitionTo('candidacy.record.edit', model);
      }
    },
    getModel(params) {
      var store = get(this, 'store');
      if (params.position) {
        let position = store.findRecord('position', params.position);
        let user_id = get(this, 'session.session.authenticated.user_id');
        let role = get(this, 'session.session.authenticated.role');
        let user = store.findRecord('user', user_id);
        let me = store.findRecord('profile', 'me');

        return position.then(function(position) {
          let c = store.createRecord('candidacy', {
            position: position,
          });
          if (role === 'helpdeskadmin') {
            return c;
          }
          return me.then(function(me) {
            let promises = [
              user,
              get(me, 'cv'),
              get(me, 'diplomas'),
              get(me, 'publications')
            ];

            return Ember.RSVP.all(promises).then((res) => {
                set(c, 'candidate', res[0]);
                set(c, 'cv', res[1]);
                set(c, 'diplomas', res[2]);
                set(c, 'publications', res[3]);
                return c;
            });

          });
        });
      }
      this.transitionTo('candidacy.index');
    },
    routeMixins: {
      queryParams: {'position': { refreshModel: true }},
    }
  },
  edit: {
    getModel(params, model) {
      // Preload position to use its data for calculations regarding files
      return model.get('position').then(function() {
        return model.get('candidate').then(() => model);
      });
    },
    fieldsets: [
      POSITION_FIELDSET,
      CANDIDATE_FIELDSET,
      CANDIDACY_FIELDSET
    ]
  },
  details: {
    getModel(params, model) {
      return model.get('position').then(function(position) {
        model.set('position_department', position.belongsTo('department').link());
        return model.get('candidate').then(() => model);
      });
    },
    page: {
      title: computed.readOnly('model.position.code')
    },
    fieldsets: [
      POSITION_FIELDSET,
      CANDIDATE_FIELDSET,
      CANDIDACY_FIELDSET_DETAILS
    ]
  },
});
