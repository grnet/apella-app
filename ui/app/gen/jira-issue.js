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
      title:'jira.user.menu_label',
    },
    menu: {
      icon: 'mail_outline',
      label: 'jira.user.menu_label',
      display: computed('role', function() {
        let role = get(this, 'role');
        return !role.startsWith('helpdesk');
      })
    },
    sort: {
      active: true,
      fields: ['issue_key'],
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
      fields: [
        field('issue_key', {label: 'code.label'}),
        field('issue_type_verbose', {label: 'issue_type.label'}),
        'created_at_format',
        field('title', {label: 'jira.title.label'}),
      ],
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
      fields: [
        field('issue_key', {label: 'code.label'}),
        'created_at_format',
        field('issue_type_verbose', {label: 'issue_type.label'}),
        'title',
        'description',
        'helpdesk_response',
      ],
      layout: {
        flex:  [100, 50, 50, 100, 100, 100]
      }
    }],
  }
});
