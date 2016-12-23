import {field} from 'ember-gen';
import {ApellaGen} from 'ui/lib/common';
import validate from 'ember-gen/validate';
import _ from 'lodash/lodash';
import {disable_field} from 'ui/utils/common/fields';

const presence = validate.presence(true),
      max_chars = validate.length({max: 200}),
      mandatory = [validate.presence(true)],
      mandatory_with_max_chars = [presence, max_chars],
      {
        get, computed, computed: { alias }
      } =Ember,
      CANDIDACY_POSTED_ID = '2',
      POSITION_POSTED_ID = '2';

let FS = {
  list:  ['position.code', 'position.department.institution.title_current',
          'position.department.title_current',
          'position.state_verbose', field('state_verbose', {label: 'candidacy.state'})],
  create: [{
    label: 'candidacy.position_section.title',
    text: 'candidacy.position_section.subtitle',
    fields: ['position'],
    flex: 100
  },
  {
    label: 'candidacy.candidate_section.title',
    text: 'candidacy.candidate_section.subtitle',
    fields: ['candidate', 'cv', 'diploma', 'publication'],
    flex: 50,
    layout: {
      flex: [50, 50, 50, 50]
    },
  },
    {
      label: 'candidacy.candidacy_section.title',
      text: 'candidacy.candidacy_section.subtitle',
      fields: ['selfEvaluation', 'additionalFiles', 'othersCanView'],
      flex: 50,
      layout: {
        flex: [50, 50, 50, 50]
      }
    }
  ],
  edit: {
    position_fields: ['position.code_and_title', 'position.title', 'position.department.institution.title_current', 'position.department.title_current', 'position.discipline','position.fek', 'position.fek_posted_at_format', 'position.starts_at_format', 'position.ends_at_format' ],
    position_layout: {
      flex: [30, 30, 30, 30, 30, 30, 30, 30, 30 ]
    }
  }

}

let actions = {
  cancelCandidacy: {
    label: 'withdrawal',
    icon: 'delete forever',
    accent: true,
    permissions: [{action: 'edit'}],
    action(route, model) {
      return model.get('candidate').then(() => {
        model.set('state', 'cancelled');
        let m = route.get('messageService')
        return model.save().then((value) => {
          m.setSuccess('form.saved');
          return value;
        }, (reason) => {
          model.rollbackAttributes();
          m.setError('reason.errors');
          return reason;
        });
      })
    },
    confirm: true,
    prompt: {
      ok: 'withdrawal',
      cancel: 'cancel',
      message: 'prompt.withdrawal.message',
      title: 'prompt.withdrawal.title',
    }
  }
}

export default ApellaGen.extend({
  appIndex: true,
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
    owned: computed('role', 'user.id', 'model.candidate.id', function() {
      return get(this, 'role') === 'institutionmanager' || get(this, 'user.id') === get(this, 'model.candidate.id');
    }), // we expect server to reply with owned resources if user is an institution manager
    others_can_view: alias('model.othersCanView'),
    participates: computed('role', function() {
      let role = get(this, 'role');
      return role === 'professor'; // TODO: resolve user.id participates
    }),
    owned_open: computed('owned', 'position.open', 'model.state', function() {
      return get(this, 'owned') && get(this, 'positionAbility.open') && get(this, 'model.state') === 'cancelled';
    })
  },

  common: {
    preloadModels: ['position', 'institution', 'department'],
    validators: {
      candidate: mandatory,
      position: mandatory,
//      cv: mandatory_with_max_chars,
//      diploma: mandatory_with_max_chars,
//      publication: mandatory_with_max_chars,
//      additionalFiles: mandatory_with_max_chars,
    }
  },
  list: {
    layout: 'table',

    getModel: function(params) {
      // TODO replace with session's user group
      let userGroup = 'admin';
      let qs = this.getModelQueryParams(params);
      if (userGroup == 'admin') {
        return this.store.query('candidacy', qs);
      } else {
      // TODO replace with session's user
        let userId = '2';
        qs['state'] = CANDIDACY_POSTED_ID;
        qs['candidate'] = userId;
        return this.store.query('candidacy', qs);
      }
    },
    sortBy: 'position.code:asc',
    search: {
      fields: FS.list,
    },
    page: {
      title: 'candidacy.menu_label',
    },
    menu: {
      label: 'candidacy.menu_label',
      icon: 'assignment',
      display: computed('role', function() {
        let role = get(this, 'session.session.authenticated.role');
        let forbiddenRoles = ['institutionmanager', 'helpdeskadmin'];

        return (forbiddenRoles.includes(role) ? false : true);
      })
    },
    row: {
      fields: FS.list,
      actions: ['gen:details', 'gen:edit', 'cancelCandidacy'],
      actionsMap: {
        cancelCandidacy: actions.cancelCandidacy
      }
    }
  },
  create: {
    fieldsets: FS.create,
  },
  details: {
    page: {
      title: computed.readOnly('model.position.code')
    },
    fieldsets:[
      {
        label: 'fieldsets.labels.candidate_details',
        fields: [
          field('candidate.full_name_current', {label: 'full_name_current.label'}),
          field('candidate.email', {label: 'email.label'}),
        ],
        layout: {
          flex: [50, 50]
        }
      },{
        label: 'fieldsets.labels.candidacy_details',
        fields: [
          'state_verbose',
          'submitted_at_format',
          'updated_at_format',
          'cv',
          'diploma',
          'publication',
          'selfEvaluation',
          'additionalFiles',
        ],
        layout: {
          flex: [100, 50, 50, 50, 50, 50, 50, 50]
        }
      }, {
        label: 'fieldsets.labels.position_details',
        fields: [
          'position.code',
          'position.state_verbose',
          'position.title',
          'position.description',
          'position.discipline',
          field('position.department.title_current', {label: 'department.label'}),
          field('position.subject_area.title_current',{label: 'subject_area.label'}),
          field('position.subject.title_current', {label: 'subject.label'}),
          'position.fek',
          'position.fek_posted_at_format',
          'position.starts_at_format',
          'position.ends_at_format',
        ],
        layout: {
          flex: [50, 50, 100, 100, 50, 50, 50, 50, 50, 50, 50, 50]
        }
      }
    ],
  },
  edit: {
    fieldsets: computed('model.position.state', function() {
      let candidacy_fields = ['selfEvaluation', 'additionalFiles', 'othersCanView', 'state'];
      if (get(this, 'model.position.state') != POSITION_POSTED_ID) {
        candidacy_fields = _.map(candidacy_fields, disable_field);
      };

      return [{
        label: 'candidacy.position_section.title',
        text: 'candidacy.position_section.subtitle',
        fields: _.map(FS.edit.position_fields, disable_field),
        layout: FS.edit.position_layout
      },
      {
        label: 'candidacy.candidate_section.title',
        text: 'candidacy.candidate_section.subtitle',
        fields: [disable_field('candidate.full_name_current'), 'cv', 'diploma', 'publication'],
        layout: {
          flex: [50, 50, 50, 50]
        },
      },
        {
          label: 'candidacy.candidacy_section.title',
          fields: candidacy_fields,
          layout: {
            flex: [50, 50, 50, 50]
          }
        }
      ];
    }),
  },
});
