import {field} from 'ember-gen';
import {ApellaGen} from 'ui/lib/common';
import gen from 'ember-gen/lib/gen';
import validate from 'ember-gen/validate';

const {
  computed,
  get
} = Ember;


export default ApellaGen.extend({
  order: 2100,
  modelName: 'jira-issue',
  resourceName: 'jira-issues',
  auth: true,
  path: 'jira-issues',
  common: {
    validators: {
      title: [validate.presence(true), validate.length({min:3, max:200})],
      description: [validate.presence(true)],
    }
  },
  list : {
    page: {
      title: computed('role', function() {
        let role = get(this, 'role');
        if (role && role.startsWith('helpdesk')){
          return 'jira.helpdesk.menu_label';
        }
        else {
          return 'jira.user.menu_label';
        }
      }),
    },
    menu: {
      icon: 'mail_outline',
      label: computed('role', function() {
        let role = get(this, 'role');
        if (role && role.startsWith('helpdesk')){
          return 'jira.helpdesk.menu_label';
        }
        else {
          return 'jira.user.menu_label';
        }
      }),
    },
    sort: {
      active: true,
      fields: ['issue_key', 'user.id'],
      serverSide: true
    },
    filter: {
      active: true,
      serverSide: true,
      search: true,
      meta: {
        fields: [
          'issue_type',
          'state',
          'resolution',
        ]
      }
    },
    row: {
      fields: computed('role', function() {
        let role = get(this, 'role');
        if (role && role.startsWith('helpdesk') )  {
          return [
            field('issue_key', {label: 'code.label'}),
            field('user.id', {label: 'user_id.label'}),
            field('user.full_name_current', {label: 'full_name_current.label'}),
            field('user.role_verbose', {label: 'role.label'}),
            field('issue_type_verbose', {label: 'issue_type.label'}),
            'created_at_format',
            'updated_at_format',
            field('state_verbose', {label: 'status_verbose.label'}),
            field('resolution_verbose', {label: 'resolution.label'}),
            'reporter_id_if_not_user',
          ];
        } else {
          return [
            field('issue_key', {label: 'code.label'}),
            field('issue_type_verbose', {label: 'issue_type.label'}),
            'created_at_format',
            field('title', {label: 'jira.title.label'}),
          ];
        }
      }),
      actions: ['gen:details'],
    },
  },
  create: {
    routeMixins: {
      queryParams: {'user_id': { refreshModel: true }},
    },
    onSubmit(model) {
      this.transitionTo('jira-issue.record.index', model);
    },
    getModel(params) {
      var store = get(this, 'store');
      let reporter_id = get(this, 'session.session.authenticated.user_id');
      let role = get(this, 'session.session.authenticated.role');
      let reporter = store.findRecord('user', reporter_id);

      return reporter.then(function(reporter) {
         if (params.user_id && role.startsWith('helpdesk')) {
          let user = store.findRecord('user', params.user_id);
          return user.then(function(user) {
            return store.createRecord('jira-issue', {
              user: user,
              reporter: reporter
            });
          })
        } else {
          return store.createRecord('jira-issue', {
            user: reporter,
            reporter: reporter
          });
        }
      })

    },
    fieldsets: [{
      text: computed('role', function(){
        if (get(this, 'role').startsWith('helpdesk')) {
          return 'jira.fieldset.helpdesk.text'
        }
          return 'jira.fieldset.user.text'
      }),
      label: computed('role', function(){
        if (get(this, 'role').startsWith('helpdesk')) {
          return 'jira.fieldset.helpdesk.label'
        }
          return 'jira.fieldset.user.label'
      }),
      fields: [
        field('user', {disabled: true, label: 'full_name_current.label'}),
        field('user.id', {disabled: true, label: 'user_id.label'}),
        field('issue_call', {
          disabled: computed('role', function(){
            return get(this, 'role').startsWith('helpdesk')? false: true;
          })
        }),
        'issue_type',
        field('title', {label: 'jira.title.label'}),
        'description',
      ],
      layout: {
        flex: [50, 50, 50, 50, 100, 100]
      }
    }],
  },
  details: {
    page: {
       title: computed.readOnly('model.issue_key'),
    },
    fieldsets: [{
      fields: computed('role', function(){
        let role = get(this, 'role');
        if (role && role.startsWith('helpdesk')) {
          return [
            field('issue_key', {label: 'code.label'}),
            'user.id',
            field('user.role_verbose', {label: 'role.label'}),
            field('user.full_name_current', {label: 'full_name_current.label'}),
            field('issue_type_verbose', {label: 'issue_type.label'}),
            field('state_verbose', {label: 'state.label'}),
            field('resolution_verbose', {label: 'resolution.label'}),
            field('issue_call_verbose', {label: 'issue_call.label'}),
            'updated_at_format',
            'created_at_format',
            'reporter_id_if_not_user',
            field('reporter_full_name_current_if_not_user', {label: 'reporter.full_name_current.label'}),
            'title',
            'description',
            'helpdesk_response',
          ];
        } else {
          return [
            field('issue_key', {label: 'code.label'}),
            'created_at_format',
            field('issue_type_verbose', {label: 'issue_type.label'}),
            'title',
            'description',
            'helpdesk_response',
          ];
        }
      }),
      layout: {
        flex: computed('role', function(){
          let role  = get(this, 'role');
          if (role && role.startsWith('helpdesk')) {
            return [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 100, 100, 100]
          } else {
            return [100, 50, 50, 100, 100, 100]
          }
        })
      }
    }],
  }
});
