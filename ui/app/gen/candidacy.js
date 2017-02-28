import {field} from 'ember-gen';
import {ApellaGen, preloadRelations} from 'ui/lib/common';
import validate from 'ember-gen/validate';
import _ from 'lodash/lodash';
import {disable_field} from 'ui/utils/common/fields';
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
      text: 'candidacy.candidate_section.subtitle',
      fields: [
        field('candidate', {
          disabled: true,
          displayAttr: 'full_name_current',
        }),
        fileField('cv', 'candidate', 'cv', {
          readonly: true,
        }),
        fileField('diplomas', 'candidate', 'diplomas', {
          readonly: true,
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
    fields: [
      fileField('self_evaluation_report', 'candidacy', 'self_evaluation_report', {
        hint: 'five_before_electors_meeting',
        readonly: computed('model.position.is_open', 'model.position.electors_meeting_date', function() {
          let electors_at = get(this, 'model.position.electors_meeting_date');
          let position_closed = !get(this, 'model.position.is_open');
          let after_deadline = false;
          if (electors_at) {
            after_deadline =  moment().add(5, 'days').isAfter(electors_at);
          }
          return position_closed || after_deadline;
        })
      }, {
        replace: true
      }),
      fileField('attachment_files', 'candidacy', 'attachment_files', {
        hint: 'one_before_electors_meeting',
        readonly: computed('model.position.is_open', 'model.position.electors_meeting_date', function() {
          let electors_at = get(this, 'model.position.electors_meeting_date');
          let position_closed = !get(this, 'model.position.is_open');
          let after_deadline = false;
          if (electors_at) {
            after_deadline =  moment().add(1, 'days').isAfter(electors_at);
          }
          return position_closed || after_deadline;
        })
      }, {
        multiple: true
      }),
      field('othersCanView', {
        disabled: computed('model.position.is_open', function(){
          return !get(this, 'model.position.is_open');
        })
     })
    ],
    flex: 100,
};

let CANDIDACY_FIELDSET_DETAILS =  {
    label: 'candidacy.candidacy_section.title',
    fields: [
      fileField('self_evaluation_report', 'candidacy', 'self_evaluation_report', {
        readonly: true,
        hint: 'five_before_electors_meeting',
      }, { replace: true}),
     fileField('attachment_files', 'candidacy', 'attachment_files', {
        readonly: true,
        hint: 'one_before_electors_meeting',
      }, { replace: true, multiple: true}),
      'othersCanView'
    ],
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
  list:  ['position.code', 'position.title', 'position.department.institution.title_current',
          'position.department.title_current',
          'position.state_calc_verbose', field('state_verbose', {label: 'candidacy.state'})],
  list_with_user_id:  ['position.code', field('candidate.id', {label: 'candidate.user_id.label'}), 'position.title', 'position.department.institution.title_current',
          'position.department.title_current',
          'position.state_calc_verbose', field('state_verbose', {label: 'candidacy.state'})],

  create_helpdeskadmin: [
    POSITION_FIELDSET,
    {
      label: 'fieldsets.labels.candidate',
      fields: [field('candidate', {
        query: function(table, store, field, params) {
          let promises = [
            store.query('user', {role: 'professor'}),
            store.query('user', {role: 'candidate'}),
          ]

          var promise = Ember.RSVP.all(promises).then(function(arrays) {
            var mergedArray = Ember.A();
            arrays.forEach(function (records) {
              mergedArray.pushObjects(records.toArray());
            });
            return mergedArray.uniqBy('id')
          })

          return DS.PromiseArray.create({
            promise: promise,
          })
        }
      })],
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
      let ability = getOwner(this).lookup('ability:positions')
      let props = this.getProperties('role', 'user');
      props.model = get(this, 'model.position');
      ability.setProperties(props);
      return ability;
    }),
    position_open: alias('model.position.is_open'),
    others_can_view: alias('model.othersCanView'),

    owned: computed('role', 'user.user_id', 'model.candidate.id', function() {
      let is_institutionmanager = get(this, 'role') === 'institutionmanager';
      let is_candidate_owning = get(this, 'user.user_id') == get(this, 'model.candidate.id')
      return is_institutionmanager || is_candidate_owning;
    }),

    owned_open: computed('owned', 'position_open', 'model.state', function() {
      let position_open = get(this, 'position_open');
      let candidacy_not_cancelled = get(this, 'model.state') != 'cancelled';
      return get(this, 'owned') && position_open && candidacy_not_cancelled;
    }),

    five_before_electors_meeting: computed('model.state', 'position_open', 'model.position.electors_meeting_date', 'owned', function() {
      let electors_at = get(this, 'model.position.electors_meeting_date');
      let candidacy_not_cancelled = get(this, 'model.state') != 'cancelled';
      let position_open = get(this, 'position_open');
      let owned = get(this, 'owned');
      let before_deadline = true;
      if (electors_at) {
        before_deadline =  moment().add(5, 'days').isBefore(electors_at);
      }
      return candidacy_not_cancelled && (position_open || before_deadline) && owned;
    }),

    one_before_electors_meeting: computed('model.state', 'position_open', 'model.position.electors_meeting_date', 'owned', function() {
      let electors_at = get(this, 'model.position.electors_meeting_date');
      let candidacy_not_cancelled = get(this, 'model.state') != 'cancelled';
      let position_open = get(this, 'position_open');
      let before_deadline = true;
      let owned = get(this, 'owned');
      if (electors_at) {
        before_deadline =  moment().add(1, 'days').isBefore(electors_at);
      }
      return candidacy_not_cancelled && (position_open || before_deadline) && owned;
    })

  },

  common: {
    preloadModels: [],
    fieldsets: FS.common,
    validators: {
    }
  },
  list: {
    layout: 'table',
    actions: [],

    getModel: function(params) {
      let role = get(this, 'session.session.authenticated.role');
      if (role == 'candidate' || role == 'professor') {
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
      searchFields: ['position.code', 'position.title', 'candidate.id'],
    },
    page: {
      title: 'candidacy.menu_label',
    },
    menu: {
      label: 'candidacy.menu_label',
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
          fs = FS.list
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
      if (get(this, 'role') == 'helpdeskadmin') {
        return FS.create_helpdeskadmin
      } else {
        return FS.common
      }
    }),
    onSubmit(model) {
      this.transitionTo('candidacy.record.edit', model)
    },
    getModel(params) {
      var self = this;
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
          if (role == 'helpdeskadmin') {
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
                return c
            });

          })
        })
      }
      this.transitionTo('candidacy.index')
    },
    routeMixins: {
      queryParams: {'position': { refreshModel: true }},
    }
  },
  edit: {
    fieldsets: [
      POSITION_FIELDSET,
      CANDIDATE_FIELDSET,
      CANDIDACY_FIELDSET
    ]
  },
  details: {
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
