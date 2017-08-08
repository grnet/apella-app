import {field} from 'ember-gen';
import {ApellaGen} from 'ui/lib/common';
import gen from 'ember-gen/lib/gen';
import validate from 'ember-gen/validate';
import USER from 'ui/utils/common/users';
import {deactivateUser, activateUser, createIssue} from 'ui/utils/common/actions';

const {
  computed,
  get,
  computed: {reads}
} = Ember;

const issuesField = field('jira_issues', {
  refreshValueQuery: true,
  valueQuery: function(store, params, model, value) {
    model = model._content ? model._content : model;
    let user_id = model.get('id');
    console.log(user_id);
    return store.query('jira-issue', { user_id: user_id });
  },
  label: null,
  modelMeta: {
    row: {
      fields: [
        field('issue_key', {label: 'code.label'}),
        field('issue_type_verbose', {label: 'issue_type.label'}),
        'created_at_format',
        'updated_at_format',
        field('state_verbose', {label: 'status_verbose.label'}),
        field('resolution_verbose', {label: 'resolution.label'}),
        'reporter_id_if_not_user',
      ],
      actions: ['view_details'],
      actionsMap: {
        view_details: {
          icon: 'open_in_new',
          detailsMeta: {
            fieldsets: [{
              fields: [
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
              ],
              layout: {
                flex:  [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 100, 100, 100]
              }
            }]
          },
          action: function() {},
          label: 'details',
          confirm: true,
          prompt: {
            title: reads('model.issue_key'),
            cancel: 'close',
            contentComponent: 'model-quick-view'
          }
        }
      }
    },
  },
});



export default ApellaGen.extend({
  order: 700,
  modelName: 'user',
  auth: true,
  path: 'users',
  common: {
    validators: USER.VALIDATORS,
  },
  list: {
    page: {
      title: 'user.menu_label',
    },
    menu: {
      icon: 'account_box',
      label: 'user.menu_label'
    },
    filter: {
      active: true,
      meta: {
        fields: ['role', 'is_active', field('has_accepted_terms', {label: 'has_accepted_terms.filter.label'})]
      },
      serverSide: true,
      search: true,
      searchFields: ['id', 'email', 'username', 'first_name', 'last_name']
    },
    sort: {
      active: true,
      serverSide: true,
      fields: ['id', 'username', 'email']
    },
    row: {
      fields: [field('id', {label: 'user_id.label'}), field('old_user_id'), 'has_accepted_terms_verbose', field('status_verbose', {label: 'state.label'}), 'username', 'email', 'full_name_current', 'role_verbose', 'login_method'],
      actions: ['gen:details', 'gen:edit', 'remove', 'activateUser', 'deactivateUser', 'createIssue'],
      actionsMap: {
        deactivateUser: deactivateUser,
        activateUser: activateUser,
        createIssue: createIssue,
      }

    },
  },
  details: {
    page: {
      title: computed.readOnly('model.full_name_current')
    },
    fieldsets: [
      USER.FIELDSET_DETAILS_USER,
      {
        label: 'jira.helpdesk.menu_label',
        fields: [issuesField]
      }
    ]
  },
  edit: {
    fieldsets: [
      USER.FIELDSET_EDIT_USER,
    ]
  },
  create: {
    fieldsets: [
      USER.FIELDSET_CREATE,
    ]
  }
});
