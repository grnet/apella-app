import {ApellaGen} from 'ui/lib/common';
import gen from 'ember-gen/lib/gen';
import {field} from 'ember-gen';

const {
  computed,
  get
} = Ember;


export default ApellaGen.extend({
  order: 10,
  modelName: 'jira-issue',
  resourceName: 'jira-issues',
  auth: true,
  path: 'jira-issues',
  list : {
    menu: {
      icon: 'mail_outline',
      label: computed('role', function() {
        let role = get(this, 'role');
        if (role.startsWith('helpdesk')){
          return 'jira.helpdesk.menu_label';
        }
        else {
          return 'jira.user.menu_label';
        }
      }),
    }
  },
  create: {
    routeMixins: {
      queryParams: {'user_id': { refreshModel: true }},
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
      fields: computed('role', function(){
        let role = get(this, 'role');
        let fields = [
          field('user', {disabled: true, label: 'full_name_current.label'}),
          field('user.id', {disabled: true, label: 'user_id.label'}),
          'issue_type',
          field('title', {label: 'jira.title.label'}),
          'description',
        ]
        if (role.startsWith('helpdesk')) {
          return fields;
        } else {
          return fields;
        }
      }),
      layout: {
        flex: [25, 25, 50, 100, 100]
      }
    }],


  }
});
