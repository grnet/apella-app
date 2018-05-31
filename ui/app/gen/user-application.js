import {ApellaGen, prefixSelect} from 'ui/lib/common';
import {field} from 'ember-gen';
import {applicationActions, goToPosition} from 'ui/utils/common/actions';
import USERAPP from 'ui/utils/common/user-application';
import {departmentInstitutionFilterField} from 'ui/utils/common/fields';

const {
  computed,
  get
} = Ember;

const USER_APP_TYPES = prefixSelect([["tenure", "Tenure"], ["renewal", "Renewal"]], 'user_application.');



export default ApellaGen.extend({
  order: 1600,
  modelName: 'user_application',
  auth: true,
  path: 'user-applications',
  session: Ember.inject.service(),

  abilityStates: {
    can_create: computed('role', 'user.rank', 'user.is_foreign', 'model.@each', function() {
      let role = get(this, 'role'),
          rank = get(this, 'user.rank'),
          domestic = !get(this, 'user.is_foreign');
      let professor = role === 'professor',
          tenured = rank === 'Tenured Assistant Professor';
      let apps = get(this, 'model');
      if(apps && apps.content) {
        let {
          can_create_tenure: can_tenure,
          can_create_renewal: can_renewal
        } = USERAPP.can_create(apps.content);

        return professor && domestic && tenured && (can_tenure || can_renewal);
      } else {
        return professor && domestic && tenured
      }
    }),
    owned: computed('', function(){
      return true;
    })
  },

  list: {
    page: {
      title: computed('role', function() {
        let role = get(this, 'role');
        if (role === 'professor'){
          return 'my_user_application.menu_label';
        }
        else {
          return 'user_application.menu_label';
        }
      }),
    },
    getModel(params) {
      let role = get(this, 'session.session.authenticated.role');
      let user_id = get(this, 'session.session.authenticated.user_id');
      let prof = role === 'professor';

      if (params.limit && prof) {
        delete params.limit;
      }
      if (prof) {
        params.user_id = user_id;
      }
      return this.store.query('user_application', params);
    },
    menu: {
      icon: 'send',
      display: computed('role', function(){
        let role = get(this, 'role'),
            rank = get(this, 'session.session.authenticated.rank'),
            domestic = !get(this, 'session.session.authenticated.is_foreign');
        let professor = role === 'professor',
            tenured = rank === 'Tenured Assistant Professor';
        return !(professor && (!domestic || !tenured));
      }),
      label: computed('role', function() {
        let role = get(this, 'role');
        if (role === 'professor'){
          return 'my_user_application.menu_label';
        }
        else {
          return 'user_application.menu_label';
        }
      }),
    },
    filter: {
      active: true,
      serverSide: true,
      search: true,
      meta: {
        fields: ['state', 'app_type' ]
      },
    },
    row: {
      fields: computed('role', function(){
        let role = get(this, 'role');
        let fields = [
          field('id', {label: 'user_application.id.label'}),
          field('user.id', {label: 'user_id.label'}),
          field('user.full_name_current', {label: 'full_name_current.label'}),
          field('state_verbose', {label: 'state.label'}),
          field('app_type_verbose', {label: 'app_type.label'}),
          field('created_at_format', {label: 'created_at.label'}),
          'receiving_department.title_current',
        ];
        if (role === 'professor' || role === 'candidate') {
          fields.splice(1, 2);
          fields.splice(-1,1);
        }
        return fields;
      }),
      actions: ['gen:details', 'goToProfessor', 'goToPosition', 'acceptApplication', 'rejectApplication', 'createPosition', 'applyApplicationCandidacy'],
      actionsMap: {
        acceptApplication: applicationActions.acceptApplication,
        rejectApplication: applicationActions.rejectApplication,
        goToProfessor: applicationActions.goToProfessor,
        createPosition: applicationActions.createPosition,
        applyApplicationCandidacy: applicationActions.applyApplicationCandidacy,
        goToPosition: goToPosition,
      }
    }
  },
  create: {
    getModel(params) {
      var store = get(this, 'store');
      let user_id = get(this, 'session.session.authenticated.user_id');
      let apps = store.query('user_application', {user_id: user_id});

      let role = get(this, 'session.session.authenticated.role');
      if (role === 'helpdeskadmin') {
        return store.createRecord('user-application', {
          app_type: 'move'
        });
      }
      var self = this;
      return apps.then(function(apps){
        let app_type, disable=false;

        let {
          can_create_tenure: can_tenure,
          can_create_renewal: can_renewal
        } = USERAPP.can_create(apps.content);

        if (!(can_tenure || can_renewal)) {
          self.transitionTo('user-application.index');
        }

        if (!can_tenure) { app_type = 'renewal'; }
        if (!can_renewal) { app_type = 'tenure'; }
        if (app_type) { disable = true }

        return store.createRecord('user-application', {
          disable: disable,
          app_type: app_type
        });
      });
    },
    fieldsets: computed('role', function(){
      let label, text, fields;

      let fields_all = [
        field('user', {
          label: 'user_id.label',
          formComponent: 'select-model-id-field'
        }),
        field('app_type', {
          disabled: true,
        }),
        field('institution', {
          disabled: computed('model.changeset.app_type', function(){
            let app_type = get(this, 'model.changeset.app_type');
            return app_type != 'move';
          }),
        }),
        departmentInstitutionFilterField({fieldName:'receiving_department'}),
      ];

      let fields_restricted = [
        field('app_type', {
          choices: USER_APP_TYPES,
          disabled: computed('model.disable', function(){
            return get(this, 'model.disable');
          })
        }),
      ];

      if (get(this, 'role') === 'helpdeskadmin') {
        fields = fields_all;
        label = 'fieldsets.labels.user_application_create.helpdesk';
        text = 'fieldsets.text.user_application_create.helpdesk';
      } else {
        fields = fields_restricted;
        label = 'fieldsets.labels.user_application_create.applicant';
        text = 'fieldsets.text.user_application_create.applicant';
      }
      return [{
        label,
        text,
        fields,
      }];
    }),
    onSubmit(model) {
      this.transitionTo('user-application.index');
    },
  },
  details: {
    page: {
      title: computed.readOnly('model.app_type_verbose')
    },
    fieldsets: [{
      label: 'fieldsets.labels.user_application',
      fields: computed('role', 'model.app_type', function(){
        let role = get(this, 'role');
        let is_move = get(this, 'model.app_type') === 'move';
        let fields = [
          field('user.id', {label: 'user_id.label'}),
          field('user.full_name_current', {label: 'full_name_current.label'}),
          field('state_verbose', {label: 'state.label'}),
          field('app_type_verbose', {label: 'app_type.label'}),
          field('created_at_format', {label: 'created_at.label'}),
          field('updated_at_format', {label: 'updated_at.label'}),
          field('department.title_current', {label: 'user_department.title_current.label'}),
          field('department.institution.title_current', {label: 'user_institution.title_current.label'}),
        ];
        if (role === 'professor' || role === 'candidate') {
          fields.splice(0, 3);
        }
        if (is_move) {
          fields.push(
            field('receiving_department.title_current', {
              label: 'receiving_department.title_current.label'
            }),
            'receiving_department.institution.title_current',
             field('id', {label: 'user_application.id.label' }),
          );
        }

        return fields;
      }),
      layout: {
        flex: [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 100]
      }
    }]
  }
});
